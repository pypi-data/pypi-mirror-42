import re
from legalabs_scrapy_libs.stopwords import stopwords_set
from datetime import datetime

norm_num_table = {
    'primeira': '1ª',
    'segunda': '2ª',
    'terceira': '3ª',
    'quarta': '4ª',
    'quinta': '5ª',
    'sexta': '6ª',
    'sétima': '7ª',
    'setima': '7ª',
    'oitava': '8ª',
    'nona': '9ª',
    'décima': '10ª',
    'decima': '10ª',
    'vigésima': '20ª',
    'vigesima': '20ª',
    'trigésima': '30ª',
    'trigesima': '30ª',
    'quadragésima': '40ª',
    'quadragesima': '40ª',

    'primeiro': '1º',
    'segundo': '2º',
    'terceiro': '3º',
    'quarto': '4º',
    'quinto': '5º',
    'sexto': '6º',
    'sétimo': '7º',
    'setimo': '7º',
    'oitavo': '8º',
    'nono': '9º',
    'décimo': '10º',
    'decimo': '10º',
    'vigésimo': '20º',
    'vigesimo': '20º',
    'trigésimo': '30º',
    'trigesimo': '30º',
    'quadragésimo': '40º',
    'quadragesimo': '40º',
}

relator_cargo_table = {
    'des': 'Desembargador(a)',
    'desa': 'Desembargador(a)',
    'desas': 'Desembargador(a)',
    'min': 'Ministro(a)',
    'rel': '',
    'min.-rel': 'Misistro(a)'
}

roman_numbers_set = set('''
I II III IV V VI VII VIII IX X
XI XII XIII XIV XV XVI XVII XVIII
XIX XX XXI XXII XXIII XXIV XXV XXVI
XXVII XXVIII XXIX XXX XXXI XXXII XXXIII
XXXIV XXXV XXXVI XXXVII XXXVIII XXXIX
XL XLI XLII XLIII XLIV XLV XLVI XLVII
XLVIII XLIX L LI LII LIII LIV LV LVI
LVII LVIII LIX LX LXI LXII LXIII LXIV
LXV LXVI LXVII LXVIII LXIX LXX LXXI
LXXII LXXIII LXXIV LXXV LXXVI LXXVII
LXXVIII LXXIX LXXX LXXXI LXXXII LXXXIII
LXXXIV LXXXV LXXXVI LXXXVII LXXXVIII
LXXXIX XC XCI XCII XCIII XCIV XCV
XCVI XCVII XCVIII XCIX
'''.split())

def normalize_text(text):
    text = text.strip()
    return text

def normalize_relator(text):
    text = re.sub(
        r'ministr[oa]|(min\.?\s)|(\(.*?\))|des\.\(a\)|des\(a\)\.?|des\.|desembargador[a]?|federal',
        "",
        text.strip().lower(),
        flags=re.IGNORECASE
    )
    text = capitalize(text)
    return text

def normalize_relator_cargo(text):
    key = text.strip(' \t\r\n\f.ªº').lower()

    if key in relator_cargo_table:
        return relator_cargo_table[key]

    return capitalize(text)

def normalize_orgao_julgador(text):
    text = text.strip().lower()
    for key, val in norm_num_table.items():
        text = text.replace(key, val)
    for j in range(10,50,10):
        for i in range(1,10):
            text = text.replace('%dª %dª'%(j,i),'%dª'%(i+j))
            text = text.replace('%dº %dº'%(j,i),'%dº'%(i+j))
    text = capitalize(text)
    return text

def capitalize(text):
    capitalized = []
    text = text.strip().lower().split()
    for word in text:
        if word not in stopwords_set:
            word = word.capitalize()
        if word.upper() in roman_numbers_set:
            word = word.upper()
        capitalized.append(word)
    return ' '.join(capitalized)

def get_date_str(date, date_format='%d/%m/%Y'):
    return date.strftime(date_format)

def parse_date_str(date, date_format='%d/%m/%Y'):
    date = datetime.strptime(date, date_format)
    if date.year < 100:
        date = date.replace(year=date.year+2000)
    return date
