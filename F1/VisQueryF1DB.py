import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_data(df, x, y, kind_of_plot, fig_size, fig_color, text_size):
    df.plot(x, y, kind = kind_of_plot, figsize = fig_size, color = fig_color)
    plt.xlabel(x, size = text_size)
    plt.ylabel(y, size= text_size)
    plt.legend(fontsize= text_size)
    plt.xticks(size= text_size)
    plt.yticks(size= text_size)
    plt.show()

def trend_plot(trend_data, fig_size, x_label, y_label, grid_status, text_size,):
    plt.rcParams["figure.figsize"] = [12.0,8.0]
    trend_data.plot(grid = grid_status, figsize = fig_size)
    plt.xticks(size = text_size)
    plt.yticks(size= text_size)
    plt.xlabel(x_label, size = text_size)
    plt.ylabel(y_label, size = text_size)
    plt.legend(fontsize= text_size, loc="best")
    plt.show()