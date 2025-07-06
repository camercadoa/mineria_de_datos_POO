import tkinter as tk
import chardet
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import messagebox, filedialog, ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Rutas de los archivos de imagen
ICON = "images/logo.ico"
LOGO = "images/logo.png"

# Colores
COLOR1 = "#0056b3"
COLOR2 = "#333333"
COLOR3 = "#FFFFFF"
COLOR_FILA1 = "#E8E8E8"

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
        self.menu_frame = tk.Frame(self.root, background=COLOR1, height=60)
        self.menu_frame.pack(side="top", fill="x")

        # Estilo de los botones del menú
        estilo_botones = {
            "background": COLOR1,
            "foreground": COLOR3,
            "activebackground": COLOR3,
            "activeforeground": COLOR1,
            "font": ("Arial", 16, "bold"),
            "borderwidth": 0,
            "relief": "flat",
            "width": 16
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
            btn.pack(side="left", padx=30, pady=10)

        # Crear un Frame en la parte inferior para el contenido
        self.main_frame = tk.Frame(self.root, background=COLOR3)
        self.main_frame.pack(expand=True, fill="both")

        # Variable para almacenar el archivo cargado
        self.archivo_cargado = None

        # Variable para almacenar los datos
        self.datos_cargados = None

        # Cargar la ventana principal
        self.vent_principal()

    def limpiar_frame(self):
        """
        Limpiar el contenido del Frame principal.
        """
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def vent_principal(self):
        """
        Cargar la ventana principal.
        """
        self.limpiar_frame()

        # Verificar si ya se cargaron datos
        if self.datos_cargados is not None:
            # Mostrar la tabla con los datos cargados
            self.mostrar_datos(self.datos_cargados)
        else:
            # Crear un Frame para la sección principal
            principal_frame = tk.Frame(self.main_frame, background=COLOR3)
            principal_frame.pack(expand=True, fill="both", padx=20, pady=20)

            # Etiqueta de título
            titulo_label = tk.Label(principal_frame, text="Cargar datos", font=("Arial", 24, "bold"), background=COLOR3, foreground=COLOR1)
            titulo_label.pack(pady=10)

            # Contenedor para el botón de "Buscar archivo" y "Cargar"
            frame_carga = tk.Frame(principal_frame, background=COLOR3)
            frame_carga.pack(pady=10)

            # Botón para buscar archivo
            def buscar_archivo():
                archivo = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
                if archivo:
                    archivo_entry.delete(0, tk.END)
                    archivo_entry.insert(0, archivo)

            buscar_btn = tk.Button(frame_carga, text="Buscar Archivo", command=buscar_archivo, background=COLOR1, foreground=COLOR3, font=("Arial", 14))
            buscar_btn.pack(side="left", padx=5)

            # Entry para mostrar la ruta del archivo seleccionado
            archivo_entry = tk.Entry(frame_carga, font=("Arial", 14), width=80)
            archivo_entry.pack(side="left", padx=5)

            # Botón para cargar datos
            def cargar_datos():
                archivo = archivo_entry.get()
                if archivo:
                    try:
                        # Detectar codificación
                        with open(archivo, "rb") as f:
                            resultado = chardet.detect(f.read(100000))  # Analiza los primeros 100,000 bytes
                            encoding_detectado = resultado["encoding"]

                        if encoding_detectado is None:
                            raise ValueError("No se pudo detectar la codificación del archivo.")

                        # Cargar el archivo con la codificación detectada
                        self.archivo_cargado = archivo
                        self.datos_cargados = pd.read_csv(archivo, encoding=encoding_detectado)

                        # Mostrar los datos
                        self.mostrar_datos(self.datos_cargados)

                    except UnicodeDecodeError:
                        messagebox.showerror("Error", "No se pudo leer el archivo con la codificación detectada.")
                    except Exception as e:
                        messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")
                        print(e)

            cargar_btn = tk.Button(frame_carga, text="Cargar", command=cargar_datos, background=COLOR1, foreground=COLOR3, font=("Arial", 14))
            cargar_btn.pack(side="left", padx=5)

            try:
                # Imagen representativa
                logo = tk.PhotoImage(file=LOGO)
                logo_label = tk.Label(principal_frame, image=logo, background=COLOR3)
                logo_label.image = logo
                logo_label.pack(pady=10)
            except Exception as e:
                print(f"Error al cargar la imagen: {e}")

    def mostrar_datos(self, datos):
        """
        Mostrar los datos cargados en una tabla.
        """
        self.limpiar_frame()
        # Guardar los datos cargados
        self.datos_cargados = datos

        # Crear un Frame para la tabla
        tabla_frame = tk.Frame(self.main_frame, background=COLOR3)
        tabla_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Estilo de la tabla
        estilo_tabla = ttk.Style()
        estilo_tabla.configure("Treeview", font=("Arial", 12), rowheight=25, background=COLOR3, foreground=COLOR2)
        estilo_tabla.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        # Contenedor para la tabla
        contenedor_tabla = tk.Frame(tabla_frame)
        contenedor_tabla.pack(expand=True, fill="both")

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(contenedor_tabla, orient="vertical")
        scrollbar_x = ttk.Scrollbar(contenedor_tabla, orient="horizontal")

        # Tabla con scrollbars
        tabla = ttk.Treeview(contenedor_tabla, yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set, selectmode="browse")
        scrollbar_y.config(command=tabla.yview)
        scrollbar_x.config(command=tabla.xview)

        # Posicionar los scrollbars
        scrollbar_x.pack(side="bottom", fill="x")
        scrollbar_y.pack(side="right", fill="y")
        tabla.pack(expand=True, fill="both")

        # Encabezados de la tabla
        tabla["columns"] = list(datos.columns)
        tabla["show"] = "headings" # Ocultar la primera columna

        # Encabezados y columnas con ancho automático
        for col in datos.columns:
            tabla.heading(col, text=col, anchor="center")
            tabla.column(col, anchor="center", width=150)

        # Insertar los datos en la tabla con colores alternos
        for i, row in datos.iterrows():
            color_fila = COLOR_FILA1 if i % 2 == 0 else COLOR3
            tabla.insert("", "end", values=list(row), tags=("even" if i % 2 == 0 else "odd",))

        # Configurar los colores de las filas
        tabla.tag_configure("even", background=COLOR_FILA1)
        tabla.tag_configure("odd", background=COLOR3)

        def nueva_carga():
                    self.archivo_cargado = None
                    self.datos_cargados = None  # Eliminar datos almacenados
                    self.vent_principal()  # Volver a la pantalla de carga

        nueva_carga_btn = tk.Button(tabla_frame, text="Nueva Carga", command=nueva_carga,background=COLOR1, foreground=COLOR3, font=("Arial", 14))
        nueva_carga_btn.pack(pady=10)

    def analisis_datos(self):
        """
        Cargar la ventana de análisis de datos.
        """
        if not self.archivo_cargado:
            messagebox.showwarning("Advertencia", "Debe cargar un archivo antes de realizar análisis.")
            return

        self.limpiar_frame()

        # Frame principal para el análisis de datos
        analisis_frame = tk.Frame(self.main_frame, background=COLOR3)
        analisis_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Título
        label_title = tk.Label(analisis_frame, text="Análisis de Datos", font=("Arial", 24), background=COLOR3, foreground=COLOR1)
        label_title.pack(pady=10)

        # Crear un contenedor para el Frame con scroll
        canvas = tk.Canvas(analisis_frame, background=COLOR3)
        scrollbar = tk.Scrollbar(analisis_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, background=COLOR3)

        # Configurar el frame dentro del canvas
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Agregar el scroll al canvas
        frame_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        # Empaquetar el canvas y el scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Vincular scroll con el mouse
        def vincular_scroll(event):
            widget = event.widget
            if isinstance(widget, tk.Canvas):  # Solo si el evento ocurre en un Canvas
                widget.yview_scroll(-1 * int((event.delta / 120)), "units")

        root.bind_all("<MouseWheel>", vincular_scroll)  # Vincular a la raíz

        # Contenedor para la selección de columna y tipo de dato
        seleccion_frame = tk.Frame(scroll_frame, background=COLOR3)
        seleccion_frame.pack(fill="x", pady=10)

        # Selección de columna
        tk.Label(seleccion_frame, text="Seleccione una columna:", font=("Arial", 14), background=COLOR3, foreground=COLOR2).grid(row=0, column=0, padx=10, pady=5, sticky="w")

        columna_seleccionada = tk.StringVar()
        combo_columnas = ttk.Combobox(seleccion_frame, textvariable=columna_seleccionada, state="readonly", font=("Arial", 12))
        combo_columnas["values"] = list(self.datos_cargados.columns)
        combo_columnas.grid(row=0, column=1, padx=10, pady=5)

        # Seleccion del tipo de dato
        tk.Label(seleccion_frame, text="Seleccione el tipo de dato:", font=("Arial", 14), background=COLOR3, foreground=COLOR2).grid(row=0, column=2, padx=10, pady=5, sticky="w")

        tipo_datos = tk.StringVar()
        tk.Radiobutton(seleccion_frame, text="Categórico", variable=tipo_datos, value="Categorico", font=("Arial", 12), background=COLOR3, foreground=COLOR2).grid(row=0, column=3, padx=5)
        tk.Radiobutton(seleccion_frame, text="Continuo", variable=tipo_datos, value="Continuo", font=("Arial", 12), background=COLOR3, foreground=COLOR2).grid(row=0, column=4, padx=5)

        # Función para generar el análisis
        def generar_analisis():
            """
            Generar el análisis de la columna seleccionada.
            """
            # Limpiar el Frame de análisis
            for widget in scroll_frame.winfo_children():
                if (isinstance(widget, tk.Label) and widget != label_title) or isinstance(widget, ttk.Separator) or (isinstance(widget, tk.Frame) and widget != seleccion_frame):
                    widget.destroy()

            # Obtener la columna y el tipo de dato seleccionado
            columna = columna_seleccionada.get()
            tipo = tipo_datos.get()

            # Validar que se haya seleccionado una columna y un tipo de dato
            if not columna:
                messagebox.showwarning("Advertencia", "Debe seleccionar una columna.")
                return
            if not tipo:
                messagebox.showwarning("Advertencia", "Debe seleccionar el tipo de dato.")
                return

            # Título - HEAD
            tk.Label(scroll_frame, text="HEAD", font=("Arial", 18), background=COLOR3, foreground=COLOR1).pack(pady=10)

            # # Mostrar las primeras 10 filas de la columna seleccionada
            # frame_head = tk.Frame(scroll_frame, background=COLOR3)
            # frame_head.pack(pady=10)

            # # Crear el Treeview
            # tree_head = ttk.Treeview(frame_head, columns=("Index", "Valor"), show="headings", height=10)

            # # Configurar encabezados
            # tree_head.heading("Index", text="Índice")
            # tree_head.heading("Valor", text=columna)

            # # Ajustar tamaño de columnas
            # tree_head.column("Index", width=100, anchor="center")
            # tree_head.column("Valor", width=200, anchor="center")

            # # Insertar datos
            # for i, valor in enumerate(self.datos_cargados[columna].head(10)):
            #     tree_head.insert("", "end", values=(i, valor))

            # # Agregar Treeview al frame
            # tree_head.pack()

            tk.Label(scroll_frame, text=f"Primeras filas de la columna {columna}:", font=("Arial", 16), background=COLOR3, foreground=COLOR2).pack(pady=10)
            tk.Label(scroll_frame, text=self.datos_cargados[columna].head(10), font=("Arial", 14), background=COLOR3, foreground=COLOR2).pack(pady=10)

            # Separador
            ttk.Separator(scroll_frame, orient="horizontal").pack(fill="x", pady=10)

            # Título - Total de registros y valores nulos y únicos
            tk.Label(scroll_frame, text="TOTAL DE REGISTRO - VALORES NULOS - VALORES ÚNICOS", font=("Arial", 18), background=COLOR3, foreground=COLOR1).pack(pady=10)

            # Cantidad de registros y valores nulos y unicos
            total_registros = len(self.datos_cargados)
            valores_nulos = self.datos_cargados[columna].isnull().sum()
            valores_unicos = self.datos_cargados[columna].nunique()

            tk.Label(scroll_frame, text=f"Total de registros: {total_registros}", font=("Arial", 14), background=COLOR3, foreground=COLOR2).pack(pady=5)
            tk.Label(scroll_frame, text=f"Valores nulos en {columna}: {valores_nulos}", font=("Arial", 14), background=COLOR3, foreground=COLOR2).pack(pady=5)
            tk.Label(scroll_frame, text=f"Valores únicos en {columna}: {valores_unicos}", font=("Arial", 14), background=COLOR3, foreground=COLOR2).pack(pady=5)

            # Separador
            ttk.Separator(scroll_frame, orient="horizontal").pack(fill="x", pady=10)

            # Título - Total de registros y valores nulos y únicos
            tk.Label(scroll_frame, text="ESTADÍSTICA DESCRIPTIVA", font=("Arial", 18), background=COLOR3, foreground=COLOR1).pack(pady=10)

            # Estadistica descriptiva
            estadistica_columna = self.datos_cargados[columna].describe()

            tk.Label(scroll_frame, text=f"Estadísticas de la columna {columna}:", font=("Arial", 16), background=COLOR3, foreground=COLOR2).pack(pady=10)
            tk.Label(scroll_frame, text=estadistica_columna, font=("Arial", 14), background=COLOR3, foreground=COLOR2).pack(pady=10)

            # Separador
            ttk.Separator(scroll_frame, orient="horizontal").pack(fill="x", pady=10)

            # Título - Gráficos
            tk.Label(scroll_frame, text="GRÁFICOS", font=("Arial", 18), background=COLOR3, foreground=COLOR1).pack(pady=10)

            # Frame para los gráficos
            graficos_frame = tk.Frame(scroll_frame, background=COLOR3)
            graficos_frame.pack(fill="both", expand=True, pady=10)

            # Graficar la columna seleccionada
            if tipo == "Categorico":
                # Conteo de valores
                datos = self.datos_cargados[columna].value_counts()

                # Gráfico de Barras
                fig = Figure(figsize=(5, 3), dpi=150)
                ax = fig.add_subplot(111)
                datos.plot(kind="bar", ax=ax, color=COLOR1, edgecolor="black")
                ax.set_title(f"Distribución de {columna}", fontsize=12)
                ax.set_ylabel("Frecuencia", fontsize=10)
                ax.grid(axis="y", linestyle="--", alpha=0.6)
                ax.set_axisbelow(True)
                ax.tick_params(axis="both", rotation=15, labelsize=5)

                canvas = FigureCanvasTkAgg(fig, master=graficos_frame)
                canvas.get_tk_widget().pack(pady=10)
                canvas.draw()

                # Gráfico de Torta
                fig2 = Figure(figsize=(5, 5), dpi=150)
                ax2 = fig2.add_subplot(111)
                datos.plot(kind="pie", ax=ax2, autopct="%1.1f%%", startangle=90, colors=[COLOR1, COLOR3, COLOR2], wedgeprops={"edgecolor": "black"})
                for text in ax2.texts:
                    text.set_fontsize(5)  # Ajusta el tamaño de fuente

                ax2.set_title(f"Distribución de {columna}", fontsize=12)
                ax2.set_ylabel("")
                ax2.axis("equal")

                canvas2 = FigureCanvasTkAgg(fig2, master=graficos_frame)
                canvas2.get_tk_widget().pack(pady=10)
                canvas2.draw()

            elif tipo == "Continuo":
                # Convertir a numérico y eliminar valores no válidos
                datos = pd.to_numeric(self.datos_cargados[columna], errors="coerce").dropna()

                # Verificar si hay datos numéricos después de la conversión
                if datos.empty:
                    messagebox.showerror("Error", f"La columna '{columna}' no contiene datos numéricos válidos.")
                    return

                # Histograma
                fig = Figure(figsize=(5, 3), dpi=150)
                ax = fig.add_subplot(111)
                datos.plot(kind="hist", ax=ax, color=COLOR1, bins=20, edgecolor="black", alpha=0.75)
                ax.set_title(f"Distribución de {columna}", fontsize=12)
                ax.set_ylabel("Frecuencia", fontsize=10)
                ax.grid(axis="y", linestyle="--", alpha=0.6)
                ax.set_axisbelow(True)
                ax.tick_params(axis="both", rotation=15, labelsize=5)

                canvas = FigureCanvasTkAgg(fig, master=graficos_frame)
                canvas.get_tk_widget().pack(pady=10)
                canvas.draw()

                # Caja de Bigotes
                fig2 = Figure(figsize=(5, 3), dpi=150)
                ax2 = fig2.add_subplot(111)
                self.datos_cargados.boxplot(column=columna, ax=ax2, vert=False, patch_artist=True,
                                            boxprops=dict(facecolor=COLOR1, color="black"),
                                            whiskerprops=dict(color="black"),
                                            capprops=dict(color="black"),
                                            medianprops=dict(color="red", linewidth=2))
                ax2.set_title(f"Distribución de {columna}", fontsize=12)
                ax2.tick_params(axis="both", rotation=15, labelsize=5)

                canvas2 = FigureCanvasTkAgg(fig2, master=graficos_frame)
                canvas2.get_tk_widget().pack(pady=10)
                canvas2.draw()

        # Botón para generar el análisis
        generar_analisis_btn = tk.Button(seleccion_frame, text="Generar Análisis", command=lambda: generar_analisis(), background=COLOR1, foreground=COLOR3, font=("Arial", 12))
        generar_analisis_btn.grid(row=0, column=5, padx=10)

    def insetar_datos(self):
        """
        Cargar la ventana con el formulario de insertar datos.
        """
        if not self.archivo_cargado:
            messagebox.showwarning("Advertencia", "Debe cargar un archivo antes de insertar datos.")
            return

        self.limpiar_frame()
        insertar_frame = tk.Frame(self.main_frame, background=COLOR3)
        insertar_frame.pack(expand=True, fill="both", padx=20, pady=20)

        label = tk.Label(insertar_frame, text="Insertar Datos", font=("Arial", 24), background=COLOR3, foreground=COLOR1)
        label.pack(pady=10)

        # Crear un frame contenedor con scrollbar
        contenedor = tk.Frame(insertar_frame)
        contenedor.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = tk.Canvas(contenedor, background=COLOR3)
        scrollbar = tk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, background=COLOR3)

        # Configurar la región de desplazamiento
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Empaquetar el Canvas y la Scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Diccionario para almacenar las entradas de cada campo
        self.entradas = {}

        # Crear formulario dinámico basado en las columnas del DataFrame
        if self.datos_cargados is None or self.datos_cargados.empty:
            messagebox.showerror("Error", "No hay datos cargados para determinar la estructura.")
            return

        form_frame = tk.Frame(scroll_frame, background=COLOR3)
        form_frame.pack(pady=10, padx=50, fill="both")


        for columna in self.datos_cargados.columns:
            frame_campo = tk.Frame(form_frame, background=COLOR3)
            frame_campo.pack(pady=5, fill="x", expand="True")

            label = tk.Label(frame_campo, text=columna, background=COLOR3, foreground=COLOR1, font=("Arial", 12, "bold"))
            label.pack(side="left", padx=10)

            entrada = tk.Entry(frame_campo, font=("Arial", 12), bd=2, relief="solid", width=60)
            entrada.pack(side="left", fill="x", expand=True, padx=10, ipady=5)
            self.entradas[columna] = entrada  # Guardar la referencia

        # Frame para los botones
        btn_frame = tk.Frame(insertar_frame, background=COLOR3)
        btn_frame.pack(pady=15)

        # Botón para guardar los datos
        btn_guardar = tk.Button(btn_frame, text="Guardar", command=self.guardar_datos, background=COLOR1, foreground=COLOR3, font=("Arial", 12))
        btn_guardar.pack(side="left", padx=10)

        # Botón para exportar el archivo CSV con la data actualizada
        btn_exportar = tk.Button(btn_frame, text="Exportar CSV", command=self.exportar_csv, background=COLOR2, foreground=COLOR3, font=("Arial", 12))
        btn_exportar.pack(side="left", padx=10)

    def guardar_datos(self):
        """
        Guarda los datos ingresados y actualiza la tabla.
        """
        nueva_fila = {col: self.entradas[col].get() for col in self.datos_cargados.columns}

        # Convertir los valores numéricos si es necesario
        for col in self.datos_cargados.select_dtypes(include=['int64', 'float64']).columns:
            try:
                nueva_fila[col] = float(nueva_fila[col]) if '.' in nueva_fila[col] else int(nueva_fila[col])
            except ValueError:
                messagebox.showerror("Error", f"El valor en '{col}' debe ser numérico.")
                return

        # Agregar la nueva fila al DataFrame
        self.datos_cargados = pd.concat([self.datos_cargados, pd.DataFrame([nueva_fila])], ignore_index=True)

        # Actualizar la tabla en la interfaz
        self.mostrar_datos(self.datos_cargados)

        messagebox.showinfo("Éxito", "Datos insertados correctamente.")

    def exportar_csv(self):
        """
        Exporta el DataFrame actualizado a un archivo CSV.
        """
        if self.datos_cargados is None or self.datos_cargados.empty:
            messagebox.showerror("Error", "No hay datos para exportar.")
            return

        archivo_guardar = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv")],
            title="Guardar archivo CSV"
        )

        if archivo_guardar:
            self.datos_cargados.to_csv(archivo_guardar, index=False)
            messagebox.showinfo("Éxito", f"Datos exportados correctamente a:\n{archivo_guardar}")

    def acercade(self):
        """
        Cargar la ventana de "Acerca de".
        """
        self.limpiar_frame()

        # Frame para centrar el contenido
        acerca_frame = tk.Frame(self.main_frame, background=COLOR3)
        acerca_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Imagen representativa
        logo = tk.PhotoImage(file=LOGO, master=acerca_frame)
        logo_label = tk.Label(acerca_frame, image=logo, background=COLOR3)
        logo_label.image = logo
        logo_label.pack(pady=10)

        about_text = (
            "Minería de Datos v1.0\n"
            "2025\n"
            "Desarrollado por: Camilo Mercado\n"
            'Aplicación para análisis de datos extraídos de "Datos Abiertos"'
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