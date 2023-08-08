# Consultant.AI Post-Interview Application (Flask Back-End)

**Note: This is the back-end repo. For the front-end repo, please visit [https://github.com/PacificCoastEyes/consultantai-fe](https://github.com/PacificCoastEyes/consultantai-fe).**

## Deployed Address

[https://consultantai-be.azurewebsites.net/api](https://consultantai-be.azurewebsites.net/api)

## About the App

### Purpose

This backend app handles the storage and retrieval of user account data (including encryption of passwords), issues 7-day authentication tokens and blocklists them upon user logout, and verifies the validity of tokens when requested by the client to access private pages/routes in the frontend.

### Languages, Tools, and Frameworks

The app is built in Python on the Flask web framework. Access to the PostgreSQL database is mediated with the Prisma for Python ORM. Authentication tokens are signed and decoded using PyJWT and passwords are hashed and verified using bcrypt.

The app is hosted in a Linux-based Docker container in Microsoft Azure App Service and served using an Azure-provided Guicorn server for Flask applications.

### Endpoints

-   /register - Creates a new user record in the database
-   /login - Verfies hash of user's provided password against hashed password stored in the database
-   /check-if-existing-user - Checks if an email used during sign-up already exists on an account; if so, client asks user to log in instead
-   /logout - Adds user's current authentication token to a blocklist table in the database to prevent further use. Client then deletes token from localStorage
-   /validate-token - Tells client whether provided authentication token is valid or is invalid (malformed or in blocklist) or expired
