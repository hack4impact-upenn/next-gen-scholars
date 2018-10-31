# Next Generation Scholars

## Team Members
#### UPenn
* Client-facing Project Manager: Hana Pearlman
* Team-facing Project Manager: Katie Jiang
* Aruna Prasad
* Kasra Koushan
* Steven Bursztyn

#### University of Richmond
* Codirectors: Emily Everett and Melissa Gu
* Wallace He, Jonathan Huang, Katrina Kuhn, Tracy Nguyen

## Setting up for Python 3
__Must use Python3__

#####  Clone the repo

```bash
$ git clone https://github.com/hack4impact/next-gen-scholars.git
$ cd next-gen-scholars
```

##### Initialize a virtualenv

```bash
$ pip install venv
$ python3 -m venv env
$ source env/bin/activate
```

Note: you must use python3+

##### (If you're on a mac) Make sure xcode tools are installed

```bash
$ xcode-select --install
```

##### Add Environment Variables

Create a file called `config.env` that contains environment variables in the following syntax: `ENVIRONMENT_VARIABLE=value`. For example,
the mailing environment variables can be set as the following. We recommend using Sendgrid for a mailing SMTP server. But anything else will work as well. You must have `PLOTLY_USERNAME` and `PLOTLY_API_KEY` set in order to run the application. Make an account on [Plotly](http://plot.ly) for more details.

```python3
PLOTLY_USERNAME=MyPlotlyUsername
PLOTLY_API_KEY=XXXXXXXXXXXX
MAIL_USERNAME=MySendgridUsername
MAIL_PASSWORD=MySendgridPassword
SECRET_KEY=SuperRandomStringToBeUsedForEncryption
CLIENT_SECRETS_FILE=NameOfFileWithClientSecret
```

Other Key value pairs:

* `ADMIN_EMAIL`: set to the default email for your first admin account (default is `flask-base-admin@example.com`)
* `ADMIN_PASSWORD`: set to the default password for your first admin account (default is `password`)
* `DATABASE_URL`: set to a postgresql database url (default is `data-dev.sqlite`)
* `REDISTOGO_URL`: set to Redis To Go URL or any redis server url (default is `http://localhost:6379`)
* `RAYGUN_APIKEY`: api key for raygun (default is `None`)
* `FLASK_CONFIG`: can be `development`, `production`, `default`, `heroku`, `unix`, or `testing`. Most of the time you will use `development` or `production`.


**Note: do not include the `config.env` file in any commits. This should remain private.**

##### Install the dependencies

```bash
$ pip install -r requirements.txt
```

##### Other dependencies for running locally

You need [Redis](http://redis.io/), and [Sass](http://sass-lang.com/). Chances are, these commands will work:


**Sass:**

```bash
$ gem install sass
```

**Redis:**

_Mac (using [homebrew](http://brew.sh/)):_

```bash
$ brew install redis
```

_Linux:_

```bash
$ sudo apt-get install redis-server
```

You will also need to install **PostgresQL**

_Mac (using homebrew):_

```bash
$ brew install postgresql
```

_Linux:_

```bash
$ sudo apt-get install libpq-dev
```


##### Create the database

```bash
$ python3 manage.py recreate_db
```

##### Other setup (e.g. creating roles in database)

```bash
$ python3 manage.py setup_dev
```

Note that this will create an admin user with email and password specified by the `ADMIN_EMAIL` and `ADMIN_PASSWORD` config variables. If not specified, they are both `flask-base-admin@example.com` and `password` respectively.

##### [Optional] Add fake data to the database

```bash
$ python3 manage.py add_fake_data
```

## Running the app

```bash
$ source env/bin/activate
$ honcho start -f Local
```

## Formatting code

Before you submit changes to next-gen-scholars, you may want to autoformat your code with `python manage.py format`.


## License
[MIT License](LICENSE.md)
