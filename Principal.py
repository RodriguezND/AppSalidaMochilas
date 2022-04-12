from tkinter import *
from tkinter import ttk
from index import Principal
from ttkthemes import ThemedTk


if __name__ == "__main__":

    
    window = ThemedTk(theme="aquativo")

    app= Principal(window)

    window.mainloop() 
