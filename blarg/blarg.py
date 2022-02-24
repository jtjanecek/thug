import asyncio
import websockets
import json
import os

import sys
sys.path.append("..")

import logging
from logging import handlers

from collections import deque

from medius.dme_serializer import TcpSerializer as tcp_map
from medius.dme_serializer import UdpSerializer as udp_map

from utils.utils import *

class Blarg:
    def __init__(self, config: dict):
        self._config = config

        self._logger = logging.getLogger('blarg')
        self._logger.setLevel(logging.getLevelName(config['logger']))
        formatter = logging.Formatter('%(asctime)s %(name)s | %(levelname)s | %(message)s')
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        sh.setLevel(logging.getLevelName(config['logger']))
        self._logger.addHandler(sh)

        filehandler = logging.FileHandler(os.path.join(os.path.dirname(os.path.realpath(__file__)),'logs','blarg.log'), mode='w')
        filehandler.setFormatter(formatter)
        filehandler.setLevel(logging.DEBUG)
        self._logger.addHandler(filehandler)
        self._logger.setLevel(logging.getLevelName(config['logger']))

    def run(self):
        asyncio.get_event_loop().run_until_complete(self.read_websocket())

    def process(self, packet: dict):
        '''
        Process json from Robo's websocket.
        Structure:
        {
            "type": udp/tcp
            "dme_world_id": int
            "src": the source player dme id
            "dst": the destination player dme id, -1 for sending to all
            "data": a hex string of the raw data
        }
        '''

        # Convert to list. E.g. '000102030405' -> ['00', '01', '02', '03', '04', '05']
        data = deque([packet['data'][i:i+2] for i in range(0,len(packet['data']),2)])

        '''
        There may be multiple messages in each message.
        So we have to read the current message, and see if there's any leftover
        data which would be another message
        '''
        # Keep reading until data is empty
        while len(data) != 0:
            packet_id = data.popleft() + data.popleft() # E.g. '0201'

            # if self._config['filter'] == packet_id:
            #     d = packet_id + ''.join(list(data))
            #     self._logger.info(f"{packet['type']} | {d} | {d[14:22]} | {bytes_to_int_little(hex_to_bytes(d[14:22]))}")

            # Check if the packet_id exists. If it does, serialize it
            if packet['type'] == 'tcp':
                if packet_id not in tcp_map.keys():
                    if self._config['warn_on_unknown'] == 'True':
                        self._logger.warning(f"Unknown {packet['type']} packet id: {packet_id} | data: {packet['data']}")
                    break
                else:
                    serialized = tcp_map[packet_id].serialize(data)

                self._logger.info(f"{packet['src']} | {serialized}")

            elif packet['type'] == 'udp':
                if packet_id not in udp_map.keys():
                    if self._config['warn_on_unknown'] == 'True':
                        self._logger.warning(f"Unknown {packet['type']} packet id: {packet_id} | data: {packet['data']}")
                    break
                else:
                    serialized = udp_map[packet_id].serialize(data)

                self._logger.info(f"{packet['src']} | {serialized}")

            # Don't print correctly serialized unless it matches filter or the filter is empty.
            #if (self._config['filter'] == packet_id or self._config['filter'] == '') and serialized != {} and self._config['log_serialized'] != 'False':

    async def read_websocket(self):
        uri = f"ws://{self._config['robo_ip']}:8765"
        async with websockets.connect(uri) as websocket:
            while True:
                data = await websocket.recv()
                self._logger.debug(f"{data}")
                self.process(json.loads(data))


def read_config(config_file='config.json'):
    with open(config_file, 'r') as f:
        return json.loads(f.read())

if __name__ == '__main__':
    config = read_config()

    blarg = Blarg(config)
    blarg.run()