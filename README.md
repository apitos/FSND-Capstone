# Casting-Agency

## Project Description
This is the capstone project for Full-Stack Udacity Nanodegree. Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. There are three different roles in the company Casting Assistant, Casting Director, and Executive Producer. Each of them has a different set of permissions to view, add, update and delete movies and actors in the databse.

Though the front-end is very simple, most of the work are done in the back-end. I wrote Restful APIs, built a database using SQLAlchemey, secured the application using Auth0, tested the application using unit tests and via Postman, and finally deploy the application to Heroku.

## Project Result
Heroku: https://capstone-castingag-app.herokuapp.com/

Localhost: http://127.0.0.1:5000/

## Tech Stack
* **PostgreSQL** as our database of choice
* **Python3** and **Flask** as our server language and server framework
* **Auth0** for authentication management
* **Heroku** for deployment
* **JSON** for rendering the results.
* **HTML**, **CSS** is planned for the next development of the application.


## Getting Started

1. Initialize and activate a virtualenv:
  ```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ virtualenv --no-site-packages venv
  $ source venv/bin/activate // for MAC
  $ source venv/Scripts/activate // for Windows
  ```

2. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```
  This will install all of the required packages we selected within the `requirements.txt` file.

3. run ```source setup.sh``` to set the environnement variables, and the user tokens the user jwts, auth0 credentials

3. Database Setup

  ```
  CREATE DATABASE capstone; // to create capstone database 
  ----> psql casting < casting.pgsql
  ```

4. Run the development server:
  ```
  $ export FLASK_APP=myapp
  $ export FLASK_ENV=development # enables debug mode
  flask run --reload # reload server after any changes detected
  ```

## Testing
To run the tests, run 
```
dropdb capstone
createdb capstone
---> psql casting_test < casting.pgsql
python -m unittest test_app.py
```

## API Reference

### Endpoints

#### GET '/movies'
- General:
    - Return all movies in the database
    - Role Authorized: Casting Assistant, Casting Director, Executive Producer
- Example: ```curl -H "Authorization: Bearer <Token>" http://127.0.0.1:5000/movies```
```
{
	"movies":
	{
		"1":
		{
			"actors": [
			{
				"age": 22,
				"gender": "Male",
				"id": 1,
				"movie_id": 1,
				"name": "Jack"
			}],
			"id": 1,
			"release_date": "1966",
			"title": "Bibro"
		},
		"2":
		{
			"actors": [
			{
				"age": 35,
				"gender": "Male",
				"id": 11,
				"movie_id": 2,
				"name": "Brown"
			}],
			"id": 2,
			"release_date": "2010",
			"title": "March of the Penguins"
		},
		"3":
		{
			"actors": [
			{
				"age": 60,
				"gender": "Female",
				"id": 10,
				"movie_id": 3,
				"name": "Michelle"
			}],
			"id": 3,
			"release_date": "2010",
			"title": "Way down"
		},
		"success": true
	}
}
```
#### GET '/actors'
- General:
    - Return all actors in the database
    - Role Authorized: Casting Assistant, Casting Director, Executive Producer
- Example: ```curl -H "Authorization: Bearer <Token>" http://127.0.0.1:5000/actors```
```
{
	"actors":
	{
		"1":
		{
			"age": 22,
			"gender": "Male",
			"id": 1,
			"movie_id": 1,
			"name": "Jack"
		},
		"3":
		{
			"age": 32,
			"gender": "Male",
			"id": 3,
			"movie_id": 10,
			"name": "Julian"
		},
		"4":
		{
			"age": 55,
			"gender": "Female",
			"id": 4,
			"movie_id": 9,
			"name": "Mary"
		}
	},
	"success": true
}
```

#### POST '/movies'
- General:
    - Add a new movie. The new movie must have all two information. 
    - Role Authorized: Executive Producer
- Example: ```curl -X POST  http://127.0.0.1:5000/movies -H "Content-Type: application/json" -H "Authorization: Bearer <TOKEN>" -d '{"title": "Locked Down", "release_date": "2021"}'```
```
{
	"movies":
	{
		"45":
		{
			"actors": [],
			"id": 45,
			"release_date": "2021",
			"title": "Locked Down"
		}
	},
	"success": true
}
```

#### POST '/actors'
- General:
    - Add a new actor. The new movie must have all four information. 
    - Role Authorized: Casting Director, Executive Producer
- Example: ```curl -X POST  http://127.0.0.1:5000/actors -H "Content-Type: application/json" -H "Authorization: Bearer <TOKEN>" -d '{"name": "Anne Hathaway", "age": 39, "gender": "Female", "movie_id": 45}'```

```
{
	"actors":
	{
		"12":
		{
			"age": 39,
			"gender": "Female",
			"id": 12,
			"movie_id": 45,
			"name": "Anne Hathaway"
		}
	},
	"success": true
}
```

#### PATCH '/movies/<int:id>'
- General:
    - Update some information of a movie based on a payload.
    - Roles authorized : Casting Director, Executive Producer.
- Example: ```curl -X PATCH http://127.0.0.1:5000/movies/42 -H "Content-Type: application/json" -H "Authorization: Bearer <TOKEN>" -d '{"title":"The Empire", "release_date":"1988"}'```
```
{
	"movies":
	{
		"42":
		{
			"actors": [
			{
				"age": 22,
				"gender": "Female",
				"id": 6,
				"movie_id": 42,
				"name": "Yu"
			}],
			"id": 42,
			"release_date": "1988",
			"title": "The Empire"
		},
		"success": true
	}
}
```

#### PATCH '/actors/<int:id>'
- General:
    - Update some information of an actor based on a payload.
    - Roles authorized : Casting Director, Executive Producer.
- Example: ```curl -X PATCH http://127.0.0.1:5000/actors/1 -H "Content-Type: application/json" -H "Authorization: Bearer <TOKEN>" -d '{"name": "Julian Grey", "age": 32, gender:"Male", "movie_id":10}'```
```
{
	"actors":
	{
		"3":
		{
			"age": 32,
			"gender": "Male",
			"id": 3,
			"movie_id": 10,
			"name": "Julian Grey"
		}
	},
	"success": true
}
```

#### DELETE '/movis/<int:id>'
- General:
    - Deletes a movie by id from the url parameter.
    - Roles authorized : Executive Producer.
- Example: ```curl -X DELETE http://127.0.0.1:5000/movies/10 -H "Content-Type: application/json" -H "Authorization: Bearer <TOKEN>"```
```
{
	"deleted": 10,
	"success": true
}
```

#### DELETE '/actors/<int:id>'
- General:
    - Deletes a movie by id form the url parameter.
    - Roles authorized : Casting Director, Executive Producer.
- Example: ```curl -X DELETE http://127.0.0.1:5000/actors/5 -H "Content-Type: application/json" -H "Authorization: Bearer <TOKEN>"```
```
{
	"deleted": 5,
	"success": true
}
```

### Error Handling
Errors are returned in the following json format:
```
{
    'success': False,
    'error': 404,
    'message': 'Resource not found. Input out of range.'
}
```
The API returns 6 types of errors:
- 400: bad request
- 404: not found
- 403: forbidden
- 422: unprocessable
- 500: internal server error
- AuthError: which mainly results in 401 (unauthorized)
