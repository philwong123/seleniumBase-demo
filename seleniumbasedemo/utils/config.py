#!/usr/bin/env python3

import yaml


class Config(object):
    """ Basic methods for configurations.

    load_config: load configuration.

    Attributes:
        config: A dictionary of configuration settings.

    """

    def __init__(self, path_to_config):
        self.config = self.load_config(path_to_config)

    def load_config(self, path_to_config):
        """Load config from config file

        Args:
            path_to_config_file: path of configuration file.

        Returns:
            A dictionary of configuration settings.

        Raises:
            yaml.YAMLError: An error occurred load to configuration file.
        """
        with open(path_to_config) as file:
            try:
                parsed_yaml = yaml.safe_load(file)
            except yaml.YAMLError as error:
                if hasattr(error, 'problem_mark'):
                    mark = error.problem_mark
                    print(
                        f"Error parsing Yaml file at line {mark.line}, column {mark.column+1}.")
                else:
                    print("Something went wrong while parsing yaml file")
                return

            return parsed_yaml
