import text_games
from time import sleep


class BJ_Card(text_games.Card):
    '''Regular blackjack game card.'''

    @property
    def value(self):
        if self.is_face_up:
            v = text_games.Deck.RANKS.index(self.rank) + 1
            if v > 10:
                v = 10
        else:
            v = None
        return v


class BJ_Hand(text_games.Hand):
    '''Collection of cards to do something with.'''

    def __str__(self):
        re = super(BJ_Hand, self).__str__()
        if self.total:
            re += 'in total: (' + str(self.total) + ')'
        return re

    @property
    def total(self):
        for card in self.card_set:
            if card.value == None:
                return None

        t = 0
        for card in self.card_set:
            t += card.value

        has_ace = False
        for card in self.card_set:
            if card.value == 0:
                has_ace = True

        if has_ace and t <= 21:
            t += 10

        return t

    def is_busted(self):
        return self.total > 21


class BJ_Player(text_games.Player, BJ_Hand):
    '''Blackjack game player representation.'''

    START_MONEY = 1000

    def __init__(self, name, money=START_MONEY):
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
            print('Thank you for your visit. Come again soon.')
            print(f'*you leave with ${self.money}*')
            self.is_cashing_out = True
        elif choice == 'n':
            return choice

    def place_a_bet(self):
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

    def gamble_or_leave(self):
        choice = None
        while choice not in ('p', 'c'):
            choice = input('[P]lace a bet or [c]ash out.').lower()

        if choice == 'p':
            result = self.place_a_bet()
            return result
        elif choice == 'c':
            self.cash_out()
        else:
            print('err: something went wrong in BJ_Player:')
            print('gamble_or_leave()')

    def hit_or_stand(self):
        choice = None
        while choice not in ('h', 's'):
            choice = input('[H]it or [s]tand.').lower()

        return choice


class BJ_Dealer(text_games.Player, BJ_Hand):
    '''Casino house host representation.'''

    def __init__(self, name):
        super().__init__(name)
        self.card_set = []

    def is_hitting(self):
        return self.total < 17

    def flip_first_card(self):
        self.card_set[0].flip()


class BJ_Deck(text_games.Deck):
    '''Blackjack session total of cards.'''

#    def __init__(self):
#        super(BJ_Deck, self).__init__()
#        self.used_cards = []

    @property
    def amount(self):
        a = 0
        for card in self.card_set:
            a += 1
        return a

    def fill_in(self, stacks=1):
            for stack in range(stacks):
                for suit in self.SUITS:
                    for rank in self.RANKS:
                        self.stack_on(
                            single_card=BJ_Card(rank=rank, suit=suit)
                        )

    def time_to_shuffle(self):
        if self.amount < 52:
            return True

    def restore(self):
        if self.amount < 52:
            self.transfer_all(
                given_set=self.used_cards,
                route=self.card_set
            )
            self.shuffle()


class BJ_Game(object):
    '''Blackjack gameplay logic.'''

    def __init__(self):
        self.player = BJ_Player(name='Player')
        self.dealer = BJ_Dealer(name='Croupier')
        self.deck = BJ_Deck()
        self.deck.fill_in(stacks=2)
        self.deck.shuffle()
        self.used_deck = BJ_Deck()
        self.__round = 1
        self.__bet_bank = 0

    @property
    def players(self):
        in_game = (self.player, self.dealer)
        return in_game

    def display_players(self):
        print(f'Dealer   >>>   {self.dealer}')
        print(f'Player   >>>   {self.player}')

    def display_dealer(self):
        print(f'Dealer   >>>   {self.dealer}')

    def display_round(self):
        print(f'Round no.   ( {self.__round} )')

    def count_round(self):
        self.__round += 1

    def display_account(self):
        print(f'Bank:   ( ${self.player.money} )')

    def fetch_money(self, money):
        money *= 2
        self.__bet_bank = money

    def display_bet(self):
        print(f'Bet:   {self.__bet_bank}')

    def reset_bet(self):
        self.__bet_bank = 0

    def reward_player(self):
        self.player.money += self.__bet_bank

    def evaluate_round(self):
        if self.player.is_busted():
            print('You\'ve got busted. You lose.')
        elif self.dealer.is_busted():
            print('Dealer got busted. You win.')
            self.reward_player()
        elif self.player.total > self.dealer.total:
            print('You win.')
            self.reward_player()
        elif self.player.total < self.dealer.total:
            print('Dealer wins.')
        else:
            print('A tie - push.')

    def run(self):
        # The game runs while the player has money or wishes to cash out.
        while not self.player.is_broke() and not self.player.is_cashing_out:
            self.display_account()
            print(f'used: {self.used_deck}')

            # Inspect if total deck cards are lower than 52,
            # and if so, restore the deck and shuffle it.
#            if self.deck.time_to_shuffle():
#                self.deck.restore()

            # Allow the player to cash_out or place a bet.
            player_bet = 'n'
            while player_bet == 'n':
                player_bet = self.player.gamble_or_leave()

            # Fetch money into the bank and start round.
            if player_bet:
                self.display_round()
                self.fetch_money(money=player_bet)

                # Deal both the player and croupier two initial cards.
                self.deck.hand_out(hands=self.players, per_hand=2)
                self.dealer.flip_first_card()
                self.display_players()

                # Allow the player to hit or stand.
                while not self.player.is_busted() \
                          and self.player.hit_or_stand() == 'h':
                    self.deck.hand_out(hands=[self.player])
                    self.display_players()

                # Croupier move.
                self.dealer.flip_first_card()
                self.display_dealer()
                if not self.player.is_busted():
                    while not self.dealer.is_busted() \
                              and self.dealer.is_hitting():
                        self.deck.hand_out(hands=[self.dealer])
                        self.display_dealer()
                        sleep(1)

                # Evaluate scores.
                print()
                self.display_players()
                self.evaluate_round()

                # Increment round counter.
                self.count_round()

                # Reset bet, fetch used cards and clear hands before
                # new round.
                self.reset_bet()
                self.display_bet()
                for player in self.players:
                    player.transfer_all(route=self.used_deck)


def main():
    print('blackjack-cli v.0.1 by jfajkovv')
    print('Welcome to the House!')
    input('Press [Enter] to play...')

    bj_session = BJ_Game()
    bj_session.run()


if __name__ == '__main__':
    main()
