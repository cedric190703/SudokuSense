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
    binary = cv2.adaptiveThreshold(blur, 255,
                                cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 4)
    return binary

def findGrid(binary):
    # Find the contours on the binary image
    contours, _ = cv2.findContours(binary, 
                                   cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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

# Function to normalized the points
# Needed to the perspective transform
def normalizedP(contours):
    # Create a new arrays of size (4 x 2)
    rect = np.zeros((4, 2))

    # Convert array in float32 type
    rect = np.float32(rect)

    # Get the sum of the contours
    s = contours.sum(axis=1)

    # Get the min and max value of the sum of the array
    rect[0] = contours[np.argmin(s)]
    rect[2] = contours[np.argmax(s)]

    # Get the diff in the sum of the array
    diff = np.diff(contours, axis=1)

    # Get the min and max value of the diff of the sum of the original array
    rect[1] = contours[np.argmin(diff)]
    rect[3] = contours[np.argmax(diff)]
    return rect

# Function to get the perspective transform to facilitate the cutting of the grid after
def perspectiveTransform(binary, contours):
    # Defines the desired size of the transformed grid in pixels
    grid_size = 400

    # Represents the desired points to the corners destination
    destination_corners = np.float32([[0, 0], [grid_size, 0],
                                    [grid_size, grid_size], [0, grid_size]])
    
    # Ensure the source points are of type np.float32
    contours = np.float32(contours)
    
    # Normalized the points for the perspective transform
    normalized = normalizedP(contours)

    # Calculates the transformation matrix needed to perform the perspective transform
    transformation_matrix = cv2.getPerspectiveTransform(normalized, destination_corners)
    
    # Apply the perspective transform on the binary image
    transformed = cv2.warpPerspective(binary,
                                    transformation_matrix, (grid_size, grid_size))
    return transformed

# Function that extract the digits on the image
# Cutting the image that have the perspective image
def extractDigits(transformed):
    # Create an array that contains all the digits images
    digitImages = []

    sized = 400//9

    for i in range(9):
        for j in range(9):
            found = 0
            x1, y1 = i * (sized), j * (sized)
            x2, y2 = (i + 1) * sized, (j + 1) * sized
            
            # Get the contours on the image cropped
            image = transformed[y1:y2, x1:x2]
            contours, _ = cv2.findContours(image, cv2.RETR_LIST,
                                        cv2.CHAIN_APPROX_SIMPLE)

            # Clean and append each digit image
            for contour in contours:
                imX1, imY1, imX2, imY2 = cv2.boundingRect(contour)

                # In case we have a digit contour detected
                if(0.4 * sized < imY2 < 0.8 * sized and
                    0.2 * sized <  imX2 < 0.8 * sized):
                    # Clean the digit image
                    digitImage = image[imY1:imY1 + imY2,
                                        imX1:imX1 + imX2]
                    digitImages.append((digitImage, i, j, 1))
                    found = 1
                    break

            # Empty case
            if(not found):
                digitImages.append((image, i, j, 0))
    return digitImages

def mainProcessing(image_path):
    print("IM HERE")
    digitImages = []

    # Load the image from a PIL image
    image = cv2.cvtColor(np.array(image_path), cv2.COLOR_RGB2BGR)

    # preprocess the image to get a binary image
    binary = processing(image)

    # Try to find the Sudoku grid
    grid = findGrid(binary)

    # To see the contous on the image
    # cv2.drawContours(image, [grid], -1, (0, 255, 0), 2)
    
    if(grid is not None):
        try:
            # Reshape the grid contour into the expected shape
            reshaped_grid = grid.reshape(4, 2)

            # Apply the perspective transform to the binary image
            transformed = perspectiveTransform(binary, reshaped_grid)

            # Invert the pixels on the image to have better digits on the image
            # White, Black pixels  -> Black, White pixels
            inverted = cv2.bitwise_not(transformed)

            # Display the transformed image
            # cv2.imshow('Transformed Image', inverted)

            #  Get the list of all the digiit cases
            digitImages = extractDigits(inverted)

            # Tests to check the number of digits recognized           
            """cpt = 0
            for digit in digitImages:
                if(digit[3]):
                    cpt+=1
            print(cpt)"""

        except Exception as e:
            # cv2.destroyAllWindows()
            return (0, digitImages)

    # Destroy all the windows to liberate memory allocation
    # cv2.destroyAllWindows()
    return (1, digitImages)

# Test the function here :
"""image_path = 'PATH HERE'
mainProcessing(image_path)"""