import numpy as np
import random
import unreal
import time
import os

class Node:
    def __init__(self,x,y,rotation1, rotation2 = None):
        self.x = x
        self.y = y
        self.rotatew1 = rotation1
        self.rotatew2 = rotation2
        
        self.visited = False
        self.deleteWall1Bottom = False
        self.deleteWall2Right = False
        self.isSideWall = False
        self.isDummy = False
    
    def __str__(self):
        wall2_info = f", RC({self.x},{self.y},{self.rotatew2})" if self.rotatew2 != None else ""
        return f"RC({self.x},{self.y}, {self.rotatew1}){wall2_info}"

def parse_randomness(maze,solution_path):
    directions = [(0,1),(1,0),(0,-1),(-1,0)]
    
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            for direction in directions:
                r,c = i+ direction[0], j + direction[1] #maze length returns 10,10
                if 0 <= r < len(maze)-1 and 0 <= c < len(maze[0]) - 1:
                    if maze[r][c] in solution_path or maze[r][c].isSideWall:
                        continue
                    node = maze[r][c]
                    rng = random.randint(0,2)

                    match(rng):
                        case 0:
                            if node.deleteWall2Right == False:
                                node.deleteWall2Right = True
                        case 1:
                            if node.deleteWall2Right == False and node.deleteWall1Bottom == False:
                                node.deleteWall2Right = True
                                node.deleteWall1Bottom = True
                        case _:
                            continue
                
                                      
def generate_maze(row,col):
    maze = []
    print("GEN MAZE")
    maze = [[None for _ in range(row)] for _ in range(col)]
    for i in range(row):
        for j in range(col):
            if (i >= 0 and j == 0): #If the row 0 - MAX and Column 0, Left Wall Only one node    
                if i == row-1:
                    maze[i][j] = Node(i,j,90)
                    maze[i][j].isSideWall = True
                    maze[i][j].isDummy = True
                else:
                    maze[i][j] = Node(i,j,0)
                    maze[i][j].isSideWall = True

            elif(j >=0 and i ==0):
                maze[i][j] = Node(i,j,-90)
                maze[i][j].isSideWall = True
            else:
                two_walls = Node(i,j,180)
                two_walls.rotatew2 = -90
                maze[i][j] = two_walls
    
    for row in maze:
        for node in row:
            print(node)
    return maze
def DFS(maze,start,end): #Make sure to pass in a Node Object from Maze[i][j]
    stack = []
    solution_path = []
    stack.append(start)
    print("Start DFS")
    while stack:
        current = stack.pop()
        if current.visited:
            continue
        current.visited = True
        solution_path.append(current)

        if current == end:
            break
        row,col = current.x, current.y

        neighbor_moves = [
            (row-1 , col), #Up
            (row, col-1),  #Left
            (row+1, col),   #Down
            (row, col+1)   #Right
        ]
        for r,c in neighbor_moves:
            if 0 <= r < len(maze) and 0 <= c < len(maze[0]):
                neighbor = maze[r][c]
                if neighbor == None:
                    continue
                if not neighbor.visited:
                    stack.append(neighbor)
    if not solution_path or solution_path[-1] != end:
        print("No Solution")
        return maze, []
    print("--------------SOLUTION PATH------------------")
    for i in range(len(solution_path)):
        print(solution_path[i])   
    
    return maze, solution_path

def parse_solution(solution_path, maze):
    for p in range(len(solution_path) - 1):
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if maze[i][j] == solution_path[p]:
                    current = maze[i][j]
                    next_cell = solution_path[p+1]
                    x,y = current.x, current.y
                    nx,ny = next_cell.x, next_cell.y
                    if current.isSideWall:
                        third_cell = solution_path[p+2]
                        third_cell.deleteWall2Right = True
                        third_cell.deletWall1Bottom = True
                    if (nx,ny) == (x-1,y): #go right
                        next_cell.deleteWall2Right = True
                    if (nx,ny) == (x+1,y): #go left
                        current.deleteWall2Right = True
                    if (nx,ny) == (x,y-1): #go down
                        next_cell.deleteWall1Bottom = True
                    if (nx,ny) == (x,y+1): #go up
                        current.deleteWall1Bottom = True
                        

