import blackjack
 
from numpy import *
from random import *
from scipy import *
numEpisodes = 10000000
 
 
def showOneGame():
    s=blackjack.init()
    moves=[0,1,0] 
    turn=0
    e = 0.1
    while s!=-1: #-1 is terminal
        a=moves[turn]
        r,sp=blackjack.sample(s,a)
        print("turn %d: s %d a %d -> r %d sp %d "%(turn,s,a,r,sp),end="")
        print("\t Player Sum: %d  Dealer Card: %d  Usable Ace: %d"%(blackjack.playerSum,blackjack.dealerCard, blackjack.usableAce))
        s=sp
        turn+=1
    return None
 
 
returnSum = 0.0

Q = 0.00001*rand(182 , 2)
Q[0,:] = 0
Q[-1,:] = 0 

for episodeNum in range(numEpisodes):

    G = 0
    s = blackjack.init()
    while s != -1:
    #random.random() gives random number between 0 and 1
    #do argmax on this
        a = random.random()
        e = 0
        if a < e:
            a = random.randint(0,2)
        else:
            a = argmax(Q[s,:])    
        r, sp = blackjack.sample(s,a)
        G += r
        alpha = 0.08
        Q[s,a] = Q[s,a] + alpha * (r + max(Q[sp,:])-Q[s,a]) 
        s = sp
    if episodeNum % 10000 == 0:
        print("Episode: ", episodeNum, "Return: ", G, "Current Average: ", returnSum/numEpisodes)
    returnSum = returnSum + G
blackjack.printPolicy(lambda s : argmax(Q[s,:]))
print("Average return: ", returnSum/numEpisodes)
