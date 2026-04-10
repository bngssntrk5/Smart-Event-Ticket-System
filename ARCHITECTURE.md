# Software Architecture Document: Smart Event Ticket System

## Change History

Version 0.1 (22.02.2026): Project initialization and repository setup by Bengisu Şentürk.

Version 0.2 (01.03.2026): Database schema design and core SQL constraints implementation by Bengisu Şentürk.

Version 0.3 (08.03.2026): Ticketing logic development and module integration by Bengisu Şentürk.

Version 0.4 (10.03.2026): Initial implementation of event management services by Ömer Faruk Soylu.

Version 0.5 (22.03.2026): SQL syntax refactoring and environment security fixes by Bengisu Şentürk.

Version 0.6 (04.04.2026): Finalizing user authentication and session handling logic by Ömer Faruk Soylu.

Version 0.7 (09.04.2026): Development of front-end event modules by Ilgaz Alagöz.

Version 1.0 (09.04.2026): Finalizing 4+1 Architectural Views and project documentation for Part 2 submission by Bengisu Şentürk, Omer Faruk Soylu, and Ilgaz Alagöz.

## 1. Scope

This document defines the software architecture of the Smart Event Ticket System. It covers the modular structure, database relationships, and user process flows using the 4+1 View Model.

## 3. Software Architecture

The system is built using the Python/Flask micro-framework with a Modular Monolith architecture. It utilizes a relational data model with SQL Server to ensure data integrity and ACID compliance.

## 5. Logical Architecture

The system consists of three primary logical components:

- **Auth Component:** Handles user registration, login, and session management.
- **Event Component:** Manages event creation, scheduling, and capacity constraints.
- **Ticket Component:** Manages the core ticketing logic, unique ticket code generation, and SQL-based occupancy reporting.

## 6. Process Architecture

When a user attempts to purchase a ticket, the following process occurs:

1. User selects an event from the dashboard.
2. The system invokes `modules/tickets.py` to check real-time capacity via SQL.
3. If capacity is available, a transaction is initiated, an `INSERT` operation is performed, and a unique ticket code is generated.

## 7. Development Architecture

The project follows a layered folder structure for maintainability:

- `/modules`: Contains back-end business logic (Ticket, Event, Auth modules).
- `/templates`: Front-end presentation layer using Jinja2 templates.
- `/static`: Assets for styling (CSS) and client-side logic (JS).
- `app.py`: The main entry point of the Flask application.

## 8. Physical Architecture

- **Web Server:** Localhost (Flask built-in development server).
- **Database Server:** SQL Server / SQLite.
- **Environment:** Python 3.x runtime environment.

## 9. Scenarios

- **Scenario 1 (Ticket Purchase):** A user logs in, selects an event, and completes a purchase. The system updates the remaining capacity instantly.
- **Scenario 2 (Reporting):** An administrator monitors occupancy rates (%) via the `ticket_view.html` dashboard, fueled by real-time SQL queries.

## 10. Size and Performance

The system is optimized for concurrent ticketing operations, ensuring that the database remains consistent even under high traffic through relational constraints and efficient SQL queries.
