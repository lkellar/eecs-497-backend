# Backend for SoleSpeaks (EECS497 Capstone Project)

## Setup

Setting up on local isn't too tricky. To run locally, you'll need Postgres, which you can install with [Homebrew](https://brew.sh) on macOS

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

Troubleshoot: if when you get `Error: Invalid value for '--cert':` at this point, check if flask is inside the virtual environment. If it's not, then reinstall flask inside the env and run `python -m flask --app backend --debug run --cert=adhoc` instead.

When you first try to access it, you may get a scary warning about invalid cert. You can just ignore it (since we're having it use a fake SSL cert locally so logins work).
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
   "id": 3382592932
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

### `/lang/<lang_id>/word/<word_id>` (DELETE) Login Required

Delete a word from a language

#### Response
* Returns `200 OK` upon successful delete
* Returns `400 Bad Request` or `404 Not Found` along with an `error` attribute explaining the issue

```json
{
    "error": "invalid word id"
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

Returns all words, lessons, and data associated with a language.

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
           "definition": null,
           "id": 21
       },
       {
           "english": "catfish",
           "translation": "ᎤᏍᏉᎴᏆ",
           "definition": "A group of fish named for their prominent barbels, resembling a cat's whiskers",
           "id": 500
       }
   ],
   "lessons": [
      {
         "title": "Basic Grammar",
         "id": 3234324324
      }
   ]
}
```

### `/lang/<lang_id>/lesson` (POST)

Creates a new lesson and returns the lesson id.

#### Body (JSON)
* `title` (string)
* `text` (string): Primary text of lesson. Images can be encoded in Markdown format `![image alt text](https://lkellar.org/img/pippinGrass.jpg)`

    
```json
{
    "title": "Basic Grammar",
    "text": "Basic Grammar follows the rules from this picture: ![grammar rules](https://example.com/grammar.jpg)"
}
```

#### Response
* Returns `201 Created` upon successful creation, along with a language id

```json
{
   "id": 3382592932
}
```

* Returns `400 Bad Request` along with an `error` attribute explaining the issue

```json
{
    "error": "missing 'text' attribute"
}
```

### `/lang/<lang_id>/lesson/<lesson_id>` (GET)

Fetch a lesson from its ID

#### Response

Returns 200 and the following if found, 404 if not

```json
{
   "id": 3382592932,
   "title": "Basic Grammar",
   "text": "Basic Grammar follows the rules from this picture: ![grammar rules](https://example.com/grammar.jpg)"
}
```

### `/lang/<lang_id>/lesson/<lesson_id>` (POST)

Update an existing lesson from its ID

#### Body (JSON)

```json
{
    "title": "Basic Grammar",
    "text": "Basic Grammar follows the rules from this picture: ![grammar rules](https://example.com/grammar.jpg)"
}
```

#### Response

* Returns `200 OK` if successful
* Returns `400 Bad Request` along with an `error` attribute explaining the issue

```json
{
    "error": "missing 'text' attribute"
}
```
