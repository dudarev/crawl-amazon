"""
Testing Amazon login with requests

Based on
http://theautomatic.net/2017/08/19/logging-into-amazon-with-python/

See also
https://stackoverflow.com/questions/18265376/why-i-can-log-in-amazon-website-using-python-mechanize-but-not-requests-or-urll

It seems old solutions from 2017 and earlier do now work anymore.
"""

import urllib

import requests
from bs4 import BeautifulSoup

from credentials import AMAZON_EMAIL, AMAZON_PASSWORD


site = 'https://www.amazon.com/gp/sign-in.html'
 
session = requests.Session()
session.headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)' +
    'AppleWebKit/537.36 (KHTML, like Gecko)' +
    'Chrome/68.0.3440.75 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': site
}


print('--- SIGNIN ---')
resp = session.get(site, allow_redirects=True)
html = resp.text
print(resp.status_code)
print(html)
 
soup = BeautifulSoup(html, 'html.parser')

data = {}
form = soup.find('form', {'name': 'signIn'})
for field in form.find_all('input'):
    try:
        data[field['name']] = field['value']
    except Exception:
        pass
data[u'email'] = AMAZON_EMAIL
data[u'password'] = AMAZON_PASSWORD


post_resp = session.post('https://www.amazon.com/ap/signin', data=data)
post_soup = BeautifulSoup(post_resp.content, 'html.parser')


print('--- POST ---')
print(post_resp.status_code)
print(post_resp.text)


SEARCH_URL_TEMPLATE = 'https://www.amazon.com/s/url=search-alias%3Daps&field-keywords={}'
SEARCH_URL = SEARCH_URL_TEMPLATE.format(
    urllib.parse.quote_plus(
        'Python for data analysis'))
 

search_resp = session.post(SEARCH_URL)
search_soup = BeautifulSoup(search_resp.content, 'html.parser')

print('--- SEARCH ---')
print(search_resp.status_code)
print(search_resp.text)
