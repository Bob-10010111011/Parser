import shutil
from pathlib import Path
import random
import logging
import datetime as dt




class move_rename:
    def __init__(self, question_of_dst, f_path_str, destination=None):
        self.question_of_dst = question_of_dst
        self.destination = destination
        self.file_path = Path(f_path_str+f' {dt.date.today()}.db')

        if self.destination is None:
            self.destination = Path('Data')



    def if_f_ex(self): # renaming files if they exist in save location
        for child in Path(self.destination).iterdir():
            if self.file_path.name == child.name:
                suf = self.file_path.suffix
                stem = self.file_path.stem
                target_name = stem + f" ind-({random.randint(1, 124)})" + suf
                new_n = self.file_path.with_name(target_name)
                self.file_path.rename(new_n)
                logging.info(f'Renamed file "{self.file_path}" to "{target_name}"')
                self.file_path = Path(target_name)




    def f_move(self):
        if self.question_of_dst == 'y':

            if Path(self.destination).exists():
                p1 = Path(self.destination).resolve()
                self.if_f_ex()
                shutil.move(self.file_path, p1)
                logging.info(f'File saved to "{self.destination}".')
            else:
                p1 = Path(self.destination).resolve()
                p1.mkdir()
                self.if_f_ex()
                shutil.move(self.file_path, p1)
                logging.info(f'File saved to "{self.destination}".')


        else: # Selecting a location to save files
            try:
                Path(self.destination).mkdir()
                self.if_f_ex()
                shutil.move(self.file_path, Path(self.destination))
                logging.info(f'File saved to "{self.destination}".')
            except Exception as e:
                logging.error(f'Saving failed: {e}')
                self.destination = Path('Data')
                self.if_f_ex()
                shutil.move(self.file_path, Path(self.destination))
                logging.info(f'File saved to "{self.destination}".')





def cl_cache(destination):
    if Path('__pycache__').exists(): # clearing the cache in local directory
        shutil.rmtree(Path('__pycache__'))

    if Path(destination+ r'\\__pycache__').exists(): # clearing the cache in Data directory
        shutil.rmtree(Path(destination+ r'\\__pycache__'))

    logging.info('Cache deleted.')


    if Path('sourse.html').exists():
        Path('sourse.html').unlink()

    logging.info('File "sourse.html" deleted.')







