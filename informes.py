# informes.py
import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

def generar_informe_paciente(paciente_id):
    try:
        conexion = psycopg2.connect(
            host="localhost",
            database="clinica_db",
            user="postgres",
            password="334003562Mn#"
        )
        cursor = conexion.cursor()

        query = f"SELECT * FROM generar_informe_paciente({paciente_id});"
        cursor.execute(query)
        resultado = cursor.fetchall()

        informe_texto = "\n=== 📝 INFORME DEL PACIENTE ===\n"
        for fila in resultado:
            informe_texto += (
                f"\n📌 Nombre: {fila[0]}"
                f"\n📅 Fecha de Nacimiento: {fila[1]}"
                f"\n📞 Teléfono: {fila[2]}"
                f"\n🏠 Dirección: {fila[3]}"
                f"\n🩺 Médico: {fila[4]}"
                f"\n🗓 Fecha de Consulta: {fila[5]}"
                f"\n📋 Diagnóstico: {fila[6]}"
                f"\n🔎 Estado de la Consulta: {fila[7]}"
                f"\n📖 Historial Diagnóstico: {fila[8]}"
                f"\n💊 Historial de Tratamiento: {fila[9]}"
                f"\n{'-' * 60}\n"
            )

        cursor.close()
        conexion.close()
        return informe_texto

    except Exception as e:
        return f"❌ Error al generar el informe: {e}"

