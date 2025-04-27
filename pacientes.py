#pacientes.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import psycopg2
from datetime import date
from auditoriapac import mostrar_auditoria

# Conexion a la base de datos
conexion = psycopg2.connect(
    host="localhost",
    database="clinica_db",
    user="postgres",
    password="334003562Mn#"
)
cursor = conexion.cursor()

def mostrar_ventana():
    ventana = tk.Tk()
    ventana.title("Gestión de Pacientes")
    ventana.geometry("1100x550")
    ventana.configure(bg="#e6f2ff")

    titulo = tk.Label(ventana, text="GESTIÓN DE PACIENTES", font=("Helvetica", 18, "bold"),
                      bg="#e6f2ff", fg="#004080")
    titulo.pack(pady=10)

    marco_contenido = tk.Frame(ventana, bg="#e6f2ff")
    marco_contenido.pack(fill="both", expand=True, padx=10, pady=10)

    #formulario
    frame_form = tk.LabelFrame(marco_contenido, text="Formulario de Paciente", bg="#f0f8ff",
                               font=("Arial", 12, "bold"), bd=2, relief="groove")
    frame_form.pack(side="left", fill="both", expand=True, padx=10)

    labels = ["Nombre Completo:", "Fecha de Nacimiento:", "Género:", "Dirección:",
              "Teléfono:", "Email:", "Tipo de Sangre:", "Seguro Médico:"]
    entradas = []

    for i, texto in enumerate(labels):
        tk.Label(frame_form, text=texto, bg="#f0f8ff").grid(row=i, column=0, sticky="w", padx=10, pady=5)
        if texto == "Fecha de Nacimiento:":
            entry = DateEntry(frame_form, width=27, background='darkgreen',
                              foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        elif texto in ["Género:", "Tipo de Sangre:"]:
            valores = []
            if texto == "Género:":
                valores = ["Masculino", "Femenino"]
            elif texto == "Tipo de Sangre:":
                valores = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
            entry = ttk.Combobox(frame_form, values=valores, width=27)
        else:
            entry = tk.Entry(frame_form, width=30)

        entry.grid(row=i, column=1, padx=10, pady=5)
        entradas.append(entry)

    (entry_nombre, entry_fecha, entry_genero, entry_direccion, entry_telefono,
     entry_email, entry_sangre, entry_seguro) = entradas

    #botones
    frame_botones = tk.Frame(frame_form, bg="#f0f8ff")
    frame_botones.grid(row=8, columnspan=2, pady=15)

    tk.Button(frame_botones, text="Guardar", width=10, bg="#4CAF50", fg="white",
              command=lambda: guardar_paciente()).grid(row=0, column=0, padx=5)
    tk.Button(frame_botones, text="Actualizar", width=10, bg="#2196F3", fg="white",
              command=lambda: actualizar_paciente()).grid(row=0, column=1, padx=5)
    tk.Button(frame_botones, text="Eliminar", width=10, bg="#f44336", fg="white",
              command=lambda: eliminar_paciente()).grid(row=0, column=2, padx=5)
    tk.Button(frame_botones, text="Limpiar", width=10, bg="#9E9E9E", fg="white",
              command=lambda: limpiar_campos()).grid(row=0, column=3, padx=5)
    tk.Button(frame_botones, text="Cambios", width=10, bg="#FF9800", fg="white",
          command=mostrar_auditoria).grid(row=0, column=4, padx=5)

    #tabla pacientes
    frame_tabla = tk.LabelFrame(marco_contenido, text="Lista de Pacientes Registrados", bg="#f0f8ff",
                                font=("Arial", 12, "bold"), bd=2, relief="groove")
    frame_tabla.pack(side="right", fill="both", expand=True, padx=10)

    scroll_y = tk.Scrollbar(frame_tabla, orient="vertical")
    scroll_y.pack(side="right", fill="y")

    scroll_x = tk.Scrollbar(frame_tabla, orient="horizontal")
    scroll_x.pack(side="bottom", fill="x")

    columnas = ("ID", "Nombre", "Fecha Nac.", "Género", "Dirección", "Teléfono",
                "Email", "Tipo de Sangre", "Seguro Médico")
    tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings",
                        yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    scroll_y.config(command=tree.yview)
    scroll_x.config(command=tree.xview)

    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    tree.bind("<<TreeviewSelect>>", lambda event: seleccionar_paciente())

    def guardar_paciente():
        try:
            datos = (
                entry_nombre.get(),
                entry_fecha.get(),
                entry_genero.get(),
                entry_direccion.get(),
                entry_telefono.get(),
                entry_email.get(),
                entry_sangre.get(),
                entry_seguro.get()
            )
            cursor.execute("""
                INSERT INTO pacientes (nombre_completo, fecha_nacimiento, genero, direccion, telefono, email, tipo_sangre, seguro_medico)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, datos)
            conexion.commit()
            messagebox.showinfo("Éxito", "Paciente registrado correctamente")
            limpiar_campos()
            mostrar_pacientes()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            conexion.rollback()

    def actualizar_paciente():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un paciente para actualizar")
            return
        paciente_id = tree.item(selected)["values"][0]
        try:
            datos = (
                entry_nombre.get(),
                entry_fecha.get(),
                entry_genero.get(),
                entry_direccion.get(),
                entry_telefono.get(),
                entry_email.get(),
                entry_sangre.get(),
                entry_seguro.get(),
                paciente_id
            )
            cursor.execute("""
                UPDATE pacientes
                SET nombre_completo=%s, fecha_nacimiento=%s, genero=%s, direccion=%s,
                    telefono=%s, email=%s, tipo_sangre=%s, seguro_medico=%s
                WHERE paciente_id=%s
            """, datos)
            conexion.commit()
            messagebox.showinfo("Éxito", "Datos actualizados")
            limpiar_campos()
            mostrar_pacientes()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            conexion.rollback()

    def eliminar_paciente():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un paciente para eliminar")
            return
        paciente_id = tree.item(selected)["values"][0]
        try:
            cursor.execute("DELETE FROM pacientes WHERE paciente_id = %s", (paciente_id,))
            conexion.commit()
            messagebox.showinfo("Éxito", "Paciente eliminado")
            mostrar_pacientes()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            conexion.rollback()

    def limpiar_campos():
        for entry in entradas:
            if isinstance(entry, DateEntry):
                entry.set_date(date.today())
            else:
                entry.delete(0, tk.END)

    def mostrar_pacientes():
        for row in tree.get_children():
            tree.delete(row)
        cursor.execute("SELECT * FROM pacientes  ORDER BY paciente_id")
        for paciente in cursor.fetchall():
            tree.insert("", tk.END, values=paciente)

    def seleccionar_paciente():
        selected = tree.focus()
        if not selected:
            return
        valores = tree.item(selected)["values"]
        if valores:
            (entry_nombre.delete(0, tk.END), entry_nombre.insert(0, valores[1]))
            entry_fecha.set_date(valores[2])
            entry_genero.set(valores[3])
            (entry_direccion.delete(0, tk.END), entry_direccion.insert(0, valores[4]))
            (entry_telefono.delete(0, tk.END), entry_telefono.insert(0, valores[5]))
            (entry_email.delete(0, tk.END), entry_email.insert(0, valores[6]))
            entry_sangre.set(valores[7])
            (entry_seguro.delete(0, tk.END), entry_seguro.insert(0, valores[8]))

    mostrar_pacientes()
    ventana.mainloop()

if __name__ == "__main__":
    mostrar_ventana()