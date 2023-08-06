import io
import json
import boto3
import scrapy
import PyPDF2
import random
import hashlib
import pathlib

from datetime import datetime, timedelta, timezone

class LegalLabsSpider(scrapy.Spider):

    def init(self):
        self.init_S3()
        self.date_len = int(self.settings.attributes['CRAWLER_DATE_LEN'].value)
        self.date = self.settings.attributes['CRAWLER_DATE'].value
        if type(self.date) == str:
            self.date = datetime.strptime(self.date, '%d/%m/%Y').replace(tzinfo=timezone.utc)
        self.date_end = self.date
        self.date_start = self.date-timedelta(days=self.date_len)

    def init_S3(self):
        self.tribunal = self.settings.attributes['TRIBUNAL'].value
        self.pdf_bucket = self.settings.attributes['AWS_BUCKET'].value
        self.save_mode = self.settings.attributes['SAVE_MODE'].value.upper()
        self.S3 = boto3.client('s3',
            aws_access_key_id=self.settings.attributes['AWS_ACCESS_KEY_ID'].value,
            aws_secret_access_key=self.settings.attributes['AWS_SECRET_ACCESS_KEY'].value
        )

    def get_cookies(self, response):
        cookies = response.headers.getlist('Set-Cookie')
        if cookies:
            cookies = cookies[0].decode().split('; ')
            cookies = {cookie.split('=')[0]:"=".join(cookie.split('=')[1:]) for cookie in cookies}
            try:
                if 'cookies' not in response.meta:
                    response.meta['cookies'] = {}
                response.meta['cookies'].update(cookies)
            except:
                pass

    def save_diario(self, response, date, name):
        name = self.get_UUID(self.get_date_str(date, date_format='%d%m%Y')+name+'secret')
        file = self.save_file(response, name, type_='diario', extension='pdf')
        return {'file': file, 'id': name}

    def save_html_as_pdf(self, response=None, url=None, name="", type_='inteiro_teor'):
        import pdfkit
        pdf = pdfkit.from_url(url, False, options = {
            'quiet': ''
        })
        response = response.replace(body=pdf)
        self.save_file(response, name=name, type_='inteiro_teor', extension='pdf', check_response_type=False)

    def save_pdf(self, response, name="", type_='inteiro_teor'):
        return self.save_file(response, name, type_, extension='pdf')

    def save_file(self, response, name="", type_='inteiro_teor', extension='pdf', check_response_type='pdf'):
        content = None
        if hasattr(response, 'seek'):
            content = response.body
        else:
            if check_response_type:
                if response.headers.get('Content-Type').decode().find(check_response_type)==-1:
                    return None
            content = response.body
        if not content:
            return None
        file = self.tribunal.lower()+'/'+type_+'/'+name+'.'+extension.strip('.')
        if self.save_mode=='S3':
            f = io.BytesIO(content)
            self.S3.upload_fileobj(f, self.pdf_bucket, file, ExtraArgs={
                'ContentType': 'application/pdf'
            })
            return file
        elif self.save_mode=='LOCAL':
            file = pathlib.Path(file)
            file.parent.mkdir(parents=True, exist_ok=True)
            with file.open('wb') as f:
                f.write(content)
            return str(file)

    def extract_pdf_text(self, file):
        pages = []
        if not hasattr(file, 'seek'):
            file = open(file, 'rb')
        pdfReader = PyPDF2.PdfFileReader(file)
        count = pdfReader.numPages
        for i in range(count):
            page = pdfReader.getPage(i)
            pages.append(page.extractText())
        file.close()
        return pages

    def get_date_str(self, date, date_format='%d/%m/%Y'):
        return date.strftime(date_format)

    def parse_date_str(self, date, date_format='%d/%m/%Y'):
        return datetime.strptime(date, date_format).replace(tzinfo=timezone.utc)

    def get_UUID(self, data):
        return hashlib.sha256(json.dumps(data).encode('utf-8')).hexdigest()