def mostrar_ventana():
    ventana = tk.Toplevel()
    ventana.title("Generar Informe de Paciente")
    ventana.geometry("1050x350")
    ventana.config(bg="#f0f0f0")

   
    frame = tk.Frame(ventana, bg="#f0f0f0")
    frame.pack(pady=10)

    tk.Label(frame, text="Selecciona un paciente:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)

    combo_pacientes = ttk.Combobox(frame, state="readonly", width=40)
    combo_pacientes.grid(row=0, column=1, padx=5, pady=5)

    
    try:
        conexion = psycopg2.connect(
            host="localhost",
            database="clinica_db",
            user="postgres",
            password="334003562Mn#"
        )
        cursor = conexion.cursor()
        cursor.execute("SELECT paciente_id, nombre_completo FROM pacientes ORDER BY paciente_id;")
        pacientes = cursor.fetchall()
        conexion.close()

        lista_pacientes = [f"{p[0]} - {p[1]}" for p in pacientes]
        combo_pacientes["values"] = lista_pacientes

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la lista de pacientes:\n{e}")

    
    frame_texto = tk.Frame(ventana, bg="#f0f0f0")
    frame_texto.pack(pady=10, fill="both", expand=True)

    # Scrollbars
    scrollbar_y = tk.Scrollbar(frame_texto, orient="vertical")
    scrollbar_x = tk.Scrollbar(frame_texto, orient="horizontal")

    frame_texto.columnconfigure(0, weight=1)
    frame_texto.rowconfigure(0, weight=1)

    text_informe = tk.Text(frame_texto, wrap="none", yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set,
                       bg="#ffffff", font=("Courier New", 10))
    text_informe.grid(row=0, column=0, sticky="nsew")

    scrollbar_y.config(command=text_informe.yview)
    scrollbar_y.grid(row=0, column=1, sticky="ns")

    scrollbar_x.config(command=text_informe.xview)
    scrollbar_x.grid(row=1, column=0, sticky="ew")

    # boton generar informe
    def generar_informe():
        seleccion = combo_pacientes.get()
        if not seleccion:
            messagebox.showwarning("Aviso", "Debes seleccionar un paciente.")
            return

        paciente_id = seleccion.split(" - ")[0]
        informe = generar_informe_paciente(paciente_id)
        text_informe.delete("1.0", tk.END)
        text_informe.insert(tk.END, informe)

    btn_generar = tk.Button(frame, text="Generar Informe", command=generar_informe,
                            bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
    btn_generar.grid(row=0, column=2, padx=5, pady=5)

    # consulta avanzada
    btn_avanzada = tk.Button(frame, text="Clasificación Pacientes", command=mostrar_consulta_avanzada,
                             bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
    btn_avanzada.grid(row=0, column=3, padx=5, pady=5)

    btn_asignar_medico = tk.Button(frame, text="Asignar Médico", command=mostrar_asignacion_medico,
                               bg="#FF9800", fg="white", font=("Arial", 10, "bold"))
    btn_asignar_medico.grid(row=0, column=4, padx=5, pady=5)
    btn_resumen = tk.Button(frame, text="Resumen Consultas", command=mostrar_resumen_consultas,
                        bg="#9C27B0", fg="white", font=("Arial", 10, "bold"))
    btn_resumen.grid(row=0, column=5, padx=5, pady=5)

#  consulta avanzada con CASE según edad
def mostrar_consulta_avanzada():
    ventana_avanzada = tk.Toplevel()
    ventana_avanzada.title("Clasificación de Pacientes por Edad")
    ventana_avanzada.geometry("600x350")
    ventana_avanzada.resizable(False, False)
    ventana_avanzada.config(bg="#f0f0f0")

    label_titulo = tk.Label(ventana_avanzada, text="Clasificación de Pacientes por Edad",
                            font=("Arial", 14, "bold"), bg="#f0f0f0", fg="#333")
    label_titulo.pack(pady=10)

    frame_tree = tk.Frame(ventana_avanzada)
    frame_tree.pack(padx=10, pady=10, fill="both", expand=True)

    columnas = ("Nombre", "Edad", "Clasificación")
    tree = ttk.Treeview(frame_tree, columns=columnas, show="headings", height=10)
    tree.pack(side="left", fill="both", expand=True)

    # cabeceras y anchos
    tree.heading("Nombre", text="Nombre")
    tree.heading("Edad", text="Edad")
    tree.heading("Clasificación", text="Clasificación")

    tree.column("Nombre", anchor="center", width=260)
    tree.column("Edad", anchor="center", width=80)
    tree.column("Clasificación", anchor="center", width=140)

    # Scrollbar vertical
    scrollbar_y = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    scrollbar_y.pack(side="right", fill="y")

    # Scrollbar horizontal
    scrollbar_x = ttk.Scrollbar(ventana_avanzada, orient="horizontal", command=tree.xview)
    scrollbar_x.pack(side="bottom", fill="x")

    tree.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)

    try:
        conexion = psycopg2.connect(
            host="localhost",
            database="clinica_db",
            user="postgres",
            password="334003562Mn#"
        )
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                nombre_completo, 
                EXTRACT(YEAR FROM AGE(fecha_nacimiento)) AS edad,
                CASE 
                    WHEN EXTRACT(YEAR FROM AGE(fecha_nacimiento)) < 18 THEN 'Menor de Edad'
                    WHEN EXTRACT(YEAR FROM AGE(fecha_nacimiento)) BETWEEN 18 AND 60 THEN 'Adulto'
                    ELSE 'Adulto Mayor'
                END AS clasificacion
            FROM pacientes
            ORDER BY edad DESC;
        """)
        registros = cursor.fetchall()
        conexion.close()

        for i, reg in enumerate(registros):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            tree.insert("", "end", values=reg, tags=(tag,))

        tree.tag_configure("evenrow", background="#f9f9f9")
        tree.tag_configure("oddrow", background="#e0e0e0")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo realizar la consulta avanzada:\n{e}")

def buscar_medico(departamento_id):
    try:
        conexion = psycopg2.connect(
            host="localhost",
            database="clinica_db",
            user="postgres",
            password="334003562Mn#"
        )
        cursor = conexion.cursor()

        query = "SELECT medico_id, nombre_completo FROM asignar_medico_por_departamento(%s);"
        cursor.execute(query, (departamento_id,))
        resultado = cursor.fetchall()  

        cursor.close()
        conexion.close()

        if resultado:
            texto_resultado = "✅ Médicos asignados:\n"
            for medico_id, nombre_completo in resultado:
                texto_resultado += f"\n🆔 ID: {medico_id}\n👨‍⚕️ Nombre: {nombre_completo}\n{'-' * 20}"
            return texto_resultado
        else:
            return "⚠️ No hay médicos disponibles en ese departamento."

    except Exception as e:
        return f"❌ Error al buscar médicos: {e}"

#Ventana para asignar médico por especialidad
def mostrar_asignacion_medico():
    ventana = tk.Toplevel()
    ventana.title("Asignar Médico por Especialidad")
    ventana.geometry("400x300")
    ventana.config(bg="#f0f0f0")

    tk.Label(ventana, text="Selecciona un departamento:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)

    try:
        conexion = psycopg2.connect(
            host="localhost",
            database="clinica_db",
            user="postgres",
            password="334003562Mn#"
        )
        cursor = conexion.cursor()
        cursor.execute("SELECT departamento_id, nombre_departamento FROM departamentos ORDER BY departamento_id")
        departamentos = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
        cursor.close()
        conexion.close()
    except Exception as e:
        departamentos = []
        messagebox.showerror("Error", f"No se pudieron cargar los departamentos: {e}")

    combo_departamento = ttk.Combobox(ventana, state="readonly", values=departamentos, width=35)
    combo_departamento.pack(pady=5)

    text_resultado = tk.Text(ventana, height=8, width=45, bg="#ffffff", font=("Arial", 10))
    text_resultado.pack(pady=10)

    def asignar_medico():
        seleccion = combo_departamento.get()
        if not seleccion:
            messagebox.showwarning("Aviso", "Debes seleccionar un departamento.")
            return

        departamento_id = int(seleccion.split(" - ")[0])
        resultado = buscar_medico(departamento_id)
        text_resultado.delete("1.0", tk.END)
        text_resultado.insert(tk.END, resultado)

    btn_buscar = tk.Button(ventana, text="Asignar Médico", command=asignar_medico,
                           bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
    btn_buscar.pack(pady=5)

def mostrar_resumen_consultas():
    ventana_resumen = tk.Toplevel()
    ventana_resumen.title("Resumen de Consultas por Médico")
    ventana_resumen.geometry("500x350")
    ventana_resumen.config(bg="#f0f0f0")

    label_titulo = tk.Label(ventana_resumen, text="Resumen de Consultas por Médico",
                            font=("Arial", 14, "bold"), bg="#f0f0f0", fg="#333")
    label_titulo.pack(pady=10)

    frame_tree = tk.Frame(ventana_resumen)
    frame_tree.pack(padx=10, pady=10, fill="both", expand=True)

    columnas = ("Médico", "Pendientes", "Finalizadas")
    tree = ttk.Treeview(frame_tree, columns=columnas, show="headings", height=12)
    tree.pack(side="left", fill="both", expand=True)

    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=140)

    scrollbar_y = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    scrollbar_y.pack(side="right", fill="y")
    tree.configure(yscroll=scrollbar_y.set)

    try:
        conexion = psycopg2.connect(
            host="localhost",
            database="clinica_db",
            user="postgres",
            password="334003562Mn#"
        )
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                m.nombre_completo AS medico,
                COUNT(*) FILTER (WHERE c.estado_consulta = 'Pendiente') AS pendientes,
                COUNT(*) FILTER (WHERE c.estado_consulta = 'Finalizada') AS finalizadas
            FROM consultas c
            JOIN medicos m ON c.medico_id = m.medico_id
            GROUP BY m.nombre_completo
            ORDER BY m.nombre_completo;
        """)
        registros = cursor.fetchall()
        conexion.close()

        for i, reg in enumerate(registros):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            tree.insert("", "end", values=reg, tags=(tag,))

        tree.tag_configure("evenrow", background="#f9f9f9")
        tree.tag_configure("oddrow", background="#e0e0e0")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener el resumen:\n{e}")