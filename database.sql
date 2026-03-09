-- Smart Event & Ticket Management System Database Schema

-- User Table (Ömer)
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY IDENTITY(1,1),
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Tickets Table (Bengisu)
CREATE TABLE Tickets (
    ticket_id INTEGER PRIMARY KEY IDENTITY,
    user_id INTEGER,
    event_id INTEGER,
    ticket_code TEXT UNIQUE, 
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (event_id) REFERENCES Events(event_id)
);