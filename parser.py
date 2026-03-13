from bs4 import BeautifulSoup
import urllib.request, urllib.error
from urllib.request import urlopen
import ssl


# Ignore errors of SSL-certificate
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://online.dr-chuck.com/' # - source for parse

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
links = p.get_links()
headers = p.get_headers()

print(f'Connecting to: {url} ...\n')


fname = input('Enter the file name: ')+'.txt'

try: # do if file exist
    with open(fname) as f:
        old_text = f.read()
    with open(fname,'w') as f:
        f.write(old_text + '\n') # rewrite file


except FileNotFoundError: #  do if file not exist
    print(f'File not found. Creating new file: {fname}\n')
    with open(fname, 'w') as f:
        pass

with open(fname, 'a') as f:
    num = 0
    while True:
        f.write(f'Number of course: {num + 1}\n')
        f.write(f'Name of course: {headers[num]}\n')
        f.write(f'Link: {links[num]}\n\n')
        num += 1
        if len(links) <= num: break

print(f'File "{fname}" is done. You can open and read.')








