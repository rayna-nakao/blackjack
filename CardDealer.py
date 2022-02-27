# Author: Erin Eckerman
# Date: 2/22/22
# Description: Card Dealer is a microservice that continuously watches deck.txt and writes a randomly ordered list of
# cards (without suits) to deck.txt when the file contains only the word 'run'.


import time
import os
from random import shuffle

def watch_file(filename, start, time_limit=3600, check_interval=1):
    # Captures time at which watch begins and returns true if file is modified before time_limit is reached
    last_time = start + time_limit

    while time.time() <= last_time:
        if os.path.getctime(filename) > start:
            return True
        else:
            time.sleep(check_interval)

def check_for_run(filename):
    f_prng = open(filename, 'r')
    content = str.rstrip(f_prng.read())
    f_prng.close()

    return content == 'run'

def generate_deck(filename):
    cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    deck = []

    for i in range(4):
        deck.extend(cards)

    shuffle(deck)
    print(deck)

    # write deck to text file
    deck_file = open(filename, 'w')
    deck_file.write(str(deck))
    deck_file.close()

if __name__ == "__main__":
    # Watch text file for changes
    while True:
        service_start = time.time()
        command_file_changed = watch_file("deck.txt", service_start)
        deck_request = check_for_run("deck.txt")

        if command_file_changed and deck_request:
            generate_deck("deck.txt")
