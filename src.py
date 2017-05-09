from random import randint, choice

class Deck(object):
    """Deck is a class with one attribute: cards.  This is where one can choose the set
   of cards/value that will make up the Players' hands and the prize deck. The
   standard deck is a full suit: values 1 through 13 (i.e. range(1,14).  The
   Player class has an attribute called 'hand', which is a Deck object. Prize is
   the only sub-class of Deck.

    """

    def __init__(self):
        self.cards =  list(range(1, 5))


class Player(object):
    """Player is a class with 4 attributes: name, hand, score, and current_bid. A
    Player can be the end-user or an AI, programmed in the Engine class. Player
    contains a `reset_current_bid` method and several methods for players to
    make bids.  Currently, a bid can be determined by user input using
    `bid_from_input` or by random selection, using `random_bid`. The range of
    bid methods may grow as the AI is developed.

    """

    def __init__(self, name):
        self.name = name
        self.hand = Deck().cards
        self.score = 0
        self.current_bid = None

    def bid(self, card):
        """Method `bid` takes self and card parameters, removes the card from the
        player's hand, and returns the card (an integer). `bid` is not used
        outside the Player class. `bid` does not handle cases in which the card
        argument is not an integer or is not found in the player's hand. Those
        situations are handled by the functions that call bid, such as
        `bid_from_input`.

        """
        i = self.hand.index(card)
        self.hand.pop(i)
        return card

    def reset_current_bid(self):
        self.current_bid = None

    def input_to_int(self):
        """Gets player input for bid. If the input is a non-integer, the player is prompted
        to try again. If the input is an integer, the input string is converted
        to an int and returned.

        """
        str_input = input("Your bid: ")
        while True:
            try:
                val = int(str_input)
            except ValueError:
                print("\nBid must be an integer. Choose one from your hand:")
                print(self.hand)
                str_input = input("Your bid: ")
            else:
                break
        return val

    def bid_from_input(self):
        """Calls `input_to_int` to get the player's bid as an integer. Prints player's
        hand (i.e. available bids) and calls `input_to_int` again if the user
        did not input a valid bid. Once a valid bid is entered, `bid` is called
        to remove the bid-card from the player's hand and return the bid.

        """
        card = self.input_to_int()
        while card not in self.hand:
            print("""\nYou don't have that card to bid! You can choose from these:""")
            print(self.hand)
            card = self.input_to_int()
        return self.bid(card)

    def random_bid(self):
        card = choice(self.hand)
        self.current_bid = self.bid(card)
        return self.current_bid

class Prize(Deck):

    def __init__(self):
        super(Prize, self).__init__()
        self.showing = []

    def next_card(self):
        i = randint(0, len(self.cards) - 1)
        card = self.cards.pop(i)
        self.showing.append(card)
        return card

    def reset_count(self):
        self.showing = []


class Engine(object):
    def __init__(self):
        self.prize = Prize()
        self.AI = Player("AI")
        human_name = raw_input("Enter your name: ")
        self.human = Player(human_name)

    def identify_winner(self, player1, player2):
        if player1.current_bid > player2.current_bid:
            winner = player1
        else:
            winner = player2
        player1.reset_current_bid()
        player2.reset_current_bid()
        return winner

    def award_prize(self, player1, player2, prize):
        winner = self.identify_winner(player1, player2)
        winner.score += prize
        print("%s won that round, for a prize of %d points." %
              (winner.name, prize))

    def play(self):
        while self.prize.cards:
            self.prize.next_card()
            print("\nThe prize currently showing is: %s" % self.prize.showing)
            print("\nHere's your hand, %s: " % self.human.name)
            print(self.human.hand)

            self.human.current_bid = self.human.bid_from_input()
            self.AI.current_bid = self.AI.random_bid()
            print("AI bid: %s" % self.AI.current_bid)

            if self.human.current_bid == self.AI.current_bid:
                print("A tie bid!")
                continue
            else:
                prize = sum(self.prize.showing)
                self.award_prize(self.human, self.AI, prize)
                self.prize.reset_count()


        print("\nGAME OVER!")
        print("\nFinal score:")
        print("  You: %s" % self.human.score)
        print("  AI:  %s" % self.AI.score)

new_game = Engine()
new_game.play()