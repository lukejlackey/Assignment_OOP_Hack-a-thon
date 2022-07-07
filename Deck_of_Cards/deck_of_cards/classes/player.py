from tkinter.font import names
from . import card

class Player:

    def __init__( self, isUser = False ):
        self.isUser = isUser
        self.cards = []

    def show_hand( self, target ):
        print( self.name )
        for c in target:
            c.card_info()