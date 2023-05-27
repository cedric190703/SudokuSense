import cv2
import numpy as np

# Function to get the binary image
# First step of this entire part give a clean image (binary)
def processing(image):
    # Convert the image in a Grayscale image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply gaussian blur on the Grayscale image
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    # Apply the threshold on the blur image
    binary = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 4)
    return binary

def findGrid(binary):
    # Find the contours on the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter the contours based on their area
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 1000]

    # Sort the contours by area in descending order
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Find the largest contour with 4 sides
    for cnt in contours:
        perimeter = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)
        if len(approx) == 4:
            return approx.reshape(4, 2)

    # If no suitable contour is found, return None
    return None

# Function to get the perspective transform to facilitate the cutting of the grid after
def perspectiveTransform(binary, contours):
    # Defines the desired size of the transformed grid in pixels
    grid_size = 400

    # Represents the desired points to the corners destination
    destination_corners = np.float32([[0, 0], [grid_size, 0], [0, grid_size], [grid_size, grid_size]])
    
    # Ensure the source points are of type np.float32
    contours = np.float32(contours)

    # Need to rotate the image if the grid have a angle not at 90 degrees
    # TODO

    # Calculates the transformation matrix needed to perform the perspective transform
    transformation_matrix = cv2.getPerspectiveTransform(contours, destination_corners)

    # Apply the perspective transform on the binary image
    transformed = cv2.warpPerspective(binary, transformation_matrix, (grid_size, grid_size))
    return transformed

def mainProcessing(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # preprocess the image to get a binary image
    binary = processing(image)

    cv2.imshow('Result', binary)
    cv2.waitKey(0)
    # Try to find the Sudoku grid
    grid = findGrid(binary)

    cv2.drawContours(image, [grid], -1, (0, 255, 0), 2)
    cv2.imshow('Result2', image)
    
    if(grid is not None):
        try:
            # Reshape the grid contour into the expected shape
            reshaped_grid = grid.reshape(4, 2)

            # Apply the perspective transform to the binary image
            transformed = perspectiveTransform(binary, reshaped_grid)

            # Display the transformed image
            cv2.imshow('Transformed Image', transformed)
            cv2.waitKey(0)
        except:
            cv2.destroyAllWindows()
            return 0

    # Destroy all the windows to liberate memory allocation
    cv2.destroyAllWindows()
    return 1

# Test the function here :
image_path = 'C:\\Users\\cbrzy\\OneDrive\\Bureau\\R.jpg'
print(mainProcessing(image_path))