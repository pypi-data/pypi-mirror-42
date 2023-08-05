# -*- coding: utf8 -*-
import os
import warnings

import six

try:
    import ConfigParser as configparser
except ImportError:
    import configparser


config_file_name = 'config'


def parse_bool(val):
    return val.lower() in ['true', '1']


class DataVolumeConfig(object):
    def __init__(self, path, general_config_path=None):
        self._config_file = os.path.join(path, config_file_name)

        parser = configparser.RawConfigParser()
        config_files = [self._config_file]
        if general_config_path is not None:
            config_files.append(general_config_path)

        parser.read(config_files)

        self.parser = parser
        self._sections = {}

    @property
    def embedded(self):
        val = self.general_config.get('embedded', False)

        if isinstance(val, six.string_types):
            val = parse_bool(val)

        return val

    @property
    def org(self):
        return self.get('org')

    @property
    def volume_id(self):
        return int(self.get('id', mandatory=True))

    def get_boolean(self, section, name, default_value=False, must_exists=False):
        try:
            return self.parser.getboolean(section, name)
        except (configparser.NoSectionError, configparser.NoOptionError):
            if must_exists:
                raise

            return default_value

    @property
    def db_type(self):
        return self.db_config.get('type')

    @property
    def object_store_type(self):
        return self.object_store_config.get('type')

    def get(self, key, mandatory=False):
        if mandatory:
            return self.general_config[key]

        return self.general_config.get(key)

    @property
    def data_path(self):
        return self.general_config.get('datapath')

    @property
    def general_config(self):
        return self.items('general')

    @property
    def db_config(self):
        return self.items('db')

    @property
    def object_store_config(self):
        object_store_config = self.items('object_store')

        return object_store_config

    def items_from_parse(self, parser, section, must_exists):
        try:
            if section not in self._sections:
                self._sections[section] = dict(parser.items(section))

            return self._sections[section]
        except configparser.NoSectionError:
            if must_exists:
                raise

            return self._sections.setdefault(section, {})

    def items(self, section, most_exists=False):
        return self.items_from_parse(self.parser, section, must_exists=most_exists)

    def set(self, section, key, val):
        try:
            self.parser.add_section(section)
        except configparser.DuplicateSectionError:
            pass

        if six.PY2 and isinstance(val, str):
            val = val.encode('utf8')

        self.parser.set(section, key, val)

    def _write(self, fo):
        self.parser.write(fo)

    def save(self):
        with open(self._config_file, 'w') as configfile:
            self._write(configfile)

    def update_and_save(self, d):
        for section, section_values in d.items():
            for key, val in section_values.items():
                if val is None:
                    continue

                self.set(section, key, val)

        self.save()

    def remove_option(self, section, name):
        try:
            self.parser.remove_option(section, name)
        except configparser.NoSectionError:
            pass
