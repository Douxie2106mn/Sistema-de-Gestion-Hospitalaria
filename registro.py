#registro.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import conexion

def registrar_usuario(usuario, correo, contrasena):
    if not usuario or not correo or not contrasena:
        messagebox.showerror("Error", "Por favor, completa todos los campos")
        return

    conn = conexion.conectar()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO usuarios (usuario, correo, contrasena) VALUES (%s, %s, %s)", 
                        (usuario, correo, contrasena))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el usuario: {e}")

def abrir_ventana_registro():
    reg = tk.Toplevel()
    reg.title("Registro de Usuario")
    reg.geometry("400x400")
    reg.configure(bg="#f0f4ff")

    # Titulo
    tk.Label(
        reg,
        text="Registro de Usuario",
        font=("Helvetica", 16, "bold"),
        fg="#0047ab",
        bg="#f0f4ff"
    ).pack(pady=15)

    # Subtitulo
    tk.Label(
        reg,
        text="Completa los siguientes campos:",
        font=("Arial", 12),
        fg="#333333",
        bg="#f0f4ff"
    ).pack(pady=5)

    frame_form = tk.Frame(reg, bg="#f0f4ff")
    frame_form.pack(pady=20)

    tk.Label(frame_form, text="Usuario:", font=("Arial", 11), bg="#f0f4ff").grid(row=0, column=0, sticky="w", pady=5)
    entry_usuario = ttk.Entry(frame_form, font=("Arial", 11), width=30)
    entry_usuario.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame_form, text="Correo:", font=("Arial", 11), bg="#f0f4ff").grid(row=1, column=0, sticky="w", pady=5)
    entry_correo = ttk.Entry(frame_form, font=("Arial", 11), width=30)
    entry_correo.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame_form, text="Contraseña:", font=("Arial", 11), bg="#f0f4ff").grid(row=2, column=0, sticky="w", pady=5)
    entry_contra = ttk.Entry(frame_form, font=("Arial", 11), show="*", width=30)
    entry_contra.grid(row=2, column=1, padx=10, pady=5)

    # botones
    frame_buttons = tk.Frame(reg, bg="#f0f4ff")
    frame_buttons.pack(pady=20)

    def guardar():
        registrar_usuario(entry_usuario.get(), entry_correo.get(), entry_contra.get())
        reg.destroy()

    boton_registrar = tk.Button(
        frame_buttons,
        text="Registrar",
        command=guardar,
        width=15,
        height=1,
        bg="#28a745",
        fg="white",
        font=("Arial", 11, "bold"),
        relief="solid",
        bd=2,
        activebackground="#218838",
        activeforeground="white",
        cursor="hand2"
    )
    boton_registrar.grid(row=0, column=0, padx=10)

    boton_cancelar = tk.Button(
        frame_buttons,
        text="Cancelar",
        command=reg.destroy,
        width=15,
        height=1,
        bg="#d32f2f",
        fg="white",
        font=("Arial", 11, "bold"),
        relief="solid",
        bd=2,
        activebackground="#c62828",
        activeforeground="white",
        cursor="hand2"
    )
    boton_cancelar.grid(row=0, column=1, padx=10)

    # Pie de página
    tk.Label(
        reg,
        text="© 2025 Sistema de Gestión. Todos los derechos reservados.",
        font=("Arial", 9),
        fg="#666666",
        bg="#f0f4ff"
    ).pack(side="bottom", pady=10)