import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, render_template, request, \
    flash, abort, redirect, url_for
from pathlib import Path
from page_analyzer.Fdb import FDataBase
from page_analyzer.tool import short_address, validate_urls, \
    get_req_code, get_html_paser

load_dotenv()
file = os.path.join(Path(__file__).parent.parent, 'database.sql')

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', False)
DATABASE_URL = os.getenv('DATABASE_URL')
dbase = FDataBase(DATABASE_URL)
FLASH_SUCCESSFUL = 'alert-success'
FLASH_DANGER = 'alert-danger'


def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = psycopg2.connect(DATABASE_URL)
    cursor = db.cursor()
    with app.open_resource(file, mode='r') as db_file:
        cursor.execute(db_file.read())
    db.commit()
    db.close()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def index():
    return render_template('index.html', url='')


@app.route('/urls/<int:id>')
def get_urls_id(id):
    url = dbase.get_id(id)
    if url is None:
        abort(404)
    checks = dbase.get_for_url_checks(id)
    return render_template('urls_id.html', url=url, checks=checks)


@app.post('/urls')
def post_urls():
    url = request.form.to_dict().get('url')
    error = validate_urls(url)
    if error:
        if 'wrong' in error:
            flash('Некорректный URL', FLASH_DANGER)
        if 'empty' in error:
            flash('URL обязателен', FLASH_DANGER)
        if 'long' in error:
            flash('URL превышает 255 символов', FLASH_DANGER)
        return render_template('index.html', url=url), 422
    url = short_address(url)
    id_url = dbase.get_name(url)
    if id_url:
        id_url = id_url['id']
        flash('Страница уже существует', FLASH_SUCCESSFUL)
    else:
        id_url = dbase.add_url(url)
        flash('Страница успешно добавлена', FLASH_SUCCESSFUL)

    return redirect(url_for('get_urls_id', id=id_url)), 301


@app.post('/urls/<int:id>/checks')
def check_urls(id):
    url = dbase.get_id(id)['name']
    check = get_req_code(url)
    if check is None:
        flash('Произошла ошибка при проверке', FLASH_DANGER)
        return redirect(url_for('get_urls_id', id=id))
    status_code, text_html = check
    seo = get_html_paser(text_html)
    dbase.add_urls(id, status_code, seo['h1'], seo['title'], seo['description'])
    flash('Страница успешно проверена', FLASH_SUCCESSFUL)
    return redirect(url_for('get_urls_id', id=id))


@app.route('/urls')
def show_urls():
    urls = dbase.get_for_urls()
    return render_template('urls.html', urls=urls)


if __name__ == "__main__":
    app.run(debug=DEBUG)
