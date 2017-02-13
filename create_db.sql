CREATE TABLE factgroups (id integer primary key);
CREATE TABLE definitions (id integer primary key, factgroup integer, def text not null, foreign key(factgroup) references factgroups(id));
CREATE TABLE names (id integer primary key, factgroup integer, name not null unique, foreign key(factgroup) references factgroups(id));
