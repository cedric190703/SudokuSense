import cv2
import numpy as np

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

                    digitImages.append((digitImage, i, j, 1))
                    found = 1
                    break

            # Empty case
            if(not found):
                digitImages.append((image, i, j, 0))
    return digitImages

def mainProcessing(grid, binary):
    digitImages = []
    # To see the contous on the image
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

        except Exception as e:
            # cv2.destroyAllWindows()
            return (0, digitImages, inverted)

    # Destroy all the windows to liberate memory allocation
    # cv2.destroyAllWindows()
    return (1, digitImages, inverted)