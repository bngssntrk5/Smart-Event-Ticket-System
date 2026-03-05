-- Smart Event & Ticket Management System Database Schema

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