import pymongo
import tkinter as tk
from tkinter import ttk
import matplotlib
import matplotlib.pyplot as plt
import time
import numpy
import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
matplotlib.use('TkAgg') #Use tkAgg

def view_all_data():
    Window2 = tk.Toplevel()
    Window2.title("View All Data")
    Window2.geometry("640x640")
    view_all_fig = plt.figure(2, figsize=[6, 6])
    plt.clf()
    matplotlib.dates.DateFormatter('%m-%d %H:%M')
    plt.autoscale(enable=True, axis='x', tight=False)
    plt.title("View all data of the voltage of VR")
    plt.xlabel("Time")
    plt.ylabel("Voltage(V)")
    plt.ylim(-0.5, 3.5)

    cursor = mycol.find()
    all_y_plot = [0]*int(mycol.count_documents({}))
    count = 0
    all_dates = [0]*int(mycol.count_documents({}))
    for document in cursor:
        all_y_plot[count] = float(document["Random_Num"])
        dt_object = datetime.datetime.fromtimestamp(document["Time_stamp"])
        all_dates[count] = dt_object
        count += 1

    x_format = matplotlib.dates.DateFormatter('%m/%d %H:%M:%S')
    plt.gca().xaxis.set_major_formatter(x_format)
    # beautify the x-labels
    plt.gcf().autofmt_xdate()
    plt.autoscale(enable=True, axis='x', tight=True)
    plt.plot(all_dates, all_y_plot, 'r')

    view_all_canvas = FigureCanvasTkAgg(view_all_fig, master=Window2)  # A tk.DrawingArea.
    #canvas.draw()
    view_all_canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)

    view_all_toolbar_frame = tk.Frame(Window2)
    view_all_toolbar_frame.grid(row=1, column=0, columnspan=2)
    view_all_toolbar_frame= NavigationToolbar2Tk(view_all_canvas, view_all_toolbar_frame)
    view_all_toolbar_frame.update()

def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)

def update_plot():
    plt.figure(1)
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
        plt.ylim(-0.5, 3.5)
        graph_update_time = time.time()
    cursor = mycol.find(sort=[("_id", pymongo.DESCENDING)]).limit(10)
    count = 0
    dates = [0]*10
    for document in cursor:
        y_plot[count] = float(document["Random_Num"])
        #For debug
        #print(str(document["Random_Num"]))
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

def list_time():
    cursor = mycol.find()
    list1 = []
    for documents in cursor:
        #print((documents["Time_stamp"]))
        list1.append(time.asctime(time.localtime(documents["Time_stamp"])))
        #print(datetime.datetime.strptime(time.asctime(time.localtime(documents["Time_stamp"])), "%a %b %d %H:%M:%S %Y").timestamp())
        for i in range(0, 20):
            try:
                next(cursor)
            except StopIteration:
                break
    list_time_box["values"] = list1 
    Window1.after(10, list_time)

def listed_time_selected():
    if list_time_box.get() == '':
        return
    Window3 = tk.Toplevel()
    Window3.title("View Data")
    Window3.geometry("640x640")
    fig = plt.figure(3, figsize=[6, 6])
    plt.figure(3)
    plt.clf()
    matplotlib.dates.DateFormatter('%m-%d %H:%M')
    plt.autoscale(enable=True, axis='x', tight=False)
    plt.title("View data of the voltage of VR")
    plt.xlabel("Time")
    plt.ylabel("Voltage(V)")
    plt.ylim(-0.5, 3.5)
    

    selected_time = int(datetime.datetime.strptime(list_time_box.get(), "%a %b %d %H:%M:%S %Y").timestamp())
    #print(datetime.datetime.strptime(selected_time, "%a %b %d %H:%M:%S %Y").timestamp())
    cusor = mycol.find()
    count = 0
    documents_time = []
    documents_volt = []
    
    for documents in cusor:
        if selected_time == int(documents["Time_stamp"]):
            count += 1
        if count != 0:
            documents_time.append(datetime.datetime.fromtimestamp(documents["Time_stamp"]))
            documents_volt.append(documents["Random_Num"])
            count += 1
            if count >= 20:
                break

    x_format = matplotlib.dates.DateFormatter('%m/%d %H:%M:%S')
    plt.gca().xaxis.set_major_formatter(x_format)
    # beautify the x-labels
    plt.gcf().autofmt_xdate()
    plt.autoscale(enable=True, axis='x', tight=True)
    plt.plot(documents_time, documents_volt, 'g')

    canvas = FigureCanvasTkAgg(fig, master=Window3)  # A tk.DrawingArea.
    #canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)

    toolbar_frame = tk.Frame(Window3)
    toolbar_frame.grid(row=1, column=0, columnspan=2)
    toolbar_frame= NavigationToolbar2Tk(canvas, toolbar_frame)
    toolbar_frame.update()


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
Window1.geometry('1024x768')
title1 = tk.Label(Window1, text="Current time:")
title1.grid(row=0, column=0, sticky='w', columnspan=3)
btn1 = tk.Button(Window1, text="View all data", command=view_all_data)
btn1.grid(row=1, column=0, sticky='w')
list_label = tk.Label(Window1, text="View values in specific time interval")
list_label.grid(row=1, column=1, sticky='e')
list_time_box = ttk.Combobox(Window1)
list_time_box.grid(row=1, column=2) 
btn2 = tk.Button(Window1, text="GO", command=listed_time_selected)
btn2.grid(row=1, column=3, sticky='w')

fig = plt.figure(figsize=[6, 6])
x_format = matplotlib.dates.DateFormatter('%m-%d %H:%M')
plt.autoscale(enable=True, axis='x', tight=False)
plt.title("Voltage of VR")
plt.xlabel("Time")
plt.ylabel("Voltage(V)")
plt.ylim(0, 3.5)


canvas = FigureCanvasTkAgg(fig, master=Window1)  # A tk.DrawingArea.
#canvas.draw()
canvas.get_tk_widget().grid(row=3, column=0, columnspan=4)

toolbar_frame = tk.Frame(Window1)
toolbar_frame.grid(row=4, column=0, columnspan=4)
toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
toolbar.update()


    


canvas.mpl_connect("key_press_event", on_key_press)
 


Window1.after(1, update_plot)    
Window1.after(10, list_time)
Window1.mainloop()

