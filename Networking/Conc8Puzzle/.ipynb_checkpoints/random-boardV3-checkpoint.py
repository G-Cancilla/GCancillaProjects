import random
import sys

def shuffleBoard(ShuffleMe, shuffles):
    possibleMoves = [(-1,0),(1,0),(0,-1),(0,1)]
    MAX_LENGTH = 8
    num_shuffles = shuffles

    for _ in range(num_shuffles):
        # This randomly selects an item on the list of possibleMoves
        # This effectively chooses which direction a tile is slid
        randomMove = random.choice(possibleMoves)
        
        #Find index of the empty tile denoted by a 0
        startIndex = ShuffleMe.index(0)
        
        emptyRow = startIndex // 3
        emptyCol = startIndex % 3

        nextRow = emptyRow + randomMove[0]
        nextCol = emptyCol + randomMove[1]

        if(0 <= nextRow < 3 and 0 <= nextCol < 3):
            endIndex = nextRow*3 + nextCol
            temp = ShuffleMe[startIndex]
            ShuffleMe[startIndex] = ShuffleMe[endIndex]
            ShuffleMe[endIndex] = temp 
    return ShuffleMe

def inversions(arr):
    inv_count = 0
    empty_value = -1
    for i in range(0, 9):
        for j in range(i + 1, 9):
            if arr[j] != empty_value and arr[i] != empty_value and arr[i] > arr[j]:
                inv_count += 1
    return inv_count

def isSolvable(puzzle) :
    # Count inversions in given 8 puzzle
    inv_count = inversions([j for sub in puzzle for j in sub])
    return inv_count %2 ==0

def printBoard(ShuffleMe):
    for row in ShuffleMe:
        for value in row:
            print(value," ", end='')
        print()



    
def main():
    #Seperate the arguments, they will be input as strings, so file doesnt need anything extra
    goalState= open(sys.argv[1], 'r')

    #Import seed number Arg 2 cast to an integer
    randNumSeedGen = int(sys.argv[2])

    #Import random shuffle amount, cast to integer
    shuffles = int(sys.argv[3])

    alwaysSolvable = [ [1,2,3],[4,5,6],[0,7,8]]
    #print("file: ", goalState)
    #print("Seed: ", randNumSeedGen)
    #print("Shuffles: ", shuffles)

    #Set the seed from arguments
    random.seed(randNumSeedGen)
    
    #count = 0
    initialArray = []
    #print("Begin filling Initial Array")
    for numberString in goalState.read():
        if not numberString.isspace():
            initialArray.append(int(numberString))
            #print("Index: ", count, "Number:", initialArray[count]) #This initializes the OLA-1 Input to the goal state [0,1,2,3,4,5,6,7,8]
            #Initial Array Contents
            # 0    1    2
            # 3    4    5
            # 6    7    8
            #count+=1
    shuffledBoard = [initialArray[i:i + 3] for i in range(0, 9, 3)]
    shuffledBoard = shuffleBoard(shuffledBoard,shuffles)
    if not (isSolvable(shuffledBoard)):
        printBoard(alwaysSolvable)
    else:
        printBoard(shuffledBoard)
    
    """
    reshuffle = 0
    while True:
        shuffledBoard = shuffleBoard(shuffledBoard,shuffles+reshuffle)
        reshuffle+=1
        if isSolvable(shuffledBoard):
            break
        reshuffle+=1
    """
    #print("Total Count is : ", count)
    goalState.close()
    #print("Close Completed")

main()