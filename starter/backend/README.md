# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 

8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 



```
## API Refrence

Getting started
Base URL: this api is run locally "http://127.0.0.1:5000/"

Error Handling
Errors are return in json format 
example:
{
    "success": False, 
    "error": 400,
    "message": "Bad Request"
}

API returns the following error types in case of failed requests:
404: Not Found
422: unprocessable
400: Bad Request


Endpoints:

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

SET '/categories'
- sets a new category in the database
- Request Arguments: takes a jsno with a single key "category" and its value to be the new category name

{
    "category": "category_name"
}
- Returns: A json object with success = true, the id & type of the added category
{
    "category": {
        "id": 7,
        "type": "category_name"
    },
    "success": true
}

GET '/questions'
- Fetches a dictionary of categories, list of questions and current categories, pagination is allowed e.g. '/questions?page=2'
- Request Arguments: None
- Returns: An object  as follows
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": [
        1,
        2,
        3,
        4,
        5,
        6
    ],
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        }
        .
        .
        etc.
    ],
    "total_questions": 19
}

POST '/questions'
- request could be used for searching existing questions or adding new questions.
    in case of new question:
    - Request Arguments: question, answer, categroy id (it should already exist among categories) & difficulty (choose from 1 to 5 )
    {
        "searchTerm":null,
        "answer": "answer here",
        "category": 1,
        "difficulty": 1,
        "question": "The new question?"
    }
    - Returns:A json object to confirm
    {
        "question": {
            "answer": "answer",
            "category": 1,
            "difficulty": 1,
            "id": 35,
            "question": "question?"
        },
        "success": "true"
    }
    In case of a search:
    - Request Arguments: question, answer, categroy id (it should already exist among categories) & difficulty (choose from 1 to 5 )
    {
        "searchTerm":'key word'  
    }
    - Returns:An object  as follows
    {
        "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        },
        "current_category": [
            1,
            2,
            3,
            4,
            5,
            6
        ],
        "questions": [
            {
                "answer": "Maya Angelou",
                "category": 4,
                "difficulty": 2,
                "id": 5,
                "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            },
            {
                "answer": "Muhammad Ali",
                "category": 4,
                "difficulty": 1,
                "id": 9,
                "question": "What boxer's original name is Cassius Clay?"
            }
            .
            .
            etc.
        ],
        "total_questions": 20
    }

DELETE '/questions/<int:question_id>'
- delets a question of the id added example: DELETE '/questions/35'
- Request Arguments: None
- Returns: A json object  as follows
{
    "message": "Question deleted",
    "success": true
}

GET '/categories/<int:cat_id>/questions'
- Fetches a dictionary of questions based on the specific category,example using category = 1 '/categories/1/questions' 
- pagination is allowed e.g. '/categories/1/questions?page=2'
- Request Arguments: None
- Returns: An object  as follows
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": [
        1
    ],
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        }
    ],
    "total_questions": 3
}

POST '/quizzes'
- This endpoint is to get the next question in trivia game randomly based on the category
- Request Arguments: a json object of a list of the ids of previous questions, quiz_category dictionary with id arg to determine category of the game (in case of all categories id = 0)
{
    "previous_questions": [21],
    "quiz_category": {
        "id":1
    }
}
- Returns: An object  of the next question in the quiz category as follows:
{
    "question": {
        "answer": "Blood",
        "category": 1,
        "difficulty": 4,
        "id": 22,
        "question": "Hematology is a branch of medicine involving the study of what?"
    },
    "questions_per_cat": 3,
    "success": true
}

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```