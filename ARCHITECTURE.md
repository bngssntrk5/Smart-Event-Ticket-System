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

Version 1.0.1 (17.04.2026): Bengisu Şentürk started final UI enhancements and refined the core ticketing modules for the final phase.

Version 1.0.5 (20.04.2026): Ömer Faruk Soylu and Ilgaz Alagöz completed their final pushes, finalizing the Authentication and Event Management logic for integration.

Version 1.1 (26.04.2026): Final Submission. Final integration, premium CSS implementation, and Fetch API real-time occupancy updates completed by Bengisu Şentürk. Project ready for Part 3 delivery.

# 1. Scope

This document defines the final software architecture for the Smart Event Ticket System. It focuses on the transition from a static application to a dynamic, real-time management tool with a focus on data integrity and user experience (UX).

# 3. Software Architecture

The system follows a Modular Monolith architecture. While the core is built on the Flask micro-framework, the final version utilizes a decoupled communication pattern where the frontend interacts with the backend via JSON-based API calls for the ticketing process.

# 5. Logical Architecture

The project is divided into three functional modules with shared responsibilities:

Auth Module (auth.py): Handles secure user onboarding, authentication, and session persistence using flask.session.

Event Module (events.py): Manages the lifecycle of events, including administrative creation and SQL-backed capacity settings.

Ticket & Analysis Module (tickets.py): The core logic engine that calculates real-time occupancy using SQL JOIN and COUNT functions and manages ticket transactions.

# 6. Process Architecture (Final Build)

We implemented a Non-Blocking Purchase Workflow:

User Action: The user clicks the "Buy Ticket" button on the dashboard.

Asynchronous Request: A JavaScript Fetch API call is sent to the backend without reloading the page.

Backend Processing: The server validates the request and performs a SQL transaction (ACID compliant).

JSON Feedback: The server returns a success/failure JSON response.

Dynamic UI Update: The DOM is updated instantly to reflect the new Occupancy Percentage and Progress Bar width.

# 7. Development Architecture

The folder structure is optimized for the final build:

/modules: Encapsulated backend logic files.

/templates: Dynamic HTML templates using the Jinja2 engine.

/static:

/css: Custom premium styling for modern look & feel.

/js: Client-side logic for real-time occupancy updates.

app.py: Central routing and environment configuration.

# 8. Physical Architecture

Environment: Python 3.x with Flask Web Server.

Database: MS SQL Server (accessed via pyodbc).

Security: Sensitive credentials managed via a .env file (Environment Variables).

# 9. Scenarios

Scenario 1 (Real-time Purchase): A user buys a ticket; the occupancy bar increases instantly for all users viewing that event without a manual refresh.

Scenario 2 (Safety Constraint): If an event reaches 100% capacity, the system triggers an automatic UI update to disable the "Buy" button and change the status to "Sold Out".

# 10. Performance and Scalability

By offloading UI calculations to the client-side and using optimized SQL queries, the system ensures low latency even as the number of events grows. The modular design allows for future features (like payment integration) to be added without disrupting existing services.
