from urllib.parse import urlsplit, urlunsplit
import validators
import requests
from bs4 import BeautifulSoup


def short_address(url: str) -> str:
    new_url = urlsplit(url)
    new_scheme = (new_url.scheme, new_url.netloc, '', '', '')
    return urlunsplit(new_scheme)


def validate_urls(url):
    errors = list()
    if url == '':
        errors.append('empty')
    len_url = len(url)
    if len_url > 255:
        errors.append('long')
    if not validators.url(url):
        errors.append('wrong')
    return errors if len(errors) > 0 else None


def get_req_code(url):
    try:
        r = requests.get(url)
        r.encoding = 'utf-8'
        code = r.status_code
        if code == 200:
            return code, r.text
    except requests.exceptions.RequestException:
        return None


def get_data_seo(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string
    h1_ = soup.find('h1')
    new_h1 = " ".join(h1_.text.strip().split()) if h1_ else ""
    descr_ = soup.find("meta", attrs={"name": "description"})
    descr = descr_["content"] if descr_ else ""
    return {'title': title,
            'h1': new_h1,
            'description': descr}
