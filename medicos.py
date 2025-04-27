#medicos.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import psycopg2
from datetime import date

# Configuracion de conexion a la base de datos
conexion = psycopg2.connect(
    host="localhost",
    database="clinica_db",
    user="postgres",
    password="334003562Mn#"
)
cursor = conexion.cursor()

def mostrar_ventana():
    ventana = tk.Tk()
    ventana.title("Gestión de Médicos")
    ventana.geometry("1100x550")
    ventana.configure(bg="#e6f2ff")

    # Titulo
    titulo = tk.Label(ventana, text="GESTIÓN DE MÉDICOS", font=("Helvetica", 18, "bold"), bg="#e6f2ff", fg="#004080")
    titulo.pack(pady=10)

    marco_contenido = tk.Frame(ventana, bg="#e6f2ff")
    marco_contenido.pack(fill="both", expand=True, padx=10, pady=10)

    #FORMULARIO 
    frame_form = tk.LabelFrame(marco_contenido, text="Formulario de Médico", bg="#f0f8ff",
                               font=("Arial", 12, "bold"), bd=2, relief="groove")
    frame_form.pack(side="left", fill="both", expand=True, padx=10)

    labels = ["Nombre Completo:", "Especialidad:", "Número Licencia:", "Fecha Ingreso:", "Departamento ID:", "Email Contacto:"]
    entradas = []

    for i, texto in enumerate(labels):
        tk.Label(frame_form, text=texto, bg="#f0f8ff").grid(row=i, column=0, sticky="w", padx=10, pady=5)

        if texto == "Fecha Ingreso:":
            entry = DateEntry(frame_form, width=27, background='darkgreen', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        elif texto == "Departamento ID:":
            entry = ttk.Combobox(frame_form, width=27, state="readonly")
            cursor.execute("SELECT departamento_id, nombre_departamento FROM departamentos ORDER BY departamento_id")
            departamentos = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
            entry["values"] = departamentos
        else:
            entry = tk.Entry(frame_form, width=30)

        entry.grid(row=i, column=1, padx=10, pady=5)
        entradas.append(entry)

    entry_nombre, entry_especialidad, entry_licencia, entry_fecha, entry_departamento, entry_email = entradas

    # botones
    frame_botones = tk.Frame(frame_form, bg="#f0f8ff")
    frame_botones.grid(row=6, columnspan=2, pady=15)

    tk.Button(frame_botones, text="Guardar", width=10, bg="#4CAF50", fg="white",
              command=lambda: guardar_medico()).grid(row=0, column=0, padx=5)
    tk.Button(frame_botones, text="Actualizar", width=10, bg="#2196F3", fg="white",
              command=lambda: actualizar_medico()).grid(row=0, column=1, padx=5)
    tk.Button(frame_botones, text="Eliminar", width=10, bg="#f44336", fg="white",
              command=lambda: eliminar_medico()).grid(row=0, column=2, padx=5)
    tk.Button(frame_botones, text="Limpiar", width=10, bg="#9E9E9E", fg="white",
              command=lambda: limpiar_campos()).grid(row=0, column=3, padx=5)

    # TABLA
    frame_tabla = tk.LabelFrame(marco_contenido, text="Lista de Médicos Registrados", bg="#f0f8ff",
                                font=("Arial", 12, "bold"), bd=2, relief="groove")
    frame_tabla.pack(side="right", fill="both", expand=True, padx=10)

    scroll_y = tk.Scrollbar(frame_tabla, orient="vertical")
    scroll_y.pack(side="right", fill="y")

    scroll_x = tk.Scrollbar(frame_tabla, orient="horizontal")
    scroll_x.pack(side="bottom", fill="x")

    columnas = ("ID", "Nombre", "Especialidad", "Licencia", "Ingreso", "Depto ID", "Email")
    tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings",
                        yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    scroll_y.config(command=tree.yview)
    scroll_x.config(command=tree.xview)

    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    tree.bind("<<TreeviewSelect>>", lambda event: seleccionar_medico())

    #funciones
    def guardar_medico():
        try:
            datos = (
                entry_nombre.get(),
                entry_especialidad.get(),
                entry_licencia.get(),
                entry_fecha.get(),
                int(entry_departamento.get().split(" - ")[0]),
                entry_email.get()
            )
            cursor.execute("""
                INSERT INTO medicos (nombre_completo, especialidad, numero_licencia, fecha_ingreso, departamento_id, email_contacto)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, datos)
            conexion.commit()
            messagebox.showinfo("Éxito", "Médico registrado correctamente")
            limpiar_campos()
            mostrar_medicos()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            conexion.rollback()

    def actualizar_medico():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un médico para actualizar")
            return
        medico_id = tree.item(selected)["values"][0]
        try:
            datos = (
                entry_nombre.get(),
                entry_especialidad.get(),
                entry_licencia.get(),
                entry_fecha.get(),
                int(entry_departamento.get().split(" - ")[0]),
                entry_email.get(),
                medico_id
            )
            cursor.execute("""
                UPDATE medicos
                SET nombre_completo=%s, especialidad=%s, numero_licencia=%s, fecha_ingreso=%s,
                    departamento_id=%s, email_contacto=%s
                WHERE medico_id=%s
            """, datos)
            conexion.commit()
            messagebox.showinfo("Éxito", "Datos actualizados correctamente")
            limpiar_campos()
            mostrar_medicos()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            conexion.rollback()

    def eliminar_medico():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un médico para eliminar")
            return
        medico_id = tree.item(selected)["values"][0]
        try:
            cursor.execute("DELETE FROM medicos WHERE medico_id = %s", (medico_id,))
            conexion.commit()
            messagebox.showinfo("Éxito", "Médico eliminado correctamente")
            mostrar_medicos()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            conexion.rollback()

    def limpiar_campos():
        for entry in entradas:
            if isinstance(entry, DateEntry):
                entry.set_date(date.today())
            else:
                entry.delete(0, tk.END)

    def mostrar_medicos():
        for row in tree.get_children():
            tree.delete(row)
        cursor.execute("SELECT * FROM medicos ORDER BY medico_id")
        for medico in cursor.fetchall():
            tree.insert("", tk.END, values=medico)

    def seleccionar_medico():
        selected = tree.focus()
        if not selected:
            return
        valores = tree.item(selected)["values"]
        if not valores or len(valores) < 7:
            return  # Protección contra valores incompletos
        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, valores[1])
        entry_especialidad.delete(0, tk.END)
        entry_especialidad.insert(0, valores[2])
        entry_licencia.delete(0, tk.END)
        entry_licencia.insert(0, valores[3])
        entry_fecha.set_date(valores[4])
        # Asignar el valor exacto del combo
        for val in entry_departamento["values"]:
            if val.startswith(str(valores[5])):
                entry_departamento.set(val)
                break
        entry_email.delete(0, tk.END)
        entry_email.insert(0, valores[6])

    mostrar_medicos()
    ventana.mainloop()

if __name__ == "__main__":
    mostrar_ventana()