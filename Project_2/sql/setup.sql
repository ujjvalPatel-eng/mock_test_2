CREATE DATABASE SupportAnalysis;

USE SupportAnalysis;

CREATE TABLE Teams (
    team_id VARCHAR(10) PRIMARY KEY,
    team VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL
);

CREATE TABLE Tickets (
    ticket_id INT PRIMARY KEY,
    month VARCHAR(10) NOT NULL,
    team_id VARCHAR(10) NOT NULL,
    channel VARCHAR(20),
    resolution_hours INT,
    department VARCHAR(100) NOT NULL,
    satisfaction INT,
    breach_flag TINYINT NOT NULL
);

ALTER TABLE Tickets ADD constraint fk_tickets_teams
        FOREIGN KEY (team_id)
        REFERENCES Teams(team_id) ;
