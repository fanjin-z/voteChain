drop table if exists entries;
create table entries (
  addr BLOB primary key,
  cert BLOB not null
);
