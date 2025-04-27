# asignar_medico.py
import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

def buscar_medico(departamento_id):
    try:
        conexion = psycopg2.connect(
            host="localhost",
            database="clinica_db",
            user="postgres",
            password="334003562Mn#"
        )
        cursor = conexion.cursor()

        query = f"SELECT * FROM asignar_medico_por_departamento(%s);"  # función ajustada
        cursor.execute(query, (departamento_id,))
        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        if resultado:
            medico_id, nombre_completo = resultado
            return f"✅ Médico asignado:\n\n🆔 ID: {medico_id}\n👨‍⚕️ Nombre: {nombre_completo}"
        else:
            return "⚠️ No hay médicos disponibles en ese departamento."

    except Exception as e:
        return f"❌ Error al buscar médico: {e}"

def mostrar_ventana():
    ventana = tk.Toplevel()
    ventana.title("Asignar Médico por Especialidad")
    ventana.geometry("400x300")
    ventana.config(bg="#f0f0f0")

    tk.Label(ventana, text="Selecciona un departamento:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)

    #obtener departamentos desde la BD
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

        departamento_id = int(seleccion.split(" - ")[0])  # Extraemos solo el ID
        resultado = buscar_medico(departamento_id)
        text_resultado.delete("1.0", tk.END)
        text_resultado.insert(tk.END, resultado)

    btn_buscar = tk.Button(ventana, text="Asignar Médico", command=asignar_medico,
                           bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
    btn_buscar.pack(pady=5)