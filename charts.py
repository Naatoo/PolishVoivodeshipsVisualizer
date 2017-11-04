import pandas
from bokeh.plotting import figure, output_file, show
from numpy import pi
from bokeh.io import export_png
import cv2


def add_charts():
    file = pandas.read_excel("cieplo.xlsx")

    names = ["Dolnośląskie", "Kujawsko-pomorskie", "Lubelskie",	"Lubuskie",	"Łódzkie", "Małopolskie",
     "Mazowieckie",	"Opolskie",	"Podkarpackie",	"Podlaskie", "Pomorskie",
     "Śląskie",	"Świętokrzyskie", "Warmińsko-mazurskie", "Wielkopolskie", "Zachodniopomorskie"]

    regions_data = []
    for region_name in names:
        regions_data.append(file[region_name])

    try:
        for region in regions_data:
            for index, number in enumerate(region):
                if "," in number:
                    number = number.replace(",", ".")
                if " " in number:
                    temp = number.split(" ", 1)
                    final_number = "".join(temp)
                    region[index] = float(final_number)
                else:
                    region[index] = float(number)
    except TypeError:
        pass

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

    starts = []
    ends = []
    for region in percents:
        starts.append([p*2*pi for p in region[:-1]])
        ends.append([p * 2 * pi for p in region[1:]])

    colors = ["red", "green", "blue"]
    p = figure(x_range=(-1, 1), y_range=(-1, 1), width=200, height=200)
    p.background_fill_alpha = 1
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.axis.visible = False

    file = open("charts_colors.txt")
    background_colors = file.read()
    clr = background_colors.split(",")
    file.close()


    regions_to_paste_coords = (
        (118,333),(236,159),(478,321),(50,239),(287,296),(327,452),(379,217),(204,383),
        (439,433),(485,140),(204,55),(262,406),(364,373),(356,84),(151,234),(68,107)
    )
    index = 0
    for start, end in zip(starts, ends):
        map_without = cv2.imread('final_map.png')
        p.background_fill_color = clr[index]
        p.wedge(x=0, y=0, radius=1, start_angle=start, end_angle=end, color=colors, alpha=1)

        export_png(p, filename="chart.png")

        original_chart = cv2.imread("chart.png", 1)
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
