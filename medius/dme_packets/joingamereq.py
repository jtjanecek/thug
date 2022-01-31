from utils.utils import *

'''
This packet is sent to others when they join the game.

This packet is received when first joining a game, and they send it to us
'''

class JoinGameReqSerializer:
    data_dict = [
        {'name': 'dme_id', 'n_bytes': 2, 'cast': None},
        {'name': 'unk1', 'n_bytes': 4, 'cast': bytes_to_int_little},
        {'name': 'unk2', 'n_bytes': 4, 'cast': bytes_to_int_little},
        {'name': 'unk4', 'n_bytes': 4, 'cast': None}, # C0A84400C0A84400C0A84400C0A8440000AF430000AF430000AF430000AF430000000000000000424242424242424242424242424200414242424242424242424242427E3200004242424200000000
    ]

    def serialize(self, data: bytearray):
        return dme_serialize(data, self.data_dict, __name__)

    @classmethod
    def build(self, player_id, message_type=2):
        packet = [
            {'name': __name__},
            {'dme_id': b'\x02\x10'},
            {'src_player_id?': int_to_bytes_little(4, player_id)},
            {'message_type': int_to_bytes_little(4, message_type)},
            {'unk': hex_to_bytes('00C0A84400C0A84400C0A84400C0A8440000AF430000AF430000AF430000AF430000000000000000424242424242424242424242424200414242424242424242424242427E3200004242424200000000')} # stats, username, clan tag
        ]
        return packet
