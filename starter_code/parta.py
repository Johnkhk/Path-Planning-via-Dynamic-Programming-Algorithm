from collections import defaultdict
from curses import has_key
from mimetypes import init
import numpy as np
import gym
from utils import *
from example import example_use_of_gym_env
import matplotlib.pyplot as plt

MF = 0 # Move Forward
TL = 1 # Turn Left
TR = 2 # Turn Right
PK = 3 # Pickup Key
UD = 4 # Unlock Door

def doorkey_problem(env, info , path):
    '''
    You are required to find the optimal path in
        doorkey-5x5-normal.env
        doorkey-6x6-normal.env
        doorkey-8x8-normal.env
        
        doorkey-6x6-direct.env
        doorkey-8x8-direct.env
        
        doorkey-6x6-shortcut.env
        doorkey-8x8-shortcut.env
        
    Feel Free to modify this fuction
    '''
    ### static variables ###
    height = info["height"]
    width = info["width"]
    goal_pos = info["goal_pos"]
    key_pos = info["key_pos"]
    door_pos = info["door_pos"]
    door = env.grid.get(info['door_pos'][0], info['door_pos'][1])
    is_open = door.is_open
    is_locked = door.is_locked
    init_agent_pos = info["init_agent_pos"]
    init_agent_dir = info["init_agent_dir"]
    init_state = (init_agent_pos[0],init_agent_pos[1],tuple(init_agent_dir), is_locked, env.carrying is not None)
    print("Initial State: ", init_state)

    states={}
    # print(dir(env.grid))
    num=1
    stateset=set()
    wallset=set()
    for col in range(width):
        for row in range(height):
            # pass
            cell = env.grid.get(col, row) # NoneType, Wall, Key, door
            if cell and (cell.type=="wall"):
                wallset.add((col,row))
                continue
            for ori in [(-1,0),(1,0),(0,1),(0,-1)]: # left right down up
                for door_locked in [True, False]:
                    for have_key in [True, False]:
                        # if cell and (cell.type=="goal"):
                        #     states[(col,row,ori,door_open,have_key)] = [0, 0]
                        #     continue
                        states[(col,row,ori,door_locked,have_key)] = [float("inf"), 0] # V, pi
                        stateset.add((col,row,ori,door_locked,have_key))
    
    # ### Build Motion Model ###
    def pf3(x,action):
        col,row,ori,door_locked,have_key = x

        if action == MF:
            if (col+ori[0],row+ori[1]) in wallset:
                return x
            if (col+ori[0],row+ori[1]) == tuple(door_pos) and door_locked:
                return x
            if col+ori[0]==goal_pos[0] and row+ori[1]==goal_pos[1]:
                # print("GOAL")
                return (col+ori[0],row+ori[1],ori,door_locked,have_key)
            # elif (col+ori[0],row+ori[1]) not in states:
                # return x
            # cost, done = step(env, MF) 
            return (col+ori[0],row+ori[1],ori,door_locked,have_key)
        elif action == TL:
            if ori == (0,-1): newori = (-1,0)
            elif ori == (-1,0): newori = (0,1)
            elif ori == (0,1): newori = (1,0)
            else: newori = 0,-1
            return (col,row,newori,door_locked,have_key)
        elif action == TR:
            if ori == (0,-1): newori = (1,0)
            elif ori == (-1,0): newori = (0,-1)
            elif ori == (0,1): newori = (-1,0)
            else: newori = 0,1
            return (col,row,newori,door_locked,have_key)
        elif action == PK:
            if col+ori[0]==key_pos[0] and row+ori[1]==key_pos[1]:
                return (col,row,ori,door_locked,True)
            return x
        elif action == UD:
            if col+ori[0]==door_pos[0] and row+ori[1]==door_pos[1] and have_key:
                return (col,row,ori,False,have_key)
            else:
                return x
            


    ### Dynamic Programming Algorithm ###
    N = len(states)
    T = N - 1
    X = states
    U = list(range(5))
    V = [{} for i in range(T+1)]

    ## initialize V, Q and Pi
    pi = [{} for i in range(T)]
    Q = [defaultdict(list) for i in range(T-1)]
    for t in range(T-1):
        for s in states.keys():
            if (s[0],s[1]) == tuple(goal_pos):
                continue
            # print("wot")
            V[t][s] = float("inf")
    for s in states.keys():
        if (s[0],s[1]) == tuple(goal_pos):
                continue
        V[-2][s] = 1
        pi[-1][s] = MF
    for t in range(len(V)):
        for s in states.keys():
            if (s[0],s[1]) == tuple(goal_pos):
                V[t][s] = 0

    ### main algorithm
    for t in reversed(range(T-1)):
        for s in states.keys():
            if (s[0],s[1]) == tuple(goal_pos):
                continue
            for j,u in enumerate(U):
                newx = pf3(s,u)
                Q[t][s].append(1 + V[t+1][newx])
            tmp = np.array(Q[t][s])
            V[t][s] = np.min(tmp)
            # if np.min(Q[t,i,:]) == np.max(Q[t,i,:]):
            #     pi[t,i] = np.nan
            #     continue
            pi[t][s] = np.argmin(tmp)
    

    optim_val = []
    optim_act_seq = []
    print(len(states))
    new_s = init_state 
    for t in range(T):
        if (new_s[0],new_s[1]) == tuple(goal_pos):
            # print(pi[t][new_s], new_s)
            # add
            # new_s = pf3(new_s, pi[t][new_s])
            print("GOAL!")
            break
        print(pi[t][new_s], new_s)
        optim_act_seq.append(pi[t][new_s])
        optim_val.append(V[t][new_s])
        new_s = pf3(new_s, pi[t][new_s])

    # draw sequence
    draw_gif_from_seq(optim_act_seq,env, "gif/"+path.split("/")[-1] +".gif")

    # plot value over time
    # plt.plot(list(range(1,len(optim_val)+1)),optim_val)
    plt.plot(optim_act_seq, optim_val,'r')
    plt.title("Optimal Value VS Optimal Policy " +path.split("/")[-1])
    plt.xlabel("Policy")
    plt.xlabel("Value")
    plt.show(block=True)

    





def partA():
    # env_path = './envs/example-8x8.env'
    # env_path = './envs/doorkey-5x5-normal.env'
    # env_path = './envs/doorkey-6x6-direct.env'
    # env_path = './envs/doorkey-6x6-normal.env'
    # env_path = './envs/doorkey-6x6-shortcut.env'
    # env_path = './envs/doorkey-8x8-direct.env'
    # env_path = './envs/doorkey-8x8-normal.env'
    env_path = './envs/doorkey-8x8-shortcut.env'





    # env_path = './envs/doorkey-8x8-shortcut.env'

    
    # env_path = './envs/doorkey-8x8-direct.env'
    env, info = load_env(env_path) # load an environment
    seq = doorkey_problem(env, info, env_path) # find the optimal action sequence
    # draw_gif_from_seq(seq, load_env(env_path)[0]) # draw a GIF & save
    
def partB():
    env_folder = './envs/random_envs'
    env, info, env_path = load_random_env(env_folder)

if __name__ == '__main__':
    # example_use_of_gym_env()
    partA()
    #partB()

    
