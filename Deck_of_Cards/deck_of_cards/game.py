import random
import matplotlib.pyplot as plt
import numpy as np
from classes.deck import Deck
from classes.player import Player


fig1, ax1 = plt.subplots()

episodes = []
rewards = []
avg_rewards = []


class Game:
    
    games_played = 0
    
    def __init__( self, number_of_players, training=False ):
        self.number_of_players = number_of_players
        self.training = training
        Game.games_played += 1
        self.deck = Deck()      
        random.shuffle( self.deck.cards )
        self.create_players()
        for player in self.players:
            for i in range( 2 ):
                self.deal_cards( player )
        self.gameover = False
        while not self.gameover:
            self.take_turn()
            self.check_gameover()
    
    def check_gameover(self):
        if all([ player.standing for player in self.players ]):
            self.gameover = True
            # print("GAME OVER")
            winners = []
            legal_scores = [p.count for p in self.players if p.count <= 21]
            winning_score = max(legal_scores) if len(legal_scores) > 0 else None
            for plr in self.players:
                if plr.count != winning_score:
                    plr.ai.learn(plr.count, plr.ai.give_reward(plr.count, False))
                else:
                    winners.append(plr)
            scores = [player.count for player in self.players]
            episodes.append(len(episodes))
            rewards.append(self.players[1].count if self.players[1] in winners else -25)
            avg_rewards.append(sum(rewards)/len(rewards))
            if self.games_played % 25 == 0:
                ax1.plot(episodes, avg_rewards, color='r', label='Control')
                print(f"Scores: {scores}")
                print(f"Winner: {[winner.name for winner in winners]}")

    def create_players( self ):
        self.players = []
        if not self.training:
            self.players.append( Player( True ) )
        else:
            self.players.append( self.training )
        for player in range( self.number_of_players - 1 ):
            self.players.append( Player() )
        for idx in range( len(self.players) ) :
            self.players[idx].name = "Player " + str(idx + 1)
            # print( self.players[idx].name, "has joined the table" )
            self.players[idx].standing = False
            self.players[idx].cards = []
            self.players[idx].count = 0
            self.players[idx].ai.state = 0

    def deal_cards( self, *target ):
        for player in target:
            newCard = self.deck.cards.pop(0)
            player.cards.append( newCard )
            # if newCard.point_val == 1:
            #     if player.isUser:
            #         self.view_cards()
            #         value = input( "Would you like the Ace to be 1 or 11? " )
            #     else:
            #         value = random.choice( [1, 11] )
            #     newCard.point_val = int(value)
            if not player.isUser:
                player.ai.state = int(player.count)
            player.count = sum( [card.point_val for card in player.cards] )

    def view_cards( self ):
        for player in self.players:
            if player.isUser:
                player.show_hand( player.cards )
            else:
                hand = player.cards[:][1:]  
                player.show_hand( hand )

    def take_turn( self ):
        for player in self.players:
            move = 0
            if player.standing == False:
                # print( player.name + " turn" )
                if player.isUser:
                    while int(move) < 1:
                        self.view_cards()
                        print( "0: View Cards" )
                        print( "1: Hit" )
                        print( "2: Stand" )
                        move = input( "Select an option " )
                else:
                    move = player.ai.pick_action(player.count)
                if int(move) == 1:
                    self.deal_cards( player )
                    if player.count >= 21:
                        player.standing = True
                else:
                    player.standing = True
                if not player.isUser:
                    player.ai.learn(player.count, player.ai.give_reward(player.count))



# def startup():
#     print( "0: EXIT this program " )
#     print( "1: Start Game " )
#     option1 = input( "Select an option: " )

#     if option1 == '1':
#         numOfPlayers = input( "Choose number of players, 1-5 " )
#         while int(numOfPlayers) > 9:
#             numOfPlayers = input( "Tables full, please try again " )
#         newGame = Game( int(numOfPlayers) )

# startup()



