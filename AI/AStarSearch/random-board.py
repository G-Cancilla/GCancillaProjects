#!/opt/conda/bin/python

import random
import sys

def shuffleBoard(ShuffleMe, shuffles):
    possibleMoves = [(-1,0),(1,0),(0,-1),(0,1)]
    MAX_LENGTH = 8
    num_shuffles = shuffles
    for _ in range(num_shuffles):
        randomMove = random.choice(possibleMoves)
        for i in range(3):
            for j in range(3):
                if ShuffleMe[i][j] == 0:
                    emptyRow,emptyCol = i,j
                    break
        
        nextRow = emptyRow + randomMove[0]
        nextCol = emptyCol+ randomMove[1]
        
        if 0 <= nextRow < 3 and 0 <=nextCol < 3:
            temp = ShuffleMe[emptyRow][emptyCol]
            ShuffleMe[emptyRow][emptyCol] = ShuffleMe[nextRow][nextCol]
            ShuffleMe[nextRow][nextCol] = temp
    
    return ShuffleMe

def inversions(arr):
    inversions = 0
    for i in range(len(arr)):
        if arr[i] == 0:
            continue
        for j in range(i+1, len(arr)):
            if(arr[j] == 0):
                continue
            if(arr[i] > arr[j]):
                inversions += 1
    return inversions

def isSolvable(puzzle) :
    # Count inversions in given 8 puzzle
    inv_count = inversions(puzzle)
    return inv_count % 2 ==0

def printBoard(ShuffleMe):
    for row in ShuffleMe:
        for num in row:
            print(num," ", end = '')
        print()

    
def main():
    #Seperate the arguments, they will be input as strings, so file doesnt need anything extra
    goalState= open(sys.argv[1], 'r')

    #Import seed number Arg 2 cast to an integer
    randNumSeedGen = int(sys.argv[2])

    #Import random shuffle amount, cast to integer
    shuffles = int(sys.argv[3])
    
    #print("file: ", goalState)
    #print("Seed: ", randNumSeedGen)
    #print("Shuffles: ", shuffles)

    #Set the seed from arguments
    random.seed(randNumSeedGen)
    
    #count = 0
    initialArray = []
    initial2D = [[0,0,0],[0,0,0],[0,0,0]]
    count = 0
    #print("Begin filling Initial Array")
    for numberString in goalState.read():
        if not numberString.isspace():
            row = count//3
            col = count %3
            initial2D[row][col] = int(numberString)
            count+=1
            #print("Index: ", count, "Number:", initialArray[count]) #This initializes the OLA-1 Input to the goal state [0,1,2,3,4,5,6,7,8]
            #Initial Array Contents
            # 0    1    2
            # 3    4    5
            # 6    7    8
            #count+=1
    shuffledBoard = shuffleBoard(initial2D,shuffles)
    reshuffle = 0
    while True:
        if isSolvable(shuffledBoard):
            break
        else:
            reshuffle+=1
            shuffledBoard = shuffleBoard(shuffledBoard,shuffles+reshuffle)
        
    printBoard(shuffledBoard)
    #print("Total Count is : ", count)
    goalState.close()
    #print("Close Completed")

main()