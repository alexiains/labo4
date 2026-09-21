# Alumnas: Insua Alexia y Barra Azul
# Laboratorio 4
# Repositorio: https://github.com/alexiains/labo4.git
import tkinter as tk
from tkinter import messagebox
import numpy as np

class CramerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Resolucion de sistemas de ecuaciones lineales mediante la Regla de Cramer")
        self.tamano = tk.IntVar(value=2)
        self.entradas_A = []
        self.entradas_b = []
        self.entradas_x = []

        self.crear_interfaz()

    def crear_interfaz(self):
        # Marco de Selección de Dimensión
        marco_dim = tk.LabelFrame(self.root, text="Dimensión")
        marco_dim.grid(row=0, column=0, rowspan=6, padx=10, pady=5, sticky="n")
        tk.Radiobutton(marco_dim, text="2 x 2", variable=self.tamano, value=2, command=self.actualizar_entradas).pack(anchor="w")
        tk.Radiobutton(marco_dim, text="3 x 3", variable=self.tamano, value=3, command=self.actualizar_entradas).pack(anchor="w")
        tk.Radiobutton(marco_dim, text="4 x 4", variable=self.tamano, value=4, command=self.actualizar_entradas).pack(anchor="w")

        # Encabezados superiores A, b, x
        tk.Label(self.root, text="A", font=("Arial", 10, "bold")).grid(row=0, column=2, columnspan=4, sticky="ew")
        tk.Label(self.root, text="b", font=("Arial", 10, "bold")).grid(row=0, column=6, sticky="ew")
        tk.Label(self.root, text="x", font=("Arial", 10, "bold")).grid(row=0, column=7, sticky="ew")

        # Números de columnas
        for j in range(4):
            tk.Label(self.root, text=str(j)).grid(row=1, column=j+2, sticky="ew")

        # Números de filas
        for i in range(4):
            tk.Label(self.root, text=str(i)).grid(row=i+2, column=1, sticky="e", padx=(5, 2))

        # Entradas de la Matriz A
        self.entradas_A = [[tk.Entry(self.root, width=5) for j in range(4)] for i in range(4)]
        for i in range(4):
            for j in range(4):
                self.entradas_A[i][j].grid(row=i+2, column=j+2, padx=3, pady=2)

        # Entradas del Vector b
        self.entradas_b = [tk.Entry(self.root, width=5) for _ in range(4)]
        for i in range(4):
            self.entradas_b[i].grid(row=i+2, column=6, padx=(15, 3), pady=2)

        # Entradas del Vector x (Resultado)
        self.entradas_x = [tk.Entry(self.root, width=5, state="disabled") for _ in range(4)]
        for i in range(4):
            self.entradas_x[i].grid(row=i+2, column=7, padx=(5, 3), pady=2)

        for col in range(2, 8):
            self.root.columnconfigure(col, weight=1)

        # Texto de ayuda
        texto = ("Ayuda: el sistema de ecuaciones permite calcular A.x = b\n"
                 "Se deben cargar los valores de A y b y luego,\n"
                 "al calcular, se obtienen los valores de x")
        tk.Label(self.root, text=texto, justify="left", fg="gray").grid(row=6, column=0, columnspan=8, sticky="w", padx=10, pady=(10, 0))

        # Botones
        tk.Button(self.root, text="Borrar valores", command=self.borrar_todo).grid(row=7, column=4, columnspan=2, pady=5)
        tk.Button(self.root, text="Calcular", command=self.calcular).grid(row=7, column=6, columnspan=2, pady=5)
        
        tk.Label(self.root, text="Determinante:").grid(row=8, column=4, columnspan=2, sticky="e")
        self.det_label = tk.Label(self.root, text="---", width=10, bg="white", relief="sunken")
        self.det_label.grid(row=8, column=6, padx=2)
        tk.Button(self.root, text="Calcular det.", command=self.calcular_determinante).grid(row=8, column=7, pady=5)

        self.actualizar_entradas()

    def actualizar_entradas(self):
        n=self.tamano.get()
        for i in range(4):
            for j in range(4):
                estado = "normal" if i < n and j < n else "disabled"
                self.entradas_A[i][j].config(state=estado)
            self.entradas_b[i].config(state="normal" if i < n else "disabled")
            self.entradas_x[i].config(state="disabled")
            if i >= n:
                self.entradas_x[i].config(state="normal")
                self.entradas_x[i].delete(0, tk.END)
                self.entradas_x[i].config(state="disabled")

    def borrar_todo(self):
        for fila in self.entradas_A:
            for entrada in fila:
                entrada.config(state="normal")
                entrada.delete(0, tk.END)
        for entrada in self.entradas_b + self.entradas_x:
            entrada.config(state="normal")
            entrada.delete(0, tk.END)
            if entrada in self.entradas_x:
                entrada.config(state="disabled")
        self.det_label.config(text="---")
        self.actualizar_entradas()

    def obtener_datos(self):
        n = self.tamano.get()
        A = np.zeros((n, n))
        b = np.zeros(n)
        for i in range(n):
            for j in range(n):
                try:
                    A[i, j] = float(self.entradas_A[i][j].get())
                except ValueError:
                    messagebox.showerror("Error", f"Valor inválido en A[{i+1},{j+1}]")
                    return None, None
            try:
                b[i] = float(self.entradas_b[i].get())
            except ValueError:
                messagebox.showerror("Error", f"Valor inválido en b[{i+1}]")
                return None, None
        return A, b

    def calcular_determinante(self):
        A, _ = self.obtener_datos()
        if A is not None:
            det = round(np.linalg.det(A), 4)
            self.det_label.config(text=str(det))

    def calcular(self):
        A, b = self.obtener_datos()
        if A is not None and b is not None:
            det_A = np.linalg.det(A)
            if np.isclose(det_A, 0):
                messagebox.showerror("Error", "El determinante de A es cero, el sistema no tiene solución única.")
                return
            n = self.tamano.get()
            x = np.zeros(n)
            for i in range(n):
                A_i = A.copy()
                A_i[:, i] = b
                x[i] = round(np.linalg.det(A_i) / det_A, 4)
            for i in range(n):
                self.entradas_x[i].config(state="normal")
                self.entradas_x[i].delete(0, tk.END)
                self.entradas_x[i].insert(0, str(x[i]))
                self.entradas_x[i].config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = CramerGUI(root)
    root.mainloop()