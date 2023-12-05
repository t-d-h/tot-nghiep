
CREATE DATABASE databasename;

CREATE TABLE users (
    user_id varchar(255),
    username varchar(255),
    password varchar(255),
    email varchar(255),
    role varchar(255),
    team varchar(255)
);

CREATE TABLE servers (
    server_id varchar(255),
    serial varchar(255),
    cpu_cores int,
    memory_gb int,
    disk_gb int,
    running_services varchar(255),
    server_status varchar(255),
    ip_address varchar(255)
);