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

myclient = pymongo.MongoClient('mongodb://192.168.0.13:27017')
print(myclient.list_database_names())
mydb = myclient["test_database"]
mycol = mydb["Running_time"]



##It is about the GUI
Window1 = tk.Tk()
Window1.title("Analysis")
Window1.geometry('640x480')
title1 = tk.Label(Window1, text="Chart of Number")
title1.grid(row=0, column=0, sticky='w')


fig = plt.figure(figsize=[6, 6])
x_format = matplotlib.dates.DateFormatter('%m-%d %H:%M')
plt.autoscale(enable=True, axis='x', tight=False)
ax = plt.subplot(111)
ax.set_ylim([0, 4])


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
    cursor = mycol.find({})
    count = 0
    dates = [0]*10
    for document in cursor:
        #print(document["Random_Num"])
        y_plot[count] = int(document["Random_Num"])
        print(str(document["Random_Num"]))
        dt_object = datetime.datetime.fromtimestamp(document["Time_stamp"])
        dates[count] = dt_object
        count += 1
    #dt_object = datetime.datetime.fromtimestamp(x_plot)
    #dates = matplotlib.dates.date2num(dt_object)
    #matplotlib.pyplot.plot_date(dates, y_plot)   
    #line.set_xdata(numpy.append(line.get_xdata(), x_plot))
    #line.set_ydata(numpy.append(line.get_ydata(), y_plot))
    x_format = matplotlib.dates.DateFormatter('%m/%d %H:%M:%S')
    ax.xaxis.set_major_formatter(x_format)
    # beautify the x-labels
    plt.gcf().autofmt_xdate()
    plt.autoscale(enable=True, axis='both', tight=True)
    ax.plot(dates, y_plot, 'b')
    #plt.plot(x_plot, y_plot, 'b')
    fig.canvas.draw()
    #fig.canvas.flush_events()
    Window1.after(1, update_plot) 

Window1.after(1, update_plot)    
Window1.mainloop()
