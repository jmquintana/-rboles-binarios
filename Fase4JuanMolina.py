import tkinter as tk
from tkinter import messagebox
import datetime

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha   = None


class ArbolBST:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo_actual, valor):
        if valor < nodo_actual.valor:
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = Nodo(valor)
            else:
                self._insertar_recursivo(nodo_actual.izquierda, valor)
        elif valor > nodo_actual.valor:
            if nodo_actual.derecha is None:
                nodo_actual.derecha = Nodo(valor)
            else:
                self._insertar_recursivo(nodo_actual.derecha, valor)
  
    def preorden(self, nodo, resultado):
        if nodo:
            resultado.append(nodo.valor)
            self.preorden(nodo.izquierda, resultado)
            self.preorden(nodo.derecha,   resultado)

    def inorden(self, nodo, resultado):
        if nodo:
            self.inorden(nodo.izquierda, resultado)
            resultado.append(nodo.valor)
            self.inorden(nodo.derecha,   resultado)

    def posorden(self, nodo, resultado):
        if nodo:
            self.posorden(nodo.izquierda, resultado)
            self.posorden(nodo.derecha,   resultado)
            resultado.append(nodo.valor)

    def buscar(self, valor):
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, nodo, valor):
        if nodo is None:
            return False
        if valor == nodo.valor:
            return True
        elif valor < nodo.valor:
            return self._buscar_recursivo(nodo.izquierda, valor)
        else:
            return self._buscar_recursivo(nodo.derecha, valor)


class VentanaLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Fase4JuanMolina")
        self.root.resizable(False, False)
        self._centrar_ventana(380, 260)

        tk.Label(root, text="Aplicación: Arboles Binarios",
                 font=("Arial", 12, "bold")).pack(pady=(25, 4))


        tk.Label(root, text="Estudiante: Juan Molina",
                 font=("Arial", 11)).pack(pady=4)


        fecha = datetime.date.today().strftime("%d/%m/%Y")
        tk.Label(root, text=f"Fecha: {fecha}",
                 font=("Arial", 11)).pack(pady=4)


        tk.Label(root, text="Contraseña:",
                 font=("Arial", 11)).pack(pady=(15, 2))

        self.entrada_clave = tk.Entry(root, show="*", width=20,
                                      font=("Arial", 11))
        self.entrada_clave.pack()
        self.entrada_clave.bind("<Return>", lambda e: self._verificar())

        tk.Button(root, text="Ingresar", width=12,
                  command=self._verificar).pack(pady=18)

    def _verificar(self):
        if self.entrada_clave.get() == "ARBOL":
            self.root.destroy()
            root2 = tk.Tk()
            VentanaPrincipal(root2)
            root2.mainloop()
        else:
            messagebox.showerror("Error", "Contraseña incorrecta")
            self.entrada_clave.delete(0, tk.END)

    def _centrar_ventana(self, ancho, alto):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - ancho) // 2
        y = (self.root.winfo_screenheight() - alto)  // 2
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")


