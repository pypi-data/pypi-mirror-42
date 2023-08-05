""" Console logging functionality """
import logging
import coloredlogs

logger = logging.getLogger('sink') # pylint: disable=invalid-name

coloredlogs.install(level=logging.INFO,
                    fmt='%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s')

def get_logger(name):
    """ Return a child logger for use within a specific module """
    log = logger.getChild(name)
    return log

def set_debug_logging():
    """ Set logging output to DEBUG """
    logger.setLevel(logging.DEBUG)
