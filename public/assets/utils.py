# utils.py

import os
import logging
from datetime import datetime
from typing import Dict, List

class Logger:
    def __init__(self, name: str, level: int = logging.INFO):
        self.name = name
        self.level = level
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.handler = logging.StreamHandler()
        self.handler.setLevel(level)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

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

def get_current_time() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_file_size(path: str) -> int:
    return os.path.getsize(path)

def create_directory(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def load_json_file(path: str) -> Dict:
    with open(path, 'r') as file:
        return json.load(file)

def save_json_file(data: Dict, path: str) -> None:
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

def get_list_from_json_array(json_array: List) -> List:
    return [d['id'] for d in json_array]