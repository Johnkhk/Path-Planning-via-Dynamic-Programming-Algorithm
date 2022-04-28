# PLEASE read README.txt












































# from collections import defaultdict
# from curses import has_key
# import numpy as np
# import gym
# from utils import *
# from example import example_use_of_gym_env

# MF = 0 # Move Forward
# TL = 1 # Turn Left
# TR = 2 # Turn Right
# PK = 3 # Pickup Key
# UD = 4 # Unlock Door

# def doorkey_problem(env, info):
#     '''
#     You are required to find the optimal path in
#         doorkey-5x5-normal.env
#         doorkey-6x6-normal.env
#         doorkey-8x8-normal.env
        
#         doorkey-6x6-direct.env
#         doorkey-8x8-direct.env
        
#         doorkey-6x6-shortcut.env
#         doorkey-8x8-shortcut.env
        
#     Feel Free to modify this fuction
#     '''
#     ### static variables ###
#     height = info["height"]
#     width = info["width"]
#     goal_pos = info["goal_pos"]
#     key_pos = info["key_pos"]
#     door_pos = info["door_pos"]
#     door = env.grid.get(info['door_pos'][0], info['door_pos'][1])
#     is_open = door.is_open
#     is_locked = door.is_locked
#     init_agent_pos = info["init_agent_pos"]
#     init_agent_dir = info["init_agent_dir"]
#     init_state = (init_agent_pos[0],init_agent_pos[1],tuple(init_agent_dir), is_locked, env.carrying is not None)
#     print("Initial State: ", init_state)
#     # print("iadir",init_agent_dir)
#     # print
#     #dic of value funcs
    


#     # cell = env.grid.get(1, 3) # NoneType, Wall, Key, Goal
#     # print(cell)

#     ### build state space ###
#     states = []
#     statemap={}
#     # states={}
#     # print(dir(env.grid))
#     num=1
#     stateset=set()
#     wallset=set()
#     for col in range(width):
#         for row in range(height):
#             # pass
#             cell = env.grid.get(col, row) # NoneType, Wall, Key, door
#             if cell and (cell.type=="wall"):
#                 wallset.add((col,row))
#             if cell and (cell.type=="wall" or cell.type=="goal"):
#                 continue
#             for ori in [(-1,0),(1,0),(0,1),(0,-1)]: # left right down up
#                 for door_open in [True, False]:
#                     for have_key in [True, False]:
#                         if (col,row,ori,door_open,have_key) == init_state:
#                             states.insert(0, (col,row,ori,door_open,have_key))
#                             stateset.add((col,row,ori,door_open,have_key))
#                             statemap[(col,row,ori,door_open,have_key)] = 0
#                             # num+=1
#                             continue

#                         # states[(i,j)].append((i,j,ori,door_open,have_key))
#                         # states.append((i,j,ori,door_open,have_key, num)) # num is stateidx
#                         states.append((col,row,ori,door_open,have_key)) # num is stateidx
#                         stateset.add((col,row,ori,door_open,have_key))
#                         statemap[(col,row,ori,door_open,have_key)] = num
#                         num+=1
#     # N = len(states*16)
#     # states[(goal_pos[0],goal_pos[1])].append("goal")
#     for ori in [(-1,0),(1,0),(0,1),(0,-1)]: # left right down up
#         for door_open in [True, False]:
#             for have_key in [True, False]:
#                 states.append((goal_pos[0],goal_pos[1],ori,door_open,have_key))
#                 stateset.add((goal_pos[0],goal_pos[1],ori,door_open,have_key))
#                 statemap[(goal_pos[0],goal_pos[1],ori,door_open,have_key)] = num
#                 num+=1
    
#     # states.append((goal_pos[0],goal_pos[1]))
#     N = len(states)
#     # print(states[-1], N)


#     # print("STATE"*20, states[0], init_state)

#     # for s in states:
#         # print(s)
    
#     # ### Build Motion Model ###
#     def pf3(x,action):
#         col,row,ori,door_open,have_key = x

