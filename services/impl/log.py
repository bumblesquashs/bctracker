
import logging
import sys

from logging.handlers import TimedRotatingFileHandler

from dataclasses import dataclass

@dataclass(init=False, slots=True)
class LogService:
    
    logger: logging.Logger
    
    def __init__(self, name: str = 'bctracker'):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')
        
        fileHandler = TimedRotatingFileHandler(filename=f'logs/{name}.log', when='d', interval=7)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)
        
        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setFormatter(formatter)
        logger.addHandler(consoleHandler)
        
        self.logger = logger
    
    def debug(self, msg: str):
        self.logger.debug(msg)
    
    def info(self, msg: str):
        self.logger.info(msg)
    
    def warning(self, msg: str):
        self.logger.warning(msg)
    
    def error(self, msg: str):
        self.logger.error(msg)
    
    def critical(self, msg: str):
        self.logger.critical(msg)