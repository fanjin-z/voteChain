drop table if exists entries;
create table entries (
  addr TEXT primary key,
  cert TEXT not null
);
