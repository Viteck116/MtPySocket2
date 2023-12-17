# -*- coding: utf-8 -*-
"""
Vital$oft (c) 2023
"""
# package import
# import the package to create controls
import tkinter as tk
from tkinter import *
# import matplotlib
#import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import(FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
# import dialog package
#from tkinter.messagebox import showerror
# import warning package
#import warnings
# import package waiting for I/O to complete
#import select
# import thread management package
import threading
# import timer package
#import time
# import keyboard package
#import keyboard 
# import socket creation package
import socket, numpy as np
# import mathematics linear regression
from sklearn.linear_model import LinearRegression
#---
# class Socket creating
class socketserver:
# constructor
    def __init__(self, address = '', port = 9090):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.sock)
        #self.sock.setblocking(False)
        self.address = address
        self.port = port
        self.sock.bind((self.address, self.port))
        self.cummdata = ''
        
# let's connect       
    def recvmsg(self):
        self.sock.listen(1)    
        self.conn, self.addr = self.sock.accept()
        print('Connected to', self.port)
        global RUN1
        if RUN1:
            if self.port == 9091:
                clientname1(self.addr)
            if self.port == 9092:
                clientname2(self.addr)    
        self.cummdata = ''         
        while RUN1:
            self.data = self.conn.recv(10000)
            self.cummdata+=self.data.decode('UTF-8')
            if not self.data:
                print('Client disconnected...')
                if self.port == 9091:
                    clientname1("no connection")
                if self.port == 9092:
                    clientname2("no connection")                  
                break  
            if self.port == 9091:
                self.conn.send(bytes(calcregr1(self.cummdata), 'UTF-8'))
            if self.port == 9092:
                self.conn.send(bytes(calcregr2(self.cummdata), 'UTF-8'))
            return self.cummdata
            
# destructor
    def __del__(self):
        self.sock.close()
        print('Socket closed')
 
# working with data received from socket 1       
def calcregr1(msg = ''):
    chartdata = np.fromstring(msg, dtype=float, sep= ' ')     
    Y = np.array(chartdata).reshape(-1,1)
    X = np.array(np.arange(len(chartdata))).reshape(-1,1)   
    # drawing a graph
    graph1(X,Y)
    lr = LinearRegression()
    lr.fit(X, Y)
    Y_pred = lr.predict(X)
    global P
    P = Y_pred.astype(str).item(-1) + ' ' + Y_pred.astype(str).item(0)
    print(P)
    return str(P)
# working with data received from socket 2       
def calcregr2(msg = ''):
    chartdata = np.fromstring(msg, dtype=float, sep= ' ')     
    Y = np.array(chartdata).reshape(-1,1)
    X = np.array(np.arange(len(chartdata))).reshape(-1,1)   
    # drawing a graph
    graph2(X,Y)
    lr = LinearRegression()
    lr.fit(X, Y)
    Y_pred = lr.predict(X)
    global P
    P = Y_pred.astype(str).item(-1) + ' ' + Y_pred.astype(str).item(0)
    print(P)
    return str(P)



# create 2 socket instances
serv1 = socketserver('localhost', 9091)
serv2 = socketserver('localhost', 9092)
# cycle management where needed
RUN1 = False
# socket 1 run
def SocketRun1(): 
    global RUN1
    RUN1 = True
    print('\nSocked1 is running')
    print('Waiting for connection...')
    while RUN1:  
       msg = serv1.recvmsg()
       if not serv1.data:                     
           print('Socket1 disconnected')   
           clientname1("no connection")
           #break
# socket 2 run          
def SocketRun2(): 
    global RUN1
    RUN1 = True
    print('\nSocked2 is running')
    print('Waiting for connection...')
    while RUN1:         
       msg = serv2.recvmsg()
       if not serv2.data:                     
           print('Socket2 disconnected')   
           clientname2("no connection")
           #break
           
