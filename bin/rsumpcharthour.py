"""Create charts for viewing on Raspberry Pi Web Server."""

# put in /opt/raspi-sump/bin

# Raspi-sump, a sump pump monitoring system.
# Al Audet
# https://www.linuxnorth.org/raspi-sump/
#
# All configuration changes should be done in raspisump.conf
# MIT License -- https://www.linuxnorth.org/raspi-sump/license.htmlimport os

import os
import subprocess
import time
import numpy as np
import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams
import pandas as pd

rcParams.update({"figure.autolayout": True})

def main():
    """Create a chart of sump pit activity and save to web folder"""
    csv_file = f"/home/pi/raspi-sump/csv/waterlevel-{time.strftime('%Y%m%d')}.csv"
    filename = f"/home/pi/raspi-sump/charts/hour.png"
    graph(csv_file, filename)

def graph(csv_file, filename):
    """Create a line graph from a two column csv file."""

    unit = "imperial"


    # Load the CSV file, parsing the date column and setting it as index
    df = pd.read_csv(csv_file)

    plot_df = df.tail(500)
    x_column = df.columns[0]
    y_column = df.columns[1]


    fig = plt.figure(figsize=(10, 3.5))

    fig.add_subplot(111, facecolor="white", frameon=False)

    rcParams.update({"font.size": 9})
	
	plt.plot(
        plot_df[x_column],
        plot_df[y_column],
        ls="solid",
        linewidth=2,
        color="#13C355",
        marker="",
    )

    # Format the x-axis to use the specified formats and interval
    ax = plt.gca()
    ax.xaxis.set_major_locator(plt.MaxNLocator(8))

    title = f"Water Level {time.strftime('%Y-%m-%d %H:%M')}"
    title_set = plt.title(title)
    title_set.set_fontsize(20.0)
    title_set.set_y(1.09)
    plt.subplots_adjust(top=0.86)

    if unit == "imperial":
        plt.ylabel("inches", fontsize=16)
    if unit == "metric":
        plt.ylabel("centimeters", fontsize=16)

    plt.xlabel("Time of Day", fontsize=16)
	plt.xticks(rotation=30)
    plt.grid(True, color="#ECE5DE", linestyle="solid")
    plt.tick_params(axis="x", bottom=False, top=False)
    plt.tick_params(axis="y", left=False, right=False)
    plt.savefig(filename, transparent=True, dpi=72)

main()