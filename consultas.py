#consultas.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import psycopg2
from datetime import date
from auditoriaconsul import mostrar_auditoria_consultas

# Conexión a la base de datos
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

def cargar_medicos():
    cursor.execute("SELECT medico_id, nombre_completo FROM medicos")
    return cursor.fetchall()

def mostrar_ventana():
    ventana = tk.Tk()
    ventana.title("Gestión de Consultas")
    ventana.geometry("1200x580")
    ventana.configure(bg="#e6f2ff")

    titulo = tk.Label(ventana, text="GESTIÓN DE CONSULTAS", font=("Helvetica", 18, "bold"), bg="#e6f2ff", fg="#004080")
    titulo.pack(pady=10)

    marco_contenido = tk.Frame(ventana, bg="#e6f2ff")
    marco_contenido.pack(fill="both", expand=True, padx=10, pady=10)

    frame_form = tk.LabelFrame(marco_contenido, text="Formulario de Consulta", bg="#f0f8ff",
                               font=("Arial", 12, "bold"), bd=2, relief="groove")
    frame_form.pack(side="left", fill="both", expand=True, padx=10)

    entradas = {}

    tk.Label(frame_form, text="Paciente:", bg="#f0f8ff").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    pacientes = cargar_pacientes()
    paciente_combobox = ttk.Combobox(frame_form, values=[f"{p[1]} (ID: {p[0]})" for p in pacientes], width=27)
    paciente_combobox.grid(row=0, column=1, padx=10, pady=5)
    entradas["Paciente"] = paciente_combobox
    entradas["Pacientes Lista"] = pacientes

    tk.Label(frame_form, text="Médico:", bg="#f0f8ff").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    medicos = cargar_medicos()
    medico_combobox = ttk.Combobox(frame_form, values=[f"{m[1]} (ID: {m[0]})" for m in medicos], width=27)
    medico_combobox.grid(row=1, column=1, padx=10, pady=5)
    entradas["Medico"] = medico_combobox
    entradas["Medicos Lista"] = medicos

    tk.Label(frame_form, text="Fecha de Consulta:", bg="#f0f8ff").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    fecha_consulta = DateEntry(frame_form, width=27, background='darkgreen', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    fecha_consulta.grid(row=2, column=1, padx=10, pady=5)
    entradas["Fecha de Consulta"] = fecha_consulta

    tk.Label(frame_form, text="Diagnóstico:", bg="#f0f8ff").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    entradas["Diagnostico"] = tk.Entry(frame_form, width=30)
    entradas["Diagnostico"].grid(row=3, column=1, padx=10, pady=5)

    tk.Label(frame_form, text="Tratamiento:", bg="#f0f8ff").grid(row=4, column=0, sticky="w", padx=10, pady=5)
    entradas["Tratamiento"] = tk.Entry(frame_form, width=30)
    entradas["Tratamiento"].grid(row=4, column=1, padx=10, pady=5)

    tk.Label(frame_form, text="Estado:", bg="#f0f8ff").grid(row=5, column=0, sticky="w", padx=10, pady=5)
    estado_combobox = ttk.Combobox(frame_form, values=["Pendiente", "Finalizada"], width=27, state="readonly")
    estado_combobox.grid(row=5, column=1, padx=10, pady=5)
    entradas["Estado"] = estado_combobox

    frame_botones = tk.Frame(frame_form, bg="#f0f8ff")
    frame_botones.grid(row=6, columnspan=2, pady=15)

    tk.Button(frame_botones, text="Guardar", width=10, bg="#4CAF50", fg="white",
              command=lambda: guardar_consulta(entradas, tabla)).grid(row=0, column=0, padx=5)
    tk.Button(frame_botones, text="Actualizar", width=10, bg="#2196F3", fg="white",
              command=lambda: actualizar_registro(entradas, tabla)).grid(row=0, column=1, padx=5)
    tk.Button(frame_botones, text="Eliminar", width=10, bg="#f44336", fg="white",
              command=lambda: eliminar_registro(tabla)).grid(row=0, column=2, padx=5)
    tk.Button(frame_botones, text="Limpiar", width=10, bg="#9E9E9E", fg="white",
              command=lambda: limpiar_campos(entradas)).grid(row=0, column=3, padx=5)
    tk.Button(frame_botones, text="Cambios", width=10, bg="#FF9800", fg="white",
              command=mostrar_auditoria_consultas).grid(row=0, column=4, padx=5)


    frame_tabla = tk.LabelFrame(marco_contenido, text="Consultas Registradas", bg="#f0f8ff",
                                font=("Arial", 12, "bold"), bd=2, relief="groove")
    frame_tabla.pack(side="right", fill="both", expand=True, padx=10)

    scroll_y = tk.Scrollbar(frame_tabla, orient="vertical")
    scroll_y.pack(side="right", fill="y")

    scroll_x = tk.Scrollbar(frame_tabla, orient="horizontal")
    scroll_x.pack(side="bottom", fill="x")

    columnas = ("ID", "Paciente ID", "Medico ID", "Fecha", "Diagnóstico", "Tratamiento", "Estado")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings",
                         yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    scroll_y.config(command=tabla.yview)
    scroll_x.config(command=tabla.xview)

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=120, anchor="center")

    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    mostrar_consultas(tabla)

    tabla.bind("<<TreeviewSelect>>", lambda event: cargar_datos_seleccionados(entradas, tabla))

    ventana.mainloop()

