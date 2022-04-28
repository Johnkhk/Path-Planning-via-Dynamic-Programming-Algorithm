from collections import defaultdict
from curses import has_key
import numpy as np
import gym
from utils import *
from example import example_use_of_gym_env
import pickle
import time

start_time=time.time()
MF = 0 # Move Forward
TL = 1 # Turn Left
TR = 2 # Turn Right
PK = 3 # Pickup Key
UD = 4 # Unlock Door
orientations = [(-1,0),(1,0),(0,1),(0,-1)]
key_locations = [(1, 1), (2, 3), (1, 6)]
goal_locations = [(5, 1), (6, 3), (5, 6)]
door_locations = [(4,2),(4,5)]
lock_configs = [(True, True),(True,False),(False,True), (False, False)] #door1, door2
agent_init_pos = (3,5)
agent_init_dir = (0,-1)

agent_pos = agent_init_pos
agent_dir = agent_init_dir

### load env



### create state space

# create walls
wallset=set()
for col in range(8):
    wallset.add((col,0))
    wallset.add((col,7))
for row in range(8):
    wallset.add((0,row))
    wallset.add((7,row))
for i in range(8):
    if i == 2 or i==5:
        continue
    wallset.add((4,i))
print("WALLSET Created: ")
print(len(wallset))

# create states
X=[]
for col in range(8):
    for row in range(8):
        if (col,row) in wallset:
            continue
        for ori in orientations:
            for have_key in [True, False]:
                for key_pos in key_locations:
                    for goal_pos in goal_locations:
                        for lock_config in lock_configs:
                            X.append((col,row,ori,key_pos,goal_pos,have_key,lock_config))
print("STATES CREATED")

#create initial states
init_states = []
for key_pos in key_locations:
    for goal_pos in goal_locations:
        for lock_config in lock_configs:
            init_states.append((3,5,(0,-1),key_pos,goal_pos,False,lock_config))
print("INITIAL STATES CREATED ", len(init_states))

# motion model check motion model
def pf4(x,action):
    col,row,ori,key_pos,goal_pos,have_key,lock_config = x

    if action == MF:
        # if env.grid.get(env.front_pos[0],env.front_pos[1]).type == "wall":
            # return x
        if (col+ori[0],row+ori[1]) in wallset:
            return x
        if ((col+ori[0],row+ori[1]) == door_locations[0]) and lock_config[0]==True:
            return x
        if ((col+ori[0],row+ori[1]) == door_locations[1]) and lock_config[1]==True:
            return x
        if col+ori[0]==goal_pos[0] and row+ori[1]==goal_pos[1]:
            # print("GOAL")
            return (col+ori[0],row+ori[1],ori,key_pos,goal_pos,have_key,lock_config)
            # return x
        return (col+ori[0],row+ori[1],ori,key_pos,goal_pos,have_key,lock_config)
    elif action == TL:
        if ori == (0,-1): newori = (-1,0)
        elif ori == (-1,0): newori = (0,1)
        elif ori == (0,1): newori = (1,0)
        else: newori = 0,-1
        return (col,row,newori,key_pos,goal_pos,have_key,lock_config)
    elif action == TR:
        if ori == (0,-1): newori = (1,0)
        elif ori == (-1,0): newori = (0,-1)
        elif ori == (0,1): newori = (-1,0)
        else: newori = 0,1
        return (col,row,newori,key_pos,goal_pos,have_key,lock_config)

    elif action == PK:
        if col+ori[0]==key_pos[0] and row+ori[1]==key_pos[1]:
            return (col,row,ori,key_pos,goal_pos,True,lock_config)
        return x
    elif action == UD:
        if (col+ori[0],row+ori[1]) == door_locations[0] and have_key:
            return (col,row,ori,key_pos,goal_pos,True,(False,lock_config[1]))
        elif (col+ori[0],row+ori[1]) == door_locations[1] and have_key:
            return (col,row,ori,key_pos,goal_pos,True,(lock_config[0],False))
        else:
            return x

### 
#{doorcoord, lockstatus}

# ### Dynamic Programming Algorithm ###
N = len(X)
T = N - 1
# X = states
U = list(range(5))
V = [{} for i in range(T+1)]

