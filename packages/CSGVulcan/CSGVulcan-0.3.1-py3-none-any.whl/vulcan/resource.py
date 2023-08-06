# -*- coding: utf-8 -*-
"""
*** ALERT *** 
--- To use Vulcan in it's current state, copy this file into the directory of your project.
 __   ___   _ _    ___   _   _  _ 
 \ \ / / | | | |  / __| /_\ | \| |
  \ V /| |_| | |_| (__ / _ \| .` |
   \_/  \___/|____\___/_/ \_\_|\_|
                                  

Vulcan enables anyone to compose a resource they want to share
so that any interested party can consume it in a structured way. 

This module defines the core components of the Vulcan library.

Attributes:
    VulcanResource (ABC):
        A small and consistent interface for describing data-sources.
    VulcanSQLResource (ABC):
        A small and consistent interface for describing sql data-sources.
    VulcanAPI (Flask):
        A zero-config RESTful wrapper for your VulcanResources.

Example:
    Here we describe a list of friends as a VulcanResource...

    from vulcan import VulcanResource, VulcanAPI

    # First we create our resource
    class BestFriends(VulcanResource):
        friends = [
            {'id': 1, 'name': 'Warren'},
            {'id': 2, 'name': 'Nathan'},
            {'id': 3, 'name': 'Ryan'}
        ]
        def init(self, context):
            return None

        def fetch_one(self, context):
            return next(friend for friend in self.friends if friend['id'] == context['id'])
        
        def fetch_all(self, context):
            return self.friends
        
    # Now we can turn our best-friends VulcanResource into a RESTful VulcanAPI
    best_friends_resource = BestFriends()
    best_friends_api = VulcanAPI(resource=best_friends_resource)
    best_friends_api.run(port=8888)

Todo:
    * Create pip installable package
    * Register VulcanResource with Ambrosia on initialization
    * Logging 
    * Metrics, Caching, Retry Logic, and Circuit Breaker for VulcanAPI
    * Testing
    * Documentation

   Vulcan follows Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""
from abc import ABCMeta, abstractmethod


class VulcanResource(metaclass=ABCMeta):
    """
    Base class definition for VulcanResource

    Resources describe a consistent interface over a given datasource. To create a VulcanResource
    inherit from the VulcanResource class. To do so, you must implement three methods: init, fetch_one, and
    fetch_all.
    """

    def __init__(self, name=__name__):
        self._name = name

    @abstractmethod
    def init(self, context):
        pass

    @abstractmethod
    def fetch_one(self, context):
        pass

    @abstractmethod
    def fetch_all(self, context):
        pass


class VulcanSQLResource(VulcanResource):
    """VulcanSQLResource describes a set of functionality around SQL data-sources.

    VulcanSQLResources inherits from VulcanResource and is therefore expected to implement
    init, fetch_one, and fetch_all. Where VulcanSQLResources differ, is there particular
    details around how to interact with SQL data-sources.

    VulcanSQLResources makes use of SQLAlchemy and pandas to access SQL databases. When implementing
    a VulcanSQLResource you are expected to provide a SQLAlchemy connection engine along with init,
    fetch_one, and fetch_all queries respectively.
    """

    def __init__(self, name=__name__, conn_engine=None, init_query=None, fetch_one_query=None, fetch_all_query=None):
        """
        Args:
            conn_engine (SQLAlchemy.Connection_Engine): SQLAlchemy Connection engine for you data-source
            init_query (function): Function returning your `init` sql-query
            fetch_one_query (function): Function returning your `fetch-one` sql-query
            fetch_all_query (function): Function returning your `fetch-all` sql-query
        """
        self._conn_engine = conn_engine
        self._init_query = init_query
        self._fetch_one_query = fetch_one_query
        self._fetch_all_query = fetch_all_query