def mostrar_consultas(tabla):
    for row in tabla.get_children():
        tabla.delete(row)
    cursor.execute("SELECT consulta_id, paciente_id, medico_id, fecha_consulta, diagnostico, tratamiento, estado_consulta FROM consultas ORDER BY consulta_id")
    for registro in cursor.fetchall():
        tabla.insert("", tk.END, values=registro)

def eliminar_registro(tabla):
    selected = tabla.focus()
    if not selected:
        messagebox.showwarning("Advertencia", "Selecciona una consulta para eliminar")
        return
    consulta_id = tabla.item(selected)["values"][0]
    try:
        cursor.execute("DELETE FROM consultas WHERE consulta_id = %s", (consulta_id,))
        conexion.commit()
        messagebox.showinfo("Éxito", "Consulta eliminada")
        mostrar_consultas(tabla)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        conexion.rollback()

def limpiar_campos(entradas):
    entradas["Paciente"].set('')
    entradas["Medico"].set('')
    entradas["Fecha de Consulta"].set_date(date.today())
    entradas["Diagnostico"].delete(0, tk.END)
    entradas["Tratamiento"].delete(0, tk.END)
    entradas["Estado"].set('')

def cargar_datos_seleccionados(entradas, tabla):
    selected = tabla.focus()
    if not selected:
        return
    valores = tabla.item(selected, "values")
    paciente_id = valores[1]
    medico_id = valores[2]

    for p in entradas["Pacientes Lista"]:
        if str(p[0]) == str(paciente_id):
            entradas["Paciente"].set(f"{p[1]} (ID: {p[0]})")
            break
    for m in entradas["Medicos Lista"]:
        if str(m[0]) == str(medico_id):
            entradas["Medico"].set(f"{m[1]} (ID: {m[0]})")
            break

    entradas["Fecha de Consulta"].set_date(valores[3])
    entradas["Diagnostico"].delete(0, tk.END)
    entradas["Diagnostico"].insert(0, valores[4])
    entradas["Tratamiento"].delete(0, tk.END)
    entradas["Tratamiento"].insert(0, valores[5])
    entradas["Estado"].set(valores[6])

def actualizar_registro(entradas, tabla):
    selected = tabla.focus()
    if not selected:
        messagebox.showwarning("Advertencia", "Selecciona una consulta para actualizar")
        return
    consulta_id = tabla.item(selected)["values"][0]

    paciente_id = next((p[0] for p in entradas["Pacientes Lista"] if f"{p[1]} (ID: {p[0]})" == entradas["Paciente"].get()), None)
    medico_id = next((m[0] for m in entradas["Medicos Lista"] if f"{m[1]} (ID: {m[0]})" == entradas["Medico"].get()), None)

    if not paciente_id or not medico_id:
        messagebox.showwarning("Advertencia", "Selecciona paciente y médico válidos")
        return

    datos = (
        paciente_id,
        medico_id,
        entradas["Fecha de Consulta"].get(),
        entradas["Diagnostico"].get(),
        entradas["Tratamiento"].get(),
        entradas["Estado"].get(),
        consulta_id
    )

    try:
        cursor.execute("""
            UPDATE consultas
            SET paciente_id=%s, medico_id=%s, fecha_consulta=%s, diagnostico=%s,
                tratamiento=%s, estado_consulta=%s
            WHERE consulta_id=%s
        """, datos)
        conexion.commit()
        messagebox.showinfo("Éxito", "Consulta actualizada")
        mostrar_consultas(tabla)
        limpiar_campos(entradas)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        conexion.rollback()

def guardar_consulta(entradas, tabla):
    paciente_id = next((p[0] for p in entradas["Pacientes Lista"] if f"{p[1]} (ID: {p[0]})" == entradas["Paciente"].get()), None)
    medico_id = next((m[0] for m in entradas["Medicos Lista"] if f"{m[1]} (ID: {m[0]})" == entradas["Medico"].get()), None)

    if not paciente_id or not medico_id:
        messagebox.showwarning("Advertencia", "Selecciona paciente y médico válidos")
        return

    try:
        cursor.execute("CALL registrar_consulta(%s, %s, %s, %s, %s, %s)", (
            paciente_id,
            medico_id,
            entradas["Fecha de Consulta"].get(),
            entradas["Diagnostico"].get(),
            entradas["Tratamiento"].get(),
            entradas["Estado"].get()
        ))
        conexion.commit()
        messagebox.showinfo("Éxito", "Consulta guardada")
        mostrar_consultas(tabla)
        limpiar_campos(entradas)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        conexion.rollback()

if __name__ == "__main__":
    mostrar_ventana()