-- switch to a different database
\c postgres

-- drop the database if it exists
DROP DATABASE IF EXISTS greenpointsdb;

-- create the database
CREATE DATABASE greenpointsdb;

-- switch to the new database
\c greenpointsdb;

-- drop the table if it exists
DROP TABLE IF EXISTS records;

CREATE TABLE records (
  id SERIAL PRIMARY KEY,
  objects VARCHAR(255),
  time TIMESTAMP(6)
);

INSERT INTO records (objects, time) VALUES ('["can","can"]','2023-04-14 20:14:42.000000'),
                                           ('["bottle","bottle"]','2023-04-14 20:15:48.000000'),
                                           ('["cup","bottle"]','2023-04-14 20:15:54.000000');
