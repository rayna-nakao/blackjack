import time
import os

class Player:
    def __init__(self):
        self.money = 100
        self.bet = 0
        self.gameOver = False

    # gets and validates players bet, subtract bet from player’s money
    def placebet(self):
        done = False
        while not done:
            try: 
                print("You currently have: " + str(self.money) + " credits")
                self.bet = int(input("How much would you like to bet? "))
            except:
                print("Not a valid input. Try again.\n")
            else:
                if self.bet > self.money:
                    print("\nYour bet is too large.")
                elif self.bet <= 0:
                    print("\nYour bet is too small.")
                else:
                    print("Good luck!\n")
                    done = True
                    return

    # add players winnings, if any, to player’s money
    def payout(self, win):
        # player blackjack, pay 1.5 times bet
        if win == 'B':
            print("You won: " + str(1.5 * self.bet) + " credits")
            self.money += (1.5 * self.bet)

        # player beat dealer, pay 1 times bet + bet
        elif win == 'W':
            print("You won: " + str(self.bet) + " credits")
            self.money += (self.bet)

        # player pushes, pay bet
        elif win == 'P':
            print("Push!")

        # player lost, check money, if none then end game
        else:
            self.money -= self.bet
            if self.money <= 0:
                print("You've run out of credits! Thanks for playing.")
                self.gameOver = True
                return
        self.playagain()

    # check if player wants to continue playing or quit
    def playagain(self):
        while True:
            toContinue = input("Press enter to continue or enter q to quit the game: ")
            if toContinue == 'q':
                while True:
                    print("Are you sure you want to quit? Your progress will not be saved.")
                    sure = input("Enter y to quit or n to continue playing: ")
                    if sure == "y":
                        print("Thanks for playing! Goodbye!")
                        self.gameOver = True
                        return
                    elif sure == "n":
                        print("\n")
                        return
                    else:
                        print("Not a valid input.")
            elif toContinue == "":
                print("\n")
                return
            else:
                print("Not a valid input.")

    def getgamestatus(self):
        return self.gameOver

