import datetime
import dateutil.parser
import re

def is_capitalized(text, stopwords=[]):
    if type(text) != str:
        raise Exception('Text input must be string')

    stopwords_type = type(stopwords)

    if stopwords_type != list and stopwords_type != tuple and \
       stopwords_type != dict and stopwords_type != set:
        raise Exception('Stopwords must be list/tuple/dict/set')

    words = text.split()

    for word in words:
        word_lower = word.lower()
        if word_lower in stopwords:
            if word_lower != word:
                return False
        else:
            if not word[0].isupper():
                return False
            if word[1:] != word_lower[1:]:
                return False

    return True


def is_proper_name(text, stopwords=[]):
    names = re.sub(r'\(.*?\)|[-.]','',text)
    if len(names)<2 or len(names)>200:
        return False
    return True

def is_date_reasonable(date, min_year=1950, future_day_limit=10):
    if type(date) == str:
        try:
            date = dateutil.parser.parse(date).replace(tzinfo=datetime.timezone.utc)
        except:
            return False

    if type(date) != datetime.datetime:
        raise Exception('Input must be a datetime')

    today = datetime.datetime.now(datetime.timezone.utc)

    # Either too old or in the future
    if date.year < min_year or (date > today and (date - today).days > future_day_limit):
        return False

    return True

# 0000001-03.2008.8.26.0358
# 0000001.03.2008.8.26.0358
__validator_case_number_regex = re.compile(r'^\d{7}[-.]\d\d\.[12]\d{3}\.\d\.\d\d\.\d{4}$')

def is_tribunal_case_number_valid(case_number):
    if type(case_number) != str:
        raise Exception('Input must be str')
    if not __validator_case_number_regex.match(case_number):
        return False

    return True

__states_acronyms_set = set('''
AC AL AP AM BA
CE DF ES GO MA
MT MS MG PA PB
PR PE PI RJ RN
RS RO RR SC SP
SE TO
'''.split())

def is_valid_state_acronym(string):
    if type(string) != str:
        raise Exception('Input must be str')
    
    # OTHER COUNTRIES
    valid_len = len(string.strip())==2 or len(string.strip())==3
    
    return (string.strip().upper() in __states_acronyms_set) or valid_len
