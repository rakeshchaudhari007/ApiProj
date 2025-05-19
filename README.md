High-Level Design (HLD) for Flask API on Azure
 1. Overview
This document outlines the architecture and high-level design for a Flask-based REST API deployed on Azure App Service. The API supports:

User registration and login (with password hashing).

Azure Virtual Network (VNet) and subnet provisioning via Azure SDK.

Data storage in Azure SQL Database.

Secure deployment and scalability using Azure App Service.

+-------------------+        HTTPS       +-----------------------+
|    Client (UI /   | <----------------> | Azure App Service     |
|    Postman / API  |                   | (Flask Application)   |
+-------------------+                   +-----------------------+
                                               |
                                               | PyODBC
                                               V
                                      +---------------------+
                                      | Azure SQL Database  |
                                      +---------------------+
                                               |
                             Azure SDK (Network & Resource Mgmt)
                                               |
                                               V
                                     +-----------------------+
                                     | Azure Resource Manager |
                                     +-----------------------+
                                               |
                        +------------------------------------------+
                        | Azure Network Resources (VNets, Subnets) |
                        +------------------------------------------+



⚙️ 3. Components
3.1. Frontend / Client
Tools: Postman, Browser, or any HTTP client

Purpose: Sends API requests for user operations and VNet provisioning.

3.2. Azure App Service
Runtime: Python 3.x (Linux)

App: Flask REST API (app.py)

Startup: startup.sh with gunicorn

Environment Variables:

SQL_SERVER, SQL_DATABASE, SQL_USERNAME, SQL_PASSWORD

subscription_id, region, etc.

3.3. Flask Application
Features:

/register: Registers new users with password hashing.

/login: Authenticates users and sets sessions.

/create_vnet: Provisions Azure VNet and subnets using Azure SDK.

/api/subnets: Fetches subnet details from the database.

Security: Session management and hashed passwords using werkzeug.security.

3.4. Azure SQL Database
Tables:

Users: Stores username, hashed password, and email.

Resources: Logs VNet creation.

Subnets: Stores subnet name, address, and associated VNet.

Access: Via pyodbc driver using ODBC Driver 17 for SQL Server.


3.5. Azure Resource Manager & SDK
Libraries Used:

azure.identity.DefaultAzureCredential

azure.mgmt.network.NetworkManagementClient

azure.mgmt.resource.ResourceManagementClient

Functionality:

Provision Resource Groups, VNets, and Subnets dynamically based on API requests.


🚀 8. Future Enhancements
Add authentication using JWT tokens.

Implement user role management.

Create UI using React or Angular frontend.

Add Azure Function triggers for event-based automation.

Implement Terraform/Bicep for infrastructure-as-code.



Step I followed.
Created SQL Database in Azure and created 3 tables using query.sl file
created python script to create APIs.
created web app in Azure and configured with local git config and run below cmds


below commaand 
1.  az webapp deployment user set --user-name rc565 --password pwd
2. az webapp config appsettings set --name rrc1  --resource-group apiapps --settings   subscription_id='d4'     AZURE_CLIENT_ID=''     AZURE_TENANT_ID='e'     AZURE_CLIENT_SECRET='' SQL_SERVER='.database.windows.net' SQL_DATABASE='appd' SQL_USERNAME='rakesh' SQL_PASSWORD='pwqd'

3. git remote add azure https://<git_username>@<app_name>.scm.azurewebsites.net:443/<app_name>.git
git add .
git commit -m "Initial commit"
git push azure master

az webapp config appsettings set --name appsc  --resource-group appsvc --settings   subscription_id='4'     AZURE_CLIENT_ID='29ed0f2'     AZURE_TENANT_ID=''     AZURE_CLIENT_SECRET='0' SQL_SERVER='api01.database.windows.net' SQL_DATABASE='appd' SQL_USERNAME='rakesh' SQL_PASSWORD='Secu2345' 

git init

git remote add azure https://.scm.centralindia-01.azurewebsites.net:443/appsc.git

git add .
git commit -m "Initial commit"
git push azure master

az webapp deployment user set --user-name rc565 --password 1234567

az webapp log tail --name appsc --resource-group appsvc

