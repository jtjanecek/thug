
from model.states.state import State
from butils.utils import *
from medius.dme_packets import *

class static_shoot_initial(State):
    def __init__(self, state_machine):
        super().__init__(state_machine)

    def enter(self, msg:dict):
        self.starting_coord = [27205, 54135, 7418] # Marc by flag drop
        self.target = self.state_machine.game_state.players[0].coord


    def update(self):
        self.target = self.state_machine.game_state.players[0].coord
        self.state_machine.game_state.player.coord = self.starting_coord
        self.state_machine.update_joystick_input_and_angle(self.state_machine.game_state.player.coord, self.state_machine.game_state.player.coord)

        target_local = self.state_machine.game_state.map.transform_global_to_local(self.target)
        print(target_local)
        unk1 = "00"
        unk2 = bytes_to_hex(int_to_bytes_little(1, int((target_local[0] - int(target_local[0]))*255))) + bytes_to_hex(int_to_bytes_little(2, int(target_local[0])))
        unk3 = "00"
        unk4 = bytes_to_hex(int_to_bytes_little(1, int((target_local[1] - int(target_local[1]))*255))) + bytes_to_hex(int_to_bytes_little(2, int(target_local[1])))
        unk5 = "00"
        unk6 = bytes_to_hex(int_to_bytes_little(1, int((target_local[2] - int(target_local[2]))*255))) + bytes_to_hex(int_to_bytes_little(2, int(target_local[2])))

        unk = unk1+unk2+unk3+unk4+unk5+unk6 + "00000000"

        print(len(unk)/2)

        self.state_machine.model.dmetcp_queue.put(['B', tcp_020C_info.tcp_020C_info(subtype=f'p1_flag_drop', object_type='131000F7',timestamp=self.state_machine.game_state.player.time,data={'flag_drop_unk': unk})])
