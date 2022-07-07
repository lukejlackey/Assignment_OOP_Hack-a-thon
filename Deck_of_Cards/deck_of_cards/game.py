import random
from classes.deck import Deck
from classes.player import Player
bicycle = Deck()

# bicycle.show_cards()

class Game:
    def __init__( self, number_of_players ):
        self.number_of_players = number_of_players
        self.deck = Deck()      
        random.shuffle( self.deck.cards )
        self.players = []
        self.create_players()
        for player in self.players:
            for i in range( 2 ):
                self.deal_cards( player )
        while not all( [ player.standing for player in self.players ] ):
            self.take_turn()


    def create_players( self ):
        self.players.append( Player( True ) )
        for player in range( self.number_of_players - 1 ):
            self.players.append( Player() )
        for index in range( len(self.players) ) :
            self.players[index].name = "Player " + str(index + 1)
            print( self.players[index].name, "has joined the table" )
            self.players[index].standing = False
            self.players[index].count = 0

    def deal_cards( self, *target ):
        for player in target:
            newCard = self.deck.cards.pop(0)
            player.cards.append( newCard )
            if newCard.point_val == 1:
                if player.isUser:
                    self.view_cards()
                    value = input( "Would you like the Ace to be 1 or 11? " )
                else:
                    value = random.choice( [1, 11] )
                newCard.point_val = int(value)
            player.count = sum( [card.point_val for card in player.cards] )

    def view_cards( self ):
        for player in self.players:
            if player.isUser:
                player.show_hand( player.cards )
            else:
                hand = player.cards[:] #[1:]  
                player.show_hand( hand )

    def take_turn( self ):
        for player in self.players:
            if player.standing == False:
                print( player.name + " turn" )
                if player.isUser:
                    print( "0: View Cards" )
                    print( "1: Hit" )
                    print( "2: Stand" )
                    move = input( "Select an option " )
                else:
                    move = random.randint( 1, 2)
                while int(move) < 1:
                    self.view_cards()
                    print( "0: View Cards" )
                    print( "1: Hit" )
                    print( "2: Stand" )
                    move = input( "Select an option " )
                if move == "1":
                    self.deal_cards( player )
                    player.standing = True if player.count > 21 else False
                elif move == "2":
                    player.standing = True




print( "0: EXIT this program " )
print( "1: Start Game " )
option1 = input( "Select an option: " )


if option1 == '1':
    numOfPlayers = input( "Choose number of players, 1-5 " )
    while int(numOfPlayers) > 5:
        numOfPlayers = input( "Tables full, please try again " )
    newGame = Game( int(numOfPlayers) )
    # print( newGame.players )





