"""
Usage:

python3 obfuscate_csv.py \
--column_regex_replace <column>-'<regex>'-'<replace>' \
--output_csv obfuscated.csv

NAME REGEX '(?<=\w{1})\w'
EMAIL REGEX '(?<=.{1}).(?=[^@]*?@)'
PHONE REGEX '\d(?!\d{0,3}$)'

"""
import re
import csv
import click
import pandas as pd
import yaml
import os
import errno


def load_csv_file_to_dataframe(csv_file_path):
    """
    Loads CSV file into pandas DataFrame
    """
    return pd.read_csv(csv_file_path, encoding='utf-8')


def save_csv_file(dataframe, csv_file_path):
    """
    Save CSV file
    """
    if not os.path.exists(os.path.dirname(csv_file_path)):
        try:
            os.makedirs(os.path.dirname(csv_file_path))
        except OSError as e: # Guard against race condition
            if e.errno != errno.EEXIST:
                raise
    
    dataframe.to_csv(csv_file_path, encoding='utf-8', index=False)


@click.command()
@click.option(
    '--input_csv',
    type=click.File('r'),
    required=True,
    help='Input CSV file to be obfuscated'
)
@click.option(
    '--output_csv',
    type=click.File('w'),
    required=True,
    help='Output obfuscated CSV file to be saved'
)
@click.option(
    '--config_file',
    type=click.File('r'),
    required=True,
    help='YAML file to configure obfuscation'
)
@click.option(
    '--string_data',
    type=click.STRING,
    default=False,
    help='Read CSV data as str'
)
def anonimize(input_csv, output_csv, config_file, string_data):
    """
    Anonymize CSV file
    """
    dataframe = load_csv_file_to_dataframe(input_csv.name)
    
    """
    Read data as str
    """
    if string_data:
        dataframe = dataframe.astype(str)
    
    """
    Read YAML file with flat paths
    """
    with open(config_file.name, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            """
            Parse configurations
            """
            for column in config.keys():
                regex = config[column]['regex']
                replace = config[column]['replace']
                dataframe[column].replace(value=replace, regex=regex, inplace=True)
        except yaml.YAMLError as e:
            print(e)

    save_csv_file(dataframe, output_csv.name)
    

if __name__ == '__main__':
    main()