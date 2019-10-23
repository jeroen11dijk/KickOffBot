"""Main module"""
from rlutilities.linear_algebra import *
from rlutilities.mechanics import Dodge, Drive
from rlutilities.simulation import Game
from rlbot.agents.base_agent import BaseAgent
from rlbot.agents.base_agent import SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from derevo.boost import init_boostpads, update_boostpads
from derevo.kick_off import init_kickoff, kick_off, Step


class Derevo(BaseAgent):
    """Main bot class"""

    def __init__(self, name, team, index):
        """Initializing all parameters of the bot"""
        super().__init__(name, team, index)
        Game.set_mode("soccar")
        self.game = Game(index, team)
        self.name = name
        self.team = team
        self.index = index
        self.drive = None
        self.dodge = None
        self.controls = SimpleControllerState()
        self.kickoff = False
        self.prev_kickoff = False
        self.kickoffStart = None
        self.step = None

    def initialize_agent(self):
        """Initializing all parameters which require the field info"""
        init_boostpads(self)
        self.drive = Drive(self.game.my_car)
        self.dodge = Dodge(self.game.my_car)

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        """The main method which receives the packets and outputs the controls"""
        self.game.read_game_information(packet, self.get_rigid_body_tick(), self.get_field_info())
        update_boostpads(self, packet)
        self.prev_kickoff = self.kickoff
        self.kickoff = packet.game_info.is_kickoff_pause and norm(vec2(self.game.ball.location - vec3(0, 0, 0))) < 100
        if self.kickoff and not self.prev_kickoff:
            init_kickoff(self)
            self.prev_kickoff = True
        elif self.kickoff or self.step is Step.Dodge_2:
            kick_off(self)
        else:
            self.drive.target = self.game.ball.location
            self.drive.speed = 1410
            self.drive.step(self.game.time_delta)
            self.controls = self.drive.controls
        if not packet.game_info.is_round_active:
            self.controls.steer = 0
        return self.controls
