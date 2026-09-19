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