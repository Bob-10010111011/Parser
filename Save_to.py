import ssl
from bs4 import BeautifulSoup
from urllib.request import urlopen
import logging



class Saving_to:
    def __init__(self):
        self.url = 'https://online.dr-chuck.com/' # - source
        logging.info(f'Connecting to {self.url}')
        self.f_name = 'sourse.html' # - name of file

        # Ignore errors of SSL-certificate
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE



    def save_to_html(self):
        try:
            data = urlopen(self.url, context=self.ctx).read()
            soup = BeautifulSoup(data, 'html.parser')
            logging.info(f'Saving HTML file.')

            with open(self.f_name, 'w') as f:
                f.write(soup.decode())
                return self.f_name
        except Exception as e:
            logging.error(f'Failed to download or save HTML: {e}')

            raise