class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Árbol Binario de Búsqueda")
        self.root.resizable(True, True)
        self._centrar_ventana(900, 620)

        self.arbol = ArbolBST()
        self._construir_interfaz()

    def _construir_interfaz(self):

        barra = tk.Frame(self.root)
        barra.pack(pady=8)

        self.entrada = tk.Entry(barra, width=10, font=("Arial", 11))
        self.entrada.pack(side=tk.LEFT, padx=4)
        self.entrada.bind("<Return>", lambda e: self._agregar())

        tk.Button(barra, text="Agregar Nodo",
                  command=self._agregar).pack(side=tk.LEFT, padx=2)
        tk.Button(barra, text="Buscar Nodo",
                  command=self._buscar).pack(side=tk.LEFT, padx=2)
        tk.Button(barra, text="Limpiar",
                  command=self._limpiar).pack(side=tk.LEFT, padx=2)
        tk.Button(barra, text="Salir",
                  command=self.root.destroy).pack(side=tk.LEFT, padx=2)

        self.canvas = tk.Canvas(self.root, bg="white",
                                relief=tk.SUNKEN, bd=1)
        self.canvas.pack(fill=tk.BOTH, expand=True,
                         padx=10, pady=(0, 5))

        barra_inf = tk.Frame(self.root)
        barra_inf.pack(fill=tk.X, padx=10, pady=(0, 10))

        tk.Label(barra_inf, text="Preorden",
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        self.txt_pre = tk.Entry(barra_inf, width=22,
                                font=("Arial", 9), state="readonly")
        self.txt_pre.pack(side=tk.LEFT, padx=(2, 20))

        tk.Label(barra_inf, text="Inorden",
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        self.txt_ino = tk.Entry(barra_inf, width=22,
                                font=("Arial", 9), state="readonly")
        self.txt_ino.pack(side=tk.LEFT, padx=(2, 20))

        tk.Label(barra_inf, text="Posorden",
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        self.txt_pos = tk.Entry(barra_inf, width=22,
                                font=("Arial", 9), state="readonly")
        self.txt_pos.pack(side=tk.LEFT, padx=2)

    def _agregar(self):
        texto = self.entrada.get().strip()

        try:
            valor = int(texto)
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número entero")
            self.entrada.delete(0, tk.END)
            return

        nivel = self._nivel_nuevo(valor)
        if nivel > 4:
            messagebox.showerror("Error", "No puede exceder 4 niveles")
            self.entrada.delete(0, tk.END)
            return

        self.arbol.insertar(valor)
        self.entrada.delete(0, tk.END)
        self._actualizar_todo()

    def _nivel_nuevo(self, valor):
        nodo  = self.arbol.raiz
        nivel = 1
        while nodo is not None:
            if valor == nodo.valor:
                return nivel
            elif valor < nodo.valor:
                nodo = nodo.izquierda
            else:
                nodo = nodo.derecha
            nivel += 1
        return nivel

    def _buscar(self):
        texto = self.entrada.get().strip()
        try:
            valor = int(texto)
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número entero")
            self.entrada.delete(0, tk.END)
            return

        if self.arbol.buscar(valor):
            messagebox.showinfo("Buscar Nodo",
                                f"Valor {valor} encontrado en el árbol ✓")
        else:
            messagebox.showinfo("Buscar Nodo",
                                f"Valor {valor} no existe en el árbol")
        self.entrada.delete(0, tk.END)

    def _limpiar(self):
        self.arbol = ArbolBST()
        self.canvas.delete("all")
        self._escribir_entry(self.txt_pre, "")
        self._escribir_entry(self.txt_ino, "")
        self._escribir_entry(self.txt_pos, "")

    def _actualizar_todo(self):
        self.canvas.delete("all")
        self.canvas.update()

        ancho    = self.canvas.winfo_width()
        cx       = ancho // 2
        radio    = 22
        origen_y = 45

        if self.arbol.raiz:
            self._dibujar_nodo(self.arbol.raiz,
                               cx, origen_y, ancho // 4, radio)

        pre, ino, pos = [], [], []
        self.arbol.preorden(self.arbol.raiz,  pre)
        self.arbol.inorden(self.arbol.raiz,   ino)
        self.arbol.posorden(self.arbol.raiz,  pos)

        self._escribir_entry(self.txt_pre, " ".join(map(str, pre)))
        self._escribir_entry(self.txt_ino, " ".join(map(str, ino)))
        self._escribir_entry(self.txt_pos, " ".join(map(str, pos)))

    def _dibujar_nodo(self, nodo, x, y, offset, radio):
        if nodo is None:
            return

        if nodo.izquierda:
            xi = x - offset
            yi = y + 90
            self.canvas.create_line(x, y + radio, xi, yi - radio, width=1.5)
            self._dibujar_nodo(nodo.izquierda, xi, yi, offset // 2, radio)

        if nodo.derecha:
            xd = x + offset
            yd = y + 90
            self.canvas.create_line(x, y + radio, xd, yd - radio, width=1.5)
            self._dibujar_nodo(nodo.derecha, xd, yd, offset // 2, radio)

        self.canvas.create_oval(x - radio, y - radio,
                                x + radio, y + radio,
                                fill="white", outline="black", width=1.5)
        self.canvas.create_text(x, y, text=str(nodo.valor),
                                font=("Arial", 10))

    def _escribir_entry(self, entry, texto):
        entry.config(state="normal")
        entry.delete(0, tk.END)
        entry.insert(0, texto)
        entry.config(state="readonly")

    def _centrar_ventana(self, ancho, alto):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - ancho) // 2
        y = (self.root.winfo_screenheight() - alto)  // 2
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")


if __name__ == "__main__":
    root = tk.Tk()
    VentanaLogin(root)
    root.mainloop()