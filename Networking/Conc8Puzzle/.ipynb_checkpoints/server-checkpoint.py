#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading
import argparse
import sys
import pickle
import string
import random
import csv
import time

player_count = 0
player_count_lock = threading.Lock()
start_game_event = threading.Event()
shuffleAmountMult = random.randint(1,100)
shared_seed = random.randint(1,1000)
def printBoard(ShuffleMe):
    # all this does is prints the given board configuration
    # loops through the 2D array sent to it and just prints the number with a space
    for row in ShuffleMe:
        for num in row:
            print(num," ", end = '')
        print()

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


def startSinglePlayerGame(client_socket, shuffleAmount, goalState):
    shuffledState = shuffleBoard(goalState, shuffleAmount)
    return shuffledState

def startMultiplayerGame(client_socket,shuffleAmount, shared_seed, goalState):
    shuffledState = shuffleBoardMultiplayer(goalState,shuffleAmount,shared_seed)
    return shuffledState

def stateToString2D(state):
    stateToString = "" 
    endStateFlag = 0
    for row in state:
        for num in row:
            stateToString += str(num)
        endStateFlag +=1
        if(endStateFlag < 3):
            stateToString += "\n"
    return stateToString

def stateToString1D(lst):
    result = ""
    for i, value in enumerate(lst, 1):
        result += str(value)
        if i % 3 == 0 and i != len(lst):
            result += "\n"
        else:
            result += " "
    return result


def shuffleBoard(initialState, shuffles):
    possibleMoves = [(-1,0),(1,0),(0,-1),(0,1)]
    MAX_LENGTH = 8
    num_shuffles = shuffles
    
    random.seed(shuffles + 10) #initialze a random seed using the amount of shuffles + 10
    for _ in range(num_shuffles):
        # This randomly selects an item on the list of possibleMoves
        # This effectively chooses which direction a tile is slid
        randomMove = random.choice(possibleMoves)
        
        #Find index of the empty tile denoted by a 0
        startIndex = initialState.index(0)
        
        emptyRow = startIndex // 3
        emptyCol = startIndex % 3

        nextRow = emptyRow + randomMove[0]
        nextCol = emptyCol + randomMove[1]

        if(0 <= nextRow < 3 and 0 <= nextCol < 3):
            endIndex = nextRow*3 + nextCol
            temp = initialState[startIndex]
            initialState[startIndex] = initialState[endIndex]
            initialState[endIndex] = temp 
    return initialState


def shuffleBoardMultiplayer(initialState, shuffles, shared_seed):
    possibleMoves = [(-1,0),(1,0),(0,-1),(0,1)]
    MAX_LENGTH = 8
    num_shuffles = shuffles
    
    random.seed(shared_seed) #initialze a random seed using the amount of shuffles + 10
    for _ in range(num_shuffles):
        # This randomly selects an item on the list of possibleMoves
        # This effectively chooses which direction a tile is slid
        randomMove = random.choice(possibleMoves)
        
        #Find index of the empty tile denoted by a 0
        startIndex = initialState.index(0)
        
        emptyRow = startIndex // 3
        emptyCol = startIndex % 3

        nextRow = emptyRow + randomMove[0]
        nextCol = emptyCol + randomMove[1]

        if(0 <= nextRow < 3 and 0 <= nextCol < 3):
            endIndex = nextRow*3 + nextCol
            temp = initialState[startIndex]
            initialState[startIndex] = initialState[endIndex]
            initialState[endIndex] = temp 
    return initialState

def flatten_2d_list(matrix):
    return [element for row in matrix for element in row]

def write_to_csv(name, score):
    with open('highscores.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, score])

def read_and_return_HS():
    try:
        with open('highscores.csv', 'r') as file:
            reader = csv.reader(file)
            highscores = list(reader)

            # Sort the high scores based on the second column (score)
            sorted_highscores = sorted(highscores, key=lambda x: int(x[0]))

            high_scores_string = "High Scores:\n"
            for rank, (name, score) in enumerate(sorted_highscores, start=1):
                high_scores_string += f"{rank}. {name}: {score}\n"
    except FileNotFoundError:
        high_scores_string = "No highscores found."
    return high_scores_string




def mainServerFunction(client_socket):
    global player_count, player_count_lock
    goalState = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    goalState = flatten_2d_list(goalState)
    response = stateToString1D(goalState)
    client_socket.send(response.encode('utf-8'))
    done = False
    
    while not done:
        choice = client_socket.recv(1024).decode('utf-8')
        if choice == '2':
            shuffleAmount = int(client_socket.recv(1024).decode('utf-8'))
            shuffledState = startSinglePlayerGame(client_socket, shuffleAmount, goalState)
            sendState = stateToString1D(shuffledState)
            client_socket.send(sendState.encode('utf-8'))
            score = client_socket.recv(1024).decode('utf-8')
            name = client_socket.recv(1024).decode('utf-8')
            write_to_csv(name,score)
            highscores = read_and_return_HS()
            client_socket.send(highscores.encode('utf-8'))
            
        elif choice == '3':
            global shared_seed, shuffleAmountMult
            
            
            client_socket.send("Player 2 has joined...Starting Game".encode('utf-8'))
        
            
            shuffledState = startMultiplayerGame(client_socket, shuffleAmountMult, shared_seed, goalState)
            sendState = stateToString1D(shuffledState)
            client_socket.send(sendState.encode('utf-8'))

           
            score = client_socket.recv(1024).decode('utf-8')
            name = client_socket.recv(1024).decode('utf-8')
            write_to_csv(name,score)
            highscores = read_and_return_HS()
            client_socket.send(highscores.encode('utf-8'))

        elif choice == '4':
            done = True


    
def handle_client(client_socket):
    request = client_socket.recv(1024)
    print(f"Message from Client: {request.decode('utf-8')}")
    mainServerFunction(client_socket)
    client_socket.close()


def main():
    parser = argparse.ArgumentParser(description = 'Concurrent 8 Puzzle Server')
    parser.add_argument('--host', default = '127.0.0.1' ,help = 'Example: --host 127.0.0.1')
    parser.add_argument('--port', help = 'Example: -- host 127.0.0.1 --port 3240')
    args = parser.parse_args()

    if(args.host == 'localhost'):
        args.host = '127.0.0.1'
    server_address = (args.host,int(args.port))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_socket.bind(server_address)
    server_socket.listen(5)

    print(f"Server listening on {server_address[0]}:{server_address[1]}")
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
            
            client_handler = threading.Thread(target = handle_client, args = (client_socket,))
            client_handler.start()
    
    except KeyboardInterrupt:
        print("Server Shutting Down")
        server_socket.close()



if __name__ == "__main__":
    main()