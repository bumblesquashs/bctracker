
import logging
import sys

from logging.handlers import TimedRotatingFileHandler
from requestlogger import WSGILogger, ApacheFormatter

from dataclasses import dataclass

@dataclass(init=False, slots=True)
class LogService:
    
    name: str
    logger: logging.Logger
    
    def __init__(self, name: str = 'bctracker'):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')
        
        file_handler = TimedRotatingFileHandler(filename=f'logs/{name}.log', when='d', interval=7)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        self.name = name
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
    
    def get_access_logger(self, server) -> WSGILogger:
        handler = TimedRotatingFileHandler(filename='logs/access_log.log', when='d', interval=7)
        return WSGILogger(server, [handler], ApacheFormatter())
    
    def read_logs(self) -> list[str]:
        try:
            with open(f'logs/{self.name}.log', 'r') as file:
                return file.readlines()
        except Exception as e:
            self.error(f'Failed to read logs: {e}')
            return []
