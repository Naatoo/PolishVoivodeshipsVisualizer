from tkinter import Tk, Label, Entry, StringVar, Listbox, Scrollbar, Button, END, PhotoImage, Canvas, Frame, LEFT, BOTTOM, RIGHT, BOTH, X, OptionMenu
from map_generator import Map, DataRead
from PIL import Image, ImageTk


class App:
    def __init__(self):
        self.data = DataRead()

        window = Tk()
        window.wm_title("Polish Regions Data Visualizer")

        upperframe = Frame(window)
        upperframe.pack(expand=True, fill=X)

        bottomframe = Frame(window)
        bottomframe.pack(side=BOTTOM)

        left_bottom_frame = Frame(bottomframe)
        left_bottom_frame.pack(side=LEFT)

        dataframe = Frame(left_bottom_frame)
        dataframe.pack(side=LEFT, fill=BOTH)

        imageframe = Frame(left_bottom_frame)
        imageframe.pack(side=RIGHT)

        rigth_bottom_frame = Frame(bottomframe)
        rigth_bottom_frame.pack(side=RIGHT)



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

        data_label = Label(dataframe, text="Current data:")
        data_label.grid(row=0, column=0)

        data_for_region = {}
        for region in range(16):
            data_for_region["d{}".format(region)] = self.data.column[region]
        index = 0
        for k, v in data_for_region.items():
            k = Label(dataframe, text=v)
            k.grid(row=index + 1, column=0)
            dataframe.grid_rowconfigure(index + 1, minsize=34)
            index += 1



      #  self.image = "test.png"
        self.map_image = PhotoImage(file="test.png")
        self.label = Label(imageframe, image=self.map_image)
        self.label.pack()

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

        for column in range(6):
            upperframe.grid_columnconfigure(column, minsize=126)

        b1 = Button(rigth_bottom_frame, text="Generate map", width=10, command=self.generate_map)
        b1.pack()

        self.chosen_color = StringVar(rigth_bottom_frame)
        self.chosen_color.set("Green")  # default value
        colors = ("Green", "Blue", "Orange", "Red", "Purple", "Gray")

        w = OptionMenu(rigth_bottom_frame, self.chosen_color, *colors)
        w.pack()

        window.mainloop()

    def generate_map(self):
        final_intervals = self.get_intervals()
        map = Map(self.data.column, final_intervals, self.chosen_color.get())
        self.map_image = PhotoImage(file="test.png")
        self.label.config(image=self.map_image)

    def get_intervals(self):
        intervals_all = [
            self.interval1_value.get(), self.interval2_value.get(), self.interval3_value.get(),
            self.interval4_value.get(), self.interval5_value.get(), self.interval6_value.get()
            ]
        final_intervals = []
        for interval_id in range(6):
            if intervals_all[interval_id] != '':
                final_intervals.append(int(intervals_all[interval_id]))
            else:
                break
        return final_intervals



m1 = App()



