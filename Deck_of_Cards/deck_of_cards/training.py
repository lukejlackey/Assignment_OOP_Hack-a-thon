import random
import matplotlib.pyplot as plt
import classes.player as plr
from game import Game

plt.ion()
plt.pause(.2)


def train(player):
    plt.ylabel('total rewards')
    plt.xlabel('episodes')
    plt.plot(player.ai.total_rewards)
    plt.pause(.2)
    plt.show()
    for episode in range(player.ai.EPISODES):
        training_game = Game(random.randint(2,9), player)
        plt.scatter(episode, player.ai.total_rewards)
        plt.pause(.2)

testplayer = plr.Player()

train(testplayer)