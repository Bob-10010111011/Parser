from bs4 import BeautifulSoup
import logging



class Parser:
    def __init__(self, html_file):
        self.soup = None
        self.html_file = html_file


    def load_html_file(self):
        logging.info('Loading HTML file.')
        with open(self.html_file, 'r') as html:
            self.soup = BeautifulSoup(html, "html.parser")
            return


    def get_headers(self): # func for giving header of courses
        result1 = []

        for i in [i.find_all("a") for i in self.soup.body.find_all('template')]:
            for u in i:
                result1.append(u.string)

        return result1


    def get_links(self): # func for giving links on courses
        result2 = []

        for i in [i.find_all("a") for i in self.soup.body.find_all('template')]:
            for u in i:
                result2.append(u.get('href'))

        return result2
