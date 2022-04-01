from brainzutils import cache
from brainzutils.musicbrainz_db import label as db
from brainzutils.musicbrainz_db import serialize
from brainzutils.musicbrainz_db import unknown_entities

from critiquebrainz.frontend.external.musicbrainz_db import DEFAULT_CACHE_EXPIRATION
from critiquebrainz.frontend.external.relationships import label as label_rel


def label_is_unknown(label):
    return label['name'] == unknown_entities.unknown_label.name


def get_label_by_id(mbid):
    """Get label with MusicBrainz ID.

    Args:
        mbid (uuid): MBID(gid) of the label.
    Returns:
        Dictionary containing the label information
    """
    key = cache.gen_key('label', mbid)
    label = cache.get(key)
    if not label:
        label = db.get_label_by_id(
            mbid,
            includes=['artist-rels', 'url-rels'],
            unknown_entities_for_missing=True
        )
        if label_is_unknown(label):
            return None
        cache.set(key=key, val=label, time=DEFAULT_CACHE_EXPIRATION)
    return label_rel.process(label)
