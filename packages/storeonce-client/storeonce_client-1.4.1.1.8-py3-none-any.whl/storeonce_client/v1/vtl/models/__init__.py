# coding: utf-8

# flake8: noqa
"""
    (C) Copyright 2018-2019 Hewlett Packard Enterprise Development LP

    VTL

    unused  # noqa: E501

    Component version: 3.1.8-SNAPSHOT
"""


from __future__ import absolute_import

# import models into model package
from storeonce_client.v1.vtl.models.barcode_template import BarcodeTemplate
from storeonce_client.v1.vtl.models.batch_barcode_action import BatchBarcodeAction
from storeonce_client.v1.vtl.models.cartridge import Cartridge
from storeonce_client.v1.vtl.models.cartridge_get_model_collection import CartridgeGetModelCollection
from storeonce_client.v1.vtl.models.create_library_port import CreateLibraryPort
from storeonce_client.v1.vtl.models.create_vtl_barcode_template import CreateVtlBarcodeTemplate
from storeonce_client.v1.vtl.models.create_vtl_cartridge import CreateVtlCartridge
from storeonce_client.v1.vtl.models.create_vtl_cartridge_in_empty_slot import CreateVtlCartridgeInEmptySlot
from storeonce_client.v1.vtl.models.create_vtl_library import CreateVtlLibrary
from storeonce_client.v1.vtl.models.create_vtl_protocol import CreateVtlProtocol
from storeonce_client.v1.vtl.models.drive import Drive
from storeonce_client.v1.vtl.models.drive_cartridge_get_model import DriveCartridgeGetModel
from storeonce_client.v1.vtl.models.drive_get_model_collection import DriveGetModelCollection
from storeonce_client.v1.vtl.models.extended_error import ExtendedError
from storeonce_client.v1.vtl.models.external_docs import ExternalDocs
from storeonce_client.v1.vtl.models.fibre_channel_properties import FibreChannelProperties
from storeonce_client.v1.vtl.models.iscsi_properties import ISCSIProperties
from storeonce_client.v1.vtl.models.l10n_string_struct import L10nStringStruct
from storeonce_client.v1.vtl.models.library import Library
from storeonce_client.v1.vtl.models.library_get_model_collection import LibraryGetModelCollection
from storeonce_client.v1.vtl.models.library_replication import LibraryReplication
from storeonce_client.v1.vtl.models.library_storage_parametrics import LibraryStorageParametrics
from storeonce_client.v1.vtl.models.library_storage_parametrics_collection import LibraryStorageParametricsCollection
from storeonce_client.v1.vtl.models.library_throughput_parametrics import LibraryThroughputParametrics
from storeonce_client.v1.vtl.models.library_throughput_parametrics_collection import LibraryThroughputParametricsCollection
from storeonce_client.v1.vtl.models.mail_slot import MailSlot
from storeonce_client.v1.vtl.models.mail_slot_get_model_collection import MailSlotGetModelCollection
from storeonce_client.v1.vtl.models.message_info import MessageInfo
from storeonce_client.v1.vtl.models.model_property import ModelProperty
from storeonce_client.v1.vtl.models.modify_barcode_template import ModifyBarcodeTemplate
from storeonce_client.v1.vtl.models.modify_library_drive import ModifyLibraryDrive
from storeonce_client.v1.vtl.models.modify_vtl_cartridge import ModifyVtlCartridge
from storeonce_client.v1.vtl.models.modify_vtl_drive import ModifyVtlDrive
from storeonce_client.v1.vtl.models.modify_vtl_library import ModifyVtlLibrary
from storeonce_client.v1.vtl.models.modify_vtl_port import ModifyVtlPort
from storeonce_client.v1.vtl.models.modify_vtl_protocol import ModifyVtlProtocol
from storeonce_client.v1.vtl.models.port import Port
from storeonce_client.v1.vtl.models.protocol import Protocol
from storeonce_client.v1.vtl.models.replication import Replication
from storeonce_client.v1.vtl.models.replication_mapping import ReplicationMapping
from storeonce_client.v1.vtl.models.service import Service
from storeonce_client.v1.vtl.models.slot import Slot
from storeonce_client.v1.vtl.models.slot_get_model_collection import SlotGetModelCollection
from storeonce_client.v1.vtl.models.xml import Xml
