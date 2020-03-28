import pymongo
import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
import time
import numpy
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
matplotlib.use('TkAgg') #Use tkAgg

y_plot = [0]*10
x_plot = [0]*10

myclient = pymongo.MongoClient('mongodb://192.168.0.13:27017')
print(myclient.list_database_names())
mydb = myclient["test_database"]

mycol = mydb["Running_time"]

cursor = mycol.find({})
total = 0
count = 0
for document in cursor:
    print(document["Random_Num"])
    #y_plot[count] = int(document["Random_Num"])
    #x_plot[count] = count
    total += int(document["Random_Num"])
    count += 1
print("Average is "+str(total/count))

##It is about the GUI
Window1 = tk.Tk()
Window1.title("Analysis")
Window1.geometry('640x480')
title1 = tk.Label(Window1, text="Chart of Number")
title1.grid(row=0, column=0, sticky='w')


fig = plt.figure(figsize=[5,4])
ax = fig.add_subplot(111)
plt.xlim(-100, 100)
plt.ylim(-10000, 10)
line, = ax.plot([], [])


canvas = FigureCanvasTkAgg(fig, master=Window1)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().grid(row=1, column=0, columnspan=3)

toolbar_frame = tk.Frame(Window1)
toolbar_frame.grid(row=2, column=0, columnspan=2)
toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
toolbar.update()

def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)


canvas.mpl_connect("key_press_event", on_key_press)
 
count = -100
def update_plot():
    global count
    if count < 100:
        for n in range(0, 10):
            x_plot[n] = count
            y_plot[n] = -(count*count)
            print(count)
            count += 1
        
        line.set_xdata(numpy.append(line.get_xdata(), x_plot))
        line.set_ydata(numpy.append(line.get_ydata(), y_plot))
        fig.canvas.draw()
        fig.canvas.flush_events()
    Window1.after(1, update_plot) 

Window1.after(1, update_plot)    
Window1.mainloop()
