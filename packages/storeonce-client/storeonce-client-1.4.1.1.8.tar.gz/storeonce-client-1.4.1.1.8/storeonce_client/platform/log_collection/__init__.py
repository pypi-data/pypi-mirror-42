# coding: utf-8

# flake8: noqa

"""
    (C) Copyright 2018-2019 Hewlett Packard Enterprise Development LP

    Log Collection

    View and manage log collections for support tickets  # noqa: E501

    Component version: 1.18-SNAPSHOT
"""


from __future__ import absolute_import

# import apis into sdk package
from storeonce_client.platform.log_collection.api.log_collection__support_ticket_api import LogCollectionSupportTicketApi

# import ApiClient
from .api_client import ApiClient
from storeonce_client.configuration import Configuration
# import models into sdk package
from storeonce_client.platform.log_collection.models.log_collection_list import LogCollectionList
from storeonce_client.platform.log_collection.models.log_collection_model import LogCollectionModel
