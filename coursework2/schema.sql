drop TABLE if exists entries;
create table entries (
  ID integer primary key autoincrement,
  TITLE string not null,
  TEXT string not null
);
