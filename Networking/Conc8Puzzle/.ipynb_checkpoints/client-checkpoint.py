#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading
import argparse
import sys
import time


game_event_finished = threading.Event()
def Rules(goalState):
    print()
    print()
    print("---------RULE SECTION----------")
    print("The 8 puzzle game is a game in which you need to get the orientation of the puzzle to be")
    print_2d_list(goalState)
    print("The zero in our case represents an empty tile and you must make a series of slides in order to get it into the correct orientation.")
    print()
    print("You cannot wrap around and you must stay within the puzzles boundaries.")
    print("This means that valid moves are Up-Down-Left-Right, depending on the slot that the Zero is in.")
    print("If the empty spot (the zero) is in the middle all moves are valid.")
    print("However, if the zero is not in the middle and is on a corner, then you may not move the zero across the border around to the other side.")
    print()
    print("For example, although the example shown is in the Goal Orientation. Valid moves for the zero would be down or right.")
    print("Your aim is to get the lowest score possible. The more moves you make the higher your score is and the worse you do. When playing in multiplayer the player with the lowest score will win.")
    print()
    print("---------END RULE SECTION----------")
    print("Returning to Main Menu...")
    print()
    print()
    time.sleep(5)
def string_to_2d_list(s):
    return [[int(num) for num in row.split()] for row in s.split('\n')]

def print_2d_list(matrix):
    for row in matrix:
        for value in row:
            print(value, end=' ')
        print()

def find_empty_tile(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                return i, j
    # If the empty tile is not found (which should not happen in a valid board), return None
    return None

def is_valid_move(board,move):
    
    zero_row, zero_col = find_empty_tile(board)
    if(move == "up" and zero_row > 0):
        return True
    elif(move == "down" and zero_row < 2):
        return True
    elif(move == "left" and zero_col > 0):
        return True
    elif(move == "right" and zero_col < 2):
        return True
    else:
        return False
def checkCompletion(boardState,goalState):
    if(boardState == goalState):
        return True
    else:
        return False
def apply_move(board, move):
    empty_row, empty_col = find_empty_tile(board)

    if move == 'up' and empty_row > 0:
        board[empty_row][empty_col], board[empty_row - 1][empty_col] = board[empty_row - 1][empty_col], board[empty_row][empty_col]
    elif move == 'down' and empty_row < 2:
        board[empty_row][empty_col], board[empty_row + 1][empty_col] = board[empty_row + 1][empty_col], board[empty_row][empty_col]
    elif move == 'left' and empty_col > 0:
        board[empty_row][empty_col], board[empty_row][empty_col - 1] = board[empty_row][empty_col - 1], board[empty_row][empty_col]
    elif move == 'right' and empty_col < 2:
        board[empty_row][empty_col], board[empty_row][empty_col + 1] = board[empty_row][empty_col + 1], board[empty_row][empty_col]

    return board

def playGame(startBoard, client_socket, goalConfig):
    boardState = string_to_2d_list(startBoard)
    completed = False
    score = 0
    while(completed != True):
        print("--------Goal Configuration-------")
        print_2d_list(goalConfig)
        print()
        print()
        
        print("*******Current Board State*******")
        print_2d_list(boardState)
        print()
        print()
        print("Enter a valid move (up,down,left,right, Q to Quit): ", end = '')
        move = input().lower()
        if (move == "q"):
            score = 1000
            completed = True
        if(is_valid_move(boardState,move)):
            apply_move(boardState,move)
            score += 1
            completed = checkCompletion(boardState,goalConfig)
        elif(move != "q"):
            print("Invalid Move. Please enter a valid direction. Score + 1")
            print()
            score +=1
            time.sleep(3)
    
    print("Game Completed!")
    print_2d_list(boardState)
    print("Score:", score)
    name = input("Please Enter Your Name: " )
    client_socket.send(name.encode('utf-8'))
    client_socket.send(str(score).encode('utf-8')) #send the final score to server
    highscoreString = client_socket.recv(1024).decode('utf-8')
    print(highscoreString)

        

def Menu(goalState,client_socket):
    done = False
    while(done != True):
        print("-----------8 Puzzle Game Menu-----------")
        print()
        print()
        print("Pick an Option 1-5")
        print("Option 1: 8-Puzzle Game Rules")
        print("Option 2: Single Player")
        print("Option 3: Multiplayer")
        print("Option 4: Exit Game")
        print()
        choice = input("Option Choice: ")
        client_socket.send(choice.encode('utf-8'))
        if(choice == '1'):
            Rules(goalState)
        if(choice == '2'):
            print("Starting Single Player Game...")
            print()
            print("Please enter a number 1-100, this will shuffle the initial board.")
            shuffleAmount = input()
            client_socket.send(shuffleAmount.encode('utf-8'))
            startBoard = client_socket.recv(1024).decode('utf-8') #now we need to recieve the board and then process the board in client file, then send the score to the Server.
            playGame(startBoard,client_socket,goalState)
        
        if (choice == '3'):
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
            if message == "Player 2 has joined...Starting Game":
                print("Starting Multiplayer Game...")
                print()
                startBoard = client_socket.recv(1024).decode('utf-8')
                playGame(startBoard,client_socket,goalState)
                
        if(choice == '4'):
            done = True
            client_socket.send(choice.encode('utf-8'))
    
def main():
    parser = argparse.ArgumentParser(description = 'Concurrent 8 Puzzle Server')
    parser.add_argument('--host', default = '127.0.0.1' ,help = 'Example: --host 127.0.0.1')
    parser.add_argument('--port', help = 'Example: -- host 127.0.0.1 --port 3240')
    args = parser.parse_args() 
    
    if(args.host == 'localhost'):
        args.host = '127.0.0.1'
    
    server_address = (args.host,int(args.port))
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)
    try:
        print(f"Accepted connection from {server_address[0]}:{server_address[1]}")
        message = "Connected to the server successfully"
        client_socket.send(message.encode('utf-8'))
        
        goalState = client_socket.recv(1024).decode('utf-8')
        goalState = string_to_2d_list(goalState)
        Menu(goalState,client_socket)
    
    finally:
        client_socket.close()





if __name__ == "__main__":
    main()