def draw_maze(maze_info, row, col, start,end):
    #these where some assets that I made and used but for simplicity I editted them out.
    """ regular_wall = "/Game/StarterContent/Architecture/Stonewall.Stonewall"
    secondary_wall = "/Game/StarterContent/Architecture/Glasswall.Glasswall"
    flag_asset = "/Game/StarterContent/Architecture/SM_Flag.SM_Flag" """
    
    regular_wall = "/Game/StarterContent/Architecture/Wall_400x400.Wall_400x400"
    secondary_wall = "/Game/StarterContent/Architecture/Wall_400x400.Wall_400x400"
    flag_asset = "/Script/Engine.StaticMesh'/Game/StarterContent/Props/SM_PillarFrame.SM_PillarFrame'"
    world = unreal.EditorLevelLibrary.get_editor_world()
    player_start_class = unreal.PlayerStart
    player_start_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(player_start_class, unreal.Vector(start.x * 200,start.y * 200,0), unreal.Rotator(0,0,0))
    cell_size = 400.0
    wall_asset1 = wall_asset = unreal.EditorAssetLibrary.load_asset(regular_wall)
    wall_asset2 = wall_asset = unreal.EditorAssetLibrary.load_asset(secondary_wall)
    for i in range(row):
        for j in range(col):
                if(i == row -1 and j == 0):
                    continue
                x = random.randint(0,30)
                if x > 15:
                    wall_asset = wall_asset1
                else:
                    wall_asset = wall_asset2
                
                position = unreal.Vector(maze_info[i][j].x * cell_size, maze_info[i][j].y * cell_size, 0)
                if maze_info[i][j] == end:
                    flag_assetL = unreal.EditorAssetLibrary.load_asset(flag_asset)
                    flag_position = unreal.Vector(maze_info[i][j].x * cell_size - 200, maze_info[i][j].y*cell_size - 200, 0)
                    flag_actor = unreal.EditorLevelLibrary.spawn_actor_from_object(flag_assetL,flag_position,unreal.Rotator(0,0,0))
                    flag_actor.set_actor_scale3d(unreal.Vector(10.0,10.0,10.0)) 
                if maze[i][j].isDummy:
                    continue
                if maze[i][j].isSideWall: #If the wall is a side wall only make one wall with one rotation
                    unreal.EditorLevelLibrary.spawn_actor_from_object(wall_asset,position,unreal.Rotator(0,0,maze_info[i][j].rotatew1))
                elif maze[i][j].deleteWall1Bottom: #Not Side Wall and delete bottom wall, draw Right wall only
                    unreal.EditorLevelLibrary.spawn_actor_from_object(wall_asset,position,unreal.Rotator(0,0,maze_info[i][j].rotatew2))
                elif maze[i][j].deleteWall2Right: #if we only want the bottom wall just draw the bottom wall 1
                    unreal.EditorLevelLibrary.spawn_actor_from_object(wall_asset,position,unreal.Rotator(0,0,maze_info[i][j].rotatew1))
                else: #If we want both walls because it is not int the path, draw both walls.
                    unreal.EditorLevelLibrary.spawn_actor_from_object(wall_asset,position,unreal.Rotator(0,0,maze_info[i][j].rotatew1))
                    unreal.EditorLevelLibrary.spawn_actor_from_object(wall_asset,position,unreal.Rotator(0,0,maze_info[i][j].rotatew2))
    
                
                
row, col = 10,10
maze = generate_maze(row,col)
start = maze[1][2]
end = maze[9][9]
maze,solution_path = DFS(maze,start,end)
parse_solution(solution_path, maze)
parse_randomness(maze,solution_path)
draw_maze(maze,row,col, start, end)