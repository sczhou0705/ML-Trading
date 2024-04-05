""""""  		  	   		  		 		  		  		    	 		 		   		 		  
"""  		  	   		  		 		  		  		    	 		 		   		 		  
Template for implementing QLearner  (c) 2015 Tucker Balch  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  		 		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		  		 		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  		 		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		  		 		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		  		 		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		  		 		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		  		 		  		  		    	 		 		   		 		  
or edited.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		  		 		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		  		 		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  		 		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Student Name: Tucker Balch (replace with your name)  		  	   		  		 		  		  		    	 		 		   		 		  
GT User ID: tb34 (replace with your User ID)  		  	   		  		 		  		  		    	 		 		   		 		  
GT ID: 900897987 (replace with your GT ID)  		  	   		  		 		  		  		    	 		 		   		 		  
"""  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
import random as rand  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
import numpy as np  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
class QLearner(object):  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    This is a Q learner object.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
    :param num_states: The number of states to consider.  		  	   		  		 		  		  		    	 		 		   		 		  
    :type num_states: int  		  	   		  		 		  		  		    	 		 		   		 		  
    :param num_actions: The number of actions available..  		  	   		  		 		  		  		    	 		 		   		 		  
    :type num_actions: int  		  	   		  		 		  		  		    	 		 		   		 		  
    :param alpha: The learning rate used in the update rule. Should range between 0.0 and 1.0 with 0.2 as a typical value.  		  	   		  		 		  		  		    	 		 		   		 		  
    :type alpha: float  		  	   		  		 		  		  		    	 		 		   		 		  
    :param gamma: The discount rate used in the update rule. Should range between 0.0 and 1.0 with 0.9 as a typical value.  		  	   		  		 		  		  		    	 		 		   		 		  
    :type gamma: float  		  	   		  		 		  		  		    	 		 		   		 		  
    :param rar: Random action rate: the probability of selecting a random action at each step. Should range between 0.0 (no random actions) to 1.0 (always random action) with 0.5 as a typical value.  		  	   		  		 		  		  		    	 		 		   		 		  
    :type rar: float  		  	   		  		 		  		  		    	 		 		   		 		  
    :param radr: Random action decay rate, after each update, rar = rar * radr. Ranges between 0.0 (immediate decay to 0) and 1.0 (no decay). Typically 0.99.  		  	   		  		 		  		  		    	 		 		   		 		  
    :type radr: float  		  	   		  		 		  		  		    	 		 		   		 		  
    :param dyna: The number of dyna updates for each regular update. When Dyna is used, 200 is a typical value.  		  	   		  		 		  		  		    	 		 		   		 		  
    :type dyna: int  		  	   		  		 		  		  		    	 		 		   		 		  
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		  		 		  		  		    	 		 		   		 		  
    :type verbose: bool  		  	   		  		 		  		  		    	 		 		   		 		  
    """
    def author(self):
        return 'szhou401'
    def __init__(  		  	   		  		 		  		  		    	 		 		   		 		  
        self,  		  	   		  		 		  		  		    	 		 		   		 		  
        num_states=100,  		  	   		  		 		  		  		    	 		 		   		 		  
        num_actions=4,  		  	   		  		 		  		  		    	 		 		   		 		  
        alpha=0.2,  		  	   		  		 		  		  		    	 		 		   		 		  
        gamma=0.9,  		  	   		  		 		  		  		    	 		 		   		 		  
        rar=0.5,  	# Random Action Rate
        radr=0.99,  # Random Action Decay Rate
        dyna=0,  		  	   		  		 		  		  		    	 		 		   		 		  
        verbose=False,  		  	   		  		 		  		  		    	 		 		   		 		  
    ):  		  	   		  		 		  		  		    	 		 		   		 		  
        """  		  	   		  		 		  		  		    	 		 		   		 		  
        Constructor method  		  	   		  		 		  		  		    	 		 		   		 		  
        """
        # Initialize
        self.verbose = verbose  		  	   		  		 		  		  		    	 		 		   		 		  
        self.num_actions = num_actions  		  	   		  		 		  		  		    	 		 		   		 		  
        self.s = 0  		  	   		  		 		  		  		    	 		 		   		 		  
        self.a = 0

        self.rar = rar
        self.radr = radr
        self.alpha = alpha
        self.gamma = gamma
        self.dyna = dyna

        self.qtable = np.zeros((num_states, num_actions))
        self.t_model = {}
        self.r_model = {}
    def choose_action(self,state):      #https://www.codingninjas.com/studio/library/epsilon-greedy-algorithm
        if rand.random() < self.rar:
            action = rand.randint(0,self.num_actions - 1)
        else:
            action = np.argmax(self.qtable[state])
        return action
    def querysetstate(self, s):  		  	   		  		 		  		  		    	 		 		   		 		  
        """  		  	   		  		 		  		  		    	 		 		   		 		  
        Update the state without updating the Q-table  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
        :param s: The new state  		  	   		  		 		  		  		    	 		 		   		 		  
        :type s: int  		  	   		  		 		  		  		    	 		 		   		 		  
        :return: The selected action  		  	   		  		 		  		  		    	 		 		   		 		  
        :rtype: int  		  	   		  		 		  		  		    	 		 		   		 		  
        """
        # Set the state of the learner to a new state without taking an action or receiving a reward.
        self.s = s
        action =self.choose_action(s)
        self.a= action
        if self.verbose:  		  	   		  		 		  		  		    	 		 		   		 		  
            print(f"s = {s}, a = {action}")
        return action
  		  	   		  		 		  		  		    	 		 		   		 		  
    def query(self, s_prime, r):
        """  		  	   		  		 		  		  		    	 		 		   		 		  
        Update the Q table and return an action  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
        :param s_prime: The new state  		  	   		  		 		  		  		    	 		 		   		 		  
        :type s_prime: int  		  	   		  		 		  		  		    	 		 		   		 		  
        :param r: The immediate reward  		  	   		  		 		  		  		    	 		 		   		 		  
        :type r: float  		  	   		  		 		  		  		    	 		 		   		 		  
        :return: The selected action  		  	   		  		 		  		  		    	 		 		   		 		  
        :rtype: int  		  	   		  		 		  		  		    	 		 		   		 		  
        """
        self.qtable[self.s,self.a] = self.qtable[self.s,self.a] + \
                                     self.alpha * (r + self.gamma * np.max(self.qtable[s_prime]) - self.qtable[self.s,self.a])
        self.t_model[(self.s,self.a)] = s_prime # store experience
        self.r_model[(self.s,self.a)] = r # store experience

        if self.dyna > 0: # greater than 0, we are using simulated experiences to update the Q- tables

            for _ in range(self.dyna):
                # Randomly choose previous state and action
                s_rand,a_rand = rand.choice(list(self.t_model.keys()))
                s_prime_rand = self.t_model[(s_rand,a_rand)]
                r_rand = self.r_model[(s_rand,a_rand)]
                # update q table
                self.qtable[s_rand,a_rand] = self.qtable[s_rand,a_rand] + \
                                             self.alpha * (r_rand + self.gamma * np.max(self.qtable[s_prime_rand]) - self.qtable[s_rand,a_rand])
# choose next action
        action = self.choose_action(s_prime)
        # reduce epsilon
        self.rar =self.rar * self.radr
        self.s = s_prime
        self.a = action

        if self.verbose:
            print(f"s = {s_prime}, a = {action}, r={r}")

        return action  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		  		 		  		  		    	 		 		   		 		  
    print("Remember Q from Star Trek? Well, this isn't him")  		  	   		  		 		  		  		    	 		 		   		 		  
