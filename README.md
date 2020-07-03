# Capstone Project: Casting Agency Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

It is recommended to work within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
export FLASK_ENV=development
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

# API Documentation
## Getting Started
- Base URL by default `http://127.0.0.1:5000/`
- Authentication: This version of the application requires authentication. Authentication Service from Auth0 was used

## Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

The API has the following Handlers for errors:
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 405: Method Not Allowed
- 422: Unprocessable
- 500: Internal Server Error
- AuthError: Custom error trown when authentication is not in order

## Endpoints

### GET /movies
- Returns movie parameters of `Movie` model, which contains the id, title und release_date and cast.
- Cast is returning list of artists connected to the movie through the `movie_actors` table
- Request needs to have a bearer token that includes the permission "get: movies"
- Sample: `http://127.0.0.1:5000/movies`
```
{
    "success": True,
    "id": 1,
    "title": "Star Wars: Episode V - The Empire Strikes Back",
    "release_date": "1980-05-21T15:43:18.535+02:00",
    "cast": [
        {
            "id": 1,
            "name": "Mark Hamill"
        },
        {
            ...
        }
    ]
}
```

### POST /movies
- Creates a new movie in the db, the request includes title and release_date
- Request needs to have a bearer token that includes the permission "post: movies"
- Sample Request
```
{
    "title": "The Lord of the Rings: The Return of the King",
    "release_date": "2003-12-17T15:46:53.887+01:00"
}
```

- This request will return as following
```
{
    "success": True
}
```

### PATCH /movies/<id>
- Updates the given movie in the db
- Request needs to have a bearer token that includes the permission "patch: movies"
- Sample Request
```
{
    "title": "The Lord of the Rings: The Return of the King"
}
```

- This request will return as following
```
{
    "success": True
}
```

### DELETE /movies/<id>
- Remove the given movie from the db
- Request needs to have a bearer token that includes the permission "delete: movies"

- This request will return as following
```
{
    "success": True
}
```

### GET /actors
- Returns actor parameters of `Actor` model, which contains the id, name, age, gender and movies.
- Movies is returning list of movies connected to the actor through the `movie_actors` table
- Request needs to have a bearer token that includes the permission "get: actors"
- Sample: `http://127.0.0.1:5000/actors`
```
{
    "success": True,
    "id": 1,
    "name": "Mark Hamill",
    "age": 68,
    "gender". "Male"
    "movies": [
        {
            "id": 1,
            "title": "Star Wars: Episode V - The Empire Strikes Back"
        },
        {
            ...
        }
    ]
}
```

### POST /actors
- Creates a new actor in the db, the request includes name, age and gender
- Request needs to have a bearer token that includes the permission "post: actor"
- Sample Request
```
{
    "name": "Mark Hamill",
    "age": 68,
    "gender": "Male"
}
```

- This request will return as following
```
{
    "success": True
}
```

### PATCH /actors/<id>
- Updates the given actor in the db
- Request needs to have a bearer token that includes the permission "patch: actor"
- Sample Request
```
{
    "name": "Mark Hamill"
}
```

- This request will return as following
```
{
    "success": True
}
```

### DELETE /actors/<id>
- Remove the given actor from the db
- Request needs to have a bearer token that includes the permission "delete: actors"

- This request will return as following
```
{
    "success": True
}
```