#         if action == MF:
#             # if env.grid.get(env.front_pos[0],env.front_pos[1]).type == "wall":
#                 # return x
#             if (col+ori[0],row+ori[1]) in wallset:
#                 return x
#             if (col+ori[0],row+ori[1]) == tuple(door_pos) and not have_key:
#                 return x
#             if col+ori[0]==goal_pos[0] and row+ori[1]==goal_pos[1]:
#                 # print("GOAL")
#                 return (col+ori[0],row+ori[1],ori,door_open,have_key)
#             elif (col+ori[0],row+ori[1]) not in states:
#                 return x
#             # cost, done = step(env, MF) 
#             return (col+ori[0],row+ori[1],ori,door_open,have_key)
#         elif action == TL:
#             if ori == (0,-1): newori = (-1,0)
#             elif ori == (-1,0): newori = (0,1)
#             elif ori == (0,1): newori = (1,0)
#             else: newori = 0,-1
#             return (col,row,newori,door_open,have_key)
#         elif action == TR:
#             if ori == (0,-1): newori = (1,0)
#             elif ori == (-1,0): newori = (0,-1)
#             elif ori == (0,1): newori = (-1,0)
#             else: newori = 0,1
#             return (col,row,newori,door_open,have_key)
#         elif action == PK:
#             if col+ori[0]==key_pos[0] and row+ori[1]==key_pos[1]:
#                 return (col,row,ori,door_open,True)
#             return x
#         elif action == UD:
#             if col+ori[0]==door_pos[0] and row+ori[1]==door_pos[1] and have_key:
#                 return (col,row,ori,True,True)
#             else:
#                 return x
            


#     ### Dynamic Programming Algorithm ###
#     T = N - 1
#     X = states
#     U = list(range(5))
#     V = np.ones((T+1,N))*np.inf
#     pi = np.zeros((T,N))
#     Q = np.empty((T,N,len(U)))
#     # print(states[-16:])
#     # V[-1] = float("inf")
#     V[-2,:] = 1
#     for t in reversed(range(T+1)):
#         # V[t,-16:] = 0
#         V[t,-16:] = 0
#     print(V)
#     # pi[-1] = MF
#     a = list(wallset)
#     print(sorted(a))
#     # print(a.sort(key=lambda x : x[0]))
#     policy={}
#     for t in reversed(range(T-1)):
#         for i,x in enumerate(X):
#             if i>=len(X)-16:
#                 continue

#             # print("x",x)

#             for j,u in enumerate(U):
#                 newx = pf3(x,u)
#                 # print(type(newx))
#                 # if (newx[0],newx[1]) in wallset:
#                     # print("wall")
#                 # if newx not in stateset:
#                     # print("notin", newx[0], newx[1])
#                 # print("pf",newx)
#                 # print(newx in stateset)
#                 # print("what"*30)
#                 # print(pf3(x,u))
#                 # print(type(pf3(x,u)))
#                 # print(statemap[pf3(x,u)])
#                 Q[t,i,j] = 1 + V[t+1,statemap[pf3(x,u)]]
#                 # print(Q[t,i,j])

            
#             V[t,i] = np.min(Q[t,i,:])
#             # if np.min(Q[t,i,:]) == np.max(Q[t,i,:]):
#             #     pi[t,i] = np.nan
#             #     continue
#             pi[t,i] = np.argmin(Q[t,i,:])
#             policy[x] = pi[t,i]
#     # print(V[0])
#     print(pi[0])
#     print(policy)
#     #         sim=0
#     #         for k in range(len(V[t])):
#     #             if V[t+1,k]!= V[t,k]:
#     #                 sim+=1
#     #         if sim==len(V[t]):
#     #             break

    

    






#     # ###
#     # agent_pos = env.agent_pos
#     # agent_dir = env.dir_vec # or env.agent_dir
#     # front_cell = env.front_pos # == agent_pos + agent_dir
#     # print(agent_pos,agent_dir,front_cell)
#     # # cell = env.grid.get(2, 3) # NoneType, Wall, Key, Goal

    
#     # # Get the door status
#     # door = env.grid.get(info['door_pos'][0], info['door_pos'][1])
#     # is_open = door.is_open
#     # is_locked = door.is_locked
  
#     # # Determine whether agent is carrying a key
#     # is_carrying = env.carrying is not None

#     # optim_act_seq = [TL, MF, PK, TL, UD, MF, MF, MF, MF, TR, MF]
#     # return optim_act_seq



# def partA():
#     # env_path = './envs/example-8x8.env'
#     env_path = './envs/doorkey-5x5-normal.env'
#     # env_path = './envs/doorkey-6x6-direct.env'
#     # env_path = './envs/doorkey-8x8-direct.env'
#     env, info = load_env(env_path) # load an environment
#     seq = doorkey_problem(env, info) # find the optimal action sequence
#     # draw_gif_from_seq(seq, load_env(env_path)[0]) # draw a GIF & save
    
# def partB():
#     env_folder = './envs/random_envs'
#     env, info, env_path = load_random_env(env_folder)

# if __name__ == '__main__':
#     # example_use_of_gym_env()
#     partA()
#     #partB()

        
        
    
