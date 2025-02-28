# EECS 497 Backend

we gotta think of a name for this project

## Setup

Setting up on local isn't too tricky. (Eventually we'll get this hosted probably) To run locally, you'll need Postgres (I'm using Postgres 17), which you can install with [Homebrew](https://brew.sh) on macOS

```bash
brew install postgresql@17 libpq
```

You'll probably need to add the Postgres utils to your PATH (skip this step if `psql` doesn't say something like "command not found"):

```bash
# if using Apple Silicon (M1 or later)
echo 'export PATH="/opt/homebrew/opt/libpq/bin:$PATH"' >> ~/.zshrc

# if using Intel x64
echo 'export PATH="/usr/local/opt/libpq/bin:$PATH"' >> ~/.zshrc
```

Run the following to start the db (on Homebrew):

```bash
brew services start postgresql@17
```

Then, run the following commands to create the database:

```bash
psql -d postgres # which should open the postgres shell
CREATE DATABASE eecs497_backend;
\q # to quit
```

and that should setup the db locally (yay!).

Then, clone the repo, setup your python virtualenv, and install dependencies with `pip install -r requirements.txt`.

Create an `env.sh` setting an environment variable like `export EECS497_BACKEND_SECRET_KEY='SOEMTHING'`. A suitable key can be generated with `python -c 'import secrets; print(secrets.token_hex())'`. Then `source env.sh` or run it to set that env variable.

Then, just run `flask --app backend --debug run --cert=adhoc` and the server should be running! (let me know if it doesn't work).

When you first try to access it, you may get a scary warning about invalid cert. You can just ignore it (since we're having it use a fake SSL cert locally so logins work).

## TODO
- deploy to AWS or something hosted
- support multiple users editing lang
- flashcard support (though could this just be front-end, e.g. load all the words and just do it there)
- quiz support
- the lesson plan lesson structure?
- export

## API Routes
Supports the following routes. All POST requests take JSON bodies.

All errors will return a JSON response with a message describing the rror:

```json
{
   "error": "This is the problem with the request"
}
```

### `/auth/me` (GET)

Check if a user is logged in / session cookie is valid. If successful, logged in email is returned

#### Response
* Returns `200 Created` if logged in, along with the email address
* Returns `401 Unauthorized` if logged out or not valid auth

```json
{
    "email": "john@umich.edu"
}
```

### `/auth/register` (POST)

Register a new user with email and password. Returns a session cookie if successful. Email must be unique

#### Body (JSON)
* `email` (string)
* `password` (string) Must be minimum 8 characters

```json
{
    "email": "john@umich.edu",
    "password": "jficerwjisfjiedjf"
}
```

#### Response
* Returns `201 Created` if successful registration, along with a valid session cookie
* Returns `400 Bad Request` if there's an issue in creation, along with an `error` attribute explaining the issue.

```json
{
    "error": "User with email address already exists"
}
```

### `/auth/login` (POST)

Login a user with email and password. Returns a session cookie if successful

#### Body (JSON)
* `email` (string)
* `password` (string)

```json
{
    "email": "john@umich.edu",
    "password": "jficerwjisfjiedjf"
}
```

#### Response
* Returns `200 OK` if successful login, along with a valid session cookie.
* Returns `400 Bad Request` if there's invalid input/body.
* Returns `401 Unauthorized` for invalid login.

### `/auth/logout` (POST)

Logs out user if logged in. No body required

#### Response
* Returns `200 OK` if successful logout
* Returns `401 Unauthorized` if user wasn't logged in to begin with.

### `/lang/create` (POST) (Login Required)

Create a language (required before any lessons or words can be imported)

#### Body (JSON)
* `name` (string): Name of the language (must be unique)

```json
{
    "name": "Cherokee"
}
```

#### Response
* Returns `201 OK` if successful creation, along with an id for the language.

```json
{
   "name": "Cherokee",
   "id": "3382592932"
}
```

* Returns `400 Bad Request` if unsuccessful, along with an `error` attribute explaining the issue

```json
{
    "error": "Language called Cherokee already exists"
}
```

### `/lang/<lang_id>/import` (POST) (Login Required)

Imports new word(s) to a language.

#### Body (JSON List)
* `words` (array): A JSON array of objects meeting the following format:
    * `english` (string): The word in English
    * `translation` (string): The word translated to the native language
    * `definition` (string) (optional): The definition of the word in English
    
```json
{
    "words": [
        {
            "english": "dog",
            "translation": "ᎩᏟ",
        },
        {
            "english": "catfish",
            "translation": "ᎤᏍᏉᎴᏆ",
            "definition": "A group of fish named for their prominent barbels, resembling a cat's whiskers"
        }
    ]
}
```

#### Response
* Returns `201 Created` upon successful creation
* Returns `400 Bad Request` along with an `error` attribute explaining the issue

```json
{
    "error": "missing 'english' attribute on an entry"
}
```

### `/lang` (GET)

Takes no arguments, just returns a list of active languages

```json
[
    {
       "name": "Cherokee",
       "id": 3382592932
    }
]
```

### `/lang/<lang_id>` (GET)

Returns all words and data associated with a language.

```json
{
   "language": {
      "id": 85435345345,
      "name": "Cherokee"
   },
   "words": [
      {
           "english": "dog",
           "translation": "ᎩᏟ",
           "definition": null
       },
       {
           "english": "catfish",
           "translation": "ᎤᏍᏉᎴᏆ",
           "definition": "A group of fish named for their prominent barbels, resembling a cat's whiskers"
       }
   ]
}
```