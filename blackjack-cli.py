import text_games


class BJ_Card(text_games.Card):
    '''Regular blackjack game card.'''


class BJ_Hand(text_games.Hand):
    '''Collection of cards to do something with.'''


class BJ_Player(text_games.Player, BJ_Hand):
    '''Blackjack game player representation.'''

    def __init__(self, name, money=1000):
        super().__init__(name)
        self.card_set = []
        self.money = money
        self.is_cashing_out = False

    def bet(self):
        bet_choice = None
        while bet_choice not in ('p', 'a'):
            bet_choice = input('[P]lace a bet or put [a]ll in.').lower()

        if bet_choice == 'p':
            bet = text_games.ask_int_in_range(
                range_bottom=1,
                range_top=self.money,
                user_query=f'Put the money ({1}-{self.money}): $'
            )
        elif bet_choice == 'a':
            bet = self.money
        return bet


class BJ_Dealer(text_games.Player, BJ_Hand):
    '''Casino house host representation.'''

    def __init__(self, name):
        super().__init__(name)
        self.card_set = []


class BJ_Deck(text_games.Deck):
    '''Blackjack session total of cards.'''

    @property
    def amount(self):
        a = 0
        for card in self.card_set:
            a += 1
        return a


class BJ_Game(object):
    '''Blackjack gameplay logic.'''

    def __init__(self):
        self.player = BJ_Player(name='Player')
        self.dealer = BJ_Dealer(name='Croupier')
        self.deck = BJ_Deck()
        self.deck.fill_in(stacks=2)
        self.deck.shuffle()

    def run(self):
        pass


def main():
    print('Welcome to the House!')
    input('Press [Enter] to play...')

    bj_session = BJ_Game()
    bj_session.run()


if __name__ == '__main__':
    main()
