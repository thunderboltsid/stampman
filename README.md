Stampman
========
[![Build Status](https://travis-ci.org/thunderboltsid/stampman.svg?branch=master)](https://travis-ci.org/thunderboltsid/stampman)

Almost all businesses need to send large quantities of E-mails to their customers to keep them posted about the service offerings, policy changes, etc. Since there is a lot of complexity involved with ensuring deliverability, avoiding spam filters and blacklists, it is a common practice to use an email service provider such as [Sendgrid](), [Mailgun](), [Mandrill](), [AmazonSES](), etc. in the form of an API to delegate the complexities to the E-mail providers. What happens when the E-mail provider itself goes down?

Stampman provides a high level abstraction for sending emails using multiple email service providers (AmazonSES, Mandrill, Mailgun, and Sendgrid) to ensure seamless failover designed in a way that facilitates modular addition of a new E-main provider.

Architectural Musings
---------------------
The service comprises of four components:

  - **Services**: Representing individual services (sendgrid, mailgun, etc.) that subclass `AbstractEmailService`. The two complete ones currently are `SendgridEmailService` and `MailgunEmailService`. These services are then utilized by the `PooledEmailServce` which also subclass `AbstractEmailService` and provides the interface for the REST API to communicate with. These services can be found in the `stampman.services` module.
  - **Configuration**: The configuration is managed by a `config.json` file present in project root. The file and the schema is provided and needs to be populated with API keys for individual services, the API key governing a group of services associated with a email domain, and the API key for the project admins to manage all pools. 
  - **Helpers**: These are the constructs that are useful for doing the data wrangling and providing the necessary abstractions for the `stampman.services` module to load configurations and provide an abstraction for E-mail message.
  - **Stampman API**: This is the python-flask server that provides a browsable API, verifies the interactions at the endpoints, takes care of data marshalling, and permission verification. This runs off of `stampman.main` module. Whether the API results in a browsable API or a JSON response is determined by the `accept` header in the request. The API provides the following endpoints:
  
    * `/`: List all available pools with their domains
    * `/<domain>/` List the services and priorities of a specific domain
    * `/<domain>/send`: Send an email using the pooled service using the increasing order of priorities in case of a failover.
    
Dependencies
------------
The codebase is written in Python with type annotations and works on all versions of Python 3.5 and above. The complete list of dependencies and versions is present in the `requirements.txt` file in project root. The libraries used to facilitate rapid development of the library are:

  - Flask: For creating the web API
  - Flask-API: For providing a browsable frontend for the API
  - requests: For a simple mechanism to make http requests (Mailgun only has a HTTP API)
  - python-sendgrid: Official Sendgrid library for Python for a convenient interface
  - gunicorn: wsgi server for hosting the flask app on heroku

Testing
-------
The project has unit tests for testing individual components. A Travis instance has been setup to track the status of all the builds and test cases are being run on:

  - `python3.5-dev`
  - `python3.6-dev`
  - `python3.7-dev`
  
The tests only take place on Python versions 3.5 and above because the codebase uses [type annotations (c.f. PEP 484)](https://www.python.org/dev/peps/pep-0484/) as a linting mechanism during the development to provide a better overview of the code. However, as a result, the code is not compatible with Python versions below `python3.5`.

The tests can be found under the `stampman.tests` module and comprise of four files:
   
  - `test_helpers.py`: Testing the behaviour of the functions and classes in the `stampman.helpers` module.
  - `test_api.py`: Testing the behaviour of the API endpoints under `stampman.main`.
  - `test_services.py`: Testing the behaviour of the EmailService classes under `stampman.services` module.
  - `test_sanity.py`: Tests the code cleanliness by checking whether the codebase adheres to the [style guide for python (c.f. PEP 8)](https://www.python.org/dev/peps/pep-0008/).

For running the unit tests locally, execute:
`python -m unittest discover`

Deployment
----------
Deployment is automated to ensure that production server is always using the latest and most up to date code. Every change is monitored and every time a change is made to the codebase, a build process is triggered that executes all the test cases. Every successful build on travis CI automatically gets deployed on heroku at https://stampman.herokuapp.com

The app currently uses gunicorn as a http server which is easy to setup but not optimal for production use because it's a pre-forking process model and can handle only a certain number of concurrent requests. In a full-production environment, this would be run behind a buffering reverse proxy such as nginx or with async workers.

Security
--------
There is no authentication strategy for users. However, a two-tiered authorization strategy has been provided:

  - `Pool Owner`: A pool owner has the pool api key and can send emails from the services in their pool.
  - `Admin`: Admins have the admin api key which can be used to get information about all the pools running on the system.
  
The deployment server is running on heroku and relies on TLS to protect the data.

Logging and Error handling
--------------------------
Basic logging is handled by the python [`logging`](https://docs.python.org/3/library/logging.html) module. The extent of logging currently is mostly limited to logging requests to all API endpoints, exceptions, and failures. A simple cron job can be made to backup the logs and clear the memory once the logfiles grow too big. In production, a more extensive logging and retrievable storage of failed emails would be desired. A simple redis instance, with keys being UUIDs generated by the API and values being the E-Mails to log successful and unsuccessful E-mails per pool. 

Custom exception classes are placed in `stampman.helpers.exceptions` to represent various failure conditions. With the extent of exception handling, the state of the application should not be compromised by the invalid inputs, in particular inducing an Internal Server Error.

Monitoring
----------
[Sentry.io](https://sentry.io) is used for basic error monitoring and reporting. Each deployment server must set an evironment variable called "SENTRY_API_DSN" that contains the address (incl. API key) to report the errors to.

For a more independent approach, a simple script that queries the endpoints from time to time would be sufficient.

Links
-----
  - [Hosted Application](https://stampman.herokuapp.com)
  - [Resumé](https://github.com/thunderboltsid/CV_Siddharth_Shukla/raw/master/CV_Siddharth_Shukla.pdf)