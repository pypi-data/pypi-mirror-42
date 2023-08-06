#!/usr/bin/env python3

from gv_services.proto.common_pb2 import ack
from gv_services.storage.dbstorage.dbstorage import DbStorage


class Geographer:

    # TODO: uncomment dbstorage

    def __init__(self, logger):
        super().__init__()
        self.logger = logger
        # self.dbstorage = DbStorage()
        self.network = None

    async def async_init(self):
        # await self.dbstorage.async_init()
        pass

    async def import_shapefile_to_db(self, stream):
        await stream.send_message(ack(success=True))

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
