import os
import logging
from pathlib import Path

from Parser import Parser
from Save_to import Saving_to
from Database import Database
import Move



# Logging our processes
logging.basicConfig(level=logging.INFO, filename="log.log", filemode='a',
                    format="%(asctime)s - %(levelname)s - %(lineno)d - %(message)s")
logging.info('-------------------------------------')



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

    fname = input("Please enter the name of the file containing the courses: ")  # це виніс з класу Database


    db = Database(headers, links, fname)  # giving to class our headers, links

    if not db.tables_exist():
        db.create_t()  # create tables

    db.fill_the_table()  # filling the tables
    db.closing()

    question_of_dst = input('Do you want to save files into standard directory?(y/n): ')

    if question_of_dst != 'y':
        destination = input('Please, write the destination of files: ') + r'\Data'
    else:
        destination = None

    m = Move.move_rename(question_of_dst, fname, destination)
    m.f_move()


    print("Process completed.")

    if destination is not None:
        Move.cl_cache(destination)
    else:
        destination = Path('Data')
        Move.cl_cache(str(destination))

    logging.info('Process completed.')



try:
    if __name__ == "__main__":
        run()
except Exception as e:
    logging.error(f'Error: {e}')
    print(f'Error: {e}')