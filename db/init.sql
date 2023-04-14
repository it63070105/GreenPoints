CREATE DATABASE greenpointsdb;

\c greenpointsdb;

DROP TABLE IF EXISTS records;

CREATE TABLE records (
  id SERIAL PRIMARY KEY,
  objects VARCHAR(255),
  time TIMESTAMP(6)
);

INSERT INTO records (objects, time) VALUES ('["can","can"]','2023-04-14 20:14:42.000000'),
                                           ('["bottle","bottle"]','2023-04-14 20:15:48.000000'),
                                           ('["cup","bottle"]','2023-04-14 20:15:54.000000');