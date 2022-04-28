Inside starter_code lies the code for PR1

- parta.py 
    - contains code for part a. It is sinspred by doorkey.py's format. 
    - run python3 parta.py
    - Under partA() function, change the path of env to run for a different gif
    - Will create a gif inside gif folder

- partb.py
    - Contains code for part b.
    - run python3 partb.py
    - Will run DPA for partb and create a pickle file of the optimal paths (Not the policy)

-testpartb.py
    - Contains code that loads the Picke file generated from partb.py
    - Will load "part_b_optimal_paths.pkl"
    - Will run for a random initial state
    - Will also generate a gif
