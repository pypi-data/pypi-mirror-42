"""Project: Eskapade - A python-based package for data analysis.

Class: MongoDocToCollection

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
from mongodbtools import MongoConnection, etl_utils


class MongoDocToCollection(Link):

    """Defines the content of link."""

    def __init__(self, **kwargs):
        """Initialize an instance.

        :param str name: name of link
        :param str read_key: key of input data to read from data store
        :param list store_collections: mongo collections to store doc in
        :param bool clear_first: if true, clear collections first before storage
        """
        # initialize Link, pass name from kwargs
        Link.__init__(self, kwargs.pop('name', 'MongoDocToCollection'))

        # Process and register keyword arguments. If the arguments are not given, all arguments are popped from
        # kwargs and added as attributes of the link. Otherwise, only the provided arguments are processed.
        self._process_kwargs(kwargs, read_key='', store_collections=[], clear_first=False)

        # check residual kwargs; exit if any present
        self.check_extra_kwargs(kwargs)
        # Turn off the line above, and on the line below if you wish to keep these extra kwargs.
        # self._process_kwargs(kwargs)

    def initialize(self):
        """Initialize the link.

        :returns: status code of initialization
        :rtype: StatusCode
        """
        self.check_arg_types(read_key=str, store_collections=list)
        self.check_arg_types(recurse=True, allow_none=True, store_collections=str)
        self.check_arg_vals('read_key')

        settings = process_manager.service(ConfigObject)
        process_manager.service(MongoConnection).set_config_info(settings)
        self.mdb = process_manager.service(MongoConnection).database

        return StatusCode.Success

    def execute(self):
        """Execute the link.

        :returns: status code of execution
        :rtype: StatusCode
        """
        settings = process_manager.service(ConfigObject)
        ds = process_manager.service(DataStore)

        doc = ds.get(self.read_key, assert_type=(dict, list), assert_len=True)

        self.logger.debug('Started doing storage')
        etl_utils.dostorage(self.mdb, doc, self.store_collections, self.clear_first, self.logger, self.read_key)

        return StatusCode.Success
