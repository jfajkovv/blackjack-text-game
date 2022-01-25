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

    def is_broke(self):
        if not self.money:
            return True

    def is_cashing_out(self):
        return self.is_cashing_out

    def place_a_bet(self):
        bet_choice = None
        while bet_choice not in ('p', 'a'):
            bet_choice = input('[P]lace a bet or put [a]ll in.').lower()

        if bet_choice == 'p':
            bet_amount = text_games.ask_int_in_range(
                range_bottom=1,
                range_top=self.money,
                user_query=f'Put the money ({1}-{self.money}): $'
            )
            print('bet', bet_amount)
        elif bet_choice == 'a':
            bet_amount = self.money
            print('all in', bet_amount)
        return bet_amount


class BJ_Dealer(text_games.Player, BJ_Hand):
    '''Casino house host representation.'''

    def __init__(self, name):
        super().__init__(name)
        self.card_set = []


class BJ_Deck(text_games.Deck):
    '''Blackjack session total of cards.'''

    def __init__(self):
        super(BJ_Deck, self).__init__()
        self.used_cards = []

    @property
    def amount(self):
        a = 0
        for card in self.card_set:
            a += 1
        return a

    def restore(self):
        if self.amount < 52:
            for used_card in self.used_cards:
                self.hand_out(hands=[self.card_set], per_hand=1)
            self.shuffle()


class BJ_Game(object):
    '''Blackjack gameplay logic.'''

    def __init__(self):
        self.player = BJ_Player(name='Player')
        self.dealer = BJ_Dealer(name='Croupier')
        self.deck = BJ_Deck()
        self.deck.fill_in(stacks=2)
        self.deck.shuffle()


    def run(self):
        # TODO: The game runs while the player has money or wishes
        # to cash out.
        while not self.player.is_broke() and not self.player.is_cashing_out:
            # TODO: Inspect if total deck cards are lower than 52,
            # and if so, restore the deck and shuffle it.
            self.deck.restore()

            # TODO: Allow the player to place a bet.
            self.player.place_a_bet()

        # TODO: Deal both the player and croupier two initial cards.


def main():
    print('Welcome to the House!')
    input('Press [Enter] to play...')

    bj_session = BJ_Game()
    bj_session.run()


if __name__ == '__main__':
    main()
