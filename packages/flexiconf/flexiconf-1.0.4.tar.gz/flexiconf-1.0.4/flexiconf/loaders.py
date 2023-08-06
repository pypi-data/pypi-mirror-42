import configparser
import glob
import json
import os
import re
import sys

from .utils import NOT_SET, get_caller_path, split_key_path


class BaseLoader:
    def __init__(self):
        pass

    def load(self, config_data: dict):
        raise NotImplementedError()

    @staticmethod
    def insert_path_in_dict(data: dict, key_path: str):
        inner_keys, last_key = split_key_path(key_path)
        current_dict = data
        for key in inner_keys:
            if key not in current_dict or not isinstance(current_dict[key], dict):
                current_dict[key] = dict()
            current_dict = current_dict[key]
        return current_dict, last_key

    @staticmethod
    def enumerate_files(config_files_pattern: str):
        return [filename for filename in glob.iglob(config_files_pattern, recursive=True) if os.path.isfile(filename)]

    @staticmethod
    def normalize_dict(data: dict):
        return {key.lower(): value for key, value in data.items()}


class JsonLoader(BaseLoader):
    def __init__(self, config_files_pattern: str = NOT_SET):
        super(JsonLoader, self).__init__()
        if config_files_pattern is NOT_SET:
            config_files_pattern = os.path.join(get_caller_path(), '**/*.json')
        self.files_pattern = config_files_pattern

    def load(self, config_data: dict):
        files_list = self.enumerate_files(self.files_pattern)
        for file in files_list:
            with open(file) as json_file:
                new_data = json.load(json_file)
                new_data = self.normalize_dict(new_data)
                config_data.update(new_data)


class IniLoader(BaseLoader):
    def __init__(self, config_files_pattern: str = NOT_SET):
        super(IniLoader, self).__init__()
        if config_files_pattern is NOT_SET:
            config_files_pattern = os.path.join(get_caller_path(), '**/*.ini')
        self.files_pattern = config_files_pattern

    def load(self, config_data: dict):
        files_list = self.enumerate_files(self.files_pattern)
        for file in files_list:
            config = configparser.ConfigParser()
            config.read(file)
            for section_name in config.sections():
                section_dict, _ = self.insert_path_in_dict(config_data, section_name + '._')
                read_section = self.normalize_dict(dict(config[section_name]))
                section_dict.update(read_section)


class ArgsLoader(BaseLoader):
    def __init__(self):
        super(ArgsLoader, self).__init__()

    def load(self, config_data: dict):
        cl_arguments = sys.argv[1:]
        # We are looking only for parameters that look like [--]key=value
        for arg in cl_arguments:
            if '=' in arg:
                self._insert_parameter(config_data, arg)

    @staticmethod
    def _remove_prefix(parameter: str):
        prefix_counter = 0
        for x in parameter:
            if x != '-':
                break
            prefix_counter += 1
        return parameter[prefix_counter:]

    def _insert_parameter(self, data: dict, parameter: str):
        key, value = self._remove_prefix(parameter).split('=', 1)
        if key and value:
            parent_dict, last_key = self.insert_path_in_dict(data, key)
            parent_dict[last_key] = value


class EnvLoader(BaseLoader):
    def __init__(self, key_pattern: str = None):
        super(EnvLoader, self).__init__()
        self.pattern = None
        if key_pattern:
            self.pattern = re.compile(key_pattern)

    def load(self, config_data: dict):
        for key, value in os.environ.items():
            if self.pattern and not self.pattern.fullmatch(key):
                continue
            current_dict, last_key = self.insert_path_in_dict(config_data, key)
            current_dict[last_key] = value
