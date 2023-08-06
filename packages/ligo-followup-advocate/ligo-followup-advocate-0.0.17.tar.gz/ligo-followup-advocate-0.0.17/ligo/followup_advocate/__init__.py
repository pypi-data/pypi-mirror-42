import os
import tempfile
import urllib
import webbrowser

import astropy.coordinates as coord
import astropy.time
import astropy.units as u
import healpy as hp
import lxml.etree
import numpy as np
from ligo.gracedb import rest
from ligo.skymap.io.fits import read_sky_map
from ligo.skymap.postprocess.ellipse import find_ellipse
from ligo.skymap.postprocess.find_injection import find_injection_moc

from .jinja import env
from .version import __version__  # noqa


def authors(authors, service=rest.DEFAULT_SERVICE_URL):
    """Write GCN Circular author list"""
    return env.get_template('authors.jinja2').render(authors=authors).strip()


def guess_skyloc_pipeline(comments):
    comments = comments.upper()
    skyloc_pipelines = ['cWB', 'BAYESTAR', 'LIB', 'LALInference', 'UNKNOWN']
    for skyloc_pipeline in skyloc_pipelines:
        if skyloc_pipeline.upper() in comments:
            break
    return skyloc_pipeline


def main_dict(gracedb_id, client):
    """Create general dictionary to pass to compose circular"""

    event = client.superevent(gracedb_id).json()
    preferred_event_id = event['preferred_event']
    preferred_event = client.event(preferred_event_id).json()
    preferred_pipeline = preferred_event['pipeline']
    gw_events = event['gw_events']
    other_pipelines = []
    for gw_event in gw_events:
        pipeline = client.event(gw_event).json()['pipeline']
        if pipeline not in other_pipelines and pipeline != preferred_pipeline:
            other_pipelines.append(pipeline)
    voevents = client.voevents(gracedb_id).json()['voevents']
    log = client.logs(gracedb_id).json()['log']
    files = client.files(gracedb_id).json()

    gpstime = float(preferred_event['gpstime'])
    event_time = astropy.time.Time(gpstime, format='gps').utc

    skymaps = {}
    for voevent in voevents:
        voevent_text = client.files(gracedb_id, voevent['filename']).read()
        root = lxml.etree.fromstring(voevent_text)
        alert_type = root.find(
            './What/Param[@name="AlertType"]').attrib['value'].lower()
        url = root.find('./What/Group/Param[@name="skymap_fits"]')
        if url is None:
            continue
        url = url.attrib['value']
        _, filename = os.path.split(url)
        comments = '\n'.join(entry['comment'].upper() for entry in log
                             if entry['filename'] == filename)
        skyloc_pipeline = guess_skyloc_pipeline(comments)
        issued_time = astropy.time.Time(root.find('./Who/Date').text).datetime
        if filename not in skymaps:
            for message in log:
                if filename == message['filename']:
                    tag_names = message['tag_names']
                    if 'sky_loc' in tag_names and 'lvem' in tag_names:
                        skymaps[filename] = dict(
                            alert_type=alert_type,
                            pipeline=skyloc_pipeline,
                            filename=filename,
                            latency=issued_time-event_time.datetime)
                    break
    skymaps = list(skymaps.values())
    em_brightfile = 'source_classification.json'
    if em_brightfile in files:
        source_classification = client.files(
            gracedb_id, em_brightfile).json()
    else:
        source_classification = {}

    # adding the p_atro informations if available
    preferred_event_files = client.files(preferred_event_id).json()
    p_astro_file = 'p_astro.json'
    if p_astro_file in preferred_event_files:
        classifications = client.files(preferred_event_id, p_astro_file).json()

        # Convert to percent for consistency with em_bright
        classifications = {
            key: 100 * value for key, value in classifications.items()}
    else:
        classifications = {}

    o = urllib.parse.urlparse(client.service_url)

    kwargs = dict(
        subject='Identification',
        gracedb_id=gracedb_id,
        gracedb_service_url=urllib.parse.urlunsplit(
            (o.scheme, o.netloc, '/superevents/', '', '')),
        group=preferred_event['group'],
        pipeline=preferred_pipeline,
        other_pipelines=other_pipelines,
        gpstime='{0:.03f}'.format(round(float(preferred_event['gpstime']), 3)),
        search=preferred_event.get('search', ''),
        far=preferred_event['far'],
        utctime=event_time.iso,
        instruments=preferred_event['instruments'].split(','),
        skymaps=skymaps,
        prob_has_ns=source_classification.get('Prob NS2'),
        prob_has_remnant=source_classification.get('Prob EMbright'),
        include_ellipse=None,
        classifications=classifications)

    if skymaps:
        preferred_skymap = skymaps[-1]['filename']
        cl = 90
        include_ellipse, ra, dec, a, b, pa, area, greedy_area = \
            uncertainty_ellipse(gracedb_id, preferred_skymap, client, cl=cl)
        kwargs.update(
            preferred_skymap=preferred_skymap,
            cl=cl,
            include_ellipse=include_ellipse,
            ra=coord.Longitude(ra*u.deg),
            dec=coord.Latitude(dec*u.deg),
            a=coord.Angle(a*u.deg),
            b=coord.Angle(b*u.deg),
            pa=coord.Angle(pa*u.deg),
            ellipse_area=area,
            greedy_area=greedy_area)

    return kwargs


