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
        