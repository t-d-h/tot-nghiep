
CREATE DATABASE databasename;

CREATE TABLE users (
    user_id int NOT NULL AUTO_INCREMENT,
    username varchar(255),
    password varchar(255),
    email varchar(255),
    role varchar(255),
    team varchar(255)
);

CREATE TABLE servers (
    server_id int NOT NULL AUTO_INCREMENT,
    serial varchar(255),
    cpu_cores int,
    memory_gb int,
    disk_gb int,
    running_services varchar(255),
    server_status varchar(255),
    ip_address varchar(255)
);

INSERT INTO users (username, password, email, role, team)
VALUES (hoan1, hash1, email@gmail.com, sysadmin, infra);
INSERT INTO users (username, password, email, role, team)
VALUES (hoan2, hash2, email2@gmail.com, developer, backend);
INSERT INTO users (username, password, email, role, team)
VALUES (hoan3, hash3, email3@gmail.com, manager, bod);

INSERT INTO servers (serial, cpu_cores, memory_gb, running_services, server_status, ip_address)
VALUES (abc1234, 4, 8, product_api, in_use, 10.0.6.8);
