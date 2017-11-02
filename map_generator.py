import pandas
import folium
import maps_colors_data.colors_database
import os
from selenium import webdriver
import cv2
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


class DataRead:
    def __init__(self):
        # READ FILE
        data = pandas.read_excel("power_test.xlsx")
        self.column = list(data["Moc zainstalowana"])


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
        fn = 'testmap.html'
        tmpurl = 'file://{path}/{mapfile}'.format(path=os.getcwd(), mapfile=fn)
        map_1.save(fn)

        # CONVERT HTML TO PNG
        firefox_path = open("FirefoxPath.txt")
        browser = webdriver.Firefox(executable_path=firefox_path.read())
        browser.get(tmpurl)
        browser.save_screenshot('map.png')
        browser.quit()

        # CUT IMAGE
        img = cv2.imread("map.png")
        crop_img = img[130:700, 500:1100]
        cv2.imwrite('test.png', crop_img)


        map_key = []
        interval_id = 0
        for color, interval in zip(color_set, intervals):
            if interval_id < (len(intervals) - 1):
                key = str("< " + str(interval))
                map_key.append(mpatches.Patch(color=color, label="< " + str(interval)))
            else:
                key = str("> " + str(interval))
                map_key.append(mpatches.Patch(color=color, label="> " + str(interval)))
            interval_id += 1
        plt.legend(handles=[color for color in map_key])
   #     plt.show()
