#principal.py
import tkinter as tk
from PIL import Image, ImageTk
from pacientes import mostrar_ventana as ventana_pacientes
from medicos import mostrar_ventana as ventana_medicos
from consultas import mostrar_ventana as ventana_consultas
from departamentos import mostrar_ventana as ventana_departamentos
from historialmedico import mostrar_ventana as ventana_historialmedico
from informes import mostrar_ventana as ventana_informes

def mostrar_principal():
    app = tk.Tk()
    app.title("Sistema de Gestión Hospitalaria")
    app.geometry("500x700")  # tamaño de la ventana
    app.configure(bg="#f0f4ff")


    # imagen del hospital
    try:
        img = Image.open("hospital.png")
        img = img.resize((200, 200), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        label_img = tk.Label(app, image=img_tk, bg="#f0f4ff")
        label_img.image = img_tk
        label_img.pack(pady=(10, 5))
    except Exception as e:
        print("Error cargando imagen:", e)

    # Titulo
    tk.Label(
        app,
        text="Sistema de Gestión Hospitalaria",
        font=("Helvetica", 16, "bold"),
        fg="#0047ab",
        bg="#f0f4ff"
    ).pack(pady=(0, 10))

    tk.Label(
        app,
        text="Selecciona una opción",
        font=("Arial", 12),
        bg="#f0f4ff",
        fg="#333333"
    ).pack(pady=(0, 15))

    # estilo de botones 
    def estilo_boton(frame, texto, comando):
        return tk.Button(
            frame,
            text=texto,
            command=comando,
            width=25,
            height=1, 
            bg="#28a745",
            fg="white",
            font=("Arial", 11, "bold"),
            bd=2,
            relief="solid",
            highlightthickness=2,
            highlightbackground="black",
            activebackground="#218838",
            activeforeground="white",
            cursor="hand2"
        )
    
    
    frame_botones = tk.Frame(app, bg="#f0f4ff")
    frame_botones.pack(pady=(10, 0)) 

    botones = [
        ("Pacientes", ventana_pacientes),
        ("Médicos", ventana_medicos),
        ("Consultas", ventana_consultas),
        ("Departamentos", ventana_departamentos),
        ("Historial Médico", ventana_historialmedico),
        ("Informes", ventana_informes),
        ("Salir", app.destroy)
    ]

    
    for texto, accion in botones:
        estilo_boton(frame_botones, texto, accion).pack(pady=8)

    app.mainloop()

if __name__ == "__main__":
    mostrar_principal()