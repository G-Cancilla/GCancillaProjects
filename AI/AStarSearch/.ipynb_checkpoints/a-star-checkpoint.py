#!/opt/conda/bin/python
import sys
import heapq
import math

def printBoard(ShuffleMe):
    # all this does is prints the given board configuration
    # loops through the 2D array sent to it and just prints the number with a space
    for row in ShuffleMe:
        for num in row:
            print(num," ", end = '')
        print()

class Node:
    # Our constructor function just takes all of the values we want to store in a single Node and sets them
    def __init__(self,state,depth,uniqueID,fvalue, parent = None):
        #uniqueID to store the ID's of all nodes.
        self.uniqueID = uniqueID
        
        #2D array to describe the state space of the 8 puzzle
        self.state = state
        
        # depth of node
        self.depth = depth
        
        # heuristic value calculated in the Fvalue function
        self.fvalue = fvalue
        
        #pointer to the previous node
        self.parent = parent
    
    # This helps us keep track of the 0 in the state by going through the state and finding its location
    # Using enumerate() we can find the row and column and then just return those to the function caller
    def findZero(self, state):
        for rowNum, rows in enumerate(state):
            for colNum, cols in enumerate(rows):
                if(state[rowNum][colNum] == 0):
                    return rowNum,colNum

    #Generates Children Nodes (A.k.a all other possible states) 
    def generateChildNode(self, currentNode):
        #first we find the x position and y position of the 0
        xPos,yPos = self.findZero(self.state)
        #we grab the node we passed in's ID as we will need to increment it for the children nodes
        newID = currentNode.uniqueID
        Moves = [[xPos,yPos-1],[xPos,yPos+1],[xPos-1,yPos],[xPos+1,yPos]]
        #y+1 = up one
        #y-1 = down one
        #x+1 = right 1
        #x-1 = left 1
        children = []

        #loop to pick a movement ->> see MakeMovement() method function
        #It will try to make every possible movement then check if it is a valid move
        for i in Moves:
            #This either returns a state or None  
            child = self.MakeMovement(self.state,xPos,yPos,i[0],i[1])
            
            #MakeMovement will return none if it is an invalid move
            #So if MakeMovement doesnt return None then we will make a new child node with the new state
            if child is not None:
                newID += 1
                newChild = Node(child,self.depth+1,newID,0, parent = self)
                children.append(newChild)
       
        
        return children
    # Choosing Valid Movements
    def MakeMovement(self,state,x1,y1,x2,y2):
        #if the movements are out of bounds then we need to return None
        #If it is a valid move then we need to shift the current state by performing a swap
        #This works for all sizes of puzzle as well
        if(x2 >= 0 and x2 < len(self.state) and y2 >= 0 and y2 < len(self.state)):
            temp1 = []
            temp1 = self.copy(state)
            temp = temp1[x2][y2]
            temp1[x2][y2] = temp1[x1][y1]
            temp1[x1][y1] = temp
            return temp1
        else:
            return None

    #copy function to copy the state to a list and then return that list as a 2D array
    def copy(self,ParentNode):
        temp = []
        for i in ParentNode:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp
        
    
#heuristic = h-score + g-score 
# h-score: how far the goal node is 
# g-score: number of nodes traversed from a start node to get to the current node

#Calculating the heuristic functions, also determined by choice which is why we pass choice
def fval(initialNode,goalState,choice):
    fvalue = 0
    if(choice == 0):
        #h(n) = 0
        fvalue = initialNode.depth
    if(choice == 1):
        #call Displaced Tiles
        fvalue = displacedTiles(initialNode,goalState)+initialNode.depth
    if(choice == 2):
        #Call Manhatten Distance
        fvalue = ManhattenDistanceHeuristic(initialNode,goalState)+initialNode.depth
    if(choice == 3):
        #User Defined Implementation
        # I just took the average of the displaced tiles and manhatten distance and added the f(n)
        manhatten = ManhattenDistanceHeuristic(initialNode,goalState)
        displaced = displacedTiles(initialNode,goalState)
        hattenplaced = (manhatten+displaced)//2
        fvalue = hattenplaced + initialNode.depth
    return fvalue


def displacedTiles(initialNode,goalArray):
    #to find the displaced nodes all we do is just compare the initial state with the goal state
    #Any number that is not the same we just add one to the displacement counter
    displacement = 0
    for i in range(3):
        for j in range(3):
            if (initialNode.state[i][j] != goalArray[i][j]):
                displacement +=1
    return displacement

