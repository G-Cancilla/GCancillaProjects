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

def printBoard(state):
    for x in state:
        print(x)

def main():
    check = [[4,2,8],[5,7,1],[0,3,6]]

    if(isSolvable(check)):
        print("Solvable")
        printBoard(check)
    else:
        print("Unsolvable")
        printBoard(check)
main()