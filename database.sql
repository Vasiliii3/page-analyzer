drop table if exists urls CASCADE ;

create table urls(
id smallserial primary key,
name varchar(255) unique,
created_at DATE
);