import random

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.game_state_util import GameState, BallState, Physics, Vector3
from rlbot.utils.structures.game_data_struct import GameTickPacket

from NomBot.NomBot import NomBot_1_5
from derevo.derevo import Derevo


class MyBot(BaseAgent):

    def __init__(self, name, team, index):
        super().__init__(name, team, index)
        self.name = name
        self.team = team
        self.prev_kickoff = False
        self.timeout = 1000
        self.bot = Derevo(name, team, index)
        self.bot2 = NomBot_1_5(name, team, index)
        self.active = random.choice([self.bot, self.bot2])

    def initialize_agent(self):
        self.register_bot(self.bot)
        self.register_bot(self.bot2)

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        self.bot.get_rigid_body_tick = self.get_rigid_body_tick
        self.bot2.get_rigid_body_tick = self.get_rigid_body_tick
        if self.prev_kickoff and not packet.game_info.is_kickoff_pause:
            self.timeout = packet.game_info.seconds_elapsed + 2
        self.prev_kickoff = packet.game_info.is_kickoff_pause
        if packet.game_info.seconds_elapsed > self.timeout:
            if packet.game_ball.physics.location.y > 0:
                ball_state = BallState(Physics(location=Vector3(0, 5300, 100)))
            else:
                ball_state = BallState(Physics(location=Vector3(0, -5300, 100)))
            self.active = random.choice([self.bot, self.bot2])
            self.timeout = 1000
            self.set_game_state(GameState(ball=ball_state))
        return self.active.get_output(packet)

    def register_bot(self, bot):
        bot.get_ball_prediction_struct = self.get_ball_prediction_struct
        bot.get_field_info = self.get_field_info
        bot.renderer = self.renderer
        bot.send_quick_chat = self.send_quick_chat
        bot.initialize_agent()
