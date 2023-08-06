"""Project: Eskapade - A python-based package for data analysis.

Class: MongoRetrieveLastAdded

Created: 2019-02-19

Description:
    Algorithm to ...(fill in one-liner here)

Authors:
    KPMG Advanced Analytics & Big Data team, Amstelveen, The Netherlands

Redistribution and use in source and binary forms, with or without
modification, are permitted according to the terms listed in the file
LICENSE.
"""

from escore import process_manager, ConfigObject, DataStore, Link, StatusCode
from mongodbtools import MongoConnection


class MongoRetrieveLastAdded(Link):

    """Defines the content of link."""

    def __init__(self, **kwargs):
        """Initialize an instance.

        :param str name: name of link
        :param str read_key: key of input data to read from data store
        :param str store_key: key of output data to store in data store
        """
        # initialize Link, pass name from kwargs
        Link.__init__(self, kwargs.pop('name', 'MongoRetrieveLastAdded'))

        # Process and register keyword arguments. If the arguments are not given, all arguments are popped from
        # kwargs and added as attributes of the link. Otherwise, only the provided arguments are processed.
        self._process_kwargs(kwargs, collection='', store_key='')

        # check residual kwargs; exit if any present
        self.check_extra_kwargs(kwargs)
        # Turn off the line above, and on the line below if you wish to keep these extra kwargs.
        # self._process_kwargs(kwargs)

    def initialize(self):
        """Initialize the link.

        :returns: status code of initialization
        :rtype: StatusCode
        """
        settings = process_manager.service(ConfigObject)
        process_manager.service(MongoConnection).set_config_info(settings)
        self.mdb = process_manager.service(MongoConnection).database

        self.check_arg_types(collection=str, store_key=str)
        self.check_arg_vals('collection', 'store_key')

        return StatusCode.Success

    def execute(self):
        """Execute the link.

        :returns: status code of execution
        :rtype: StatusCode
        """
        ds = process_manager.service(DataStore)

        # retrieve last document added to collection
        doc = self.mdb[self.collection].find().sort('_id', -1)[0]
        ds[self.store_key] = doc

        return StatusCode.Success
