import random
import sys

def shuffleBoard(ShuffleMe, shuffles):
    #print("Shuffle Start")
    #define the range of numbers we are allowed to shuffle by
    # This is from 0-8 because we have 9 numbers indexed to 0 so 0-8 are the indices
    min = 0
    max = 8
    # count var for debugging
    count = 0

    startIndex = 0
    endIndex = 0
    # Loop to generate a random number "Shuffles" amount of times, which is passed as an argument from stdin 
    # The Index's are then swapped and effectively shuffled
    for _ in range(shuffles):
        endIndex = random.randint(min,max)
        temp = ShuffleMe[startIndex]
        ShuffleMe[startIndex] = ShuffleMe[endIndex]
        ShuffleMe[endIndex] = temp
        count+=1
    #set an index
    indexCount = 0
    for x in ShuffleMe:
        if(indexCount < 2):
            print(ShuffleMe[x]," ", end = '')
            indexCount += 1
        else:
            print(ShuffleMe[x]," ")
            indexCount = 0
    #print("Shuffles Completed: ", count, " times.")

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
    
    shuffleBoard(initialArray,shuffles)
    #print("Total Count is : ", count)
    goalState.close()
    #print("Close Completed")

main()