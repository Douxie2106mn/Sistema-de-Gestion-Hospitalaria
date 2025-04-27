#historialmedico.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import psycopg2
from datetime import date

conexion = psycopg2.connect(
    host="localhost",
    database="clinica_db",
    user="postgres",
    password="334003562Mn#"
)
cursor = conexion.cursor()

def cargar_pacientes():
    cursor.execute("SELECT paciente_id, nombre_completo FROM pacientes")
    return cursor.fetchall()

def mostrar_ventana():
    ventana = tk.Tk()
    ventana.title("Gestión de Historial Médico")
    ventana.geometry("1100x550")
    ventana.configure(bg="#e6f2ff")

    titulo = tk.Label(ventana, text="GESTIÓN DE HISTORIAL MÉDICO", font=("Helvetica", 18, "bold"), bg="#e6f2ff", fg="#004080")
    titulo.pack(pady=10)

    marco_contenido = tk.Frame(ventana, bg="#e6f2ff")
    marco_contenido.pack(fill="both", expand=True, padx=10, pady=10)

    frame_form = tk.LabelFrame(marco_contenido, text="Formulario de Historial Médico", bg="#f0f8ff",
                               font=("Arial", 12, "bold"), bd=2, relief="groove")
    frame_form.pack(side="left", fill="both", expand=True, padx=10)

    entradas = {}

    tk.Label(frame_form, text="Paciente:", bg="#f0f8ff").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    pacientes = cargar_pacientes()
    paciente_combobox = ttk.Combobox(frame_form, values=[f"{p[1]} (ID: {p[0]})" for p in pacientes], width=27)
    paciente_combobox.grid(row=0, column=1, padx=10, pady=5)
    entradas["Paciente"] = paciente_combobox
    entradas["Pacientes Lista"] = pacientes

    tk.Label(frame_form, text="Fecha de Registro:", bg="#f0f8ff").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    fecha_registro = DateEntry(frame_form, width=27, background='darkgreen', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    fecha_registro.grid(row=1, column=1, padx=10, pady=5)
    entradas["Fecha de Registro"] = fecha_registro

    tk.Label(frame_form, text="Condición:", bg="#f0f8ff").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    entradas["Condicion"] = tk.Entry(frame_form, width=30)
    entradas["Condicion"].grid(row=2, column=1, padx=10, pady=5)

    tk.Label(frame_form, text="Medicamentos:", bg="#f0f8ff").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    entradas["Medicamentos"] = tk.Entry(frame_form, width=30)
    entradas["Medicamentos"].grid(row=3, column=1, padx=10, pady=5)

    tk.Label(frame_form, text="Alergias:", bg="#f0f8ff").grid(row=4, column=0, sticky="w", padx=10, pady=5)
    entradas["Alergias"] = tk.Entry(frame_form, width=30)
    entradas["Alergias"].grid(row=4, column=1, padx=10, pady=5)

    frame_botones = tk.Frame(frame_form, bg="#f0f8ff")
    frame_botones.grid(row=5, columnspan=2, pady=15)

    tk.Button(frame_botones, text="Guardar", width=10, bg="#4CAF50", fg="white",
              command=lambda: guardar_historial(entradas, tabla)).grid(row=0, column=0, padx=5)
    tk.Button(frame_botones, text="Actualizar", width=10, bg="#2196F3", fg="white",
              command=lambda: actualizar_registro(entradas, tabla)).grid(row=0, column=1, padx=5)
    tk.Button(frame_botones, text="Eliminar", width=10, bg="#f44336", fg="white",
              command=lambda: eliminar_registro(tabla)).grid(row=0, column=2, padx=5)
    tk.Button(frame_botones, text="Limpiar", width=10, bg="#9E9E9E", fg="white",
              command=lambda: limpiar_campos(entradas)).grid(row=0, column=3, padx=5)

    frame_tabla = tk.LabelFrame(marco_contenido, text="Historial Médico Registrado", bg="#f0f8ff",
                                font=("Arial", 12, "bold"), bd=2, relief="groove")
    frame_tabla.pack(side="right", fill="both", expand=True, padx=10)

    scroll_y = tk.Scrollbar(frame_tabla, orient="vertical")
    scroll_y.pack(side="right", fill="y")

    scroll_x = tk.Scrollbar(frame_tabla, orient="horizontal")
    scroll_x.pack(side="bottom", fill="x")

    columnas = ("ID", "Paciente ID", "Fecha", "Condición", "Medicamentos", "Alergias")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings",
                         yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    scroll_y.config(command=tabla.yview)
    scroll_x.config(command=tabla.xview)

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=120, anchor="center")

    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    mostrar_historial(tabla)

    tabla.bind("<<TreeviewSelect>>", lambda event: cargar_datos_seleccionados(entradas, tabla))

    ventana.mainloop()

