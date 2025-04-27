#login.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  
import conexion
import registro  
import principal  

def verificar_login(usuario, contrasena):
    conn = conexion.conectar()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE usuario = %s AND contrasena = %s", (usuario, contrasena))
        resultado = cur.fetchone()
        conn.close()
        if resultado:
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
            root.destroy()
            principal.mostrar_principal()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

def mostrar_registro():
    registro.abrir_ventana_registro()

root = tk.Tk()
root.title("Inicio de Sesión")
root.geometry("500x350")
root.configure(bg="#f0f4ff")

# Título
tk.Label(
    root,
    text="Sistema de Gestión Hospitalaria",
    font=("Helvetica", 16, "bold"),
    fg="#0047ab",
    bg="#f0f4ff"
).pack(pady=15)

# subtitulo
tk.Label(
    root,
    text="Inicia sesión con tu cuenta",
    font=("Arial", 12),
    fg="#333333",
    bg="#f0f4ff"
).pack(pady=5)

# Entrada de usuario
frame_form = tk.Frame(root, bg="#f0f4ff")
frame_form.pack(pady=20)

tk.Label(frame_form, text="Usuario:", font=("Arial", 11), bg="#f0f4ff").grid(row=0, column=0, sticky="w", pady=5)
entry_usuario = ttk.Entry(frame_form, font=("Arial", 11), width=30)
entry_usuario.grid(row=0, column=1, padx=10, pady=5)

# Entrada de contraseña
tk.Label(frame_form, text="Contraseña:", font=("Arial", 11), bg="#f0f4ff").grid(row=1, column=0, sticky="w", pady=5)
entry_contra = ttk.Entry(frame_form, font=("Arial", 11), show="*", width=30)
entry_contra.grid(row=1, column=1, padx=10, pady=5)

# botones
frame_buttons = tk.Frame(root, bg="#f0f4ff")
frame_buttons.pack(pady=20)

boton_login = tk.Button(
    frame_buttons,
    text="Iniciar Sesión",
    command=lambda: verificar_login(entry_usuario.get(), entry_contra.get()),
    width=20,
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
boton_login.grid(row=0, column=0, padx=10)

boton_registrar = tk.Button(
    frame_buttons,
    text="Registrar",
    command=mostrar_registro,
    width=20,
    height=1,
    bg="#0047ab",
    fg="white",
    font=("Arial", 11, "bold"),
    relief="solid",
    bd=2,
    activebackground="#003e8e",
    activeforeground="white",
    cursor="hand2"
)
boton_registrar.grid(row=0, column=1, padx=10)

#  pie de pagina
tk.Label(
    root,
    text="© 2025 Sistema Hospitalario. Todos los derechos reservados.",
    font=("Arial", 9),
    fg="#666666",
    bg="#f0f4ff"
).pack(side="bottom", pady=10)

root.mainloop()