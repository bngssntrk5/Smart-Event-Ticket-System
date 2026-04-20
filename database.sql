-- Smart Event & Ticket Management System Database Schema

-- User Table (Ömer)
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY IDENTITY(1,1),
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Events Table (Ilgaz)
CREATE TABLE Events (
    event_id INT IDENTITY(1,1) PRIMARY KEY,
    organizer_id INT NOT NULL,               
    title VARCHAR(255) NOT NULL,            
    description TEXT,                        
    event_date DATETIME NOT NULL,            
    total_capacity INT NOT NULL,            
    status VARCHAR(20) DEFAULT 'Active',     
    created_at DATETIME DEFAULT GETDATE(),   
    
    
    CONSTRAINT FK_EventOrganizer FOREIGN KEY (organizer_id) REFERENCES Users(user_id)
);

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