from collections import deque
from utils.utils import *
import os

from constants.constants import WEAPON_MAP

subtype_map = {
    '10401F00': '?_crate_destroyed',
    '41401F00': 'weapon_pickup',
    '00401F00': 'crate_destroyed',
    '02401F00': 'crate_respawn',
    '00000000': 'crate_destroyed_and_pickup',
    '10000000': '?_crate_destroyed_and_pickup',
    '40401F00': 'object_update',
    '21000000': 'flag_update',
    '02411F00': 'flag_drop',
}

class tcp_020C_info:
    def __init__(self, subtype:str=None,
                       timestamp:int=None,
                       object_id:str=None,
                       data:dict=None
                       ):

        self.name = os.path.basename(__file__).strip(".py")
        self.id = b'\x02\x0C'
        self.subtype = subtype
        self.timestamp = timestamp
        self.object_id = object_id
        self.data = data


    @classmethod
    def serialize(self, data: deque):
        print(''.join(list(data)))
        subtype = ''.join([data.popleft() for i in range(4)])
        subtype = subtype_map[subtype]
        timestamp = hex_to_int_little(''.join([data.popleft() for i in range(4)]))
        object_id = ''.join([data.popleft() for i in range(4)])

        data_dict = {}


        if subtype in ['?_crate_destroyed_and_pickup', '?_crate_destroyed']:
            data_dict['weapon_spawned'] = WEAPON_MAP[data.popleft()]
        elif subtype == 'weapon_pickup':
            data_dict['weapon_pickup_unk'] =  ''.join([data.popleft() for i in range(4)])
        elif subtype == 'object_update':
            data_dict['object_update_unk'] =  ''.join([data.popleft() for i in range(4)])
        elif subtype == 'flag_update':
            data_dict['flag_update_type'] =  ''.join([data.popleft() for i in range(2)])
        elif subtype == 'flag_drop':
            data_dict['flag_drop_unk'] =  ''.join([data.popleft() for i in range(16)])
        return tcp_020C_info(subtype, timestamp, object_id, data_dict)

    # def to_bytes(self):
    #     return self.id + \
    #         int_to_bytes_little(4, self.type) + \
    #         int_to_bytes_little(4, self.account_id) + \
    #         hex_to_bytes(self.rank) + \
    #         hex_to_bytes(self.unk1) + \
    #         hex_to_bytes({v: k for k, v in SKIN_MAP.items()}[self.skin1] + '00') + \
    #         hex_to_bytes({v: k for k, v in SKIN_MAP.items()}[self.skin2] + '00') + \
    #         str_to_bytes(self.username, 14) + \
    #         hex_to_bytes(self.unk2) + \
    #         str_to_bytes(self.username2, 12) + \
    #         hex_to_bytes(self.unk3) + \
    #         str_to_bytes(self.clan_tag, 4) + \
    #         hex_to_bytes(self.unk4)

    def __str__(self):
        return f"{self.name}; subtype:{self.subtype} " + \
                f"timestamp:{self.timestamp} object_id:{self.object_id} data:{self.data}"
