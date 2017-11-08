# PolishVoivodeshipsVisualizer
Map/charts maker. Create a map of Polish Voivodships and add a pie chart on each. 

![alt text](https://raw.githubusercontent.com/Naatoo/PolishVoivodeshipsVisualizer/master/UI_sample.png)

## Main features
1. [Maps](#maps "Maps")
1. [Pie charts](#pie-charts "Pie charts")
1. [Adding new data](#adding-new-data "Adding new data")
1. [Requirements](#requirements "Requirements")
1. [Additional information](#additional-information "Additional information")

## Maps
You can create a map of Polish Voivodships depending on your data and intervals. Choose data type from the list that interest you (default: District heating, Electrical power engineering, Gas manufacturing, Raw materials) and select chosen data record.
Then type in intervals in the entry boxes. Finally, click "Generate Map".

## Pie charts
Choose data type and data record as above. When you click "Add pie charts", they will be added to the current map. Remember that pie charts should be related to map (e.g. Energy Production map + charts showing share of every fuel in this field)

## Adding new data
##### Maps
Open data.xlsx in chosen data type folder (e.g. Gas manufacturing). Paste your data in the last column. First row should be the title of your data. Insert values to rows 1-17 in a alphabetical order (first - "Dolnośląskie", last - "Zachodniopomorskie" etc.).

##### Charts
Save <name_of_file>.xlsx in data_type_dir\pie_charts_data\. In the first row there must be Voivodships' names. In the first column name of every slice should be typed. Next, insert values in alphabetical order horizontally.

## Requirements
You have to type a path to your geckodriver.exe in GeckodriverPath.txt.

## Additional information
PolishVoivodeshipsVisualizer is still in development phase, many features are to be done. Feel free to contribute.
