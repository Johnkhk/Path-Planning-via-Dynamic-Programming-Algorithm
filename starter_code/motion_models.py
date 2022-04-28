import numpy as np
import gym
from utils import *
MF = 0 # Move Forward
TL = 1 # Turn Left
TR = 2 # Turn Right
PK = 3 # Pickup Key
UD = 4 # Unlock Door

def pf1(state, action):
        """
        MF = 0 # Move Forward
        TL = 1 # Turn Left
        TR = 2 # Turn Right
        PK = 3 # Pickup Key
        UD = 4 # Unlock Door
        """
        i,j,ori,door_open,have_key = state
        print("state"*20,state)
        if action == MF:
            ### return self if front is wall
            if env.grid.get(env.front_pos[0],env.front_pos[1]).type == "wall":
                return state
            ### return self if in front is a door and no key
            if env.grid.get(env.front_pos[0],env.front_pos[1]).type == "door":
                return state
            if ori == 0: #up
                return (i-1,j,ori,door_open,have_key)
            elif ori == 1: #left
                return (i+1,j,ori,door_open,have_key)
            elif ori == 2: #down
                return (i,j-1,ori,door_open,have_key)
            elif ori == 3: #right
                return (i,j+1,ori,door_open,have_key)
        elif action == TL:
            return (i,j,(ori+1)%4,door_open,have_key)
        elif action == TR:
            return (i,j,(ori-1+4)%4,door_open,have_key)
        elif action == PK:
            if env.front_pos == key_pos and not have_key:
                return (i,j,(ori-1+4)%4,door_open,True)
            else:
                return (i,j,(ori-1+4)%4,door_open, False)
        elif action == UD:
            if env.front_pos == door_pos and have_key:
                return (i,j,ori,True,True)
            else:
                return state
        else:
            print("BRO WHATTTTTT"*20)
            return state



# motion model
def pf2(x,action, info):
    height = info["height"]
    width = info["width"]
    goal_pos = info["goal_pos"]
    key_pos = info["key_pos"]
    door_pos = info["door_pos"]
    init_agent_pos = info["init_agent_pos"]
    init_agent_dir = info["init_agent_dir"]

    col,row,ori,key_pos,goal_pos,lock_config = x

    if action == MF:
        if col+ori[0] == 
        state =  (col+ori[0],row+ori[1],ori,key_pos,goal_pos,lock_config)
    elif action == TL:
        if ori == (0,-1): newori = (-1,0)
        elif ori == (-1,0): newori = (0,1)
        elif ori == (0,1): newori = (1,0)
        else: newori = 0,-1
        state = (col,row,newori,key_pos,goal_pos,lock_config)
    elif action == TR:
        if ori == (0,-1): newori = (1,0)
        elif ori == (-1,0): newori = (0,-1)
        elif ori == (0,1): newori = (-1,0)
        else: newori = 0,1
        state = (col,row,newori,key_pos,goal_pos,lock_config)
    elif action == PK:
        has_key_flag = True
        state = (col,row,ori,key_pos,goal_pos,lock_config)
    elif action == UD:
        for i,door_pos in enumerate(door_locations):
            if has_key_flag and agent_pos + agent_dir == door_pos:
                lock_config[i] = True
            state = (col,row,ori,key_pos,goal_pos,lock_config)
    return state


# (col,row,ori,door_open,have_key)

# motion model
def pf3(x,action):
    col,row,ori,door_open,have_key = x

    if action == MF:
        if env.grid.get(env.front_pos[0],env.front_pos[1]).type == "wall":
            return x
        cost, done = step(env, MF) 
        state =  (col+ori[0],row+ori[1],ori,door_open,have_key)
    elif action == TL:
        if ori == (0,-1): newori = (-1,0)
        elif ori == (-1,0): newori = (0,1)
        elif ori == (0,1): newori = (1,0)
        else: newori = 0,-1
        state = (col,row,newori,door_open,have_key)
    elif action == TR:
        if ori == (0,-1): newori = (1,0)
        elif ori == (-1,0): newori = (0,-1)
        elif ori == (0,1): newori = (-1,0)
        else: newori = 0,1
        state = (col,row,newori,key_pos,goal_pos,lock_config)
    elif action == PK:
        has_key_flag = True
        state = (col,row,ori,key_pos,goal_pos,lock_config)
    elif action == UD:
        for i,door_pos in enumerate(door_locations):
            if has_key_flag and agent_pos + agent_dir == door_pos:
                lock_config[i] = True
            state = (col,row,ori,key_pos,goal_pos,lock_config)
    return state
            

            
    ### build state space ###
    states = []
    # statemap={}
    # states={}
    # print(dir(env.grid))
    num=0
    for i in range(width):
        for j in range(height):
            # pass
            cell = env.grid.get(i, j) # NoneType, Wall, Key, door
            if cell and (cell.type=="wall" or cell.type=="goal"):
                continue
            for ori in [0,1,2,3]: # up left down right
                for door_open in [True, False]:
                    for have_key in [True, False]:
                        # states[(i,j)].append((i,j,ori,door_open,have_key))
                        # states.append((i,j,ori,door_open,have_key, num)) # num is stateidx
                        states.append((i,j,ori,door_open,have_key)) # num is stateidx
                        # statemap[(i,j,ori,door_open,have_key)] = num
                        num+=1
    # N = len(states*16)
    # states[(goal_pos[0],goal_pos[1])].append("goal")
    states.append((goal_pos[0],goal_pos[1],"goal"))
    N = len(states)
    print(states[-1], N)

     # algorithm start
    # for i,x in enumerate(states):
    #     if (X[i][0],X[i][1]) ==  (door_pos[0], door_pos[1]):
    #         V[T][i]=float("inf")
    #     else:
    #         V[T][i]=0
    # for i,x in enumerate(states):
    #     if (X[i][0],X[i][1]) ==  (door_pos[0], door_pos[1]):
    #         V[T][i]=float("inf")
    #     else:
    #         V[T][i]=0