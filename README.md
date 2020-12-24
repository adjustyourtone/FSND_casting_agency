# Casting Agency API

## Capstone Submission for Udacity's Full Stack Nanodegree Program

**Heroku Link** (https://localhost:5000)

## Getting Started

### Setting up your project

To run this project locally, start by cloning the repository with:

```bash
git clone https://github.com/adjustyourtone/FSND_casting_agency.git
```

#### Install Python 3

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

It is recommended to work within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Further instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the projecty directory and running:

```bash
pip install -r requirements.txt
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests.

### Database Setup

If running locally you must create a postgres database on your system using:

```bash
createdb castingagency
```

### Entering Environment Variables

This application uses a wide variety of environment variables to run successfully that include API Testing Tokens, Authentication Variables and basic URL's for our database.

If you've followed these directions completely, you must run two commands to get your API up and running:

```
source setup.sh
flask run --reload

```

Note: The --reload flag will detect changes and restart your development server automatically.

If you need to update your Postgres login credentials, this would also be done in the setup.sh file by changing the DATABASE_URL and TEST_DATABASE_URL strings, respectively.

As a reminder, these strings are formatted as:

postgresql://{username}:{password}@{host}:{port}/{database_name}

### Generating Access Tokens

This project has Role-Based authorization implemented with [Auth0](https://auth0.com) which will provide only specific operations based on the users given role: Assistant, Director and Producer.

Assistant - get:movies, get:actors

Director - All permissions of Assistant + create, edit and delete of Actor and edit:movie ONLY.

Producer - All permissions of Director + create and delete Movie.

This project has provided 3 working access tokens that are included in the **Roles.txt** and **setup.sh** files. Note the timestamp at the top of the Roles.txt file. If the time of testing is beyond the 24hrs mark, you will need to generate new access tokens. To generate a token for a role make sure your application is running and navigate to the authorization url:

```
http://localhost:5000/authorization/url
```

This will generate a login link and redirect you to Auth0 to sign-in with the provided credentials in the **Roles.txt** file in the project directory.

Upon successful login, you will be redirected to the index of your host. Inspect the url upon redirect to see the provided access token inclued within. It should look something like this:

```
http://localhost:5000/#access_token=eyJhbGciOiJSUzI1N....etc

Copy this token all the way up to the

....&expires_in=86400&token_type=Bearer (make sure to leave this section out of the token)
```

With your token in hand, make note of which credential you used to sign in and navigate over to your setup.sh file in the project directory and replace the provided JWT with your newly provided JWT.

To generate a token for a new role, navigate to '/authorization/logout' where you will be provided a logout link. Click the link to be logged out. You will be redirected to the '/authorization/url' endpoint where you can sign-in again.

Repeat as needed for each role.

Because we will be using Postman to test this API, it is recommended you replace the JWT in the Roles.txt file to limit the interaction with the setup.sh script file.

#### Testing This API

With the API running, we will use Postman to check and verify role based actions. There are two included postman collections for you to use depending on how you choose to interact with the API:

```
FSND_casting_agency.postman_collection  OR

HEROKU_casting_agency.postman_collection
```

Load your desired endpoints into Postman and with your provided access tokens you can begin interacting with the API.

### Endpoint Reference

#### GET /api/actors

- Returns a list of all actors in the database. Available across all roles.

```
Example return:

{
    "actors": [
        {
            "age": 42,
            "gender": "Male",
            "id": 4,
            "name": "Bradley Cooper"
        },
        {
            "age": 53,
            "gender": "Male",
            "id": 5,
            "name": "Will Ferrell"
        },
        {
            "age": 47,
            "gender": "Female",
            "id": 6,
            "name": "Sandra Bullock"
        }
    ],
    "success": true
}
```

#### GET /api/movies

- Returns a list of all movies in the database. **Available across all roles.**

```
Example return:

{
    "movies": [
        {
            "id": 4,
            "release_date": "February 13th, 2003",
            "title": "Old School"
        },
        {
            "id": 5,
            "release_date": "June 2nd, 2009",
            "title": "The Hangover"
        },
        {
            "id": 6,
            "release_date": "December 18th, 2018",
            "title": "Bird Box"
        }
    ],
    "success": true
}
```

#### GET /api/actors/<int:id>

- Returns an actor by ID. **Available across all roles.**

```
Example return:

{
    "actor": {
        "age": 19,
        "gender": "Female",
        "id": 1,
        "name": "Valerie Smith"
    },
    "success": true
}
```

#### GET /api/movies/<int:id>

- Returns a movie by ID. **Available across all roles.**

```
Example return:

{
    "movie": {
        "id": 2,
        "release_date": "March 31st, 1999",
        "title": "The Matrix"
    },
    "success": true
}
```

#### POST /api/actors

- Creates a new Actor. **Available for Director and Producer only.**

```
Example body:

{
    "name": "Sandra Bullock",
    "age": "47",
    "gender": "Female"
}
```

```
Example response:

{
    "actor": {
        "age": 47,
        "gender": "Female",
        "id": 7,
        "name": "Sandra Bullock"
    },
    "success": true
}
```

#### POST /api/movies

- Creates a new Movie. **Available Producer only.**

```
Example body:

{
    "title": "Bird Box",
    "release_date": "December 18th, 2018"
}
```

```
Example response:

{
    "movie": {
        "id": 7,
        "release_date": "December 18th, 2018",
        "title": "Bird Box"
    },
    "success": true
}
```

#### PATCH /api/actors/<int:id>

- Allows editing of an actor by ID. **Available to Director and Producer.**

```
Example body:

{
    "name": "John Smith"
}
```

```
Example response:

{
    "actor": {
        "age": 42,
        "gender": "Male",
        "id": 4,
        "name": "John Smith"
    },
    "success": true
}
```

#### PATCH /api/movies/<int:id>

- Allows editing of a movie by ID. **Available to Director and Producer**

```
Example body:

{
    "title": "Wedding Crashers"
}
```

```
Example response:

{
    "movie": {
        "title": Wedding Crashers,
        "release_date": "July 15th, 2006",
        "id": 4
    },
    "success": true
}
```

#### DELETE /api/actor/<int:id>

- Allows you to delete an Actor by ID. **Available to Director and Producer**

```
Make a DELETE request to a URL:
ex: http://localhost:5000/api/actor/4

Example response:

{
    "actor": {
        "age": 42,
        "gender": "Male",
        "id": 4,
        "name": "John Smith"
    },
    "success": true
}
```

#### DELETE /api/movie/<int:id>

- Allows you to delete a Movie by ID. **Available to Producer only.**

```
Make a DELETE request to a URL:
ex: http://localhost:5000/api/movies/3

Example response:

{
    "movie": {
        "title": Dodgeball,
        "release_date": "March 15th, 2003",
        "id": 2
    },
    "success": true
}
```

### Unittest Implementation

For API testing, it is recommending to use a separate version of a working database to avoid manipulating your working data. To achieve this, we will need to create a database for testing and change a configuration setting.

```bash
createdb test_castingagency
```

Make sure you are in the project directory and run the following command:

```bash
psql test_castingagency < test_castingagency.psql
```

Once this is done, you will have a new database filled with dummy data to use for testing purposes.

##### Reconfigure Application

With a testing database created, check to make sure setup.sh reflects the appropriate testing database url. Then open up the models.py file and follow the instructions to comment out the appropriate database_path variable.

As long as your Access Tokens are valid, you should be ready to test your application.

When ready, CD into your project directory and run:

###### For Windows 10

```
py test.py
```

###### For Mac/Linux

```
python3 test.py
```

There will be 15 individual tests that test a variety of Authentication, CRUD and status_code errors.
