drop TABLE if exists entries;
create table entries (
  ID integer primary key autoincrement,
  title string not null,
  text string not null
);
