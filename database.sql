drop table if exists urls CASCADE ;
drop table if exists url_checks CASCADE ;

create table urls(
id smallserial primary key,
name varchar(255) unique,
created_at DATE
);

create table url_checks(
id smallserial primary key,
url_id INTEGER REFERENCES urls (Id) on delete cascade on update cascade,
status_code INTEGER,
h1 varchar(255),
title varchar(255),
description text,
created_at DATE
);