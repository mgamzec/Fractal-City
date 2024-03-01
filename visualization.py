import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def display(resolution: [int], src: [str], title: [str], nb_raws: int = 1, cmap_name: str = "inferno"):
    """
    Display the results from previous fractal analysis from a CSV file
    :param [int] resolution: Resolutions of each fractal analysis
    :param [str] src: Directories of the CSV files
    :param [str] title: Titles to display
    :param int nb_raws: Number of raws to display
    :param str cmap_name: Name of the ColorMap Scheme to use
    :return: None
    """
    assert len(src) == len(resolution)
    assert len(src) == len(title)
    assert len(src) > 0

    data = [[[0 for _ in range(resolution[i])] for _ in range(resolution[i])] for i in range(len(src))]

    for i in range(len(src)):
        raw_data = pd.read_csv(src[i])

        for j in range(resolution[i]**2):
            data[i][int(raw_data['X'][j])][int(raw_data['Y'][j])] = float(raw_data['Fractal Dimension'][j])

    fig, axes = plt.subplots(nrows=nb_raws, ncols=len(src) // nb_raws)

    if len(src) > 1:
        i = 0
        for ax in axes.flat:
            im = ax.imshow(data[i], vmin=0, vmax=2, cmap=cmap_name)
            ax.set_title(title[i])

            i += 1  
    else:
        im = axes.imshow(data[i], vmin=0, vmax=2, cmap=cmap_name)
        axes.set_title(title[0])

    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.25, 0.03, 0.49])
    fig.colorbar(im, cax=cbar_ax, label="Estimated Fractal Dimension")

    plt.show()
