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
            print('You have no money left - you lose.')
            return True

    def cash_out(self):
        choice = text_games.ask_yes_no(
            user_query='Take cash and leave? (y/n): '
        )

        if choice == 'y':
            self.is_cashing_out = True

    def place_a_bet(self):
        print(self.money)
        bet_choice = None
        while bet_choice not in ('c', 'a'):
            bet_choice = input('[C]hoose amount or put [a]ll in.').lower()

        if bet_choice == 'c':
            MIN = 1
            MAX = self.money

            bet_amount = text_games.ask_int_in_range(
                range_bottom=MIN,
                range_top=MAX,
                user_query=f'Put the money ({MIN}-{MAX}): $'
            )
            self.money -= bet_amount
        elif bet_choice == 'a':
            bet_amount = self.money
            self.money = 0
        return bet_amount

    def take_action(self):
        choice = None
        while choice not in ('p', 'c'):
            print('[P]lace a bet or [c]ash out.')
            choice = input('\t>>> ').lower()

        if choice == 'p':
            self.place_a_bet()
        elif choice == 'c':
            self.cash_out()
        else:
            print('err: something went wrong in BJ_Player: take_action() method')


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

    def time_to_shuffle(self):
        if self.amount < 52:
            return True

    def restore(self):
        if self.amount < 52:
            self.transfer_all(given_set=self.used_cards, route=self.card_set)
            self.shuffle()


class BJ_Game(object):
    '''Blackjack gameplay logic.'''

    def __init__(self):
        self.player = BJ_Player(name='Player')
        self.dealer = BJ_Dealer(name='Croupier')
        self.deck = BJ_Deck()
        self.deck.fill_in(stacks=2)
        self.deck.shuffle()
        self.__bet_bank = 0


    def run(self):
        # TODO: The game runs while the player has money or wishes
        # to cash out.
        while not self.player.is_broke() and not self.player.is_cashing_out:
            # TODO: Inspect if total deck cards are lower than 52,
            # and if so, restore the deck and shuffle it.
            if self.deck.time_to_shuffle():
                self.deck.restore()

            # TODO: Allow the player to cash_out or place a bet.
            self.player.take_action()

        # TODO: Deal both the player and croupier two initial cards.


def main():
    print('Welcome to the House!')
    input('Press [Enter] to play...')

    bj_session = BJ_Game()
    bj_session.run()


if __name__ == '__main__':
    main()
