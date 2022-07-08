import classes.card as card
import numpy as np
import random

class Player:

    def __init__( self, isUser = False ):
        self.isUser = isUser
        self.count = 0
        self.cards = []
        if not isUser:
            self.ai = self.PlayerAI()

    def show_hand( self, target ):
        print( self.name )
        for c in target:
            c.card_info()
    
    class PlayerAI():
        
        state_space = 31
        
        actions = [1,2]
        action_space = len(actions)
        
        win_reward = 400
        
        def __init__(self) -> None:
            self.state = 0
            self.action = 0
            self.epsilon = 0.9
            self.EPISODES = 100000
            self.LEARNING_RATE = 0.85
            self.GAMMA = 0.97
            self.Q = np.zeros((self.state_space,self.action_space))
            self.total_rewards = 0
        
        def pick_action(self, counter):
            if np.random.uniform(0, 1) < self.epsilon:
                action = random.choice(self.actions)
            else:
                action = np.argmax(self.Q[counter, :])
            self.action = action - 1
            return action
        
        def give_reward(self, counter, winner=False):
            if winner:
                reward = self.win_reward
            else:
                reward = counter if counter <= 21 else 21 - counter
            self.total_rewards += reward
            return reward
        
        def learn(self, counter, reward):
            self.Q[self.state, self.action] = self.Q[self.state, self.action] + self.LEARNING_RATE * (reward + self.GAMMA * np.max(self.Q[counter, :]) - self.Q[self.state, self.action])
            