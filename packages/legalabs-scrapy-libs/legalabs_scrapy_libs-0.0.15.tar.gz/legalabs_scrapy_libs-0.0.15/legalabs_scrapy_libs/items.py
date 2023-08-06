import yaml
import os

try:
    from scrapy_libs.validator import LegalLabsValidator
except:
    from legalabs_scrapy_libs.validator import LegalLabsValidator

def init():
    path = os.path.dirname(os.path.realpath(__file__))
    schema_filename = os.path.join(path, './schemas/acordao.yaml')

    with open(schema_filename, 'r') as schema_file:
        raw_schema_yaml = schema_file.read()

    decisao_schema = yaml.load(raw_schema_yaml)
    decisao_validator = LegalLabsValidator(decisao_schema)
    return decisao_schema, decisao_validator

decisao_schema, decisao_validator = init()
