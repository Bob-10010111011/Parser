from bs4 import BeautifulSoup
import urllib.request, urllib.error
from urllib.request import urlopen
import ssl


# Ignore errors of SSL-certificate
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://online.dr-chuck.com/' # - source for parse

def get_headers(url): # func for giving header of courses
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")
    result = [tag.get_text() for tag in soup('h3')]
    return result

def get_links(url): # func for giving links on courses
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")
    directory = soup.select('div.span4 > a')
    result = [i.get('href') for i in directory]
    return result



links = get_links(url)
headers = get_headers(url)

print(f'Connecting to: {url} ...\n')


# loop for outputting information
num = 0
while True:
    print(f'Number of course: {num+1}')
    print(f'Name of course: {headers[num]}')
    print(f'Link: {links[num]}\n')
    num += 1
    if len(links) <= num: break










