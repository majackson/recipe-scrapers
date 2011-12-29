import logging
import os

from allergy_assistant import settings, db

def init(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    fh = logging.FileHandler(os.path.join(settings.LOG_PATH, logger.name))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

def log_request(request, response):

    request_dict = {}

    request_dict['request_time'] = request.request_time()
    request_dict['url'] = request.uri
    request_dict['args'] = request.arguments
    request_dict['headers'] = request.headers

    db.requests.insert({'request': request_dict, 'response': response})
