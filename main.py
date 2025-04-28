import customtkinter as ctk
import mysql.connector
from tkinter import ttk, messagebox
import os

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': '',
    'password': '',
    'database': ''
}

fila_seleccionada = None

# Función para obtener conexión a la base de datos
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Error de base de datos", f"Error: {err}")
        return None

# Crear tabla si no existe
def crear_tabla_si_no_existe():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuario (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100),
                    apellido VARCHAR(100),
                    telefono VARCHAR(20)
                )
            """)
            conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al crear tabla: {err}")
        finally:
            conn.close()

crear_tabla_si_no_existe()

def guardar_db():
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    telefono = entry_telefono.get()
    
    if nombre == "" or telefono == "" or apellido == "":
        label_estado.configure(text="Todos los campos son obligatorios")
        return
    
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuario (nombre, apellido, telefono) VALUES (%s, %s, %s)",
                (nombre, apellido, telefono)
            )
            conn.commit()
            label_estado.configure(text="✅ Registro guardado")
            
            # Limpiar campos
            entry_nombre.delete(0, ctk.END)
            entry_apellido.delete(0, ctk.END)
            entry_telefono.delete(0, ctk.END)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al guardar: {err}")
        finally:
            conn.close()

def actualizar_db():
    global fila_seleccionada
    if fila_seleccionada is None:
        return

    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    telefono = entry_telefono.get()

    if nombre == "" or telefono == "" or apellido == "":
        label_estado.configure(text="Todos los campos son obligatorios")
        return

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE usuario SET nombre = %s, apellido = %s, telefono = %s WHERE id = %s",
                (nombre, apellido, telefono, fila_seleccionada)
            )
            conn.commit()
            label_estado.configure(text="✅ Registro actualizado")
            
            # Limpiar campos y resetear selección
            entry_nombre.delete(0, ctk.END)
            entry_apellido.delete(0, ctk.END)
            entry_telefono.delete(0, ctk.END)
            fila_seleccionada = None
            boton_guardar.configure(text="Guardar", command=guardar_db)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al actualizar: {err}")
        finally:
            conn.close()

def eliminar_registro():
    item = tree.focus()
    if not item:
        return
    
    confirmar = messagebox.askokcancel("Confirmar eliminación", "¿Estás seguro de eliminar este registro?")
    if not confirmar:
        return
    
    id_registro = tree.item(item)['values'][0]  # Asumimos que el ID es la primera columna
    
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuario WHERE id = %s", (id_registro,))
            conn.commit()
            mostrar_datos()
            messagebox.showinfo("Éxito", "Registro eliminado correctamente")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al eliminar: {err}")
        finally:
            conn.close()

def mostrar_datos():
    # Limpiar treeview
    for fila in tree.get_children():
        tree.delete(fila)
    
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, apellido, telefono FROM usuario")
            resultados = cursor.fetchall()
            
            for fila in resultados:
                tree.insert("", "end", values=fila)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al cargar datos: {err}")
        finally:
            conn.close()

def cambiar_tabla():
    frame_registro.pack_forget()
    frame_tabla.pack(fill="both", expand=True)
    mostrar_datos()

def cambiar_registro():
    frame_tabla.pack_forget()
    frame_registro.pack(fill="both", expand=True)
    boton_guardar.configure(text="Guardar", command=guardar_db)
    label_estado.configure(text="")
    entry_nombre.delete(0, ctk.END)
    entry_apellido.delete(0, ctk.END)
    entry_telefono.delete(0, ctk.END)
    global fila_seleccionada
    fila_seleccionada = None

def seleccionar_fila(event):
    global fila_seleccionada
    item = tree.focus()
    valores = tree.item(item, "values")
    if not valores:
        return
    
    id_registro, nombre, apellido, telefono = valores
    cambiar_registro()

    entry_nombre.delete(0, ctk.END)
    entry_nombre.insert(0, nombre)
    entry_apellido.delete(0, ctk.END)
    entry_apellido.insert(0, apellido)
    entry_telefono.delete(0, ctk.END)
    entry_telefono.insert(0, telefono)

    fila_seleccionada = id_registro
    boton_guardar.configure(text="Actualizar", command=actualizar_db)
    label_estado.configure(text="✏️ Editando registro...")

def editar_seleccionado():
    item = tree.focus()
    if not item:
        messagebox.showwarning("Aviso", "Selecciona un registro para editar.")
        return
    seleccionar_fila(None)


# Configuración de la interfaz gráfica
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Ayuntamiento - MariaDB")
app.geometry("800x600")

# Frame de registro
frame_registro = ctk.CTkFrame(app)
frame_registro.pack(fill="both", expand=True)

label = ctk.CTkLabel(frame_registro, text="Nombre")
label.pack(pady=5)
entry_nombre = ctk.CTkEntry(frame_registro, placeholder_text="Tu nombre")
entry_nombre.pack(pady=5)

label_apellido = ctk.CTkLabel(frame_registro, text="Apellido")
label_apellido.pack(pady=5)
entry_apellido = ctk.CTkEntry(frame_registro, placeholder_text="Ejemplo: Martinez")
entry_apellido.pack(pady=5)

label_tel = ctk.CTkLabel(frame_registro, text="Teléfono")
label_tel.pack(pady=5)
entry_telefono = ctk.CTkEntry(frame_registro, placeholder_text="Ejemplo: 734218361623")
entry_telefono.pack(pady=5)

label_estado = ctk.CTkLabel(frame_registro, text="")
label_estado.pack(pady=5)

boton_guardar = ctk.CTkButton(frame_registro, text="Guardar", command=guardar_db)
boton_guardar.pack(pady=10)

boton_mostrar = ctk.CTkButton(frame_registro, text="Mostrar datos", command=cambiar_tabla)
boton_mostrar.pack(pady=10)

# Frame de tabla
frame_tabla = ctk.CTkFrame(app)

tree = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Apellido", "Teléfono"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nombre", text="Nombre")
tree.heading("Apellido", text="Apellido")
tree.heading("Teléfono", text="Teléfono")
tree.column("ID", width=50)  
tree.pack(fill="both", expand=True)

button_volver = ctk.CTkButton(frame_tabla, text="Volver a registro", command=cambiar_registro)
button_volver.pack(pady=10)

boton_eliminar = ctk.CTkButton(frame_tabla, text="Eliminar seleccionado", command=eliminar_registro)
boton_eliminar.pack(pady=10)

boton_editar = ctk.CTkButton(frame_tabla, text="Editar seleccionado", command=editar_seleccionado)
boton_editar.pack(pady=10)


app.mainloop()