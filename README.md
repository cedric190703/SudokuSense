# SudokuSense :
## OCR to detect and solve a Sudoku grid with handwritten digits in Python.
## The application uses a graphical interface.
### The user imports an image and then press the 'start' button :
## Step 1: Image processing:
###  We use filters to bring out the lines and the numbers and thus find and cut the Sudoku grid.
## Step 2 : Perspective transform :
### Once the Sudoku grid is found we apply the perspective transform to have an image with the complete grid.
## Step 3 : Cut the grid and extract each digit of it
## Step 4 : Recognize digit for each image
### Use CNN model to recognize each digit (28 x 28) pixels for each image of a digit
## Step 5 : Solve grid :
### Solve the Sudoku grid with a backtracking algorithm.
## Step 6 : Display result :
### Draw the final grid in an empty image of a Sudoku grid