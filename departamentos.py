#departamentos.py
import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

#conexion a la base de datos
conexion = psycopg2.connect(
    host="localhost",
    database="clinica_db",
    user="postgres",
    password="334003562Mn#"
)
cursor = conexion.cursor()

def mostrar_ventana():
    ventana = tk.Tk()
    ventana.title("Gestión de Departamentos")
    ventana.geometry("950x500")
    ventana.configure(bg="#e6f2ff")

    titulo = tk.Label(ventana, text="GESTIÓN DE DEPARTAMENTOS", font=("Helvetica", 18, "bold"),
                      bg="#e6f2ff", fg="#004080")
    titulo.pack(pady=10)

    marco_contenido = tk.Frame(ventana, bg="#e6f2ff")
    marco_contenido.pack(fill="both", expand=True, padx=10, pady=10)

    frame_form = tk.LabelFrame(marco_contenido, text="Formulario de Departamento", bg="#f0f8ff",
                               font=("Arial", 12, "bold"), bd=2, relief="groove")
    frame_form.pack(side="left", fill="both", expand=True, padx=10)

    labels = ["Nombre del Departamento:", "Ubicación:", "Jefe de Departamento:"]
    entradas = []

    for i, texto in enumerate(labels):
        tk.Label(frame_form, text=texto, bg="#f0f8ff").grid(row=i, column=0, sticky="w", padx=10, pady=5)
        entry = tk.Entry(frame_form, width=30)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entradas.append(entry)

    entry_nombre, entry_ubicacion, entry_jefe = entradas

    #botones
    frame_botones = tk.Frame(frame_form, bg="#f0f8ff")
    frame_botones.grid(row=3, columnspan=2, pady=15)

    tk.Button(frame_botones, text="Guardar", width=10, bg="#4CAF50", fg="white",
              command=lambda: guardar_departamento()).grid(row=0, column=0, padx=5)
    tk.Button(frame_botones, text="Actualizar", width=10, bg="#2196F3", fg="white",
              command=lambda: actualizar_departamento()).grid(row=0, column=1, padx=5)
    tk.Button(frame_botones, text="Eliminar", width=10, bg="#f44336", fg="white",
              command=lambda: eliminar_departamento()).grid(row=0, column=2, padx=5)
    tk.Button(frame_botones, text="Limpiar", width=10, bg="#9E9E9E", fg="white",
              command=lambda: limpiar_campos()).grid(row=0, column=3, padx=5)

    #tabladp
    frame_tabla = tk.LabelFrame(marco_contenido, text="Lista de Departamentos", bg="#f0f8ff",
                                font=("Arial", 12, "bold"), bd=2, relief="groove")
    frame_tabla.pack(side="right", fill="both", expand=True, padx=10)

    scroll_y = tk.Scrollbar(frame_tabla, orient="vertical")
    scroll_y.pack(side="right", fill="y")

    scroll_x = tk.Scrollbar(frame_tabla, orient="horizontal")
    scroll_x.pack(side="bottom", fill="x")

    columnas = ("ID", "Nombre", "Ubicación", "Jefe")
    tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings",
                        yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    scroll_y.config(command=tree.yview)
    scroll_x.config(command=tree.xview)

    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    tree.bind("<<TreeviewSelect>>", lambda event: seleccionar_departamento())

    def guardar_departamento():
        try:
            datos = (
                entry_nombre.get(),
                entry_ubicacion.get(),
                entry_jefe.get()
            )
            cursor.execute("""
                INSERT INTO departamentos (nombre_departamento, ubicacion, jefe_departamento)
                VALUES (%s, %s, %s)
            """, datos)
            conexion.commit()
            messagebox.showinfo("Éxito", "Departamento registrado correctamente")
            limpiar_campos()
            mostrar_departamentos()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            conexion.rollback()

    def actualizar_departamento():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un departamento para actualizar")
            return
        departamento_id = tree.item(selected)["values"][0]
        try:
            datos = (
                entry_nombre.get(),
                entry_ubicacion.get(),
                entry_jefe.get(),
                departamento_id
            )
            cursor.execute("""
                UPDATE departamentos
                SET nombre_departamento=%s, ubicacion=%s, jefe_departamento=%s
                WHERE departamento_id=%s
            """, datos)
            conexion.commit()
            messagebox.showinfo("Éxito", "Datos actualizados")
            limpiar_campos()
            mostrar_departamentos()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            conexion.rollback()

    def eliminar_departamento():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un departamento para eliminar")
            return
        departamento_id = tree.item(selected)["values"][0]
        try:
            cursor.execute("DELETE FROM departamentos WHERE departamento_id = %s", (departamento_id,))
            conexion.commit()
            messagebox.showinfo("Éxito", "Departamento eliminado")
            mostrar_departamentos()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            conexion.rollback()

    def limpiar_campos():
        for entry in entradas:
            entry.delete(0, tk.END)

    def mostrar_departamentos():
        for row in tree.get_children():
            tree.delete(row)
        cursor.execute("SELECT * FROM departamentos ORDER BY departamento_id ")
        for departamento in cursor.fetchall():
            tree.insert("", tk.END, values=departamento)

    def seleccionar_departamento():
        selected = tree.focus()
        if not selected:
            return
        valores = tree.item(selected)["values"]
        if valores:
            (entry_nombre.delete(0, tk.END), entry_nombre.insert(0, valores[1]))
            (entry_ubicacion.delete(0, tk.END), entry_ubicacion.insert(0, valores[2]))
            (entry_jefe.delete(0, tk.END), entry_jefe.insert(0, valores[3]))

    mostrar_departamentos()
    ventana.mainloop()

if __name__ == "__main__":
    mostrar_ventana()