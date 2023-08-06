# coding: utf-8

# flake8: noqa

"""
    (C) Copyright 2018-2019 Hewlett Packard Enterprise Development LP

    Licensing

    unused  # noqa: E501

    Component version: 6.0.31-SNAPSHOT
"""


from __future__ import absolute_import

# import apis into sdk package
from storeonce_client.v1.licensing.api.floating_license_resource_api import FloatingLicenseResourceApi
from storeonce_client.v1.licensing.api.license_category_status_resource_api import LicenseCategoryStatusResourceApi
from storeonce_client.v1.licensing.api.licensing_root_resource_api import LicensingRootResourceApi
from storeonce_client.v1.licensing.api.seat_license_resource_api import SeatLicenseResourceApi
from storeonce_client.v1.licensing.api.server_installed_licenses_resource_api import ServerInstalledLicensesResourceApi
from storeonce_client.v1.licensing.api.server_config_api import ServerConfigApi
from storeonce_client.v1.licensing.api.system_mode_selection_and_activation_api import SystemModeSelectionAndActivationApi

# import ApiClient
from .api_client import ApiClient
from storeonce_client.configuration import Configuration
# import models into sdk package
from storeonce_client.v1.licensing.models.action_status import ActionStatus
from storeonce_client.v1.licensing.models.cloud_archive_availablility import CloudArchiveAvailablility
from storeonce_client.v1.licensing.models.cloud_archive_reservation import CloudArchiveReservation
from storeonce_client.v1.licensing.models.cloud_archive_reservation_status import CloudArchiveReservationStatus
from storeonce_client.v1.licensing.models.extended_error import ExtendedError
from storeonce_client.v1.licensing.models.extended_info import ExtendedInfo
from storeonce_client.v1.licensing.models.external_docs import ExternalDocs
from storeonce_client.v1.licensing.models.input_stream import InputStream
from storeonce_client.v1.licensing.models.license_collection_wrapper import LicenseCollectionWrapper
from storeonce_client.v1.licensing.models.license_feature import LicenseFeature
from storeonce_client.v1.licensing.models.license_feature_collection_wrapper import LicenseFeatureCollectionWrapper
from storeonce_client.v1.licensing.models.license_server_config import LicenseServerConfig
from storeonce_client.v1.licensing.models.message_info import MessageInfo
from storeonce_client.v1.licensing.models.message_info_ex import MessageInfoEx
from storeonce_client.v1.licensing.models.message_info_ex_impl import MessageInfoExImpl
from storeonce_client.v1.licensing.models.model_property import ModelProperty
from storeonce_client.v1.licensing.models.reservation_collection_wrapper import ReservationCollectionWrapper
from storeonce_client.v1.licensing.models.status import Status
from storeonce_client.v1.licensing.models.status_collection_wrapper import StatusCollectionWrapper
from storeonce_client.v1.licensing.models.storeonce_license import StoreonceLicense
from storeonce_client.v1.licensing.models.storeonce_license_server import StoreonceLicenseServer
from storeonce_client.v1.licensing.models.summary import Summary
from storeonce_client.v1.licensing.models.system_license_mode import SystemLicenseMode
from storeonce_client.v1.licensing.models.task import Task
from storeonce_client.v1.licensing.models.xml import Xml
