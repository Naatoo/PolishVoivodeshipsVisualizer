from tkinter.ttk import Label, Entry, Button, Frame, OptionMenu
from tkinter.ttk import Scrollbar, Style
from tkinter import Tk, StringVar, PhotoImage, LEFT, BOTTOM, RIGHT, BOTH, X, TOP, Y, END, Listbox, IntVar, Checkbutton, W
from map_generator import create_map
from charts_generator import add_charts
import pandas
import os


class App:
    def __init__(self, master):
        window = Frame(master)
        window.pack()

        # ----------------------------------------------------
        # FRAMES

        dataframe = Frame(window)
        dataframe.pack(side=LEFT, fill=BOTH)

        upperframe = Frame(window)
        upperframe.pack(expand=True, fill=X)

        bottomframe = Frame(window)
        bottomframe.pack(side=BOTTOM)

        left_bottom_frame = Frame(bottomframe)
        left_bottom_frame.pack(side=LEFT)

        imageframe = Frame(left_bottom_frame)
        imageframe.pack()

        rigth_bottom_frame = Frame(bottomframe)
        rigth_bottom_frame.pack(side=RIGHT)

        rigth_bottom_frame_up = Frame(rigth_bottom_frame)
        rigth_bottom_frame_up.pack(side=TOP)

        rigth_bottom_frame_down = Frame(rigth_bottom_frame)
        rigth_bottom_frame_down.pack(side=BOTTOM)

        # ----------------------------------------------------
        # DEFAULT VALUES

        data_type = ("Ciepłownictwo", "Gazownictwo", "Elektroenergetyka", "Surowce")
        self.chosen_data_type = data_type[0]
        self.data = DataRead.read_data(self.chosen_data_type)
        self.column = self.data[list(self.data)[0]]
        self.pie_chart_path = r"regions_data\pie_chart_data\\Produkcja i rozdysponowanie ciepła.xlsx"

        master.title("Polish Voivodeships Visualizer")

        # ----------------------------------------------------
        # INTERVALS LABELS AND ENTRIES

        l1 = Label(upperframe, text="Interval 1:")
        l1.grid(row=0, column=0)

        l2 = Label(upperframe, text="Interval 2:")
        l2.grid(row=0, column=2)

        l3 = Label(upperframe, text="Interval 3:")
        l3.grid(row=0, column=4)

        l4 = Label(upperframe, text="Interval 4:")
        l4.grid(row=1, column=0)

        l5 = Label(upperframe, text="Interval 5:")
        l5.grid(row=1, column=2)

        l6 = Label(upperframe, text="Interval 6:")
        l6.grid(row=1, column=4)

        self.interval1_value = StringVar()
        e1 = Entry(upperframe, textvariable=self.interval1_value, width=10)
        e1.grid(row=0, column=1)

        self.interval2_value = StringVar()
        e2 = Entry(upperframe, textvariable=self.interval2_value, width=10)
        e2.grid(row=0, column=3)

        self.interval3_value = StringVar()
        e3 = Entry(upperframe, textvariable=self.interval3_value, width=10)
        e3.grid(row=0, column=5)

        self.interval4_value = StringVar()
        e4 = Entry(upperframe, textvariable=self.interval4_value, width=10)
        e4.grid(row=1, column=1)

        self.interval5_value = StringVar()
        e5 = Entry(upperframe, textvariable=self.interval5_value, width=10)
        e5.grid(row=1, column=3)

        self.interval6_value = StringVar()
        e6 = Entry(upperframe, textvariable=self.interval6_value, width=10)
        e6.grid(row=1, column=5)

        colors = ("Green", "Blue", "Orange", "Red", "Purple", "Gray")
        self.chosen_color = StringVar(rigth_bottom_frame_up)
        self.chosen_color.set(colors[0])  # default value
        colors_drop_down_list = OptionMenu(upperframe, self.chosen_color, *colors)
        colors_drop_down_list.grid(row=0, column=8, rowspan=2, padx=30)

        self.charts_status = IntVar()
        charts_checkbox = Checkbutton(upperframe, text="Map for pie charts", variable=self.charts_status)
        charts_checkbox.grid(row=0, column=7, rowspan=2)

        colors_types = ["Colorful", "Black and white"]
        self.colors_type = StringVar(rigth_bottom_frame_up)
        self.colors_type.set(colors_types[0])
        colors_types_drop_down_list = OptionMenu(upperframe, self.colors_type, *colors_types)
        colors_types_drop_down_list.grid(row=0, column=9, rowspan=2)

        # ----------------------------------------------------
        # LABELS FOR REGIONS CURRENT DATA

        for column in range(6):
            upperframe.grid_columnconfigure(column, minsize=126)

        data_label = Label(dataframe, text="Data:")
        data_label.grid(row=0, column=0, columnspan=2, pady=12)

        self.data_for_region = {}
        for region in range(16):
            self.data_for_region["d{}".format(region)] = self.column[region]
        index = 0

        self.label_value_row = []
        for k, v in self.data_for_region.items():
            k = Label(dataframe, text=v)
            k.grid(row=index + 1, column=0)
            self.label_value_row.append(k)
            dataframe.grid_rowconfigure(index + 1, minsize=37)
            index += 1

        # ----------------------------------------------------
        # MAP DISPLAY LABEL

        self.map_image = PhotoImage(file="final_map.png")
        self.label = Label(imageframe, image=self.map_image)
        self.label.pack()

        # ----------------------------------------------------
        # MAP CREATION TOOLS
        self.list_data_types = Listbox(rigth_bottom_frame_up, width=42, height=4, exportselection=False)
        self.list_data_types.pack(side=TOP)

        for name in data_type:
            self.list_data_types.insert(END, name)

        self.list_data_types.bind('<<ListboxSelect>>', self.get_selected_data_type)

        sb1 = Scrollbar(rigth_bottom_frame_up)
        sb1.pack(side=RIGHT, fill=Y)

        self.list1 = Listbox(rigth_bottom_frame_up, width=40, height=23)
        self.list1.pack(side=TOP)

        self.columns_names = DataRead.read_columns(self.chosen_data_type)

        self.list1.config(yscrollcommand=sb1.set)
        sb1.config(command=self.list1.yview)

        self.list1.bind('<<ListboxSelect>>', self.get_selected_name)

        b1 = Button(rigth_bottom_frame_up, text="Generate map", width=20, command=self.generate_map)
        b1.pack()

        # ----------------------------------------------------
        # PIE CHARTS CREATION TOOLS

        sb2 = Scrollbar(rigth_bottom_frame_down)
        sb2.pack(side=RIGHT, fill=Y)

        self.list2 = Listbox(rigth_bottom_frame_down, width=40, height=6)
        self.list2.pack(side=TOP)

        file_names = DataRead.give_pie_chart_files_names(self.chosen_data_type)
        for name in file_names:
            self.list2.insert(END, name)

        self.list2.config(yscrollcommand=sb1.set)
        sb2.config(command=self.list2.yview)

        self.list2.bind('<<ListboxSelect>>', self.get_selected_name_pie_chart)

        b2 = Button(rigth_bottom_frame_down, text="Add pie charts", width=20, command=self.add_pie_charts)
        b2.pack()

    def get_selected_data_type(self, event):
        self.list1.delete(0, END)
        self.list2.delete(0, END)
        index = self.list_data_types.curselection()[0]
        selected_data_type = self.list_data_types.get(index)
        self.chosen_data_type = selected_data_type
        self.columns_names = DataRead.read_columns(self.chosen_data_type)
        self.data = DataRead.read_data(self.chosen_data_type)
        for name in self.columns_names:
            self.list1.insert(END, name)
        file_names = DataRead.give_pie_chart_files_names(self.chosen_data_type)
        for name in file_names:
            self.list2.insert(END, name)

    def get_selected_name(self, event):
        try:
            index = self.list1.curselection()[0]
            selected_name = self.list1.get(index)
            self.column = self.data[selected_name]
            for row, value in zip(self.label_value_row, self.column):
                row['text'] = value
        except IndexError:
            pass

    def get_selected_name_pie_chart(self, event):
        try:
            index = self.list2.curselection()[0]
            selected_name = self.list2.get(index)
            path = r"regions_data\\" + self.chosen_data_type + r"\\pie_chart_data\\" + selected_name
            self.pie_chart_path = path
        except IndexError:
            pass

    def add_pie_charts(self):
        add_charts(self.pie_chart_path, self.colors_type.get())
        self.map_image = PhotoImage(file="final_map.png")
        self.label.config(image=self.map_image)

    def generate_map(self):
        final_intervals = self.get_intervals()
        create_map(self.column, final_intervals, self.chosen_color.get(), self.charts_status.get())
        self.map_image = PhotoImage(file="final_map.png")
        self.label.config(image=self.map_image)

    def get_intervals(self):
        intervals_all = [
            self.interval1_value.get(), self.interval2_value.get(), self.interval3_value.get(),
            self.interval4_value.get(), self.interval5_value.get(), self.interval6_value.get()
            ]
        final_intervals = []
        for interval_id in range(6):
            if intervals_all[interval_id] != '':
                try:
                    final_intervals.append(int(intervals_all[interval_id]))
                except ValueError:
                    final_intervals.append(float(intervals_all[interval_id]))
            else:
                break
        return final_intervals


class DataRead:
    # READ FILE
    @staticmethod
    def read_data(name):
        path = r"regions_data\\" + name + r"\data.xlsx"
        data = pandas.read_excel(path)
        return data

    @staticmethod
    def read_columns(name):
        path = r"regions_data\\" + name + r"\data.xlsx"
        data = pandas.read_excel(path)
        columns = list(data)
        return columns

    @staticmethod
    def give_pie_chart_files_names(name):
        files = [file for file in os.listdir(r"regions_data\\" + name + "\pie_chart_data") if file.endswith(".xlsx")]
        return files


root = Tk()
root.style = Style()
root.style.theme_use("clam")
m1 = App(root)
root.mainloop()
