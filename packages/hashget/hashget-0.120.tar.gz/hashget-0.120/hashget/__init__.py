import datetime

#from .cacheget import CacheGet
# from .hashutils import walk_arc, unpack_deb
#from .debian import DebPackage, load_release
#from .hashdb import HashDB, DirHashDB, HashPackage, HashDBClient
#from .submiturl import submit_url
#from .file import File, FileList
import os
import requests
#import cachecontrol
from .anchor import AnchorList

from . import cacheget

__version__ = '0.120'

__all__ = ["utils", "cacheget", "package", "restorefile", "hashdb", "hashpackage", "file", "submiturl"]

cacheget.user_agent = 'HashGet/{version}'.format(version=__version__)
