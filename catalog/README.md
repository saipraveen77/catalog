# Item Catalog Web App

Athukuri SaiPraveen
This web app is a project for the Udacity Full Stack Web Developer NanoDegree.

## About

This Project provides Authorization and Authentication to user.
It is a Web Application which provides a list of items within different categories as well as provide a user registration and authentication system. The Registered users will have the ability to add, update and delete their own items.
 
## In This Project

This project has one main Python module `main.py` 
--->which runs the Flask application. 
A SQL database is created using the `Data_Setup.py` module 
Insertion of data into columns and tables takes place through `database_init.py` module
--->which you can populate the database with test data
The Flask application uses stored HTML templates in the tempaltes folder to build the front-end of the application.

## Skills Required
1. Python
2. HTML
3. CSS
4. OAuth
5. Flask Framework
6. DataBaseModels
7. Vagrant
8. VirtualBox


## How to Run

1. In First Step we have to Install Vagrant.
2. Now We have to Install VirtualBox.
3. Then Open CommandPrompt in your Folder's Path.
4. First initialize the Vagrant using the command:
	$ vagrant init ubunti/xenial64
5. Launch Vagrant Using the Command
	$ vagrant up
6. Log into Vagrant using Command
	$ vagrant ssh
7. Change the directory to vagrant using command
	$ cd vagrant
8. The app imports requests which is not on this vm. Run pip install requests
9. Now we have to activate the Virtual Environment in our Folder by Using the Command
	$ venv\scripts\activate
10. Run the Data_Setup.py using the command
	$ python Data_Setup.py
	 Execution of this file leads to creation of a database file(chipset.db) 
11. Run the database_init.py using the command
	$ python database_init.py
	Execution of this file leads to insertion of data into the database file
12. And then Run the main.py using the command 
	$python main.py
	This File Executes the entire Project including Templates and remaining files
13. Access the application locally using http://localhost:8000	
	By running running main.py file in command prompt the server of our project will activates and we have to type the above url in browser.This displays basic version of our project.
14. Here we cannot be able to edit,add,delete our items.To enable edit,add,delete options we have to login to our account.

*Optional step(s)

## Using Google Login
To get the Google login working there are a few additional steps:

1. Go to [Google Dev Console](https://console.developers.google.com)
2. Sign up or Login if prompted
3. Go to Credentials
4. Select Create Crendentials > OAuth Client ID
5. Select Web application
6. Enter name 'SocHub'
7. Authorized JavaScript origins = 'http://localhost:8000'
8. Authorized redirect URIs = 'http://localhost:8000/login' && 'http://localhost:8000/gconnect'
9. Select Create
10. Copy the Client ID and paste it into the `data-clientid` in login.html
11. On the Dev Console Select Download JSON
12. Rename JSON file to client_secrets.json
13. Place JSON file in SocHub directory that you cloned from here
14. Run application using `python /SocHub/main.py`

## JSON Endpoints
The following are open to the public:

Chipsets Catalog JSON: `/SocHub/JSON`
    - Displays the whole Chipsets models catalog. Chipset Categories and all models.

Chipset Categories JSON: `/SocHub/socCompany/JSON`
    - Displays all Chipset categories
All Chipset Editions: `/SocHub/chipsets/JSON`
	- Displays all Chipset Models

Chipset Edition JSON: `/SocHub/<path:soccompany>/chipsets/JSON`
    - Displays Chipset models for a specific Chipset category

Chipset Category Edition JSON: `/SocHub/<path:soccompany>/<path:chipset_name>/JSON`
    - Displays a specific Chipset category Model.


