"""Portable Logger anywhere for import."""
import logging.config
import pdb
import yaml
import os

class SetUpLogging():
    def __init__(self):
        self.default_config = os.path.join(os.path.dirname(
            os.path.abspath('__file__')), "linkedin/spiders/configs/logging_config.yaml")

    def setup_logging(self, default_level=20):
        path = self.default_config
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
                logging.captureWarnings(True)
        else:
            logging.basicConfig(
                filename='job_description_spider.log',
                filemode='w',
                level=logging.DEBUG,
                format="%(asctime)s:%(levelname)s:%(filename)s:%(message)s"
            )