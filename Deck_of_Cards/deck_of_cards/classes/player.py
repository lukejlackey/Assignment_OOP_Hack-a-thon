from collections import defaultdict
import classes.card as card
import matplotlib.pyplot as plt
import numpy as np
import random

plt.ion()
plt.pause(.2)

fig2, ax2 = plt.subplots()
ax2.set_xlabel('Count')
ax2.set_ylabel('Action Taken')
plt.pause(.2)
plt.show()

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
    
    def show_name(self):
        return self.name
    
    class PlayerAI():
        
        state_space = 19
        
        actions = [1,2]
        action_space = len(actions)
        
        win_reward = 25
        loss_penalty = -25
        
        def __init__(self) -> None:
            self.state = 0
            self.action = 0
            self.epsilon = 0.9
            self.EPISODES = 4200
            self.LEARNING_RATE = 0.02
            self.GAMMA = 0.98
            self.Q = np.zeros((self.state_space,self.action_space))
            self.total_rewards = []
            self.history = defaultdict(list)
        
        @staticmethod
        def shrink_number(num):
            return num - 3 if num < 21 else 18
        
        def pick_action(self, counter):
            counter = self.shrink_number(counter)
            if np.random.uniform(0, 1) < self.epsilon:
                action = random.choice(self.actions)
            else:
                action = np.argmax(self.Q[counter, :]) + 1
            self.action = action - 1
            self.history[str(counter)].append(action)
            x = [int(c) for c in self.history.keys()]
            self.hit_counts = [a.count(1) for a in self.history.values() if isinstance(a, list)]
            self.stand_counts = [a.count(2) for a in self.history.values() if isinstance(a, list)]
            if len(x) == 19:
                if hasattr(self, 'hcBar'):
                    for (b, ct) in [(self.hcBar, self.hit_counts), (self.scBar, self.stand_counts)]:
                        for rect, h in zip(b, ct):
                            rect.set_height(h)
                            plt.show()
                else:
                    self.hcBar = ax2.bar(x, self.hit_counts, width=1, edgecolor="white", linewidth=0.7, color='b', label='Hits')
                    self.scBar = ax2.bar(x, self.stand_counts, width=1, edgecolor="white", linewidth=0.7, color='r', label='Stands')
                    ax2.set_ylim([0, 500])
                    ax2.legend()
            return action
        
        def give_reward(self, counter, winner=None):
            counter = self.shrink_number(counter)
            if winner is False or counter >= self.state_space:
                reward = self.loss_penalty
            else:
                reward = counter
            self.total_rewards.append(reward)
            return reward
        
        def learn(self, counter, reward):
            state = self.shrink_number(self.state)
            counter = self.shrink_number(counter)
            self.Q[state, self.action] = self.Q[state, self.action] + self.LEARNING_RATE * (reward + self.GAMMA * np.max(self.Q[counter, :]) - self.Q[state, self.action])
            self.epsilon -= .0003