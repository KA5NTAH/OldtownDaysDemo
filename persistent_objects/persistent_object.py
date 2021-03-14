from abc import ABC, abstractmethod


class PersistentObject:
    def __init__(self, config_file_path: str):
        self._config_path = config_file_path

    @abstractmethod
    def dump_into_file(self):
        """dump info in config_file"""

    @abstractmethod
    def _init_from_file(self):
        """if there is no file write empty json otherwise fill params with values in file"""
