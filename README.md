# TechConf Registration Website

## Project Overview
The TechConf website allows attendees to register for an upcoming conference. Administrators can also view the list of attendees and notify all attendees via a personalized email message.

The application is currently working but the following pain points have triggered the need for migration to Azure:
 - The web application is not scalable to handle user load at peak
 - When the admin sends out notifications, it's currently taking a long time because it's looping through all attendees, resulting in some HTTP timeout exceptions
 - The current architecture is not cost-effective 

In this project, you are tasked to do the following:
- Migrate and deploy the pre-existing web app to an Azure App Service
- Migrate a PostgreSQL database backup to an Azure Postgres database instance
- Refactor the notification logic to an Azure Function via a service bus queue message

## Dependencies

You will need to install the following locally:
- [Postgres](https://www.postgresql.org/download/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Azure Function tools V3](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#install-the-azure-functions-core-tools)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure Tools for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)

## Project Instructions

### Part 1: Create Azure Resources and Deploy Web App
1. Create a Resource group
2. Create an Azure Postgres Database single server
   - Add a new database `techconfdb`
   - Allow all IPs to connect to database server
   - Restore the database with the backup located in the data folder
3. Create a Service Bus resource with a `notificationqueue` that will be used to communicate between the web and the function
   - Open the web folder and update the following in the `config.py` file
      - `POSTGRES_URL`
      - `POSTGRES_USER`
      - `POSTGRES_PW`
      - `POSTGRES_DB`
      - `SERVICE_BUS_CONNECTION_STRING`
4. Create App Service plan
5. Create a storage account
6. Deploy the web app

### Part 2: Create and Publish Azure Function
1. Create an Azure Function in the `function` folder that is triggered by the service bus queue created in Part 1.

      **Note**: Skeleton code has been provided in the **README** file located in the `function` folder. You will need to copy/paste this code into the `__init.py__` file in the `function` folder.
      - The Azure Function should do the following:
         - Process the message which is the `notification_id`
         - Query the database using `psycopg2` library for the given notification to retrieve the subject and message
         - Query the database to retrieve a list of attendees (**email** and **first name**)
         - Loop through each attendee and send a personalized subject message
         - After the notification, update the notification status with the total number of attendees notified
2. Publish the Azure Function

### Part 3: Refactor `routes.py`
1. Refactor the post logic in `web/app/routes.py -> notification()` using servicebus `queue_client`:
   - The notification method on POST should save the notification object and queue the notification id for the function to pick it up
2. Re-deploy the web app to publish changes

## Monthly Cost Analysis
Complete a month cost analysis of each Azure resource to give an estimate total cost using the table below:

| Azure Resource                           | Service Tier      | Monthly Cost |
| ---------------------------------------  | ----------------- | ------------ |
| *Azure Postgres Database - Single Server |  Basic            |  $37.96      |
| *Azure Service Bus*                      |  Basic            |  $0.00       |
| Azure App Service - Windows OS   - 1GB   |  Free Tier (F1)   |  FREE        |
| Azure Storage Account                    |  Standard         |  $24.04      |
| Application Insights                     |      NA           | Unlimited    |
| Azure Function App                       |  Consumption      |   FREE       |
| Total Cost           |                                       |  $62.00      |
 
## Architecture Explanation
The below chart explains the service selection and route for migrating the app to azure.

![image info](images/compute-choices.png)
# Web Application Migration Goals:
   Web Application Migration Implementation
      - Cost reduction
      - Robustness
      - Scalability
      - Agility

# Azure Web App used with Postgresql Database
To solve the given problem, it was required to migrate the app to azure. Since the app was already build and it needed to migrate and as per the chart above we can clearly see the route. We did not need full control so I slected web app and functions. It is easier to migrate and scale the app or setup tp auto scale as deemand increases up.

# Azure Functions used with service bus
I used Functions with service bus for faster connectivity and message transfer during the peek demand. A Service Bus acts as yet another layer of abstraction in the never ending quest to implement a good Service Oriented Architecture. The Service Bus can handle some of the heavy lifting seen behind a good Service Oriented Architecture like Messaging, Routing, and Service Co-Ordination. This solved the problem of time taking process of notification.
