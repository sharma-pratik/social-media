## Setup

### Step 1: Environment Variables

Create a `.env` file in the root directory of the project with the following content:

```
POSTGRES_DB=social_db
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=1234
POSTGRES_HOST=db
POSTGRES_PORT=5432
DJANGO_SUPERUSER_EMAIL=superuser@test.com
DJANGO_SUPERUSER_PASSWORD=1234
```


### Step 2: Build and Run the Application

Run the following command to build and start the Docker containers:

```bash
docker-compose up -d --build
```

This command will set up the Django application and PostgreSQL database. The Django application will run the start.sh script, which will perform the following tasks:

Run the migrations
Create a superuser using the details from the .env file.
Create 20 other users.
Start the djagno server

### Step 3: Access the Application
Once the containers are up and running, you can access the Django application at:

http://0.0.0.0:8000
