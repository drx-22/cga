import ctypes as ct
import tkinter as tk 
from tkinter import ttk
from tkinter import filedialog
import os

styles = {
    "xpad" : [10],
    "ypad" : [10],
    "height": 300,
    "width": 500
}

#* Estilo de la ventana para eliminar el boton de maximizar
def setWinStyle(root):
    set_window_pos = ct.windll.user32.SetWindowPos
    set_window_long = ct.windll.user32.SetWindowLongPtrW
    get_window_long = ct.windll.user32.GetWindowLongPtrW
    get_parent = ct.windll.user32.GetParent

    # Identifiers
    gwl_style = -16

    ws_minimizebox = 131072
    ws_maximizebox = 65536

    swp_nozorder = 4
    swp_nomove = 2
    swp_nosize = 1
    swp_framechanged = 32

    hwnd = get_parent(root.winfo_id())

    old_style = get_window_long(hwnd, gwl_style) # Get the style

    new_style = old_style & ~ ws_maximizebox # New style, without max buttons

    set_window_long(hwnd, gwl_style, new_style) # Apply the new style

    set_window_pos(hwnd, 0, 0, 0, 0, 0, swp_nomove | swp_nosize | swp_nozorder | swp_framechanged)     # Updates

def about():
    abtWin = tk.Tk()
    abtWin.geometry(f"{styles['width'] + 150}x{styles['height']}")
    abtWin.resizable(False, False)
    abtWin.title("Acerca del Creador")

    label01 = ttk.Label(abtWin, text="Acerca de Mi", font=('Calibri', 16))
    label01.pack(padx=styles["xpad"][0], pady=styles["ypad"][0])

    separator = ttk.Separator(abtWin, orient='horizontal')
    separator.pack(fill='x')
    
    string =""
    with open(os.path.join("res", "resources", "about.txt")) as f:
        string = f.read()

    label = tk.Label(abtWin, text = string, font=("calibri", 11))
    label.pack()

    abtWin.after(10, lambda: setWinStyle(abtWin))
    abtWin.mainloop()
    pass

def info():
    abtWin = tk.Tk()
    abtWin.geometry(f"{styles['width'] + 150}x{styles['height'] + 250}")
    abtWin.resizable(False, False)
    abtWin.title("Informacion")

    label01 = ttk.Label(abtWin, text="Informacion", font=('Calibri', 16))
    label01.pack(padx=styles["xpad"][0], pady=styles["ypad"][0])

    separator = ttk.Separator(abtWin, orient='horizontal')
    separator.pack(fill='x')
    
    string =""
    with open(os.path.join("res", "resources", "doc.txt")) as f:
        string = f.read()

    label = tk.Label(abtWin, text = string, font=("calibri", 11))
    label.pack()

    abtWin.after(10, lambda: setWinStyle(abtWin))
    abtWin.mainloop()
    pass