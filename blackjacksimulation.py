""" A simulation environment for simple blackjack (see blackjack.pdf)
    The state is playerSum in {12-20}, dealerCard in {1-10}, and usableAce (boolean)
    The actions are hit or stick, 1 or 0
"""
 
from numpy import *
from random import *
from scipy import *
 
playerSum = 0
dealerCard = 0
usableAce = False
 
def card ():
    return min(10, randint(1,14))
 
def encode ():
    return 1 + (90 if usableAce else 0) + 9*(dealerCard-1) + (playerSum-12)
     
 
def decode (state):
    global playerSum, dealerCard, usableAce
    if state==0: 
        return
    state = state - 1
    usableAce = state >= 90
    state = state % 90
    dealerCard = 1 + state // 9
    playerSum = (state % 9) + 12
 
def init ():
    global playerSum, dealerCard, usableAce
    playerSum=0
    dealerCard=0
    usableAce=False
    return 0
 
def numActions (s):
    return 2
 
def sample (s, a):
    global playerSum, dealerCard, usableAce
    decode(s)
    if s==0: 
        return firstSample()
    if a==0: 
        return dealerPlaySample()   # sticking
    playerSum += card()                  # hitting
    if playerSum==21: 
        return dealerPlaySample()
    if playerSum > 21:
        if usableAce:
            playerSum -= 10
            usableAce = False
            return 0, encode()
        else:
            return -1, -1
    return 0, encode()
 
def firstSample ():
    global playerSum, dealerCard, usableAce
    """ deal first cards and check for naturals """
    playerCard1 = card()
    playerCard2 = card()
    playerSum = playerCard1 + playerCard2
    usableAce = playerCard1==1 or playerCard2==1
    if usableAce: 
        playerSum += 10
    dealerCard = card()
    if playerSum==21:    # player has natural
        dealerCard2 = card()
        dealerSum = dealerCard + dealerCard2
        if (dealerCard==1 or dealerCard2==1) and dealerSum==11:  # dealer has a natural too
            return 0, -1
        else:
            return 1, -1
    while playerSum < 12: 
        playerSum += card()
    if playerSum==21: 
        return dealerPlaySample()
    return 0, encode()
 
def dealerPlaySample ():
    dealerCard2 = card()
    dealerSum = dealerCard + dealerCard2
    usableAce = dealerCard==1 or dealerCard2==1  # now usableAce refers to the dealer
    if usableAce: dealerSum += 10
    if dealerSum==21: 
        return -1, -1  # dealer has a natural
    while dealerSum < 17:
        dealerSum += card()
        if dealerSum > 21:
            if usableAce:
                dealerSum -= 10
                usableAce = False
            else:
                return 1, -1
    if dealerSum < playerSum: 
        return 1, -1
    elif dealerSum > playerSum: 
        return -1, -1
    else: 
        return 0, -1
 
 
def printPolicy (policy):
    global playerSum, dealerCard, usableAce
    for usableAce in [True, False]:
        print()
        print ("" if usableAce else " No", "Usable Ace:")
        for playerSum in range(20, 11, -1):
            for dealerCard in range(1,11):
                s=encode()
                v=policy(s)
                print ("S" if v==0 else "H",end=" ")
            print (playerSum)
        for dealerCard in range(1,11): 
            print (dealerCard,end=" ")
        print ()
