# DS Platform :: Vulcan

> A tiny python library for expressing data as a resource.

## Installing / Getting started

A quick introduction of the minimal setup you need to get a hello world up &
running.

```shell
pip install CSGVulcan
```

```python
from CSGVulcan import VulcanResource, VulcanAPI

class MyNewResource(VulcanResource):
    def __init__(self, resource, name=__file__):
        self.super().__init__(resource, name=name)

    def init(self, _context):
        return "Init"

    def  fetch_one(self, _context):
        return "Fetch One"

    def fetch_all(self, _context):
        return "Fetch All"

my_new_resource = MyNewResource()
my_new_resource_api = VulcanAPI(resource=my_new_resource)
# VulcanAPI.run is a proxy for Flask.run, therefore accepts the same arguments
my_new_resource_api.run(port=8080, debug=True)
```

CSGVulcan will then spin up a Flask Web Server at 127.0.0.1:8080
with the following routes available for consumption.

- /api/ping
- /api/fetch-one
- /api/fetch-all

### For more detailed examples please see the _examples_ directory

## Developing

If you're interested in developing and contributing to Vulcan, first, clone this project
from Github. Secondly, set up your local environemnt for develpment. It is recommended to
create a python virtual environment to manage your dependencies, here is how to do
that.

Create and activate your virtualenv.

```shell
python -m venv venv
```

```shell
source ./venv/bin/activate
```

Pip install the depdencies

```shell
pip install -r requirements.txt
```

## Features

- Provides a simple and consistent interface for describing data from external resources.
- Once defined, your VulcanResource is then easily converted into a REST API.

## Contributing

If you'd like to contribute, please fork the repository and use a feature
branch. Pull requests are warmly welcomed.

Vulcan is a tool designed to serve others, so any and all feedback is expected and
encouraged. We aim to create a better pattern for accessing data, if you have ideas, contribute them.

### Styleguide

Vulcan is written using autopep8 and pylint, it is recommended to leverage those to allow
for consistent styling of source code.

## Links

Though not exhaustive, here is a list of useful links that may help in developing an understanding of Vulcan and what it is comprised of.

- [Flask](http://flask.pocoo.org/)
