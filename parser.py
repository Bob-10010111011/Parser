import os
import sqlite3
import ssl
from bs4 import BeautifulSoup
from urllib.request import urlopen
import logging

logging.basicConfig(level=logging.INFO, filename="log.log", filemode='a',
                    format="%(asctime)s - %(levelname)s - %(lineno)d - %(message)s")

# logging.debug('debug')
# logging.info('info')
# logging.warning('warning')
# logging.error('error')
# logging.critical('critical')


# url = 'https://online.dr-chuck.com/' # - source
# f_name = 'sourse.html' # - name of file

# Claas for saving as site to file
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


# Class for opening file and getting links and headers
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
        result1 = [tag.get_text() for tag in self.soup('h3')]
        return result1


    def get_links(self): # func for giving links on courses
        directory = self.soup.select('div.span4 > a')
        result2 = [i.get('href') for i in directory]
        return result2


# Class for creating and filling out the table
class Database:
    def __init__(self, headers, links):
        self.fname = 'H-L.db'
        with sqlite3.connect(self.fname) as self.conn:
            self.cur = self.conn.cursor()
        self.headers = headers
        self.links = links


    # creating a table
    def create_t(self):
        logging.info('Creating tables in DB.')
        self.cur.executescript('''
            DROP TABLE IF EXISTS Courses;
            DROP TABLE IF EXISTS Links;

            CREATE TABLE Courses (
                id  INTEGER PRIMARY KEY AUTOINCREMENT,
                course_name    TEXT UNIQUE
            );

            CREATE TABLE Links (
                id  INTEGER PRIMARY KEY AUTOINCREMENT,
                courses_id  INTEGER,
                link    TEXT UNIQUE
            );
        ''')


    def fill_the_table(self):
        if len(self.headers) == len(self.links):
            logging.info('Filling tables.')
            for name, link in zip(self.headers, self.links):
                self.cur.execute('''INSERT OR IGNORE INTO Courses(course_name) VALUES (?)''',(name,))
                self.cur.execute('SELECT id FROM Courses WHERE course_name = ? ', (name,))
                course_id = self.cur.fetchone()[0]
                self.cur.execute(
                    '''INSERT OR IGNORE INTO Links(courses_id, link) VALUES ( ?, ? )''',(course_id, link,))
            self.conn.commit()
            logging.info(f'File "{self.fname}" is done.')
        else:
            logging.error('Error: Number of headers is not equal to number of links.')

    def tables_exist(self):
        self.cur.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='Courses';
        """)
        return self.cur.fetchone() is not None


    def closing(self):
        logging.info('Closing DB.')
        self.conn.close()


def run():
    if os.path.exists('sourse.html'):
        html_path ='sourse.html'  # giving file to Parser
    else:
        s = Saving_to()  # connecting and saving file for parse
        html_path = s.save_to_html()  # giving file to Parser

    p = Parser(html_path)
    p.load_html_file()  # load file for parse

    headers = p.get_headers()
    links = p.get_links()

    db = Database(headers, links)  # giving to class our headers and links

    if not db.tables_exist():
        db.create_t()  # create tables

    db.fill_the_table()  # filling the tables
    db.closing()
    logging.info('Process completed.')

run()