# handles the blackjack game - dealing cards, determining winner
class Game:
    def __init__(self, player, deck):
        self.dealerHand = []
        self.playerHand = []
        self.player = player
        self.deck = deck
        self.handDone = False

    # request new shuffled deck
    def getDeck(self):
        self.deck.getDeck()

    # deals hand to dealer and player
    def dealHand(self):
        # deal 2 cards to each dealer and player, starting with the player
        self.playerHand.append(self.deck.getCard())
        self.dealerHand.append(self.deck.getCard())
        self.playerHand.append(self.deck.getCard())
        self.dealerHand.append(self.deck.getCard())

        # print hands
        print("Dealers hand: " + self.dealerHand[0] + " ?")
        print("Your hand: ", end = "")
        self.printHand(self.playerHand)

    # handles the actual game play
    def playHand(self):
        # check if either dealer or player has blackjack
        dealerBlackjack = self.isBlackjack(self.dealerHand)
        playerBlackjack = self.isBlackjack(self.playerHand)

        # if both dealer and player have blackjack, push
        if dealerBlackjack and playerBlackjack:
            self.playerDealerBlackjack()

        # if only dealer has blackjack, player loses
        elif dealerBlackjack and not playerBlackjack:
            self.dealerBlackjack()

        # if only player has blackjack, player win
        elif not dealerBlackjack and playerBlackjack:
            self.playerBlackjack()

        # if no blackjacks, continue
        else:
            while not self.handDone:
                move = input("\nHit or stand? Enter h for hit or s for stand: ")

                if move == 's':
                    self.dealerTurn()
                    self.handDone = True
                    if self.getTotal(self.dealerHand) > 21:
                        self.dealerBust()
                        return

                elif move == 'h':
                    self.hitCard(self.playerHand)
                    print("Your hand: ", end = "")
                    self.printHand(self.playerHand)
                    if self.getTotal(self.playerHand) > 21:
                        self.playerBust()
                        return

                else:
                    print("Not a valid input, try again.")
            self.compareHands()
        self.resetHand()

    # prints cards in hand
    def printHand(self, hand):
        for card in hand:
            print(card + " ", end = "")

    # dealer and player have blackjack, payout push
    def playerDealerBlackjack(self):
        print("Push! You and the dealer have blackjack!")
        print("Dealer had: ", end = "")
        self.printHand(self.dealerHand)
        print("\n")
        self.player.payout('P')

    # dealer has blackjack, payout loss
    def dealerBlackjack(self):
        print("\n\nBlackjack! Dealer wins!")
        print("Dealer had: ", end = "")
        self.printHand(self.dealerHand)
        print("\n")
        self.player.payout('L')

    # player has blackjack, payout blackjack
    def playerBlackjack(self):
        print("\nBlackjack! You win!")
        print("Dealer had: ", end = "")
        self.printHand(self.dealerHand)
        print("\n")
        self.player.payout('B')
    
    # dealer busts, payout player
    def dealerBust(self):
        print("Dealer bust! You win!")
        self.handDone = True
        self.resetHand()
        self.player.payout('W')

    # player busts
    def playerBust(self):
        self.handDone = True
        print("\nYou bust! Dealer wins!")
        self.resetHand()
        self.player.payout('L')

    # checks if hand is blackjack 21
    def isBlackjack(self, hand):
        if 'A' in hand and ('10' in hand or 'J' in hand or 'Q' in hand or 'K' in hand):
            return True
        else:
            return False

    # gets total value of cards in hand
    def getTotal(self, hand) -> int:
        total = 0
        aces = 0

        for card in hand:
            if card == 'J' or card == 'Q' or card == 'K':
                total += 10
            elif card == 'A':
                aces += 1
            else:
                total += int(card)

        if aces > 0:
            for i in range(aces):
                total += 11
                if total > 21:
                    total -= 10
        return total

    # player or dealer hit, draw another card
    def hitCard(self, hand):
        hand.append(self.deck.getCard())

    # dealer’s turn
    def dealerTurn(self):
        print("\nDealer playing their hand...")
        time.sleep(1.5)
        while self.getTotal(self.dealerHand) < 17:
            self.hitCard(self.dealerHand)
        print("Dealer's hand: ", end = "")
        self.printHand(self.dealerHand)
        print("\n")


    # compare dealer and player’s hands to determine winner
    # calls player function to payout
    def compareHands(self):
        dealerTotal = self.getTotal(self.dealerHand)
        playerTotal = self.getTotal(self.playerHand)

        if dealerTotal > playerTotal:
            print("Dealer wins!")
            self.player.payout('L')

        elif dealerTotal < playerTotal:
            print("You win!")
            self.player.payout('W')

        else:
            self.player.payout('P')

    def resetHand(self):
        self.dealerHand.clear()
        self.playerHand.clear()
        self.handDone = False


# handles the deck of cards - shuffle, deal (pop) from the deck, reset the deck
class Deck:
    def __init__(self):
        self.theDeck = []

    # gets a deck from microservice by writing run to text file
    # resulting text from microservice is stored in theDeck list
    def getDeck(self):
        file = open("deck.txt", "w")
        file.write("run")
        file.close()
        #modifiedTime = os.stat("deck.txt").st_atime
        modifiedTime = os.path.getctime("deck.txt")

        while os.path.getctime("deck.txt") == modifiedTime:
            time.sleep(0.5)

        with open("deck.txt", "r") as deck:
            data = deck.read()
            data = data.replace("'", "")
            self.theDeck = data.strip('][').split(', ')

    # pops a card from the deck and returns the card value/suit
    def getCard(self) -> str:
        return self.theDeck.pop()


if __name__ == "__main__":
    player = Player()
    deck = Deck()
    new_game = Game(player, deck)

    while not player.getgamestatus():
        new_game.getDeck()
        player.placebet()
        new_game.dealHand()
        new_game.playHand()  