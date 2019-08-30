import unittest
import anonymize_csv
import pandas as pd
import os.path
import os
import yaml
import click
from click.testing import CliRunner
from pathlib import Path

class TestAnonymizeCSV(unittest.TestCase):
    

    @classmethod
    def setUpClass(cls):
        config_file_name = 'test_config.yaml'
        
        yaml_data = dict(
            NAME = dict(
                regex = '(?<=\w{1})\w',
                replace = '*'
            )
        )

        with open(config_file_name, 'w') as file:
            yaml.dump(yaml_data, file, default_flow_style=False)


    @classmethod
    def tearDownClass(cls):
        os.remove('test_config.yaml')


if __name__ == '__main__':
    unittest.main()