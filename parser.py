from bs4 import BeautifulSoup
import urllib.request, urllib.error
from urllib.request import urlopen
import ssl
import sqlite3


# Ignore errors of SSL-certificate
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://online.dr-chuck.com/' # - source for parse

# opening source and getting links and headers
class Parser:
    def __init__(self, url):
        self.url = url

    def load_url(self):
        html = urlopen(self.url, context=ctx).read()
        self.soup = BeautifulSoup(html, "html.parser")

    def get_headers(self): # func for giving header of courses
        result1 = [tag.get_text() for tag in self.soup('h3')]
        return result1

    def get_links(self): # func for giving links on courses
        directory = self.soup.select('div.span4 > a')
        result2 = [i.get('href') for i in directory]
        return result2


p = Parser(url)
p.load_url()


print(f'Connecting to: {url} ...\n')

fname = input('Enter the file name: ')+'.db'


# fill out the table
class Database:
    def __init__(self, headers, links):
        try:  # do if file exist
            self.conn = sqlite3.connect(fname)

        except FileNotFoundError:  # do if file not exist
            print(f'File not found. Creating new file: {fname}\n')
            self.conn = sqlite3.connect(fname)

        self.headers = headers
        self.links = links
        self.cur = self.conn.cursor()


    # creating a table
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
        for name, link in zip(self.headers, self.links):
            self.cur.execute('''INSERT OR IGNORE INTO Courses
                    (course_name) 
                    VALUES (?)''',
                        (name,))
            self.cur.execute('SELECT id FROM Courses WHERE course_name = ? ', (name,))
            course_id = self.cur.fetchone()[0]
            self.cur.execute('''INSERT OR IGNORE INTO Links
                        (courses_id, link) 
                        VALUES ( ?, ? )''',
                        (course_id, link,))
        self.conn.commit()



db = Database(p.get_headers(),p.get_links())
db.fill_the_table()


print(f'File "{fname}" is done. You can open and read with SQLiteDatabaseBrowserPortable.exe.')

