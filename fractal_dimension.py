import numpy as np

from PIL import Image
from math import log, ceil
from map_treatment import extract


def is_in(array: np.ndarray, x: int, y: int, side: int):
    """
    Check if there is a cell with a 1 inside a square of side side which upper-left corner is (x, y)
    :param np.ndarray array: Array to analyse
    :param int x: x-coordinate of the upper-left corner
    :param int y: y-coordinate of the upper-left corner
    :param int side: Side of the square
    :return bool: Result of the test
    """
    found = False
    height, width = array.shape[:2]
    i, j = 0, 0

    # While structure : when there is a one, it stops
    while i < side and x + i < height and not found:  # Check in targeted cell is still in array
        j = 0
        while j < side and y + j < width and not found:
            found = (array[x + i][y + j] == 1)
            j += 1
        i += 1

    return found


def box_counting(array: np.ndarray):
    """
    Simple version of a Box-Counting Algorithm to determine the number of square of side 2^n needed to cover the image
    represented by array
    :param np.ndarray array: Representation of the image
    :return list * list: List of the used powers of 2, and list of the associated number of square
    """
    # Side with the minimum value
    height, width = array.shape[:2]
    side = min(height, width)

    # Higher power of 2 which is less than side
    p = ceil(log(side)/log(2))
    data = [0 for _ in range(p)]

    # For all intermediate powers of 2, we count the number of squares of side 2^e covering the image
    for e in range(p):
        # Maximum factor on x and y axis
        max_i = ceil(height/(2**e))
        max_j = ceil(width/(2**e))

        for i in range(max_i):
            for j in range(max_j):
                # For each (i, j), check for 1 in a square
                if is_in(array, i*(2**e), j*(2**e), 2**e):  # Error was here
                    data[e] += 1

        print("BOX COUNTING", int(e * 10000 / p) / 100, "%")  # Indication about the progression

    # List of the used powers of 2, then the associated number of square
    return [2**e for e in range(p)], data
                

def analyse_one_cell(image_dir: str):
    """
    Procedure of analysis on one cell of the original image (ie on one subdivision)
    :param str image_dir: Directory to the image
    :return: None
    """
    picture, empty = extract(np.array(Image.open(image_dir)))

    if empty:  # Check if the picture is empty
        print("EMPTY")
        # If so, the dimension is null
        a = 0
    else:
        absi, ordo = box_counting(picture)  # Box Counting Method

        print(absi, ordo)

        absi = [-log(r) for r in absi]
        ordo = [log(N) for N in ordo]
        
        # Determination of the fractal dimension with a linear regression between log(1/r) and log(N(r))
        regression_data = np.polyfit(absi, ordo, 1)

        a = regression_data[0]  # The fractal dimension is the slope

        #with open("correlation_coeff.txt", 'a') as file:
        #    file.write("{},{}\n".format(image_dir,regression_data[2]))
        
    return a
