from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from derevo.derevo import Derevo
from NomBot.NomBot import NomBot_1_5


class MyBot(BaseAgent):

    def __init__(self, name, team, index):
        super().__init__(name, team, index)
        self.name = name
        self.team = team
        self.bot = Derevo(name, team, index)
        self.bot2 = NomBot_1_5(name, team, index)

    def initialize_agent(self):
        self.register_bot(self.bot)
        self.register_bot(self.bot2)
        print(self.bot2.get_ball_prediction_struct())

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        self.bot.get_rigid_body_tick = self.get_rigid_body_tick
        self.bot2.get_rigid_body_tick = self.get_rigid_body_tick
        # return self.bot.get_output(packet)
        return self.bot2.get_output(packet)

    def register_bot(self, bot):
        bot.get_ball_prediction_struct = self.get_ball_prediction_struct
        bot.get_field_info = self.get_field_info
        bot.renderer = self.renderer
        bot.send_quick_chat = self.send_quick_chat
        bot.initialize_agent()