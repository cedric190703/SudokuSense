import os
from PIL import Image, ImageDraw, ImageFont

# Main function to draw a Sudoku grid in an empty grid image
def mainDraw(grid_result):
    # Get the path of the image
    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "image")

    # Open the empty Sudoku grid image
    image = Image.open(os.path.join(image_path, "empty_grid.jpg"))

    # Calculate the size of the Sudoku grid
    grid_size = len(grid_result)
    image_width, image_height = image.size
    
    # Calculate the size of each cell in the grid
    grid_size = len(grid_result)
    cell_width = image_width // grid_size
    cell_height = image_height // grid_size

    # Define the size of the grid
    font_size = int(min(cell_width, cell_height) * 0.7)
    font = ImageFont.truetype("arial.ttf", size=font_size)

    # Create a drawing object
    draw = ImageDraw.Draw(image)

    # Iterate over the Sudoku numbers and draw them on the grid image
    for i in range(grid_size):
        for j in range(grid_size):
            number = grid_result[i][j]
            if number != 0:
                # Calculate the position to draw the number
                x = j * cell_width + cell_width // 2
                y = i * cell_height + cell_height // 2

                # Center the number text within the cell
                text = str(number)
                text_width, text_height = draw.textbbox((0, 0),
                                text, font=font)[2:]
                text_position = (x - text_width // 2,
                                y - text_height // 2)

                # Draw the number on the grid image
                draw.text(text_position, text, font=font,
                        fill=(0, 0, 0))

    # Save the image with the completed Sudoku grid
    image.save("sudoku_completed.jpg")

# Tests on the main function
"""grid_result = [
    [3, 1, 6, 5, 2, 8, 4, 3, 4],
    [5, 2, 2, 1, 3, 4, 5, 6, 7],
    [3, 8, 7, 5, 6, 7, 1, 3, 1],
    [1, 2, 3, 3, 1, 5, 4, 8, 6],
    [9, 3, 4, 8, 6, 3, 2, 1, 5],
    [5, 5, 6, 2, 9, 1, 6, 7, 3],
    [1, 3, 1, 4, 5, 2, 2, 5, 8],
    [2, 4, 3, 6, 1, 8, 7, 7, 4],
    [6, 5, 5, 2, 7, 6, 3, 2, 1]
]

mainDraw(grid_result)"""