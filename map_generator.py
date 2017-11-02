import pandas
import folium
import subprocess
import colors_database
import os
import os
import time
from selenium import webdriver


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
            color_data = colors_database.green
        if color == "blue":
            color_data = colors_database.blue
        if color == "red":
            color_data = colors_database.red
        if color == "purple":
            color_data = colors_database.purple
        if color == "orange":
            color_data = colors_database.orange
        if color == "gray":
            color_data = colors_database.gray
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
            data=open("blank.json", encoding="utf=8-sig").read(),
            style_function=lambda x: {
                "color": "white",
                "weight": 1.5,
                "opacity": 1,
                "fillColor": "white",
                "fillOpacity": 1
            }))

        # CREATE LAYER WITH COLOURS
        fg_borders.add_child(folium.GeoJson(
            data=open("poland.json", encoding="utf=8-sig").read(),
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

        fn = 'testmap.html'
        tmpurl = 'file://{path}/{mapfile}'.format(path=os.getcwd(), mapfile=fn)
        map_1.save(fn)

        from selenium import webdriver
        browser = webdriver.Firefox(executable_path=r'C:\Program Files\Anaconda3\selenium\geckodriver.exe')

        browser.get(tmpurl)
        # Give the map tiles some time to load
  #      time.sleep(5)
        browser.save_screenshot('map.png')
        browser.quit()

        import cv2
        img = cv2.imread("map.png")
        crop_img = img[130:700, 500:1100]  # Crop from x, y, w, h -> 100, 200, 300, 400
        # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
        cv2.imwrite('test.png', crop_img)



        import matplotlib.patches as mpatches
        import matplotlib.pyplot as plt

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



        firefoxPath = r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe'
        #subprocess.Popen("%s %s" % (firefoxPath, html))



