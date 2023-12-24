import tkinter as tk
from window_helpers import *
from tkinter import ttk
from tkinter import messagebox
import re
import os

#* Cadena que tendra el input
string = ""
route = ""

#* procesara el archivo de texto y devolvera listas que usara el algoritmo original

def leer_archivo_c(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        contenido = archivo.read()
    
    patrón = r'long\s+(\w+)\s*\[\d+\]\s*=\s*{([^}]+)}'  # Expresión regular para buscar arreglos
    
    nombres_arreglos = []  # Aquí almacenaremos los nombres de los arreglos
    listas_numeros = []   # Aquí almacenaremos las listas de números
    
    for coincidencia in re.finditer(patrón, contenido):
        nombre = coincidencia.group(1)
        arreglo = coincidencia.group(2)
        
        nombres_arreglos.append(nombre)
        
        numeros = [int(num) for num in re.findall(r'\b\d+\b', arreglo)]
        listas_numeros.append(numeros)
    
    return nombres_arreglos, listas_numeros

#* Aplicara el algoritmo original
def process(route):

    filename = inputName.get()
    if route == "":
        messagebox.showerror("Error", "Ingresa una ruta")
    if filename == "":
        messagebox.showerror("Error", "Ingresa un nombre de archivo")
        return

    with open(os.path.join("output", f"{filename}.txt"), 'w') as f:
        error = False
        names = ["a"]
        fullList = [[0]]
        try:
            names, fullList = leer_archivo_c(route)
        except FileNotFoundError:
            messagebox.showerror("Error", "El archivo no fue encontrado")
            error = True
        
        if error:
            return
        
        masterString = ""
        nameIndex = 0
        for element in fullList:
            
            #+ Algoritmo original, diseñado en 2021
            lst = element
            menor = lst[0]
            index = 0
            for i in range(len(lst)):
                if (lst[index] < menor and index % 2 == 0):
                    menor = lst[index]
                index += 1

            menor2 = lst[0]
            index = 0
            
            for i in range(len(lst)):
                if (lst[index] < menor2 and index % 2 != 0):
                    menor2 = lst[index]
                index += 1
            #+ DEBUG
            #print (menor, menor2)

            name = names[nameIndex]
            masterString += "int " + str(name) + "(int x, int y, int color){" +  "\n" +  "    int col_ant;\n    col_ant = getcolor();\n    setcolor(color);\n"

            index = 0
            leg = int((len(lst)/2) - 1)
            for i in range(leg):
                masterString += "    line(" + str(lst[0+index]) + "-" + str(menor) + " + x" + "," + str(lst[index+1]) + "-" + str(menor2) + " + y" +  "," + str(lst[index+2]) + "-" + str(menor) + " + x" +  "," + str(lst[index+3]) + "-" + str(menor2) + " + y" + ");\n"
                index += 2

            masterString += "    line(" + str(lst[-2]) + "-" +  str(menor) +  " + x" +  "," + str(lst[-1]) + "-" + str(menor2) + " + y" +  "," + str(lst[0]) + "-" + str(menor) + " + x" +  "," + str(lst[1])  + "-" + str(menor2) + " + y" + ");"
            masterString += "\n    setcolor(col_ant);\n    return 0;\n}"
            #! DEBUG
            #print(masterString)
            f.write(masterString)
            nameIndex += 1
    messagebox.showinfo("Exito", "Proceso exitoso, revisa tu archivo en la carpeta output")


#* Obtiene la ruta del archivo, es el callback del boton de seleccion de ruta
def getRoute():
    file_path = filedialog.askopenfilename(filetypes=(("Archivos de Texto","*.txt"),("All files","*.*")))
    inputRoute.delete(0, tk.END)
    inputRoute.insert(tk.END, file_path) # add this <-----  Stack Overflow Bro :)

#* Es la funcion que genera el archivo final con las funciones, es el callback del boton generar
def generate():
    route = inputRoute.get()
    ans = messagebox.askyesno("Warning", "Antes de usar esta herramienta, asegurate de que\n" + 
                        "la sintaxis dentro del archivo de arreglos sea correcta \n" + 
                        "y que no exista ningun error dentro del archivo\n\nContinuar con el proceso?", default='yes')
    #! DEBUG
    #print(ans)

    if ans:
        #! DEBUG
        # print("yes")
        # print(process(route= route)) # Esta linea no hace nada, pero me permite debuggear, si lo quito no puedo ver nada en la consola ????
        process(route= route)

#* Coordenadas para multiples usos
styles = {
    "xpad" : [10],
    "ypad" : [10],
    "height": 300,
    "width": 500
}

#* Inicializacion de la ventana principal

root = tk.Tk()
root.geometry(f"{styles['width']}x{styles['height']}")
root.resizable(False, False)
root.title("C - Graph Assistant")

#* Boton para Acerca De
acercade = tk.Button(root, text="?", font=("Calibri", 12), command=about)
acercade.place(height=20, width=20, x=styles["width"]-50, y=10)

#* Boton para Documentacion
info = tk.Button(root, text="!", font=("Calibri", 12), command=info)
info.place(height=20, width=20, x=styles["width"]-30, y=10)

label01 = tk.Label(text="C - Graph Assistant", font=('Calibri', 16))
label01.pack(padx=styles["xpad"][0], pady=styles["ypad"][0])

separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill='x')

frame = tk.Frame(root, pady=20)
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

#ruta en texto
inputRoute = tk.Entry(frame)

# Boton para seleccionar ruta
btnRoute = tk.Button(frame, text="Seleccionar Archivo de Arreglos", command=getRoute)

labelRuta = tk.Label(frame, text="Ruta:", font=("Calibri", 12))

labelName = tk.Label(frame, text="Nombre del archivo:", font=("Calibri", 12))

inputName = tk.Entry(frame)

labelRuta.grid(row=0, column=1)
btnRoute.grid(row=1, column=0)
inputRoute.grid(row=1, column=1)
labelName.grid(row=2, column=1)
inputName.grid(row=3, column=1)

btnGenera = tk.Button(root, text="Generar Funciones de Animacion", command=generate, pady=10)
btnGenera.pack()

frame.pack(fill="x")


root.after(10, lambda: setWinStyle(root))
root.mainloop()