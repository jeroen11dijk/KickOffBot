from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from derevo.derevo import Derevo

bots = ["derevo"]


class MyBot(BaseAgent):

    def __init__(self, name, team, index):
        super().__init__(name, team, index)
        self.name = name
        self.team = team
        self.bot = Derevo(name, team, index)

    def initialize_agent(self):
        self.bot.get_ball_prediction_struct = self.bot.get_ball_prediction_struct
        self.bot.get_field_info = self.get_field_info
        self.bot.renderer = self.renderer
        self.bot.send_quick_chat = self.send_quick_chat
        self.bot.initialize_agent()

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        self.bot.get_rigid_body_tick = self.get_rigid_body_tick
        return self.bot.get_output(packet)
