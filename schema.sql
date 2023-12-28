CREATE DATABASE tot_nghiep;
GRANT ALL PRIVILEGES ON tot_nghiep.* TO 'api_user'@'%' WITH GRANT OPTION;

USE tot_nghiep;

CREATE TABLE users (
    userID int NOT NULL,
    userName varchar(255),
    userPassword varchar(255),
    userEmail varchar(255),
    userTeam varchar(255),
    userRole varchar(255),
    userSession varchar(255),
    PRIMARY KEY (userID)
);

CREATE TABLE servers (
    serverID int NOT NULL,
    serverSerial varchar(255),
    serverFQDN varchar(255),
    serverCPU varchar(255),
    serverMemory varchar(255),
    serverDiskSpace varchar(255),
    serverStatus varchar(255),
    serviceName varchar(255),
    serviceStatus varchar(255),
    serviceTicketID varchar(255),
    serviceID int,
    requesterID int,
    serverNote varchar(255),
    PRIMARY KEY (serverID),
    FOREIGN KEY (requesterID) REFERENCES users(userID)
);

CREATE TABLE services ( 
    serviceID int NOT NULL,
    serviceName varchar(255),
    serviceStatus varchar(255),
    serviceOwnerID int,
    runningServer varchar(255),
    runningServerID int,
    PRIMARY KEY (serviceID),
    FOREIGN KEY (serviceOwnerID) REFERENCES users(userID)
);

CREATE TABLE tickets ( 
    ticketID varchar(255) NOT NULL,
    ticketName varchar(255),
    ticketContent text(65535),
    serviceName varchar(255),
    ticketOwner varchar(255),
    ticketOwnerID int,
    ticketAsignee varchar(255),
    ticketAsigneeID int,
    ticketStatus varchar(255),
    PRIMARY KEY (ticketID),
    FOREIGN KEY (ticketOwnerID) REFERENCES users(userID),
    FOREIGN KEY (ticketAsigneeID) REFERENCES users(userID)
);

INSERT INTO users (userID, userName, userPassword, userEmail, userTeam, userRole, userSession)
VALUES (1, "minh", "hash1", "minh@mail.com", "front-end", "developer", NULL);
INSERT INTO users (userID, userName, userPassword, userEmail, userTeam, userRole, userSession)
VALUES (2, "tam", "hash1", "tam@mail.com", "search", "developer", NULL);
INSERT INTO users (userID, userName, userPassword, userEmail, userTeam, userRole, userSession)
VALUES (3, "hoan", "hash1", "hoan@mail.com", "infrastructure", "sysadmin", NULL);
INSERT INTO users (userID, userName, userPassword, userEmail, userTeam, userRole, userSession)
VALUES (4, "hoa", "hash1", "hoa@mail.com", "account", "account-manager", NULL);

INSERT INTO servers (serverID, serverSerial, serverFQDN, serverCPU, serverMemory, serverDiskSpace, serverStatus, serviceName, serviceID, serviceStatus, serviceTicketID, requesterID, serverNote)
VALUES (1, "JQK34ACD12", NULL, "Intel Xeon E5-2678 v3 (12C/24T, 30M Cache, 2.50 GHz)", "256 GB", "8 TB", "free", NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO servers (serverID, serverSerial, serverFQDN, serverCPU, serverMemory, serverDiskSpace, serverStatus, serviceName, serviceID, serviceStatus, serviceTicketID, requesterID, serverNote)
VALUES (2, "CLKGA123", NULL, "Intel Xeon Processor X5460 (4C/8T, 12M Cache, 3.16 GHz)", "64 GB", "1 TB", "broken", NULL, NULL, NULL, NULL, NULL, "out of warranty");
INSERT INTO servers (serverID, serverSerial, serverFQDN, serverCPU, serverMemory, serverDiskSpace, serverStatus, serviceName, serviceID, serviceStatus, serviceTicketID, requesterID, serverNote)
VALUES (3, "CMNK6341", "frontend1.example.com", "Intel Xeon Gold 6142 (16C/32T, 22M Cache, 2.6 GHz)", "512 GB", "4 TB", "running", "static-frontend", 1, "running", "FRONTEND-1", 1, NULL);

INSERT INTO services (serviceID, serviceName, serviceStatus, serviceOwnerID, runningServer, runningServerID)
VALUES (1, "static-frontend", "running", 1, "frontend1.example.com", 3);
INSERT INTO services (serviceID, serviceName, serviceStatus, serviceOwnerID, runningServer, runningServerID)
VALUES (2, "search-engine", "processing", 2, NULL, NULL);

INSERT INTO tickets (ticketID, ticketName, ticketContent, serviceName, ticketOwner, ticketOwnerID, ticketAsignee, ticketAsigneeID, ticketStatus)
VALUES ("FRONTEND-1", "Deploy new static frontend", "We need a server which have: abc, Reason for this is: ", "static-frontend", "minh", 1, "hoan", 3, "Done");
INSERT INTO tickets (ticketID, ticketName, ticketContent, serviceName, ticketOwner, ticketOwnerID, ticketAsignee, ticketAsigneeID, ticketStatus)
VALUES ("SEARCH-1", "Deploy new search engine", "We've just created new search engine, ..", "search-engine", "tam", 2, "hoan", 3, "Done");