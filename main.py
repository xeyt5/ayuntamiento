import customtkinter as ctk
from openpyxl import Workbook, load_workbook
import os
from tkinter import ttk

archivo_guardar = "Ayuntamiento.xlsx"

def guardar_excel():
    nombre = entry_nombre.get()
    telefono = entry_telefono.get()
    if nombre == "" or telefono == "":
        label.configure(text="campo vacio, necesita colocar info")
        return
    if not os.path.exists(archivo_guardar):
        wb = Workbook ()
        ws = wb.active
        ws.title = "Datos"
        ws.append(["Nombre", "Telefono"])
    else:
        wb = load_workbook(archivo_guardar)
        ws = wb.active
    
    #agregar un dato
    ws.append([nombre, telefono])
    wb.save(archivo_guardar)
    label.configure(text="dato guardado")
    entry_nombre.delete(0, ctk.END)
    entry_telefono.delete(0, ctk.END)

def mostrar_datos():
    for fila in tree.get_children():
        tree.delete(fila)
    if not os.path.exists(archivo_guardar):
        return
    
    wb = load_workbook(archivo_guardar)
    ws = wb.active

    for fila in ws.iter_rows(min_row=2, values_only=True):
        tree.insert("", "end", values=fila)
    




ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Ayuntamiento")
app.geometry("600x400")

label = ctk.CTkLabel(app, text="Nombre", font=("Arial", 20))
label.pack(pady=5)
entry_nombre = ctk.CTkEntry(app, placeholder_text="tu nombre")
entry_nombre.pack(pady=5)

label_tel = ctk.CTkLabel(app, text="Telefono")
label_tel.pack(pady=5)
entry_telefono = ctk.CTkEntry(app, placeholder_text="ejemplo: 734218361623")
entry_telefono.pack(pady=5)

button = ctk.CTkButton(app, text="guardar datos", command=guardar_excel)
button.pack(pady=10)

frame_tabla = ctk.CTkFrame(app)
frame_tabla.pack(pady=10, fill="both", expand=True)

tree = ttk.Treeview(frame_tabla, columns=("Nombre", "Telefono"), show="headings")
tree.heading("Nombre", text="Nombre")
tree.heading("Telefono", text="Telefono")
tree.pack(fill="both", expand=True)

boton_mostrar = ctk.CTkButton(app, text="mostrar datos", command=mostrar_datos)
boton_mostrar.pack(pady=10)

app.mainloop()
