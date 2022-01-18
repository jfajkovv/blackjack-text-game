import text_games


class BJ_Card(text_games.Card):
    '''Regular blackjack game card.'''


class BJ_Hand(text_games.Hand):
    '''Collection of cards to do something with.'''


class BJ_Player(text_games.Player):
    '''Blackjack game player representation.'''


class BJ_Dealer(text_games.Player):
    '''Casino house host representation.'''


class BJ_Deck(text_games.Deck):
    '''Blackjack session total of cards.'''


class BJ_Game(object):
    '''Blackjack gameplay logic.'''

    def __init__(self):
        the_player = BJ_Player(name='Player')
        the_dealer = BJ_Dealer(name='Croupier')
        cards_deck = BJ_Deck()
        cards_deck.fill_in(stacks=2)
        cards_deck.shuffle()

    def run(self):
        pass


def main():
    print('Welcome to the House!')
    input('Press [Enter] to play...')

    bj_session = BJ_Game()
    bj_session.run()


if __name__ == '__main__':
    main()
