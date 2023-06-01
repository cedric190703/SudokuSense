import time
# Algorithm for the backtracking for the solver
# Sudoku grids are of sized 9x9
Num = 9

# Function to find the first empty case in the grid
def getLocation(grid):
    for i in range(Num):
        for j in range(Num):
            if(grid[i][j] == 0):
                return (i,j)
            
    # Grid is full        
    return (-1,-1)

# Function to check if the position is correct for the num
def checkPos(grid, row, col, num):
    # Check if the column position is correct
    # Check if the row position is correct
    for i in range(Num):
        if(grid[row][i] == num or grid[i][col] == num):
            return False
        
    row -= row % 3
    col -= col % 3

    # Check if the block (3 x 3) position is correct
    for i in range(3):
        for j in range(3):
            if(grid[i+row][j+col] == num):
                return False
    
    # The position of the number is safe
    return True

# Check if the full grid is correct
def correctGrid(grid):
    for i in range(Num):
        for j in range(Num):
            num = grid[i][j]
            grid[i][j] = 0
            if(not checkPos(grid, i, j, num)):
                return False
            grid[i][j] = num
    return True

# This function do the backtracking
def backtracking(grid):
    # Find an empty case
    row, col = getLocation(grid)
    if(row == -1):
        return (1, grid)
    
    # Try to fill with a digit bewteen 1 and 9
    for num in range(1, 10):
        if(checkPos(grid, row, col, num)):
            # Position in the grid is correct
            grid[row][col] = num
            if(backtracking(grid)[0]):
                # Sudoku grid is solve
                return (1, grid)
            else:
                # Need to go back to find another number
                grid[row][col] = 0
    return (0, grid)

# Main function which is called in the main application of this project
# This function call the function that do the Backtracking algorithm
# The grid is an array of size : (9 x 9)
def mainSolver(grid):
    if(correctGrid(grid)):
        n, _ = getLocation(grid)

        # If the grid is full
        if(n == -1):
        # Check if the full grid is correct
            return (1, grid)

        # Try to get a solution
        res,newGrid = backtracking(grid)
        # Solution found
        if(res):
            return newGrid
        else:
            return -1
    
    # The original grid is not valid
    else:
        return -1
    