# ## initialize V, Q and Pi HERERERERERERERERERE goal_pos
# pi = [{} for i in range(T)]
# Q = [defaultdict(list) for i in range(T-1)]
# for t in range(T-1):
#     for s in X:
#         if (s[0],s[1]) == tuple(goal_pos):
#             continue
#         # print("wot")
#         V[t][s] = float("inf")
# for s in X:
#     if (s[0],s[1]) == tuple(goal_pos):
#             continue
#     V[-2][s] = 1
#     pi[-1][s] = MF
# for t in range(len(V)):
#     for s in X:
#         if (s[0],s[1]) == tuple(goal_pos):
#             V[t][s] = 0
# print("DPA VARIABLES INIITIALIZED")
## initialize V, Q and Pi HERERERERERERERERERE goal_pos
pi = [{} for i in range(T)]
Q = [defaultdict(list) for i in range(T-1)]
for t in range(T-1):
    for s in X:
        if (s[0],s[1]) == s[4]:
            continue
        # print("wot")
        V[t][s] = float("inf")
for s in X:
    if (s[0],s[1]) == s[4]:
        continue
    V[-2][s] = 1
    pi[-1][s] = MF
for t in range(len(V)):
    for s in X:
        if (s[0],s[1]) == s[4]:
            V[t][s] = 0
print("DPA VARIABLES INIITIALIZED")
            
### main algorithm
finalpolicies=[]
print(T-1)
for t in reversed(range(T-1)):
    print(t)
    cor = 0
    for s in X:
        if (s[0],s[1]) == s[4]:
        # if (s[0],s[1]) == tuple(goal_pos):
        # if (s[0],s[1]) == tuple(goal_locations[0]) or (s[0],s[1]) == tuple(goal_locations[1]) or (s[0],s[1]) == tuple(goal_locations[2]):
            continue

        for j,u in enumerate(U):
            newx = pf4(s,u)
            Q[t][s].append(1 + V[t+1][newx])
        tmp = np.array(Q[t][s])
        V[t][s] = np.min(tmp)
        pi[t][s] = np.argmin(tmp)
        # early stop
        if V[t][s] == V[t+1][s]:
            cor+=1
    if cor == len(V[t+1]):
        print("EARLY STOP")
        break
    # if V[t] == V[t+1]:
        # print("earlystop")
        # break
# with open('pi_partb3.pkl', 'wb') as f:
    # pickle.dump(pi, f)
print("DPA DONE")
print(time.time()-start_time)


# print(len(states))
# new_s = init_states
directions=[[] for i in init_states]
for i,new_s in enumerate(init_states):
    print("state i:", i)
    for t in range(T):
        if (new_s[0],new_s[1]) == tuple(new_s[4]):
            # print(pi[t][new_s], new_s)
            # directions[i].append((pi[t][new_s], new_s))
            # new_s = pf4(new_s, pi[t][new_s])
            print("GOAL!")
            break
        # print(pi[t][new_s], new_s)
        directions[i].append((pi[t][new_s], new_s))
        new_s = pf4(new_s, pi[t][new_s])
    print("newstate")
with open('partb_policies2.pkl', 'wb') as f:
    pickle.dump(directions, f)

print(time.time()-start_time)

# file = open('pi_partb.pkl', 'rb')
# a = pickle.load(file)
# print(len(a))





## AXIS
"""
graph for
axis policy, value
"""


# file = open('partb_policies.pkl', 'rb')
# a = pickle.load(file)
# # print(a[0][0][1])
# # for i in a[0]:
#     # print(i[0],i[1])


# init = (2, 4, (-1, 0), (1, 6), (6, 3), True, (False, True))
# new_s = init
# pi = a
# file = open('pi_partb.pkl', 'rb')
# a = pickle.load(file)
# for t in range(9194,len(a)):
#     # a[i][init]
#     if (new_s[0],new_s[1]) == tuple(new_s[4]):
#         # print(pi[t][new_s], new_s)
#         # directions[i].append((pi[t][new_s], new_s))
#         # new_s = pf4(new_s, pi[t][new_s])
#         print("GOAL!")
#         break
#     print(pi[t][new_s], new_s)
#     new_s = pf4(new_s, pi[t][new_s])