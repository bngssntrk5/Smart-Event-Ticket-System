-- Smart Event & Ticket Management System Database Schema

--Tickets Table (Bengisu)
CREATE TABLE Tickets (
    ticket_id INT IDENTITY(1,1) PRIMARY KEY, 
    user_id INT,
    event_id INT,
    ticket_code NVARCHAR(50) UNIQUE,
    purchase_date DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_UserTickets FOREIGN KEY (user_id) REFERENCES Users(user_id),
    CONSTRAINT FK_EventTickets FOREIGN KEY (event_id) REFERENCES Events(event_id)
);