def compose(gracedb_id, authors=(), mailto=False,
            service=rest.DEFAULT_SERVICE_URL, client=None):
    """Compose GCN Circular draft"""

    if client is None:
        client = rest.GraceDb(service)

    kwargs = main_dict(gracedb_id, client=client)
    kwargs.update(authors=authors)
    kwargs.update(change_significance_statement=False)

    subject = env.get_template('subject.jinja2').render(**kwargs).strip()
    body = env.get_template('initial_circular.jinja2').render(**kwargs).strip()

    if mailto:
        pattern = 'mailto:emfollow@ligo.org,dac@ligo.org?subject={0}&body={1}'
        url = pattern.format(
            urllib.parse.quote(subject),
            urllib.parse.quote(body))
        webbrowser.open(url)
    else:
        return '{0}\n{1}'.format(subject, body)


def compose_RAVEN(gracedb_id, authors=(),
                  service=rest.DEFAULT_SERVICE_URL, client=None):
    """Compose EM_COINC RAVEN GCN Circular draft"""

    if client is None:
        client = rest.GraceDb(service)

    event = client.superevent(gracedb_id).json()

    if 'EM_COINC' not in event['labels']:
        return

    preferred_event_id = event['preferred_event']
    preferred_event = client.event(preferred_event_id).json()
    group = preferred_event['group']
    superevent_far = preferred_event['far']
    gpstime = float(preferred_event['gpstime'])

    for em_event_id in event['em_events']:
        em_event = client.event(em_event_id).json()
        em_event_gpstime = float(em_event['gpstime'])
        external_pipeline = em_event['pipeline']
        # FIXME in GraceDb: Even SNEWS triggers have an extra attribute GRB.
        external_trigger = em_event['extra_attributes']['GRB']['trigger_id']
        SNEWS = (em_event['search'] == 'Supernova')
        GRB = (em_event['search'] == 'GRB')

    o = urllib.parse.urlparse(client.service_url)
    kwargs = dict(
        gracedb_service_url=urllib.parse.urlunsplit(
            (o.scheme, o.netloc, '/superevents/', '', '')),
        gracedb_id=gracedb_id,
        group=group,
        superevent_far=preferred_event['far'],
        external_pipeline=external_pipeline,
        external_trigger=external_trigger,
        SNEWS=SNEWS,
        GRB=GRB,
        latency=abs(round(em_event_gpstime-gpstime, 1)),
        beforeafter='before' if gpstime > em_event_gpstime else 'after')

    if GRB:
        # Grab GRB coincidence FARs
        files = client.files(gracedb_id).json()
        coinc_far_file = 'coincidence_far.json'
        if coinc_far_file in files:
            coincidence_far = client.files(gracedb_id, coinc_far_file).json()
            time_coinc_FAR = coincidence_far.get('temporal_coinc_far')
            space_time_coinc_FAR = coincidence_far.get(
                'spatiotemporal_coinc_far')
            kwargs.update(
                time_coinc_FAR=time_coinc_FAR,
                space_time_coinc_FAR=space_time_coinc_FAR)

        # Find combined skymap for GRB
        logs = client.logs(gracedb_id).json()['log']
        for message in reversed(logs):
            comment = message['comment']
            filename = message['filename']
            if (filename.endswith('-gbm.fits.gz')
                    or 'LVC-Fermi sky map' in comment):
                cl = 90
                include_ellipse, ra, dec, a, b, pa, area, greedy_area = \
                    uncertainty_ellipse(gracedb_id, filename, client, cl=cl)
                kwargs.update(
                    combined_skymap=filename,
                    cl=cl,
                    combined_skymap_include_ellipse=include_ellipse,
                    combined_skymap_ra=coord.Longitude(ra*u.deg),
                    combined_skymap_dec=coord.Latitude(dec*u.deg),
                    combined_skymap_a=coord.Angle(a*u.deg),
                    combined_skymap_b=coord.Angle(b*u.deg),
                    combined_skymap_pa=coord.Angle(pa*u.deg),
                    combined_skymap_ellipse_area=area,
                    combined_skymap_greedy_area=greedy_area)

    kwargs.update(main_dict(gracedb_id, client=client))
    if (group.lower() == 'cbc' and superevent_far < 3.8e-7) or \
            (group.lower() == 'burst' and superevent_far < 3.17e-8):
        kwargs.update(change_significance_statement=False)
    else:
        kwargs.update(change_significance_statement=True)

    subject = (
        env.get_template('RAVEN_subject.jinja2').render(**kwargs)
        .strip())
    body = (
        env.get_template('RAVEN_circular.jinja2').render(**kwargs)
        .strip())
    return '{0}\n{1}'.format(subject, body)


