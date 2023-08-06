# Skidward-Web UI

###### Web Interface to manage, run and schedule Python Scripts

The User Interface is created in Flask by Integrating functionality of
**Flask-admin** and **Flask-security**

By using Flask-admin and Flask-security together, we can provide custom
security for admin user and other users.

**Flask-admin** provides ready to use Admin Interface, easy to manage 
template functionality for login, logout, register and related pages. 

By default, there is no security/authentication for admin page, anyone
can access that. So in order to restrict the access of admin page so that 
only users with *administrative access* can manage all sorts of database tables,
creating users and permissions, we need to employ **Flask-Security** here.


## DATABASE:

**Skidward** has employed `SQLAlchemy` as ORM on top of `Postgresql` Relational Database
`Redis` for handlind backend processes.

In order for this Application to run, Postgres and Redis should be installed initially.

### Installing Postgres

1. **On Mac OSX**

  - Install Postgres using brew
   
        $ brew install postgres
   
  - Make sure Postgres starts every time your computer starts up
  
        $ pg_ctl -D /usr/local/var/postgres start && brew services start postgresql
        
  - Check Installation
  
        $ postgres -V
        
2. **On Linux/Ubuntu**

  - Install Postgres
  
        $ sudo apt update
        $ sudo apt-get install postgresql
        
  - Check Installation
  
        $ postgres -V 
   
  
### Installing Redis 

1. **On Mac OSX**

  - Install Redis
  
        $ brew install redis
        
  - Check if redis-server is running
  
        $ redis-cli ping
        
  - To Run redis on terminal
  
        $ redis-server

2. **On Linux/Ubuntu**

  - Install Redis
    
        $ sudo apt-update
        $ sudo apt-get install redis server
        
  - Additional configuration
  
    - Go to file /etc/redis/redis.conf. Change the line 
    > supervised no      - no supervision interaction
    - To
    > supervised systemd - no supervision interaction
    - This will allow it to make use of `systemd` init system.
    
  - Restart Redis service and check status
  
        $ sudo systemctl restart redis.service
        $ sudo systemctl status redis


## Initial Configuration for Skidward

In order to provide suitable configuration parameters, a default configuration 
file `.env.default` resides at the root **Skidward** package. 
Copy this file to a new file created with name `.env`, 
provide appropriate connection parameters in this `.env` file
specific to your database and put some randomly generated strings in 
`SECRET_KEY` and `SECURITY_PASSWORD_SALT` 

- Every database has a unique connection string which looks similar to this:

   > 'postgresql://admin:123@localhost/skidwardDB'
   
   where **admin** is username, **123** is password and **skidwardDB** is the database name.
  
- Create a new user and database in Postgres and then connect to the database using the following procedure

   - create new user (called as 'role' in postgres)

         $ createuser <user_name>;
         
   - create new database

         $ createdb <dbname>;
         
   - Run postgres as default user

         $ psql
          
         (this logs you in as superuser by default named "postgres" or your "hostname")

         postgres=#
         
   - Run postgres by logging in as a specific user
   
         $ psql -U <<username>>

   - To list all databases

         postgres=# \l
         
   - To connect to a database 

         postgres=# \c  <<database_name>>

   - To list all users

         postgres=# \du

   - To list all tables

         postgres=# \dt

Tables will be created by the application once you run it.
         
#### Setting DB connection string

- Before you can successfully run the application, you need to provide the 
Database Connection String to the `.env` file.

Like this 

    SQLALCHEMY_DATABASE_URI='postgresql://admin:123@localhost/skidwardDB'

  where you can replace 'admin' with '_yourusername_', 123' with '_yourpassword_'
  and 'skidwardDB' with '_yourDatabaseName_'

- The application is designed to load all the configuration parameters from the 
  `.env` file using `os.getenv()`
 
- Once you have set the environment variables correctly in the `.env` file, 
  you are good to go.


## RUN THE APPLICATION

1. To run the application, we need to once provide the path to Web UI:

       $ export FLASK_APP=skidward.web
      
2. Then, optionally we can set DEBUG=true, so readily accept code changes 
  every time before running the application
      
       $ export DEBUG=true
      
     (OR change flask environment to development, serves similar purpose)
      
       $ export FLASK_ENV=development
        
3. Superuser Creation

   **Note:** If this is not the first execution, you can skip to **_next point_**.
   
   For the first execution of the application, you will require to create 
   a Superuser with an Email and a Password
   
       $ flask user create <email> 
       
   > This will create a cli prompt for password, Enter your password and then 
   Run Application
   
4. Run Application with following command

       $ flask run

   > By default, application will be running on localhost:5000
   
5. You can now Login the App on the web browser as Superuser and manage other users and roles

