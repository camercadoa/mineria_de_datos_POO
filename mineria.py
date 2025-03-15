import tkinter as tk

class MineriaDeDatosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minería de Datos v1.0")
        self.setup_ui()

    #  Interfaz de usuario
    def setup_ui(self):

        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = MineriaDeDatosApp(root)
    root.mainloop()