def compose_retraction(gracedb_id, authors=(),
                       service=rest.DEFAULT_SERVICE_URL, client=None):
    """Compose GCN retraction circular"""
    if client is None:
        client = rest.GraceDb(service)
    event = client.superevent(gracedb_id).json()
    preferred_event = client.event(event['preferred_event']).json()

    kwargs = dict(
                 subject='Retraction',
                 gracedb_id=gracedb_id,
                 group=preferred_event['group'],
                 authors=authors
             )

    subject = env.get_template('subject.jinja2').render(**kwargs).strip()
    body = env.get_template('retraction.jinja2').render(**kwargs).strip()
    return '{0}\n{1}'.format(subject, body)


def read_map_gracedb(graceid, filename, client, moc_table=False):
    with tempfile.NamedTemporaryFile(mode='w+b') as localfile:
        remotefile = client.files(graceid, filename, raw=True).read()
        localfile.write(remotefile)
        localfile.flush()
        return read_sky_map(localfile.name, moc=moc_table)


def read_map_from_path(path, client):
    return read_map_gracedb(*path.split('/'), client)[0]


def mask_cl(p, level=90):
    pflat = p.ravel()
    i = np.flipud(np.argsort(p))
    cs = np.cumsum(pflat[i])
    cls = np.empty_like(pflat)
    cls[i] = cs
    cls = cls.reshape(p.shape)
    return cls <= 1e-2 * level


def compare_skymaps(paths, service=rest.DEFAULT_SERVICE_URL, client=None):
    """Produce table of sky map overlaps"""
    if client is None:
        client = rest.GraceDb(service)
    filenames = [path.split('/')[1] for path in paths]
    pipelines = [guess_skyloc_pipeline(filename) for filename in filenames]
    probs = [read_map_from_path(path, client) for path in paths]
    npix = max(len(prob) for prob in probs)
    nside = hp.npix2nside(npix)
    deg2perpix = hp.nside2pixarea(nside, degrees=True)
    probs = [hp.ud_grade(prob, nside, power=-2) for prob in probs]
    masks = [mask_cl(prob) for prob in probs]
    areas = [mask.sum() * deg2perpix for mask in masks]
    joint_areas = [(mask & masks[-1]).sum() * deg2perpix for mask in masks]

    kwargs = dict(params=zip(filenames, pipelines, areas, joint_areas))

    return env.get_template('compare_skymaps.jinja2').render(**kwargs)


def uncertainty_ellipse(graceid, filename, client, cl=90):
    """Compute uncertainty ellipses for a given skymap"""
    skymap_table = read_map_gracedb(graceid, filename, client, moc_table=True)
    result = find_injection_moc(skymap_table, contours=[cl/100])
    greedy_area = result.contour_areas[0]
    prob = read_map_gracedb(graceid, filename, client)[0]
    ra, dec, a, b, pa, ellipse_area = find_ellipse(prob, cl=cl,
                                                   projection='ARC',
                                                   nest=False)
    return ellipse_area <= 1.35*greedy_area, ra, dec, a, b, pa, \
        ellipse_area, greedy_area
