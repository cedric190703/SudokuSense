import sys

# Import the paths to use the main functions
sys.path.append('./Interface')

from appUI import main_interface

# Call the main function in the interface directory
# which is the function that handle the main process of the application
def main():
    # First lunch the interface to get the Sudoku image
    main_interface()
 
if __name__ == "__main__":
    main()