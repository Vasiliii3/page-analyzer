import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, \
    flash, abort, redirect, url_for

from page_analyzer.db import add_url, add_urls, get_name, get_id, \
    get_for_urls, get_for_url_checks
from page_analyzer.utils import short_address, validate_urls, \
    get_req_code, get_data_seo

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
FLASH_SUCCESSFUL = 'alert-success'
FLASH_DANGER = 'alert-danger'


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls/<int:id>')
def get_urls_id(id):
    url = get_id(id)
    if url is None:
        abort(404)
    checks = get_for_url_checks(id)
    return render_template('urls_id.html', url=url, checks=checks)


@app.post('/urls')
def post_urls():
    url = request.form.to_dict().get('url')
    errors = validate_urls(url)
    if errors:
        if 'wrong' in errors:
            flash('Некорректный URL', FLASH_DANGER)
        if 'empty' in errors:
            flash('URL обязателен', FLASH_DANGER)
        if 'long' in errors:
            flash('URL превышает 255 символов', FLASH_DANGER)
        return render_template('index.html', url=url), 422
    url = short_address(url)
    id_url = get_name(url)
    if id_url:
        id_url = id_url['id']
        flash('Страница уже существует', FLASH_SUCCESSFUL)
    else:
        id_url = add_url(url)
        flash('Страница успешно добавлена', FLASH_SUCCESSFUL)

    return redirect(url_for('get_urls_id', id=id_url))


@app.post('/urls/<int:id>/checks')
def check_urls(id):
    url = get_id(id)['name']
    check = get_req_code(url)
    if check is None:
        flash('Произошла ошибка при проверке', FLASH_DANGER)
        return redirect(url_for('get_urls_id', id=id))
    status_code, text_html = check
    seo = get_data_seo(text_html)
    add_urls(id, status_code, seo['h1'], seo['title'], seo['description'])
    flash('Страница успешно проверена', FLASH_SUCCESSFUL)
    return redirect(url_for('get_urls_id', id=id))


@app.route('/urls')
def show_urls():
    urls = get_for_urls()
    return render_template('urls.html', urls=urls)
