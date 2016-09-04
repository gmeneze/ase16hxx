"""This module contains code from
Think Python by Allen B. Downey
http://thinkpython.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

"""
from __future__ import division,print_function
import sys,re,traceback,random,string
sys.dont_write_bytecode=True

from Card import *

class Hist(object):
    """Represents a hand of playing cards."""
    
    def __init__(self):
        self.hand_count = {'straightflush' : 0, 'fourkind' : 0, 'fullhouse' : 0, 'flush' : 0, 'straight' : 0, 'threekind' : 0, 'twopair' : 0, 'pair' : 0, 'no_pair' : 0}

class PokerHand(Hand):
    #hand_count = {'straightflush' : 0, 'fourkind' : 0, 'fullhouse' : 0, 'flush' : 0, 'straight' : 0, 'threekind' : 0, 'twopair' : 0, 'pair' : 0, 'no_pair' : 0} 
    def suit_hist(self):
        """Builds a histogram of the suits that appear in the hand.

        Stores the result in attribute suits.
        """
        self.suits = {}
        for card in self.cards:
            self.suits[card.suit] = self.suits.get(card.suit, 0) + 1

    def rank_hist(self):
        """Builds a histogram of the ranks that appear in the hand.

        Stores the result in attribute ranks.
        """       
        self.ranks = {}
        for card in self.cards:
            self.ranks[card.rank] = self.ranks.get(card.rank, 0) + 1 

    def has_flush(self):
        """Returns True if the hand has a flush, False otherwise.
      
        Note that this works correctly for hands with more than 5 cards.
        """

        if len(self.suits) == 0:
            self.suit_hist()
        for val in self.suits.values():
            if val >= 5:
                return True
        return False

    def has_pair(self):
        """Returns True if the hand has a pair, False otherwise. """
        if len(self.ranks) == 0:
            self.rank_hist()
        for val in self.ranks.values():
            if val >= 2:
                return True
        return False

    def has_twopair(self):
        """Returns True if the hand has a two pair, False otherwise. """
        if len(self.ranks) == 0:
            self.rank_hist()
        pair_counter = 0
        for val in self.ranks.values():
            if val >= 2:
                pair_counter += 1
            if pair_counter >= 2:
                return True
        return False

    def has_threekind(self):
        """Returns True if the hand has three of a kind, False otherwise. """
        if len(self.ranks) == 0:
            self.rank_hist()
        for val in self.ranks.values():
            if val >= 3:
                return True
        return False

    def has_straight(self):
        """Returns True if the hand is a straight hand, False otherwise. """
        straight_count = 0
        prev = -2
        if len(self.ranks) == 0:
            self.rank_hist()
        key_list = list(self.ranks.keys())
        key_list.sort()

        for val in key_list:
            if self.ranks.get(val, 0) > 0:
                if val == prev+1:
                    straight_count += 1
                else:
                    straight_count = 1
            if straight_count >= 5:
                return True
            prev = val

        return False

    def has_fullhouse(self):
        """Returns True if the hand has a full house, False otherwise. """
        if len(self.ranks) == 0:
            self.rank_hist()
        two_counter = 0
        three_counter = 0
        for val in self.ranks.values():
            if val == 2:
                two_counter += 1
            if val == 3:
                three_counter += 1

        if two_counter >= 1 and three_counter >= 1:
            return True
        else:
            return False

    def has_fourkind(self):
        """Returns True if the hand has a four of a kind, False otherwise. """
        if len(self.ranks) == 0:
            self.rank_hist()
        for val in self.ranks.values():
            if val >= 4:
                return True
        return False

    def has_straightflush(self):
        """Returns True if the hand has a straight flush, False otherwise. """
        def analyze(rank_list):
            rank_list.sort()
            straight_count = 0
            prev_rank = -2
            for val in rank_list:
    
                if val == prev_rank + 1:
                    straight_count += 1
                    if straight_count >= 5:
                        return True
                else:
                    straight_count = 1
                prev_rank = val

            if straight_count >= 5:
                return True
            return False

        self.cards.sort()
        rank_list=[]
        prev_suit = -1
        for card in self.cards:
            if prev_suit == -1:
                rank_list.append(card.rank)
            elif card.suit == prev_suit:
                rank_list.append(card.rank)
            elif len(rank_list) >= 5:
                if analyze(rank_list):
                    return True
            else:
                del rank_list[:]  
                rank_list.append(card.rank)
            prev_suit = card.suit

        if analyze(rank_list):
            return True
        return False         

    def classify(self, hist):
        self.suit_hist()
        self.rank_hist()

        if self.has_straightflush():
            self.label = "straight flush"
            hist.hand_count['straightflush'] += 1
        elif self.has_fourkind():
            self.label = "four of a kind"
            hist.hand_count['fourkind'] += 1  
        elif self.has_fullhouse():
            self.label = "full house"
            hist.hand_count['fullhouse'] += 1
        elif self.has_flush():
            self.label = "flush"
            hist.hand_count['flush'] += 1
        elif self.has_straight():
            self.label = "straight"
            hist.hand_count['straight'] += 1
        elif self.has_threekind():
            self.label = "three of a kind"
            hist.hand_count['threekind'] += 1
        elif self.has_twopair():
            self.label = "two pair"
            hist.hand_count['twopair'] += 1
        elif self.has_pair():
            self.label = "pair"
            hist.hand_count['pair'] += 1
        else:
            self.label = "no pair"
            hist.hand_count['no_pair'] += 1


if __name__ == '__main__':
    hist = Hist()
    deck_count = 1000
    hand_size = 7
    hand_count = int(52/7)
    for i in range(deck_count):
        # make a deck
        deck = Deck()
        deck.shuffle()

        # deal the cards and classify the hands

        for i in range(hand_count):
            hand = PokerHand()
            deck.move_cards(hand, 7)
            hand.sort()
            print(hand)
            hand.classify(hist)
            print("label is: ", hand.label)
            print("==============================")

    total_attempts = deck_count * hand_count

    print("total number of hands tested: %d, hand size: %d" % (total_attempts, hand_size))

    for poker_hand in hist.hand_count.keys():
        if hist.hand_count[poker_hand]==0:
            continue
        print("%s, number of favorable outcomes: %d probability is: %5.2f%%" % (poker_hand,hist.hand_count[poker_hand], hist.hand_count[poker_hand] * 100/total_attempts)) 

