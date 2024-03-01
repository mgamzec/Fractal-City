import matplotlib.pyplot as plt

from fractal_dimension import analyse_one_cell
from map_treatment import prepare
from os import makedirs


def main_script(city: str, year: int, resolution: int, dilatation: int, src_dir: str, data_dir: str, result_dir: str,
                used_old_data: bool = False, show_fig: bool = True):
    """
    Main script of the Analysis, which compile all fractal dimensions in one plot according to the chosen subdivision
    :param str city: Name of the city 
    :param int year: Year of the creation of the used map
    :param int resolution: Subdivision parameter
    :param int dilatation: Factor of dilatation of the subdivisions
    :param str src_dir: Directory of the original image
    :param str data_dir: Directory where temporary data will be saved
    :param str result_dir: Directory where results will be saved
    :param bool used_old_data: If the algorithm should use old data (must exist)
    :param bool show_fig: If a figure should be displayed at the end
    :return: None
    """
    # Matrix where all fractal dimensions are saved
    matrix = [[0 for _ in range(resolution)] for _ in range(resolution)]
    data_dir = "{0}/{1}_{2}x{2}".format(data_dir, year, resolution)

    # Check if data are already created
    if not used_old_data:
        prepare(src_dir, resolution, dilatation, data_dir)  # Application of a mask, then subdivision

    # Computing for all cells
    for i in range(resolution):
        for j in range(resolution):
            print("ANALYSIS", i, j)
            matrix[i][j] = analyse_one_cell("{0}/subdivision_{1}_{2}.png".format(data_dir, i, j))

    makedirs(result_dir, exist_ok=True)

    # Saving of the fractal dimensions in a csv file
    with open("{0}/{1}_{2}_{3}x{3}.csv".format(result_dir, city, year, resolution), 'w') as file:
        file.write("X,Y,Fractal Dimension\n")

        for i in range(resolution):
            for j in range(resolution):
                file.write("{},{},{}\n".format(i, j, matrix[i][j]))

    plt.close()
    plt.imshow(matrix, cmap="inferno", vmin=0, vmax=2)  # Plot to show all the fractal dimensions
    plt.title("{0} {1} (resolution = {2})".format(city, year, resolution))
    plt.colorbar(label="Estimated Fractal Dimension")

    # Saving of the figure
    plt.savefig("{0}/{1}_{2}_{3}x{3}.png".format(result_dir, city, year, resolution), dpi=300)

    if show_fig:
        plt.show()
