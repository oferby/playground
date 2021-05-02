# https://github.com/deepmind/dm_alchemy
import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import dm_alchemy
from dm_alchemy import io
from dm_alchemy import symbolic_alchemy
from dm_alchemy import symbolic_alchemy_bots
from dm_alchemy import symbolic_alchemy_trackers
from dm_alchemy import symbolic_alchemy_wrapper
from dm_alchemy.encode import chemistries_proto_conversion
from dm_alchemy.encode import symbolic_actions_proto_conversion
from dm_alchemy.encode import symbolic_actions_pb2
from dm_alchemy.types import stones_and_potions
from dm_alchemy.types import unity_python_conversion
from dm_alchemy.types import utils

width, height = 240, 200
level_name = 'alchemy/perceptual_mapping_randomized_with_rotation_and_random_bottleneck'
seed = 1023
settings = dm_alchemy.EnvironmentSettings(
    seed=seed, level_name=level_name, width=width, height=height)
env = dm_alchemy.load_from_docker(settings)