def guardar_historial(entradas, tabla):
    paciente_seleccionado = entradas["Paciente"].get()
    if not paciente_seleccionado:
        messagebox.showwarning("Advertencia", "Selecciona un paciente")
        return

    paciente_id = None
    for p in entradas["Pacientes Lista"]:
        if f"{p[1]} (ID: {p[0]})" == paciente_seleccionado:
            paciente_id = p[0]
            break

    datos = (
        paciente_id,
        entradas["Fecha de Registro"].get(),
        entradas["Condicion"].get(),
        entradas["Medicamentos"].get(),
        entradas["Alergias"].get()
    )

    try:
        cursor.execute("""
            INSERT INTO historial_medico (paciente_id, fecha_registro, descripcion_condicion, medicamentos, alergias)
            VALUES (%s, %s, %s, %s, %s)
        """, datos)
        conexion.commit()
        messagebox.showinfo("Éxito", "Historial médico guardado correctamente")
        mostrar_historial(tabla)
        limpiar_campos(entradas)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        conexion.rollback()

def mostrar_historial(tabla):
    for row in tabla.get_children():
        tabla.delete(row)
    cursor.execute("SELECT * FROM historial_medico ORDER BY registro_id")
    for registro in cursor.fetchall():
        tabla.insert("", tk.END, values=registro)

def eliminar_registro(tabla):
    selected = tabla.focus()
    if not selected:
        messagebox.showwarning("Advertencia", "Selecciona un registro para eliminar")
        return
    registro_id = tabla.item(selected)["values"][0]
    try:
        cursor.execute("DELETE FROM historial_medico WHERE registro_id = %s", (registro_id,))
        conexion.commit()
        messagebox.showinfo("Éxito", "Registro eliminado")
        mostrar_historial(tabla)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        conexion.rollback()

def limpiar_campos(entradas):
    entradas["Paciente"].set('')
    entradas["Fecha de Registro"].set_date(date.today())
    entradas["Condicion"].delete(0, tk.END)
    entradas["Medicamentos"].delete(0, tk.END)
    entradas["Alergias"].delete(0, tk.END)

def cargar_datos_seleccionados(entradas, tabla):
    selected = tabla.focus()
    if not selected:
        return
    valores = tabla.item(selected, "values")
    paciente_id = valores[1]
    for p in entradas["Pacientes Lista"]:
        if str(p[0]) == str(paciente_id):
            entradas["Paciente"].set(f"{p[1]} (ID: {p[0]})")
            break
    entradas["Fecha de Registro"].set_date(valores[2])
    entradas["Condicion"].delete(0, tk.END)
    entradas["Condicion"].insert(0, valores[3])
    entradas["Medicamentos"].delete(0, tk.END)
    entradas["Medicamentos"].insert(0, valores[4])
    entradas["Alergias"].delete(0, tk.END)
    entradas["Alergias"].insert(0, valores[5])

def actualizar_registro(entradas, tabla):
    selected = tabla.focus()
    if not selected:
        messagebox.showwarning("Advertencia", "Selecciona un registro para actualizar")
        return
    registro_id = tabla.item(selected)["values"][0]
    paciente_id = None
    paciente_seleccionado = entradas["Paciente"].get()
    for p in entradas["Pacientes Lista"]:
        if f"{p[1]} (ID: {p[0]})" == paciente_seleccionado:
            paciente_id = p[0]
            break
    datos = (
        paciente_id,
        entradas["Fecha de Registro"].get(),
        entradas["Condicion"].get(),
        entradas["Medicamentos"].get(),
        entradas["Alergias"].get(),
        registro_id
    )
    try:
        cursor.execute("""
            UPDATE historial_medico
            SET paciente_id = %s, fecha_registro = %s, descripcion_condicion = %s,
                medicamentos = %s, alergias = %s
            WHERE registro_id = %s
        """, datos)
        conexion.commit()
        messagebox.showinfo("Éxito", "Registro actualizado")
        mostrar_historial(tabla)
        limpiar_campos(entradas)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        conexion.rollback()

if __name__ == "__main__":
    mostrar_ventana()