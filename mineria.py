import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
from tkinter import ttk

# Rutas de los archivos de imagen
ICON = "images/logo.ico"
LOGO = "images/logo.png"

# Colores
COLOR1 = "#0056b3"
COLOR2 = "#333333"
COLOR3 = "#FFFFFF"

class AnalisisDatos:
    def __init__(self, root):
        """
        Constructor de la clase AnalisisDatos.
        """
        self.root = root
        self.root.title("Minería de Datos v1.0")
        self.root.geometry("1366x700")
        self.root.resizable(False, False)
        # self.root.protocol("WM_DELETE_WINDOW", self.confirmar_salir)
        self.root.iconbitmap(ICON)

        # Crear un Frame en la parte superior como barra de menú
        self.menu_frame = tk.Frame(self.root, background=COLOR3, height=60)
        self.menu_frame.pack(side="top", fill="x")

        # Estilo de los botones del menú
        estilo_botones = {
            "background": COLOR3,
            "foreground": COLOR1,
            "activebackground": COLOR1,
            "activeforeground": COLOR3,
            "font": ("Arial", 14),
            "borderwidth": 1,
            "relief": "solid",
            "width": 16,
            "highlightbackground": COLOR1
        }

        # Botones del menú
        botones = [
            ("Principal", self.vent_principal),
            ("Análisis", self.analisis_datos),
            ("Insertar", self.insetar_datos),
            ("Acerca de", self.acercade),
            ("Salir", self.confirmar_salir)
        ]

        # Crear los botones del menú
        for texto, comando in botones:
            btn = tk.Button(self.menu_frame, text=texto, command=comando, **estilo_botones)
            btn.pack(side="left", padx=10)

        # Crear un Frame en la parte inferior para el contenido
        self.main_frame = tk.Frame(self.root, background=COLOR3)
        self.main_frame.pack(expand=True, fill="both")

        # Cargar la ventana principal
        self.vent_principal()

        # Variable para almacenar el archivo cargado
        self.archivo_cargado = None

    def limpiar_frame(self):
        """
        Limpiar el contenido del Frame principal.
        """
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # Tabla para mostrar los datos
    def mostrar_datos(self, datos):
        self.limpiar_frame()
        tabla_frame = tk.Frame(self.main_frame, background="gray")
        tabla_frame.pack(expand=True, fill="both", padx=20, pady=20)

        tabla = ttk.Treeview(tabla_frame)
        tabla.pack(expand=True, fill="both")

        tabla["columns"] = list(datos.columns)
        for col in datos.columns:
            tabla.heading(col, text=col)
            tabla.column(col, anchor="center")

        for _, row in datos.iterrows():
            tabla.insert("", "end", values=list(row))

        nueva_carga_btn = tk.Button(tabla_frame, text="Nueva Carga", command=self.vent_principal, background="white", foreground="gray", font=("Arial", 14))
        nueva_carga_btn.pack(pady=10)

    def vent_principal(self):
        """
        Cargar la ventana principal.
        """
        self.limpiar_frame()
        # Crear un Frame para la sección principal
        principal_frame = tk.Frame(self.main_frame, background=COLOR3)
        principal_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Etiqueta de título
        titulo_label = tk.Label(principal_frame, text="Cargar Datos", font=("Arial", 24), background=COLOR3, foreground=COLOR1)
        titulo_label.pack(pady=10)

        # Botón para buscar archivo
        def buscar_archivo():
            archivo = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
            if archivo:
                archivo_entry.delete(0, tk.END)
                archivo_entry.insert(0, archivo)

        buscar_btn = tk.Button(principal_frame, text="Buscar Archivo", command=buscar_archivo, background=COLOR1, foreground=COLOR3, font=("Arial", 14))
        buscar_btn.pack(pady=10)

        # Entry para mostrar la ruta del archivo seleccionado
        archivo_entry = tk.Entry(principal_frame, font=("Arial", 14), width=50)
        archivo_entry.pack(pady=10)

        # Botón para cargar datos
        def cargar_datos():
            archivo = archivo_entry.get()
            if archivo:
                try:
                    self.archivo_cargado = archivo  # Guardar el archivo cargado
                    datos = pd.read_csv(archivo)
                    self.mostrar_datos(datos)
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")
                    print(e)

        cargar_btn = tk.Button(principal_frame, text="Cargar", command=cargar_datos, background=COLOR1, foreground=COLOR3, font=("Arial", 14))
        cargar_btn.pack(pady=10)

    def analisis_datos(self):
        """
        Cargar la ventana de análisis de datos.
        """
        if not self.archivo_cargado:
            messagebox.showwarning("Advertencia", "Debe cargar un archivo antes de realizar análisis.")
            return

        self.limpiar_frame()
        analisis_frame = tk.Frame(self.main_frame, background="gray")
        analisis_frame.pack(expand=True, fill="both", padx=20, pady=20)

        label = tk.Label(analisis_frame, text="Análisis de Datos", font=("Arial", 24), background="gray", foreground="white")
        label.pack(pady=10)

        datos = pd.read_csv(self.archivo_cargado)
        resumen = datos.describe()

        text_box = tk.Text(analisis_frame, font=("Arial", 12), height=15, width=80)
        text_box.insert("1.0", resumen.to_string())
        text_box.pack()

    def insetar_datos(self):
        """
        Cargar la ventana de inserción de datos.
        """
        if not self.archivo_cargado:
            messagebox.showwarning("Advertencia", "Debe cargar un archivo antes de insertar datos.")
            return

        self.limpiar_frame()
        insertar_frame = tk.Frame(self.main_frame, background="gray")
        insertar_frame.pack(expand=True, fill="both", padx=20, pady=20)

        label = tk.Label(insertar_frame, text="Insertar Datos", font=("Arial", 24), background="gray", foreground="white")
        label.pack(pady=10)

    def acercade(self):
        """
        Cargar la ventana de "Acerca de".
        """
        self.limpiar_frame()

        # Frame para centrar el contenido
        acerca_frame = tk.Frame(self.main_frame, background=COLOR3)
        acerca_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Imagen representativa
        logo = tk.PhotoImage(file=LOGO)
        logo_label = tk.Label(acerca_frame, image=logo, background=COLOR3)
        logo_label.image = logo
        logo_label.pack(pady=10)

        about_text = (
            "Minería de Datos v1.0\n"
            "2025\n"
            "Desarrollado por: Camilo Mercado\n"
            'Aplicación para análisis de datos extraídos de "Datos Abiertos."'
        )

        about_label = tk.Label(acerca_frame, text=about_text, font=("Arial", 14), background=COLOR3, foreground=COLOR2, justify="center")
        about_label.pack(pady=10)

    def confirmar_salir(self):
        """
        Confirmar si el usuario desea salir del aplicativo.
        """
        respuesta = messagebox.askyesno("Salir", "¿Está seguro de que desea salir del aplicativo?")
        if respuesta:
            self.root.quit()

# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = AnalisisDatos(root)
    root.mainloop()