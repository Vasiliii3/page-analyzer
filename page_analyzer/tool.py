from urllib.parse import urlsplit, urlunsplit
import validators


def short_address(url):
    new_url = urlsplit(url)
    new_scheme = (new_url.scheme, new_url.netloc, '', '', '')
    return urlunsplit(new_scheme)


def validate_urls(url):
    message = list()
    if url == '':
        message.append('empty')
    len_url = len(url)
    if len_url > 255:
        message.append('long')
    if not validators.url(url):
        message.append('wrong')
    return message if len(message) > 0 else None
