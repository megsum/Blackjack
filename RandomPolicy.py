import blackjack
 
from numpy import *
from random import *
from scipy import *
numEpisodes = 20
 
 
def showOneGame():
    s=blackjack.init()
    moves=[0,1,0] 
    turn=0
    while s!=-1: #-1 is terminal
        a=moves[turn]
        r,sp=blackjack.sample(s,a)
        print("turn %d: s %d a %d -> r %d sp %d "%(turn,s,a,r,sp),end="")
        print("\t Player Sum: %d  Dealer Card: %d  Usable Ace: %d"%(blackjack.playerSum,blackjack.dealerCard, blackjack.usableAce))
        s=sp
        turn+=1
    return None
 
 
returnSum = 0.0
for episodeNum in range(numEpisodes):
    G = 0
    #
    ...
    print("Episode: ", episodeNum, "Return: ", G)
    returnSum = returnSum + G
blackjack.printPolicy()
print("Average return: ", returnSum/numEpisodes)
