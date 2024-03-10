### Linter status:
[![test lint](https://github.com/Vasiliii3/python-project-83/actions/workflows/lint.yml/badge.svg)](https://github.com/Vasiliii3/python-project-83/actions/workflows/lint.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/f583e6340e9ed5471984/maintainability)](https://codeclimate.com/github/Vasiliii3/python-project-83/maintainability)

### Web application:

[You can take look at deployed app here.](https://python-project-83-pageanalyzer.up.railway.app/)

### Description

This is webapp named "Page analyzer" made with Python on Flask framework,
where you can add websites and treat them with small "SEO checks".

### Requirements:

* Python 3.10
* Poetry 1.3.1

### Install
1. `Git clone https://github.com/Vasiliii3/page_analyzer.git`
2. `cd page_analyzer`
3. Сreate a file in the root of the project .env (example in .env_example)
4. Use this command to install the package `make install`
5. Create PostgreSQL database with cheatsheet (database.sql)
6. Run make dev for debugging (WSGI debug='True'), or make start for production (gunicorn)
