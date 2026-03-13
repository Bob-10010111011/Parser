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


try: # do if file exist
    conn = sqlite3.connect(fname)

except FileNotFoundError: #  do if file not exist
    print(f'File not found. Creating new file: {fname}\n')
    conn = sqlite3.connect(fname)

cur = conn.cursor()

# creating a table
cur.executescript(f'''
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


# fill out the table
def fill_the_table(headers, links):
    num = 0
    while True:
        cur.execute('''INSERT OR IGNORE INTO Courses
                (course_name) 
                VALUES (?)''',
                (headers[num],))
        cur.execute('SELECT id FROM Courses WHERE course_name = ? ', (headers[num],))
        course_id = cur.fetchone()[0]
        cur.execute('''INSERT OR IGNORE INTO Links
                    (courses_id, link) 
                    VALUES ( ?, ? )''',
                    (course_id, links[num],))


        num += 1
        if len(links) <= num: break

    conn.commit()

fill_the_table(p.get_headers(),p.get_links())

print(f'File "{fname}" is done. You can open and read with SQLiteDatabaseBrowserPortable.exe.')

