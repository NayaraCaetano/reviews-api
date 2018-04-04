# reviews-api

[![CircleCI](https://circleci.com/gh/NayaraCaetano/reviews-api.svg?style=svg)](https://circleci.com/gh/NayaraCaetano/reviews-api)

[![Maintainability](https://api.codeclimate.com/v1/badges/d06ab133288471b32132/maintainability)](https://codeclimate.com/github/NayaraCaetano/reviews-api/maintainability)

<a href="https://codeclimate.com/github/NayaraCaetano/reviews-api/test_coverage"><img src="https://api.codeclimate.com/v1/badges/d06ab133288471b32132/test_coverage" /></a>

A simple Python API that allows users to post and retrieve their reviews

## Environment (main tools)

- Python 3.6.4
- Postgresql
- Django Rest Framework 3.8.0
- Django 2.0.4


## Deploy Structure

The application is ready to deploy on Heroku with the following details:
- Buildpacks
    - `heroku/python`
- Continuous integration and deployment: run tests in CircleCI and, if successful,
deploy on Heroku.


## Quality tools

- Sentry is configured to report production errors
- CircleCI is configured to run tests and upload coverage in Code Climate
- Code Climate is configured to check the code quality and present code coverage


## Api documentation

Provides a HTTP REST API with the following endpoints:


### Sign In

Receives user details, saving on database.

- URL: `{base_url}/auth/sign-in`
- HTTP request type: `POST`
- Authentication: None

- Params: This endpoint will accept the following JSON template:

```
{
  "email":  // User unique identificator / Email format / Required;
  "first_name":  // String / Required;
  "last_name":  // String / Non required;
  "password":  // Password format (string) / Required;
  "confirm_password":  // Password format (string) / Required;
}
```

- Return:
  1. HTTP 400: Validation errors or
  2. HTTP 201: User created data

```
{
    "email": <user_email>,
    "first_name": <user_first_name>,
    "last_name": <user_last_name>
}
```

### Login (get token)

Receives email and password, validate and returns the api token.

- URL: `{base_url}/auth/login`
- HTTP request type: `POST`
- Authentication: None

- Params: This endpoint will accept the following JSON template:

```
{
  "email":  // user's email / Required;
  "password":  // user's password / Required;
}
```

- Return:
  1. HTTP 400: Validation errors or
  2. HTTP 200: User token, utilized for authenticate

  ```
  {
      "token": <user_token>,
  }
  ```

### Reviews

  Create and list user reviews.

  - URL: `{base_url}/review/reviews`
  - HTTP request type: `POST` or `GET`
  - Authentication: http header `"Authorization: JWT <your_token>"`

  - Params (post method): This endpoint will accept the following JSON template:

  ```
  {
    "rating":  // Integer 1 - 5 / required,
    "title":  // String, max length 64 / required,
    "summary": // Text, max lenght 10000 / required,
    "company": {
        "name": // String / required,
        "company_id": // Integer / required,
        "website": // URI format / non required
    }
  }
  ```

  - Return (post method):
    1. Validation errors or
    2. Review Created Data

    ```
    {
      "rating": <rate>,
      "title": <title>,
      "summary": <summary>,
      "ip_address": <ip_address utilized in create request>,
      "submission_date": <date od create request format YYYY-mm-dd>,
      "company": {
          "name": <company_name>,
          "company_id": <company_id>,
          "website": <website>
      },
      "reviewer": <reviewer full name>
    }
    ```

  - Return (get method):
    1. List of user's reviews and details

    ```
    [
      {
        "rating": <rate>,
        "title": <title>,
        "summary": <summary>,
        "ip_address": <ip_address utilized in create request>,
        "submission_date": <date od create request format YYYY-mm-dd>,
        "company": {
            "name": <company_name>,
            "company_id": <company_id>,
            "website": <website>
        },
        "reviewer": <reviewer full name>
      },
      ...
    ]
    ```

    - Observations:
      1. If the company id already exists, the api will update data and not create a new one

## Quick start

1. **Database**

- Create a postgresql database with name `reviews_api`

2. **Requirements**

Pip requirements

- Install a python 3.6 virtualenv
- Execute: `pip install -r reviews_api/requirements/pip-dev.txt`

3. **Environment variables**

Create a .env file containing:
```
SECRET_KEY=<django_secret_key>
SENTRY_DSN=<sentry_dsn>
```

4. **Migrate database**

- `python manage.py migrate`

5. **Initialize local server**

- `python manage.py runserver`


## Executing tests

1. **Requirements**

Pip requirements

- Install a python 3.6 virtualenv
- Execute: `pip install -r reviews_api/requirements/pip-dev.txt`

2. **Environment variables**

Create a .env file containing:
```
SECRET_KEY=<django_secret_key>
SENTRY_DSN=<sentry_dsn>
```

4. **Test**

- `pytest`
