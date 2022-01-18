from text_games import *


class BJ_Card(Card):
    '''Regular blackjack game card.'''

    @property
    def value(self):
        if self.face_up:
            v = Deck.RANKS.index(self.rank) + 1
            if v > 10:
                v = 10
        else:
            v = None
        return v
