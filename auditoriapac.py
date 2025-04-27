#auditoriapac.py
import tkinter as tk
from tkinter import ttk
import psycopg2

def mostrar_auditoria():
    ventana_auditoria = tk.Toplevel()
    ventana_auditoria.title("📋 Registro de Cambios en Pacientes")
    ventana_auditoria.geometry("1100x500")
    ventana_auditoria.configure(bg="#e8f0fe")  

    titulo = tk.Label(
        ventana_auditoria, 
        text="📋 Historial de Cambios Realizados a Pacientes",
        font=("Segoe UI", 16, "bold"),
        bg="#e8f0fe", 
        fg="#0d47a1", 
        pady=10
    )
    titulo.pack()

    marco_tabla = tk.Frame(ventana_auditoria, bg="#e8f0fe")
    marco_tabla.pack(fill="both", expand=True, padx=20, pady=10)

    # scrollbars
    scrollbar_y = tk.Scrollbar(marco_tabla, orient="vertical")
    scrollbar_x = tk.Scrollbar(marco_tabla, orient="horizontal")

    columnas = ("ID Auditoría", "ID Paciente", "Acción", "Usuario", "Fecha", "Campos Modificados")

    tree = ttk.Treeview(
        marco_tabla,
        columns=columnas,
        show="headings",
        yscrollcommand=scrollbar_y.set,
        xscrollcommand=scrollbar_x.set
    )

    scrollbar_y.config(command=tree.yview)
    scrollbar_x.config(command=tree.xview)

    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")
    tree.pack(fill="both", expand=True)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)

    anchuras = {
        "ID Auditoría": 120,
        "ID Paciente": 120,
        "Acción": 130,
        "Usuario": 120,
        "Fecha": 180,
        "Campos Modificados": 400
    }

    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=anchuras[col], stretch=False)

    # Obtener datos
    try:
        conexion = psycopg2.connect(
            host="localhost",
            database="clinica_db",
            user="postgres",
            password="334003562Mn#"
        )
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM auditoria_pacientes ORDER BY auditoria_id DESC")
        for fila in cursor.fetchall():
            tree.insert("", tk.END, values=fila)

        cursor.close()
        conexion.close()
    except Exception as e:
        print("Error al conectar con la base de datos:", e)

        
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    mostrar_auditoria()
    root.mainloop()
