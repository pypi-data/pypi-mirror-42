import logging
import os
import traceback
import sys

# TODO: Modularize code (create methods or functions)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(levelname)s]%(module)s:%(lineno)d'
                              '{%(funcName)s}:%(message)s')

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)

fh = logging.FileHandler('/logs/textos.log')

formatter = logging.Formatter('{"@timestamp":"%(asctime)s",'
                              '"@version":1,'
                              '"message": "%(message)s",'
                              '"logger_name": "%(module)s",'
                              '"thread_name": "%(threadName)s",'
                              '"level": "%(levelname)s",'
                              '"level_value": "%(levelno)s",'
                              '"stack_trace": "' +
                              traceback.format_exc().strip() + '",'
                              '"app_name": "textos"}')

fh.setFormatter(formatter)

fh.setLevel(logging.DEBUG)

logger.addHandler(fh)
logger.addHandler(handler)