# creating separate threads to run sockets 
def ThreadRun():  
    btn1["state"] = "disabled"
    btn2["state"] = "normal"
    if __name__ == '__main__':
        p1 = threading.Thread(target = SocketRun1, daemon=True)
        p1.start()
        #p1.join() 
        p2 = threading.Thread(target = SocketRun2, daemon=True)
        p2.start()
        #p2.join() 
# separate thread for updating the canvas
        p3 = threading.Thread(target = CanvasDraw, daemon=True)
        p3.start()

# stopping sockets
def SocketStop():   
    btn2["state"] = "disabled"
    btn1["state"] = "normal"
    global RUN1
    RUN1 = False  
# socket 1 stop      
    print('Wait socket1 stops...')     
    clientname1('no connection') 
# socket 2 stop     
    print('Wait socket2 stops...')       
    clientname2('no connection') 
    
   
    

    

# socket end  
#---
# GUI CREATING
# create the main window
root = Tk()    
# title at the top of the window
root.title("MT5 Socket Server Vital$oft(c) 2023") 
# main window dimensions
root.geometry("1280x600")    
# main window color
root['bg'] = 'gainsboro'
# create a frame for the chart
frameUp = Frame(root, borderwidth = 1, relief=RAISED)
# frame location
frameUp.place(x=10, y=100, width=1260, height=450)
# create a figure
figure =plt.Figure(figsize=(6, 4), dpi=100, facecolor = 'gainsboro')
# create FigureCanvasTkAgg object
figure_canvas = FigureCanvasTkAgg(figure, master=frameUp)
figure_canvas.draw()
# create the toolbar
toolbar = NavigationToolbar2Tk(figure_canvas, root)
#toolbar['bg'] = 'gainsboro'
toolbar.update()
# create axes
#axes = figure.add_subplot(1, 1, 1)
axes = figure.subplots()
# to draw the second line
axes2 = axes.twinx()
# background graphics black
axes.set_facecolor('black')
widg = figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# draw lines based on the received data
# socket 1
def graph1(X,Y):    
    # clear
    axes.clear() 
    # grid
    #axes.grid()
    # line draw 
    axes.plot(X, Y, color='red', linewidth=1)  
    
# socket 2
def graph2(X,Y):    
    # clear
    axes2.clear() 
    # grid
    #axes.grid()
    # line draw 
    axes2.plot(X, Y, color='blue', linewidth=1)  
    
# updating the canvas so that the lines move is launched in a separate thread
def CanvasDraw():
    global RUN1
    while RUN1:
        figure_canvas.draw()
    
# customer information
def clientname1(status1 = ''):
    label3.config(text = status1)
def clientname2(status2 = ''):    
    label4.config(text = status2)

 

# socket launch button 1
btn1 = Button(text="Socket Run", width=12, height=2) 
btn1.config(command=ThreadRun)
# button 1 location
btn1.place(x=10, y=10)
# button 1 color
btn1['bg'] = 'gainsboro'
# socket stop button 2
btn2 = Button(text="Socket Stop", width=12, height=2) 
btn2.config(command=SocketStop)
# button 2 location
btn2.place(x=10, y=50)
# button 2 color
btn2['bg'] = 'gainsboro'
# inactive when starting the program
btn2["state"] = "disabled"
# labels for displaying information about clients
label1 = Label(text="Client 1 status:", foreground = 'red', width=12, height=2, borderwidth=0, relief="solid")
label1['bg'] = 'gainsboro'
label1.place(x=150, y=14)
label2 = Label(text="Client 2 status:", foreground = 'blue', width=12, height=2, borderwidth=0, relief="solid")
label2['bg'] = 'gainsboro'
label2.place(x=150, y=54)
label3 = Label(text="no connection", width=40, height=2, borderwidth=0, relief="solid")
label3['bg'] = 'gainsboro'
label3.place(x=250, y=14)
label4 = Label(text="no connection", width=40, height=2, borderwidth=0, relief="solid")
label4['bg'] = 'gainsboro'
label4.place(x=250, y=54)





#---
# working in the main process
root.mainloop()

# --- End GUI