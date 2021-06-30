import logging
import sys
from .ADBSession import ADBSession 
logger = logging.getLogger(__name__)

server_mumu = ('127.0.0.1', 5037)

def create_ADBSession():
    sess = ADBSession()
    return sess