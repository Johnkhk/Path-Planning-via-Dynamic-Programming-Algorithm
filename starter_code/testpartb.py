import pickle
from collections import defaultdict
from curses import has_key
from mimetypes import init
import numpy as np
import gym
from utils import *
from example import example_use_of_gym_env
import matplotlib.pyplot as plt
# from partb import *
file = open('part_b_optimal_paths.pkl', 'rb')
a = pickle.load(file)
env_folder = './envs/random_envs'
env, info, env_path = load_random_env(env_folder)
height = info["height"]
width = info["width"]
goal_pos = info["goal_pos"]
key_pos = info["key_pos"]
door_pos = info["door_pos"]
init_agent_pos = info["init_agent_pos"]
init_agent_dir = info["init_agent_dir"]
door_locations = [(4,2),(4,5)]

lock = tuple(not a for a in info["door_open"])
init_state = (3,5,(0,-1),tuple(info["key_pos"]),tuple(info["goal_pos"]),False,lock)

polidx=0
for i in range(len(a)):
    if a[i][0][1] == init_state:
        polidx=i

opt_seq=[]
# print(a[polidx])
for j in range(len(a[polidx])):
    tmp = a[polidx][j][0]
    opt_seq.append(tmp)
print(init_state)
print(opt_seq)

# draw gif
draw_gif_from_seq(opt_seq,env, "gif/"+"random_map2"+".gif")
