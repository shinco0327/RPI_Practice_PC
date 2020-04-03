import pymongo
import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
import time
import numpy
import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
matplotlib.use('TkAgg') #Use tkAgg

y_plot = [0]*10
x_plot = [0]*10
graph_update_time = 0

myclient = pymongo.MongoClient('mongodb://192.168.0.13:27017')
print(myclient.list_database_names())
mydb = myclient["test_database"]
mycol = mydb["VR_test"]



##It is about the GUI
Window1 = tk.Tk()
Window1.title("Analysis")
Window1.geometry('640x480')
title1 = tk.Label(Window1, text="Current time:")
title1.grid(row=0, column=0, sticky='w')


fig = plt.figure(figsize=[6, 6])
x_format = matplotlib.dates.DateFormatter('%m-%d %H:%M')
plt.autoscale(enable=True, axis='x', tight=False)
plt.title("Voltage of VR")
plt.xlabel("Time")
plt.ylabel("Voltage(V)")
plt.ylim(0, 3.5)


canvas = FigureCanvasTkAgg(fig, master=Window1)  # A tk.DrawingArea.
#canvas.draw()
canvas.get_tk_widget().grid(row=1, column=0, columnspan=3)

toolbar_frame = tk.Frame(Window1)
toolbar_frame.grid(row=2, column=0, columnspan=2)
toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
toolbar.update()

def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)


canvas.mpl_connect("key_press_event", on_key_press)
 

def update_plot():
    global graph_update_time
    global title1
    title1_str = "Current time: "+ time.asctime(time.localtime(time.time()))
    title1.configure(text=title1_str)
    if time.time()-graph_update_time >= 60:
        plt.clf()
        x_format = matplotlib.dates.DateFormatter('%m-%d %H:%M')
        plt.autoscale(enable=True, axis='x', tight=False)
        plt.title("Voltage of VR")
        plt.xlabel("Time")
        plt.ylabel("Voltage(V)")
        plt.ylim(0, 3.5)
        graph_update_time = time.time()
    cursor = mycol.find(sort=[("_id", pymongo.DESCENDING)]).limit(10)
    count = 0
    dates = [0]*10
    for document in cursor:
        #print(document["Random_Num"])
        y_plot[count] = float(document["Random_Num"])
        print(str(document["Random_Num"]))
        dt_object = datetime.datetime.fromtimestamp(document["Time_stamp"])
        dates[count] = dt_object
        count += 1

    x_format = matplotlib.dates.DateFormatter('%m/%d %H:%M:%S')
    plt.gca().xaxis.set_major_formatter(x_format)
    # beautify the x-labels
    plt.gcf().autofmt_xdate()
    plt.autoscale(enable=True, axis='x', tight=True)
    plt.plot(dates, y_plot, 'b')
    
    fig.canvas.draw()
    fig.canvas.flush_events()
    Window1.after(1, update_plot) 

Window1.after(1, update_plot)    
Window1.mainloop()
