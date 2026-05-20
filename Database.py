import sqlite3
import logging
import datetime as dt


class Database:
    def __init__(self, headers, links, fname=None):
        self.fname = fname+f' {dt.date.today()}.db'
        self.conn = sqlite3.connect(self.fname)
        self.cur = self.conn.cursor()
        self.headers = headers
        self.links = links


    # creating a table
    def create_t(self):
        logging.info('Creating tables in DB.')
        self.cur.executescript('''
            
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
