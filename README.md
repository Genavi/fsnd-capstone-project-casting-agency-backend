# Capstone Project: Casting Agency Backend

## Motivation

With this project I can use all that I have learned in this Udacity programm and put it to the test. This project is an opportunity to confirm and reinforce the skills I have learned during this program.

## Authetication

In this project we are using the Authentication Service from [Auth0](https://auth0.com).

[Here](https://auth0.com/docs/quickstart/backend/python#configure-auth0-apis) you can read more on how the API was configured, the JWTs were validated and the routes were protected.

### Application Roles

#### Executive Producer

Casting Agency producer, can perform all actions.

Permissions:
```
- delete: actors
- delete: movies
- get: actors
- get: movies
- patch: actors
- patch: movies
- post: actors
- post: movies
```

Current `JWT`:
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNjVWpBTFJ2bGpxVEROZ050MHRUcCJ9.eyJpc3MiOiJodHRwczovL2RybGVhcm5pbmcuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZTM0NTA0NmNjNDM5MDAxNGM0NDA0YyIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTM5NzUzMTksImV4cCI6MTU5NDA2MTcxOSwiYXpwIjoiQ2t3bjJRMjRpQzF3M3dXQVZUSUR3NzloT3A0SlZKNksiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTogYWN0b3JzIiwiZGVsZXRlOiBtb3ZpZXMiLCJnZXQ6IGFjdG9ycyIsImdldDogbW92aWVzIiwicGF0Y2g6IGFjdG9ycyIsInBhdGNoOiBtb3ZpZXMiLCJwb3N0OiBhY3RvcnMiLCJwb3N0OiBtb3ZpZXMiXX0.Ek_vLdo29IKfmiVVbwVe0dTTE2e4LIFBeCbmU-Kv2pLX301xjZjQEikHPVIqX5gi3ctpnnYb8xcEwbaSqbeG-x1L0tBfZlxRR43DxQ0bFaEeHNGK0CgE2NP598B09lZKgZIPL7aKai_LUIvTTCmNakN---mgiWqugTSGWHwzFx9rMUE03IkHG4p6vVg8BVd-o2Z7Cdm_wKEIfteXWJEpis9JCrgqASaTfoySo-I9tMKg5e3LlsQ8488q3r8D9wn7DSIWv-oUkIfB8KhjfVNpZpLSWiWsQGt395nylavQ97ztun3oYUavFIYqcfn2j7frXAHwL4vy-QSu2TWdMNDTzw
```

#### Casting Director

Casting Agency director, can view actors and movies, add or delete an actor from the database and modify actors or movies.

Permissions:
```
- delete: actors
- delete: movies
- get: actors
- get: movies
- patch: actors
- patch: movies
- post: actors
```

Current `JWT`:
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNjVWpBTFJ2bGpxVEROZ050MHRUcCJ9.eyJpc3MiOiJodHRwczovL2RybGVhcm5pbmcuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZTM0M2JlZTFiM2U0MDAxMzFiOWNkYSIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTM5NzUzNTgsImV4cCI6MTU5NDA2MTc1OCwiYXpwIjoiQ2t3bjJRMjRpQzF3M3dXQVZUSUR3NzloT3A0SlZKNksiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTogYWN0b3JzIiwiZ2V0OiBhY3RvcnMiLCJnZXQ6IG1vdmllcyIsInBhdGNoOiBhY3RvcnMiLCJwYXRjaDogbW92aWVzIiwicG9zdDogYWN0b3JzIl19.Ogoud2JHjcwncpdqWcx-bhAtVPTjdSwRygL0xR9H7zWQKUvnPwn1-gvHZsBoJrAeoJAHl1hOYknO8RsyXI35afPxIRGSJEUWIsDtxDZzXihIBKzZkA9cukrxlSMtW2BXdUq-oQ-nc98UastVBzoVCtXQZqrjPIwir1gOGtXY1XM2XR3v4l_KfuV83iPG2rHLQL4lVHa7uXsLNV1w-kfsyBd4ORMqBQBPhQX4dFV83CFmwm8LlCW1Xfwztdy8AT94ZoslW5vdUMEiHpsl-JTyrZ0IGVUa0069q3uSKPZsaOLWwL01qzVupjydxb7nWcBAGhxTfL0PQvVaKcI4_sqMTw
```

#### Casting Assistant

Casting Agency employee, can view actors and movies.

Permissions:
```
- get: actors
- get: movies
```

Current `JWT`:
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNjVWpBTFJ2bGpxVEROZ050MHRUcCJ9.eyJpc3MiOiJodHRwczovL2RybGVhcm5pbmcuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZTM0MWZhMWZiOGMzMDAxNDcxM2RhZiIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTM5NzU0MTAsImV4cCI6MTU5NDA2MTgxMCwiYXpwIjoiQ2t3bjJRMjRpQzF3M3dXQVZUSUR3NzloT3A0SlZKNksiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDogYWN0b3JzIiwiZ2V0OiBtb3ZpZXMiXX0.txykzt6zMaShQjnJkz4jmgbPqEl982uRIq_4gTDDuau_SY-tErw9EIPwMxfyvAhvkpPJHKb_DCB9BG-wjkhMRIl-sXrNqL-ct2dp1xccPcGinZsxV2yAPwc5PKKC-xfc_uuI87BqqHL9IbD6U2OkNsmPY59BnOg7bgtUqqMrGlxnuF80Lkq9RWxbEZ9qOWNR_Gu3PpE067ItMyRSmY5r8UzRuyZbqJW2MtlXKgFiXxVHvP7YSdOYrbEfoCg-1J4tgZV8pu6eb2Xy_3k5t05wtajQK6wmEOALFf1xF97AzD7oii7JjOjbDzL9xXbhr754PaFgefWTS4H_0YKu00rGtg
```

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

- [Gunicorn](https://gunicorn.org) Gunicorn is a pure-Python HTTP server for WSGI applications. We'll be deploying our applications using the Gunicorn webserver.

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
- Heroku URL `https://drlearning-casting-agency.herokuapp.com`
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
- Sample: `https://drlearning-casting-agency.herokuapp.com/movies`
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
- Sample: `https://drlearning-casting-agency.herokuapp.com/movies`
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
- Sample: `https://drlearning-casting-agency.herokuapp.com/movies/1`
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
- Sample: `https://drlearning-casting-agency.herokuapp.com/movies/1`
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
- Sample: `https://drlearning-casting-agency.herokuapp.com/actors`
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
- Sample: `https://drlearning-casting-agency.herokuapp.com/actors`
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
- Sample: `https://drlearning-casting-agency.herokuapp.com/actors/1`
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
- Sample: `https://drlearning-casting-agency.herokuapp.com/actors/1`
- This request will return as following
```
{
    "success": True
}
```