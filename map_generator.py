import pandas
import folium
import maps_colors_data.colors_database
import os
from selenium import webdriver
import cv2
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from time import sleep


class Map:
    def __init__(self, data, intervals, color):
        super().__init__()

        # CONVERT EXCEL FORMATTING TO PYTHON
        try:
            for index, number in enumerate(data):
                if "," in number:
                    number = number.replace(",", ".")
                if " " in number:
                    temp = number.split(" ", 1)
                    final_number = "".join(temp)
                    data[index] = float(final_number)
                else:
                    data[index] = float(number)
        except TypeError:
            pass

        # ASSIGN VALUE WITH COLOR
        color = color.lower()
        if color == "green":
            color_data = maps_colors_data.colors_database.green
        if color == "blue":
            color_data = maps_colors_data.colors_database.blue
        if color == "red":
            color_data = maps_colors_data.colors_database.red
        if color == "purple":
            color_data = maps_colors_data.colors_database.purple
        if color == "orange":
            color_data = maps_colors_data.colors_database.orange
        if color == "gray":
            color_data = maps_colors_data.colors_database.gray
        color_set = color_data[len(intervals) + 1]
        colors = []
        for v in data:
            for i in range(len(intervals)):
                if v < intervals[i]:
                    colors.append(color_set[i])
                    break
            if v > intervals[len(intervals) - 1]:
                colors.append(color_set[len(intervals)])

        # EXPORT COLORS IN CASE OF MAKING PIE CHARTS
        file = open("charts_colors.txt", "w")
        for index, color in enumerate(colors):
            if index < 15:
                color = color + ","
            file.write(color)
        file.close()

        # -----------------------------------------------------------------------------
        # MAP - GEOJSON
        # -----------------------------------------------------------------------------

        # SET MAP BACKGROUND AND FEATURES
        map_1 = folium.Map((52.091342, 19.065937), zoom_start=6.2)
        fg_borders = folium.FeatureGroup(name="Heat")

        # ADD BLANK BACKGROUND
        fg_borders.add_child(folium.GeoJson(
            data=open(r"maps_colors_data\blank.json", encoding="utf=8-sig").read(),
            style_function=lambda x: {
                "color": "white",
                "weight": 1.5,
                "opacity": 1,
                "fillColor": "white",
                "fillOpacity": 1
            }))

        # CREATE LAYER WITH COLOURS
        fg_borders.add_child(folium.GeoJson(
            data=open(r"maps_colors_data\poland.json", encoding="utf=8-sig").read(),
            style_function=lambda x: {
                "color": "grey",
                "weight": 1.5,
                "opacity": 1,
                "fillColor": colors[x["properties"]["cartodb_id"]],
                "fillOpacity": 1
            }))

        # ADD LAYER TO MAP
        map_1.add_child(fg_borders)
        map_1.add_child(folium.LayerControl())

        # -----------------------------------------------------------------------------
        # FILE
        # -----------------------------------------------------------------------------

        # SAVE TO HTML
        fn = r'temp/testmap.html'
        tmpurl = 'file://{path}/{mapfile}'.format(path=os.getcwd(), mapfile=fn)
        map_1.save(fn)

        # CONVERT HTML TO PNG
        firefox_path = open("GecktodriverPath.txt")
        browser = webdriver.Firefox(executable_path=firefox_path.read())
        browser.get(tmpurl)
        sleep(5)
        browser.save_screenshot(r'temp\map.png')
        browser.quit()

        # CUT IMAGE
        img = cv2.imread(r"temp\map.png")
        map_cut = img[130:700, 500:1100]
        
        # CREATE MAP LEGEND
        map_key = []
        interval_id = 0
        fig = plt.figure(figsize=(2, 1.25))
        for color, interval in zip(color_set, intervals):
            if interval_id < (len(intervals) - 1):
                key = str("< " + str(interval))
                map_key.append(mpatches.Patch(color=color, label="< " + str(interval)))
            else:
                key = str("> " + str(interval))
                map_key.append(mpatches.Patch(color=color, label="> " + str(interval)))
            interval_id += 1
        plt.legend(handles=[color for color in map_key])
        plt.axis('off')
        plt.savefig(r"temp\legend.png")

        # ADD MAP LEGEND TO THE MAP
        original_legend = cv2.imread(r"temp\legend.png")
        legend = original_legend[25:21 * (len(intervals) + 1), 75:170]
        x_offset = 30
        y_offset = 430
        map_cut[y_offset:y_offset + legend.shape[0], x_offset:x_offset + legend.shape[1]] = legend
        cv2.imwrite('final_map.png', map_cut)
