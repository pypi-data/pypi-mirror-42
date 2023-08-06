#!/usr/bin/env python3

import asyncio
import os

from gv_services.proto.common_pb2 import ack
from gv_services.storage.dbstorage.dbstorage import DbStorage
from gv_services.settings import SHAPEFILE_NAME


class Geographer:

    # TODO: uncomment dbstorage

    def __init__(self, logger, basecartopath, *dbcredentials):
        super().__init__()
        self.logger = logger
        self.basecartopath = basecartopath
        self.dbstorage = DbStorage(*dbcredentials)

    async def async_init(self):
        await self.dbstorage.async_init()

    async def import_shapefile_to_db(self, stream):
        await asyncio.gather(stream.send_message(ack(success=True)),
                             self.dbstorage.import_shapefile(os.path.join(self.basecartopath, SHAPEFILE_NAME)))

    async def get_data_points(self, stream):
        pass

    async def get_roads(self, stream):
        pass

    async def get_zones(self, stream):
        pass

    async def get_mapping_roads_data_points(self, stream):
        pass

    async def get_mapping_zones_roads(self, stream):
        pass

    async def update_roads_freeflow_speed(self, stream):
        pass

    async def update_zones_freeflow_speed(self, stream):
        pass
