import cv2
import numpy as np

# Needed to the perspective transform
def normalized_NP(contours):
    """Normalized the points of the contours"""
    rect = np.zeros((4, 2))
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

def perspective_transform(binary, contours):
    """Get the perspective transform to facilitate the cutting of the grid after"""
    # Defines the desired size of the transformed grid in pixels
    grid_size = 400

    # Represents the desired points to the corners destination
    destination_corners = np.float32([[0, 0], [grid_size, 0],
                                    [grid_size, grid_size], [0, grid_size]])
    
    # Ensure the source points are of type np.float32
    contours = np.float32(contours)
    
    normalized = normalized_NP(contours)

    # Calculates the transformation matrix needed to perform the perspective transform
    transformation_matrix = cv2.getPerspectiveTransform(normalized, destination_corners)
    
    # Apply the perspective transform on the binary image
    transformed = cv2.warpPerspective(binary,
                                    transformation_matrix, (grid_size, grid_size))
    return transformed

def centre_pad(length, size):
    if length % 2 == 0:
        side1 = int((size - length) / 2)
        side2 = side1
    else:
        side1 = int((size - length) / 2)
        side2 = side1 + 1
    return side1, side2

def scale_ratio(r, x):
    return int(r * x)

def resize_image(img, width, height):
    return cv2.resize(img, (width, height))

def add_border(img, top, bottom, left, right, border_type, border_color):
    return cv2.copyMakeBorder(img, top, bottom, left, right, border_type, None, border_color)

def scale_and_centre(img, size, margin=0, background=0):
    h, w = img.shape[:2]

    img_width, img_height = w, h

    if h > w:
        t_pad = int(margin / 2)
        b_pad = t_pad
        ratio = (size - margin) / h
        img_width, img_height = scale_ratio(ratio, w), scale_ratio(ratio, h)
        l_pad, r_pad = centre_pad(img_width, size)
    else:
        l_pad = int(margin / 2)
        r_pad = l_pad
        ratio = (size - margin) / w
        img_width, img_height = scale_ratio(ratio, w), scale_ratio(ratio, h)
        t_pad, b_pad = centre_pad(img_height, size)

    img = resize_image(img, img_width, img_height)
    img = add_border(img, t_pad, b_pad, l_pad, r_pad, cv2.BORDER_CONSTANT, background)
    img = resize_image(img, size, size)
    return img

def find_points(image):
	cells = []
	side = image.shape[:1]
	side = side[0] / 9

	for j in range(9):
		for i in range(9):
			p1 = (i * side, j * side)
			p2 = ((i + 1) * side, (j + 1) * side) 
			cells.append((p1, p2, i, j))
	return cells

def cut_rect(image, cell):
    x1, y1 = int(cell[0][0]), int(cell[0][1])
    x2, y2 = int(cell[1][0]), int(cell[1][1])
    return image[y1:y2, x1:x2]

def find_largest_feature(image, scan_tl=None, scan_br=None):
    final_image = image.copy()
    height, width = final_image.shape[:2]
    max_area = 0
    seed_point = (None, None)

    scan_tl = scan_tl or [0, 0]
    scan_br = scan_br or [width, height]

    for x in range(scan_tl[0], scan_br[0]):
        for y in range(scan_tl[1], scan_br[1]):
            if final_image[y, x] == 255 and x < width and y < height:
                area = cv2.floodFill(final_image, None, (x, y), 64)
                if area[0] > max_area:
                    max_area = area[0]
                    seed_point = (x, y)

    for x in range(width):
        for y in range(height):
            if final_image[y, x] == 255 and x < width and y < height:
                cv2.floodFill(final_image, None, (x, y), 64)
    
    mask = np.zeros((height + 2, width + 2), np.uint8)
    if all(p is not None for p in seed_point):
        cv2.floodFill(final_image, mask, seed_point, 255)

    top, bottom, left, right = height, 0, width, 0

    for x in range(width):
        for y in range(height):
            if final_image[y, x] == 64:
                cv2.floodFill(final_image, mask, (x, y), 0)
            if final_image[y, x] == 255:
                top = min(y, top)
                bottom = max(y, bottom)
                left = min(x, left)
                right = max(x, right)

    bbox = [[left, top], [right, bottom]]
    return final_image, np.array(bbox, dtype='float32'), seed_point

def extract_digit(image, cell):
	digit = cut_rect(image, cell)

	# Try to get the contour of a digit
	h, w = digit.shape[:2]
	margin = int(np.mean([h, w]) / 2.5)
	_, feature, seed = find_largest_feature(digit, [margin, margin], [w - margin, h - margin])
	digit = cut_rect(digit, feature)

	w = feature[1][0] - feature[0][0]
	h = feature[1][1] - feature[0][1]

    # Check if the image contains a digit
	if (w * h) > 100 and len(digit) > 0 and w > 0 and h > 0:
		return (scale_and_centre(digit, 28, 4), cell[2], cell[3] , 1)
	else:
		return (image, cell[2], cell[3] , 0)

def find_digits(image, cells):
    digits_images = []
    for cell in cells:
        digits_images.append(extract_digit(image, cell))
    return digits_images

def main_processing(grid, binary):
    digitImages = []
    # To see the contous on the image
    if(grid is not None):
            try:
                # Reshape the grid contour into the expected shape
                reshaped_grid = grid.reshape(4, 2)

                # Apply the perspective transform to the binary image
                transformed = perspective_transform(binary, reshaped_grid)

                cells = find_points(transformed)
                #  Get list of digits images
                digitImages = find_digits(transformed, cells)

            except Exception as e:
                # cv2.destroyAllWindows()
                return (0, digitImages, transformed)

    # Destroy all the windows to liberate memory allocation
    # cv2.destroyAllWindows()
    return (1, digitImages, transformed)