def ManhattenDistanceHeuristic(initialNode,goalArray):
    #This one was fun
    
    #total distance and goal positions are set
    total_distance = 0
    goalPositions = {}
    #find the x,y coordinates of the goal state  
    for i in range(3):
        for j in range(3):
            goalPositions[goalArray[i][j]] = (i,j)
    #now that we have the goal positions we need to find the block distance
    for i in range(3):
        for j in range(3):
            #set tile to be the states of the shuffled board
            tile = initialNode.state[i][j]
            #if the tile isnt the location of the 0
            if tile != 0:
                #set the goal row and goal col 
                goal_row,goal_col = goalPositions[tile]
                #calc Manhatten Distance
                total_distance += abs(i - goal_row)+abs(j-goal_col)
    return total_distance

#This is the most fun function
#This is the function that checks if the node we pass it is the goal state!
#We return a boolean "yay" which can be True which means it is the goal  yay == :) 
#If yay is false we are sad and need to continue searching the tree      not yay  == >:(
def isGoal(check,goal):
    yay = True
    for i in range(3):
        for j in range(3):
            if(check[i][j] != goal[i][j]):
              yay = False  
    return yay

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
    
def main():
    #remember when accessing a 2D array that array[row][column] ->   down
    
    #Define the goal state
    #We arent required to read the goal state from any files so we must define it here
    #We are required to read the goal state when making our boards though
    #If i am misinterpreting that, welp thats probably -points 
    goalState = [[0,1,2],[3,4,5],[6,7,8]]
    
    startState = []
    #choose which heuristic to use passed as a cmd line arg
    hChoice = int(sys.argv[1])
    # find the start state passed from stdin
    
    for line in sys.stdin:
        #split the whitespace
        number = line.split()
        
        #find row and column and cast to int because stdin will be in the form of string 
        #This is us making our initial State 2D array (3x3)
        row = [int(number[i]) for i in range(3)]
        startState.append(row)
    
    #Initialize frontier and closedList
    #I use the closedList as a set because there are some nice comparison functions that can be used with a set
    #Frontier is just a list of nodes so it doesnt HAVE to be a set, but you could make it a set
    frontier = []
    closedList = set()


    #Make the first node in the list! which holds all of the following info
    #(state,depth,uniqueID,fvalue, parent = None)
    #This is the root node
    startNode = Node(startState,0,0,hChoice,None)
    
    #set the fvalue of the node and add it to the frontier
    startNode.fvalue = fval(startNode,goalState, hChoice)
    frontier.append(startNode)

    #these are just variables we use to print some stats at the end, ignore for now
    totalNodesExpanded = 0
    closedListSize = 0
    optimalDepth = 0
    childNodeCount = 0
    maxDepth = 1
    unsolve = 0
    #NOW FOR THE FUN PART
    #This is the implementation I went with for A* search
    
    while True:
        #pop the first element off the array (iteration 1 = root node)
        current = frontier.pop(0)
        #now we need to check and see if the node we popped off is in the closed list    
        
        # if current is in the closedList then Continue on to the next iteration 
        
        if tuple(map(tuple, current.state)) in closedList:
            continue
        #so if it isnt in the closed list we check if it is the goal
        # does yay return true?
        if(isGoal(current.state,goalState)):
            optimalDepth = current.depth
            maxMemoryNodes = totalNodesExpanded + closedListSize
            branching_factor = childNodeCount/maxMemoryNodes
            print("V=" , totalNodesExpanded)
            print("N=", maxMemoryNodes)
            print("d=", optimalDepth)
            print("b: {:.5f}".format(branching_factor))
            print()
            path = []
            while current is not None:
                path.append(current)
                current = current.parent
            path.reverse()
            for node in path:
                printBoard(node.state)
                print()
            break
        
        #if it isnt the goal then we need to expand it so we add 1 to the total expanded Nodes
        totalNodesExpanded +=1
        #for loop to expand our children nodes
        children = current.generateChildNode(current)
        for i in children:
            #then we update their fvalues
            #remember we return children as a list of nodes so current.generateChildNode(current) returns a list of children Nodes
            #then those children nodes have their f values updated and are added to the frontier
       
    
            
            i.fvalue = fval(i,goalState, hChoice)
            frontier.append(i)
            
        
        #the child node count is just the len of the list!
        #Add this counter like where it just goes up.
        childNodeCount += len(current.generateChildNode(current))
        #find the max depth that we go down
        if current.depth > maxDepth:
            maxDepth = current.depth
        #so we add current to the closedList here and increment the closed list size
        closedList.add(tuple(map(tuple, current.state)))
        closedListSize +=1



        #this is important, this is the INFORMED part
        #Sort the frontier based off of the lower Fvalue and if there is a tie you sort by the newest node
        #The newest node is the node with the lower uniqueID
        #So the next node to check in the frontier is going to be at Index 0, and when we go back up to current to update it
        # we just pop off the first element in the frontier and do the processing again.
        frontier.sort(key=lambda node: (node.fvalue, node.uniqueID))
 
main()