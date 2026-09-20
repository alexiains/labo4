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
        # Dimensiones
        marco_dim = tk.LabelFrame(self.root, text="Dimension")
        marco_dim.grid(row=0, column=0, padx=10, pady=5, rowspan=5)
        tk.Radiobutton(marco_dim, text="2 x 2", variable=self.tamano, value=2, command=self.actualizar_entradas).pack(anchor="w")
        tk.Radiobutton(marco_dim, text="3 x 3", variable=self.tamano, value=3, command=self.actualizar_entradas).pack(anchor="w")
        tk.Radiobutton(marco_dim, text="4 x 4", variable=self.tamano, value=4, command=self.actualizar_entradas).pack(anchor="w")

        # Etiquetas A, b, x
        for j in range(4):
            tk.Label(self.root, text=str(j)).grid(row=0, column=j+1)
        tk.Label(self.root, text="A").grid(row=0, column=0)
        tk.Label(self.root, text="b").grid(row=0, column=5)
        tk.Label(self.root, text="x").grid(row=0, column=6)

        # Entradas A
        self.entradas_A = [[tk.Entry(self.root, width=5) for j in range(4)] for i in range(4)]
        for i in range(4):
            for j in range(4):
                self.entradas_A[i][j].grid(row=i+1, column=j+1, padx=2, pady=2)

        # Entradas b
        self.entradas_b = [tk.Entry(self.root, width=5) for _ in range(4)]
        for i in range(4):
            self.entradas_b[i].grid(row=i+1, column=5)

        # Entradas x (resultado)
        self.entradas_x = [tk.Entry(self.root, width=5, state="readonly") for _ in range(4)]
        for i in range(4):
            self.entradas_x[i].grid(row=i+1, column=6)

        # Texto de ayuda
        texto = ("Ayuda: el sistema de ecuaciones permite calcular A.x = b\n"
                 "Se deben cargar los valores de A y b y luego,\n"
                 "al calcular, se obtienen los valores de x")
        tk.Label(self.root, text=texto, justify="left", fg="gray").grid(row=5, column=0, columnspan=7, sticky="w", padx=10)

        # Botones
        tk.Button(self.root, text="Borrar valores", command=self.borrar_todo).grid(row=6, column=1, pady=10)
        tk.Button(self.root, text="Calcular", command=self.calcular).grid(row=6, column=2)
        tk.Label(self.root, text="Determinante:").grid(row=6, column=3)
        self.det_label = tk.Label(self.root, text="---", width=10)
        self.det_label.grid(row=6, column=4)
        tk.Button(self.root, text="Calcular det.", command=self.calcular_determinante).grid(row=6, column=5)   

        self.actualizar_entradas()

    def actualizar_entradas(self):
        n=self.tamano.get()
        for i in range(4):
            for j in range(4):
                estado = "normal" if i < n and j < n else "disabled"
                self.entradas_A[i][j].config(state=estado)
            self.entradas_b[i].config(state="normal" if i < n else "disabled")
            self.entradas_x[i].config(state="normal" if i < n else "readonly")
            if i >= n:
                self.entradas_x[i].delete(0, tk.END)

    def borrar_todo(self):
        for fila in self.entradas_A:
            for entrada in fila:
                entrada.config(state="normal")
                entrada.delete(0, tk.END)
        for entrada in self.entradas_b + self.entradas_x:
            entrada.config(state="normal")
            entrada.delete(0, tk.END)
            if entrada in self.entradas_x:
                entrada.config(state="readonly")
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
                self.entradas_x[i].config(state="readonly")
