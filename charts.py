import pandas
from bokeh.plotting import figure, output_file, show
from numpy import pi
from bokeh.io import export_png
import cv2
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


def add_charts(path):

    # GET REGIONS' NAMES
    file = pandas.read_excel(path, index_col=0)
    names = ["Dolnośląskie", "Kujawsko-pomorskie", "Lubelskie",	"Lubuskie",	"Łódzkie", "Małopolskie",
     "Mazowieckie",	"Opolskie",	"Podkarpackie",	"Podlaskie", "Pomorskie",
     "Śląskie",	"Świętokrzyskie", "Warmińsko-mazurskie", "Wielkopolskie", "Zachodniopomorskie"]
    regions_data = []
    for region_name in names:
        regions_data.append(file[region_name])

    # CONVERT EXCEL FORMATTING TO PYTHON
    try:
        for region in regions_data:
            for index, number in enumerate(region):
                if number == 0:
                    continue
                if "," in number:
                    number = number.replace(",", ".")
                if " " in number:
                    m = number.count(" ")
                    temp = number.split(" ", m)
                    final_number = "".join(temp)
                    if " " in final_number:
                        m = final_number.count(" ")
                        temp = final_number.split(" ", m)
                        final_number = "".join(temp)
                    region[index] = float(final_number)
                else:
                    region[index] = float(number)
    except TypeError:
        pass

    # COUNT SLICES
    percents = []
    for index, region in enumerate(regions_data):
        percents.append([0])
        sum = 0
        for number in region:
            sum += number
        current_sum = 0
        for number in region:
            if number != 0:
                percents[index].append((current_sum + number) / sum)
                current_sum += number

    # ADD SLICES
    starts = []
    ends = []
    for region in percents:
        starts.append([p*2*pi for p in region[:-1]])
        ends.append([p * 2 * pi for p in region[1:]])

    # CHOOSE NUMBER OF COLORS
    colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf', '#999999']
    colors_now = colors[:file.shape[0]]

    # CREATE CHARTS LEGEND
    charts_key = []
    plt.rcParams['font.family'] = "calibri"
    fig = plt.figure(figsize=(5, 5))
    for color, name in zip(colors_now, file["Nazwa wycinka"]):
        charts_key.append(mpatches.Patch(color=color, label=name))

    plt.legend(handles=[color for color in charts_key])
    plt.axis('off')
    plt.savefig(r"temp\charts_legend.png")

    # ADD CHARTS LEGEND TO THE MAP
    img = cv2.imread(r"final_map.png")
    original_legend = cv2.imread(r"temp\charts_legend.png")
    white = np.asarray([255, 255, 255])
    for pixel_x in range(original_legend.shape[1]):
        if not np.array_equal(original_legend[80, pixel_x], white):
            x_start = pixel_x
            break
    for pixel_x in range(original_legend.shape[1] - 1, 0, -1):
        if not np.array_equal(original_legend[80, pixel_x], white):
            x_end = pixel_x
            break
    legend = original_legend[70:70 + 20 * len(colors_now), x_start + 5:x_end - 5]
    length = x_end - 5 - (x_start + 5)
    x_offset = 590
    y_offset = 250
    img[y_offset:y_offset + 20 * len(colors_now), x_offset:x_offset + length] = legend
    cv2.imwrite('final_map.png', img)

    # GET COLORS OF THE BACKGROUND
    file = open("charts_colors.txt")
    background_colors = file.read()
    clr = background_colors.split(",")
    file.close()

    # COORDINATES OF PASTING
    regions_to_paste_coords = (
        (118,333),(236,159),(478,321),(50,239),(287,296),(327,452),(379,217),(204,383),
        (439,433),(485,140),(204,55),(262,406),(364,373),(356,84),(151,234),(68,107)
    )

    # CREATE CHARTS
    p = figure(x_range=(-1, 1), y_range=(-1, 1), width=200, height=200)
    p.background_fill_alpha = 1
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.axis.visible = False
    index = 0
    for start, end in zip(starts, ends):
        map_without = cv2.imread('final_map.png')
        p.background_fill_color = clr[index]
        p.wedge(x=0, y=0, radius=1, start_angle=start, end_angle=end, color=colors_now, alpha=1)

        export_png(p, filename="temp\chart.png")

        original_chart = cv2.imread("temp\chart.png", 1)
        cropped_chart = original_chart[15:183, 6:170]
        if index not in [7, 11]:
            resized_chart = cv2.resize(cropped_chart, (int(cropped_chart.shape[1]/2.8), int(cropped_chart.shape[0]/2.8)))
        else:
            resized_chart = cv2.resize(cropped_chart, (int(cropped_chart.shape[1]/3.5), int(cropped_chart.shape[0] / 3.5)))

        x_offset = regions_to_paste_coords[index][0]
        y_offset = regions_to_paste_coords[index][1]
        map_without[y_offset:y_offset + resized_chart.shape[0], x_offset:x_offset + resized_chart.shape[1]] = resized_chart
        cv2.imwrite('final_map.png', map_without)
        index += 1
