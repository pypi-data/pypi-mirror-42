# Zeel Publisher

A Library meant to standardize the way zapi services interact with SNS/SQS.

# Getting Started

## Docker

The infrastructure of this library is designed to be run inside of various
docker containers. Specifically there is a container for:
- The python environment the library's code runs in
- A jaeger tracing instance
- The localstack AWS simulator

These containers can be viewed inside the project's docker-compose.yml

Because these containers are all needed to create a functioning local
environment, proceeding without docker is NOT recommended. It can be installed
using the docker for mac installer or via

`brew cask install docker`

## The pipenv Virtual Environment

This service's dependencies are all managed with
[https://github.com/pypa/pipenv](pipenv) and are enumerated inside the project's
Pipfile and Pipfile.lock files. Pipenv is a superset of Pip, and will create a
virtual python environment (the .venv folder) for this Service. To that end,
please ensure you have pipenv installed on your local machine.

`brew install pipenv`

### Configuring your Virtual Environment

To create a virtual environment (the .venv directory) inside your project folder
instead of your home (~) directory, save the following in your .bash_profile or .zshrc:

`export PIPENV_VENV_IN_PROJECT=1`

This is highly recommended for vscode users, as the project's linters and
formatters are configured to use binaries installed to a local .venv

### Running the Library's tests on Docker

Although tests can be run locally, it is recommended to run them through docker,
where they will have access to the infrastructure they need. To do so you can
use this command:

`docker-compose run publisher-app bash test.sh`

# Modules

## Event Publisher

A Class meant for publishing Event Messages to a single SNS topic.

# Distribution

This Code is meant for distribution across multiple projects, namely our various
zapi services which require zeel-publisher as a dependency. The library itself
is hosted on PyPi and can be found at

https://pypi.org/project/zeel-publisher/

## Versioning

Zeel publisher versioning follows the [Semantic Versioning](https://docs.npmjs.com/about-semantic-versioning) syntax:

`Major.Minor.Patch`

Make sure to update setup.py accordingly before publishing a new version.

## Commands for uploading to PyPi

Create build - `pipenv run python3 setup.py sdist`
Publish - `pipenv run twine upload dist/*`

