"""Module with all the utility methods"""
import math

from rlutilities.linear_algebra import vec2, norm


def distance_2d(vec_a, vec_b):
    """returns 2d distance between two vectors"""
    return norm(vec2(vec_a - vec_b))


def get_closest_small_pad(agent, location):
    """Gets the small boostpad closest to the bot"""
    pads = agent.small_boost_pads
    closest_pad = None
    distance = math.inf
    for pad in pads:
        if distance_2d(location, pad.location) < distance:
            distance = distance_2d(agent.game.my_car.location, pad.location)
            closest_pad = pad
    return closest_pad


def sign(num):
    """Returns 1 if the number is bigger then 0 otherwise it returns -1"""
    if num <= 0:
        return -1
    return 1


def lerp(a, b, t):
    return a + (b - a) * t
