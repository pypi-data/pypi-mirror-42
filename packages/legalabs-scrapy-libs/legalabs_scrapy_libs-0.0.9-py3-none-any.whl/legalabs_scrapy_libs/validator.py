import legalabs_scrapy_libs.validation_functions as vf
import legalabs_scrapy_libs.utils as utils
import re

from legalabs_scrapy_libs.stopwords import stopwords_set
from cerberus import Validator

class LegalLabsValidator(Validator):
    def _validate_capitalized(self, validation_value, field, value):
        """
            Tests if the input string is capitalized, excluding stopwords:
            Just an Example of Capitalized Words
            The rule's arguments are validated against this schema:
            {'type': 'boolean'}
        """
        try:
            if validation_value != vf.is_capitalized(value, stopwords_set):
                msg = 'Must {}be capitalized'.format('' if validation_value else 'not ')
                return self._error(field, msg)
        except Exception as err:
            self._error(field, str(err))

    def _validate_proper_name(self, validation_value, field, value):
        """
            Tests if the input string is a proper name with the following rules:
                - Must not have more than 10 names
                - Each name must have the min/max length of 2/12
                - Each name (exluding stopwords) must be capitalized
            Example:
            Amorim da Silva
            The rule's arguments are validated against this schema:
            {'type': 'boolean'}
        """
        try:
            if validation_value != vf.is_proper_name(value, stopwords_set):
                msg = 'Must {}be a proper name'.format('' if validation_value else 'not ')
                return self._error(field, msg)
        except Exception as err:
            self._error(field, str(err))

    def _validate_valid_state_acronym(self, validation_value, field, value):
        """
            Tests if the input string is a valid Brazil state acronym
            Examples:
                DF, MG, SP, RJ etc
            The rule's arguments are validated against this schema:
            {'type': 'boolean'}
        """
        try:
            if validation_value != vf.is_valid_state_acronym(value):
                msg = 'Must {}be a valid state acronym'.format('' if validation_value else 'not ')
                return self._error(field, msg)
        except Exception as err:
            self._error(field, str(err))

    def _validate_valid_date(self, validation_value, field, value):
        """
            Tests if the input string/date is a valid date and is within
            reasonable range (not too old, not in the future)
            The rule's arguments are validated against this schema:
            {'type': 'boolean'}
        """
        try:
            if validation_value != vf.is_date_reasonable(value):
                msg = 'Must {}be a valid date'.format('' if validation_value else 'not ')
                return self._error(field, msg)
        except Exception as err:
            self._error(field, str(err))


    def _normalize_coerce_capitalize(self, value):
        if type(value)==list:
            return [utils.capitalize(val) for val in value]
        return utils.capitalize(value)

    def _normalize_coerce_relator(self, value):
        return utils.normalize_relator(value)

    def _normalize_coerce_relator_cargo(self, value):
        return utils.normalize_relator_cargo(value)

    def _normalize_coerce_orgao_julgador(self, value):
        return utils.normalize_orgao_julgador(value)

    def _normalize_coerce_uppercase(self, value):
        return value.strip().upper()

    def _normalize_coerce_lowercase(self, value):
        return value.strip().lower()

    def _normalize_coerce_text(self, value):
        value = re.sub('E M E N T A', 'EMENTA', value, flags=re.IGNORECASE)
        value = re.sub('A C Ó R D Ã O', 'ACÓRDÃO', value, flags=re.IGNORECASE)
        value = re.sub('V O T O', 'VOTO', value, flags=re.IGNORECASE)
        value = re.sub('[\r\xa0]', '', value)
        value = re.sub('\n+', '\n', value)
        return value.strip()

# schema = {
    # 'amount': {
        # 'valid_date': True,
        # 'type': 'string'
    # }
# }
# v = LegalLabsValidator(schema)
# print(v.validate({'amount': '2008-09-03T20:56:35.450686Z'}))
# print(v.errors)

