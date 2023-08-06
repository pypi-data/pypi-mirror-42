"""Returns appropriate storage provider based on the url provided"""
from pkg_resources import iter_entry_points
from pkg_resources import load_entry_point
from urlparse import urlparse
import fs
from .interface import Interface

STORAGE_TYPES = {}
LOADED_TYPES = {}
DEFAULT_TYPE = None

for entry_point in iter_entry_points('flywheel.storage'):
    STORAGE_TYPES[entry_point.name] = entry_point


def create_flywheel_fs(url, default='osfs'):
    """
    This loads the storage provider based on the url provided
    """

    protocol = None
    url_parts = urlparse(url)
    if url_parts[0]:
        protocol = url_parts[0]

    if protocol and protocol in STORAGE_TYPES:
        if protocol not in LOADED_TYPES:
            LOADED_TYPES[protocol] = STORAGE_TYPES[protocol].load()
        return LOADED_TYPES[protocol](url)

    if default in STORAGE_TYPES:
        if default not in LOADED_TYPES:
            LOADED_TYPES[default] = STORAGE_TYPES[default].load()
        # Assume the rest are paths which we can use with osfs even though they are not urls
        return LOADED_TYPES[default](url)

    # raise ValueError('Could not load the storage type specified: {}'.format(protocol if protocol else default))
    print 'storage provider is not loaded for this type'
    print protocol


def path_from_uuid(uuid_):
    """
    create a filepath from a UUID
    e.g.
    uuid_ = cbb33a87-6754-4dfd-abd3-7466d4463ebc
    will return
    cb/b3/cbb33a87-6754-4dfd-abd3-7466d4463ebc
    """
    uuid_1 = uuid_.split('-')[0]
    first_stanza = uuid_1[0:2]
    second_stanza = uuid_1[2:4]
    path = (first_stanza, second_stanza, uuid_)
    return fs.path.join(*path)

def format_hash(hash_alg, hash_):
    """
    format the hash including version and algorithm
    """
    return '-'.join(('v0', hash_alg, hash_))
