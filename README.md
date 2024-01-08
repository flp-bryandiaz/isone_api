# ISO New England Web API

## About this project
This library implements Python to access [ISO New England's Web Services Data](https://www.iso-ne.com/participate/support/web-services-data).
Information about individual endpoints is available on [ISO-NE's Web Services API](https://webservices.iso-ne.com/docs/v1.1/) documentation page.

This project aims to facilitate access to ISO-NE public facing market data for computational applications and data warehousing. 
Access to ISO-NE data requires a valid username and password.

## Environment variables and secrets
Secrets, including usernames and passwords, are stored in a .env file which are accessed by Python through `dotenv`.
This file is not included in the repository to keep these secrets only in local environments.

### Setting up the .env secrets
- Create a new file in this same root directory called ".env"
- To the file add one line: `API_USERNAME=your_api_username`
- Add a following line: `API_PASSWORDS=your_password`

The ISO-NE API client class, `ISONEClient`, will then automatically discover these variables for use in its API calls.