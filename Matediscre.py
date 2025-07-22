import tkinter as tk
from tkinter import simpledialog, messagebox
import math
import heapq
from collections import deque
import random

# Definición de constantes para colores
LIGHT_BLUE = "#ADD8E6"
DARK_BLUE = "#323296"
BLUE = "#6464FF"
GREEN = "#64FF64"
ORANGE = "#FFA500"
PURPLE = "#B000FF"
RED = "#FF6464"
DARK_RED = "#8B0000"
BACKGROUND_COLOR = "#f0f8ff"  # Azul agua claro
BUTTON_COLOR = "#5f9ea0"       # Azul cadete
ACCENT_COLOR = "#ff7f50"       # Coral

# Clase para representar un grafo con sus propiedades
class Grafo:
    def __init__(self, nombre, nodos, aristas, posiciones, cromatico):
        # Inicialización de un objeto grafo con nombre, nodos, aristas, posiciones y número cromático
        self.nombre = nombre
        self.nodos = nodos
        self.aristas = aristas
        self.posiciones = posiciones
        self.cromatico = cromatico

class PantallaBienvenida:
    def __init__(self, root):
        self.root = root
        self.root.title("Herramienta Didáctica de Grafos")
        self.root.geometry("1000x800")
        self.root.configure(bg=BACKGROUND_COLOR)

        # Marco principal que ocupa toda la ventana y centra su contenido
        self.frame = tk.Frame(root, bg=BACKGROUND_COLOR)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Frame contenedor para todo el contenido, centrado
        contenido = tk.Frame(self.frame, bg=BACKGROUND_COLOR)
        contenido.place(relx=0.5, rely=0.5, anchor="center")  # centro absoluto

        # Universidad y asignatura
        universidad = tk.Label(contenido, text="Universidad Central del Ecuador", font=("Cooper Black", 18), bg=BACKGROUND_COLOR, fg="black")
        universidad.pack(pady=(10, 0), fill=tk.X)

        asignatura = tk.Label(contenido, text="Matemáticas Discretas", font=("Cooper Black", 16), bg=BACKGROUND_COLOR, fg="black")
        asignatura.pack(pady=(0, 20), fill=tk.X)

        # Título de la aplicación
        titulo = tk.Label(contenido, text="Herramienta Didáctica de Grafos", font=("Cooper Black", 28, "bold"), bg=BACKGROUND_COLOR, fg="black")
        titulo.pack(pady=20, fill=tk.X)

        # Texto explicativo
        texto = (
            "Aprende sobre diferentes algoritmos y conceptos fundamentales de grafos:\n\n"
            "Selecciona una opción para comenzar:"
        )
        explicacion = tk.Label(contenido, text=texto, justify="center", font=("Cooper Black", 16), bg=BACKGROUND_COLOR, fg="black", wraplength=800)
        explicacion.pack(pady=30, padx=20, fill=tk.X)

        # Marco principal para los botones
        frame_botones = tk.Frame(contenido, bg=BACKGROUND_COLOR)
        frame_botones.pack(pady=30)

        # Submarcos para colocar botones a la izquierda y a la derecha
        frame_izquierda = tk.Frame(frame_botones, bg=BACKGROUND_COLOR)
        frame_izquierda.pack(side=tk.LEFT, padx=50)

        frame_derecha = tk.Frame(frame_botones, bg=BACKGROUND_COLOR)
        frame_derecha.pack(side=tk.RIGHT, padx=50)

        btn_style = {
            "font": ("Cooper Black", 14, "bold"),
            "width": 25,
            "height": 2,
            "bd": 2,
            "relief": "solid",
            "fg": "black",
            "highlightthickness": 0,
            "highlightbackground": "black"
        }

        # Botones a la izquierda
        btn_coloreado = tk.Button(frame_izquierda, text="▶️ Coloreado de Grafos", bg=BUTTON_COLOR, **btn_style, command=self.abrir_coloreado)
        btn_coloreado.pack(pady=10)

        btn_bfs_dfs = tk.Button(frame_izquierda, text="▶️ Algoritmo de BFS/DFS", bg=ACCENT_COLOR, **btn_style, command=self.abrir_bfs_dfs)
        btn_bfs_dfs.pack(pady=10)

        # Botones a la derecha
        btn_dijkstra = tk.Button(frame_derecha, text="▶️ Algoritmo de Dijkstra", bg=ORANGE, **btn_style, command=self.abrir_dijkstra)
        btn_dijkstra.pack(pady=10)

        btn_dirigidos = tk.Button(frame_derecha, text="▶️ Grafos Dirigidos", bg=PURPLE, **btn_style, command=self.abrir_dirigidos)
        btn_dirigidos.pack(pady=10)

        # Créditos de la aplicación, pegado abajo pero centrado horizontalmente
        creditos = tk.Label(self.frame, text="© 2025 - Herramienta Didáctica de Grafos", font=("Cooper Black", 10), bg=BACKGROUND_COLOR, fg="black")
        creditos.pack(side=tk.BOTTOM, pady=10, fill=tk.X)


    # Métodos para abrir las diferentes herramientas
    def abrir_coloreado(self):
        self.frame.destroy()
        ColoringApp(self.root, self.volver_al_menu)

    def abrir_bfs_dfs(self):
        self.frame.destroy()
        BFSDFSApp(self.root, self.volver_al_menu)

    def abrir_dijkstra(self):
        self.frame.destroy()
        DijkstraApp(self.root, self.volver_al_menu)
        
    def abrir_dirigidos(self):
        self.frame.destroy()
        DirectedGraphApp(self.root, self.volver_al_menu)

    # Volver al menú principal
    def volver_al_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root)

import tkinter as tk
from tkinter import messagebox
import math

# Constantes de color (ajusta según tu código)
BACKGROUND_COLOR = "#F0F0F0"
BLUE = "#3399FF"
PURPLE = "#AA66CC"
ORANGE = "#FF9933"
GREEN = "#66CC66"
RED = "#FF6666"
DARK_RED = "#990000"

class ColoringApp:
    COLORES = ["#FF9999", "#99CCFF", "#99FF99", "#FFFF99", "#FF99FF", "#FFCC99", "#99FFFF"]

    def __init__(self, root, volver_callback):
        self.root = root
        self.root.title("Coloreado de Grafos con Validación")
        self.volver_callback = volver_callback

        self.canvas = tk.Canvas(root, width=700, height=500, bg="white", highlightthickness=1, highlightbackground="black")
        self.canvas.pack(padx=20, pady=20)

        self.frame_botones = tk.Frame(root, bg=BACKGROUND_COLOR, padx=10, pady=10)
        self.frame_botones.pack(fill=tk.X)

        botones_centrados = tk.Frame(self.frame_botones, bg=BACKGROUND_COLOR)
        botones_centrados.pack(anchor="center")

        button_style = {"font": ("Britannic Bold", 11, "bold"), "bd": 0, "fg": "black", "width": 15, "height": 2}

        self.btn_colorear = tk.Button(botones_centrados, text="Colorear", bg=ORANGE, **button_style, command=self.modo_colorear)
        self.btn_colorear.pack(side=tk.LEFT, padx=6)

        self.btn_autocolor = tk.Button(botones_centrados, text="Auto-colorear", bg=GREEN, **button_style, command=self.auto_colorear)
        self.btn_autocolor.pack(side=tk.LEFT, padx=6)

        self.btn_verificar = tk.Button(botones_centrados, text="Verificar Coloreado", bg="#ADD8E6", **button_style, command=self.verificar_coloreo)
        self.btn_verificar.pack(side=tk.LEFT, padx=6)

        self.btn_limpiar = tk.Button(botones_centrados, text="Limpiar Todo", bg=RED, **button_style, command=self.limpiar_todo)
        self.btn_limpiar.pack(side=tk.LEFT, padx=6)

        self.btn_menu = tk.Button(botones_centrados, text="Menú Principal", bg=DARK_RED, **button_style, command=self.volver_callback)
        self.btn_menu.pack(side=tk.LEFT, padx=6)

        self.frame_presets = tk.Frame(root, bg=BACKGROUND_COLOR)
        self.frame_presets.pack(fill=tk.X, padx=10, pady=5)

        presets_centrado = tk.Frame(self.frame_presets, bg=BACKGROUND_COLOR)
        presets_centrado.pack(anchor="center")

        tk.Label(presets_centrado, text="Grafos:", font=("Britannic Bold", 11), bg=BACKGROUND_COLOR).pack(side=tk.LEFT, padx=(10, 5))

        self.btn_facil = tk.Button(presets_centrado, text="Fácil", bg="#90EE90", fg="black", width=6,
                                   command=lambda: self.cargar_grafo_predefinido("facil"))
        self.btn_facil.pack(side=tk.LEFT, padx=6)

        self.btn_normal = tk.Button(presets_centrado, text="Normal", bg="#FFD700", fg="black", width=6,
                                    command=lambda: self.cargar_grafo_predefinido("normal"))
        self.btn_normal.pack(side=tk.LEFT, padx=6)

        self.btn_dificil = tk.Button(presets_centrado, text="Dificil", bg="#FF6347", fg="black", width=6,
                                     command=lambda: self.cargar_grafo_predefinido("dificil"))
        self.btn_dificil.pack(side=tk.LEFT, padx=6)

        self.info = tk.Label(root, text="Clic izquierdo para crear/mover nodos o arrastrar colores. Clic derecho para crear aristas.",
                             font=("Britannic Bold", 12), bg=BACKGROUND_COLOR)
        self.info.pack(fill=tk.X)

        self.nodos = []
        self.aristas = []
        self.adyacencia = {}
        self.nodo_seleccionado_arista = None
        self.contador = 1

        # Variables para mover nodo
        self.nodo_en_movimiento = None
        self.offset_x = 0
        self.offset_y = 0

        # Variables para arrastrar color
        self.color_actual = None
        self.drag_rect = None
        self.arrastrando_color = False

        self.crear_paleta_colores()

        # Eventos
        self.canvas.bind("<Button-1>", self.click_izquierdo_canvas)
        self.canvas.bind("<B1-Motion>", self.mover_o_arrastrar)
        self.canvas.bind("<ButtonRelease-1>", self.soltar)
        self.canvas.bind("<Button-3>", self.click_derecho_canvas)

    def crear_paleta_colores(self):
        self.color_circulos = {}
        x, y = 50, 450
        for color in self.COLORES:
            circ = self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=color, outline="black", width=2)
            self.color_circulos[circ] = color
            x += 60

    def modo_colorear(self):
        pass  # Si quieres agregar estados o botones para modos, puedes hacerlo aquí

    def click_izquierdo_canvas(self, event):
        color = self.obtener_color_paleta(event.x, event.y)
        if color:
            # Empezar a arrastrar color
            self.color_actual = color
            self.drag_rect = self.canvas.create_oval(event.x-10, event.y-10, event.x+10, event.y+10, fill=color, outline="black")
            self.arrastrando_color = True
            self.nodo_en_movimiento = None
            self.info.config(text="Arrastra el color sobre un nodo para colorearlo.")
            return

        nodo = self.obtener_nodo_en_pos(event.x, event.y)
        if nodo:
            # Iniciar movimiento de nodo
            self.nodo_en_movimiento = nodo
            self.offset_x = event.x - nodo["x"]
            self.offset_y = event.y - nodo["y"]
            self.arrastrando_color = False
            self.info.config(text=f"Mueve el nodo {nodo['nombre']} con el mouse.")
        else:
            # Crear nuevo nodo
            if not self.esta_en_paleta(event.x, event.y):
                self.agregar_nodo(event.x, event.y)
                self.info.config(text="Clic izquierdo para crear/mover nodos o arrastrar colores. Clic derecho para crear aristas.")

    def mover_o_arrastrar(self, event):
        if self.arrastrando_color and self.drag_rect:
            self.canvas.coords(self.drag_rect, event.x-10, event.y-10, event.x+10, event.y+10)
        elif self.nodo_en_movimiento:
            nuevo_x = event.x - self.offset_x
            nuevo_y = event.y - self.offset_y

            self.nodo_en_movimiento["x"] = nuevo_x
            self.nodo_en_movimiento["y"] = nuevo_y

            radio = 20
            self.canvas.coords(self.nodo_en_movimiento["circulo"],
                               nuevo_x - radio, nuevo_y - radio,
                               nuevo_x + radio, nuevo_y + radio)
            self.canvas.coords(self.nodo_en_movimiento["texto"], nuevo_x, nuevo_y)

            # Actualizar aristas conectadas
            for arista in self.aristas:
                if arista["nodo1"] == self.nodo_en_movimiento or arista["nodo2"] == self.nodo_en_movimiento:
                    x1 = arista["nodo1"]["x"]
                    y1 = arista["nodo1"]["y"]
                    x2 = arista["nodo2"]["x"]
                    y2 = arista["nodo2"]["y"]
                    self.canvas.coords(arista["linea"], x1, y1, x2, y2)

    def soltar(self, event):
        if self.arrastrando_color and self.drag_rect:
            nodo = self.obtener_nodo_en_pos(event.x, event.y)
            if nodo:
                conflicto = False
                for vecino_nombre in self.adyacencia[nodo["nombre"]]:
                    vecino = self.obtener_nodo_por_nombre(vecino_nombre)
                    if vecino and vecino["color"] == self.color_actual:
                        conflicto = True
                        break
                
                if conflicto:
                    messagebox.showerror("Color inválido",
                                         f"No puedes usar este color.\n"
                                         f"{nodo['nombre']} es adyacente a un nodo con el mismo color.")
                else:
                    nodo["color"] = self.color_actual
                    self.canvas.itemconfig(nodo["circulo"], fill=self.color_actual)

            self.canvas.delete(self.drag_rect)
            self.drag_rect = None
            self.color_actual = None
            self.arrastrando_color = False
            self.info.config(text="Clic izquierdo para crear/mover nodos o arrastrar colores. Clic derecho para crear aristas.")

        if self.nodo_en_movimiento:
            self.nodo_en_movimiento = None
            self.info.config(text="Clic izquierdo para crear/mover nodos o arrastrar colores. Clic derecho para crear aristas.")

    def click_derecho_canvas(self, event):
        nodo = self.obtener_nodo_en_pos(event.x, event.y)
        if nodo:
            if self.nodo_seleccionado_arista is None:
                self.nodo_seleccionado_arista = nodo
                self.canvas.itemconfig(nodo["circulo"], outline="orange", width=3)
                self.info.config(text=f"Nodo {nodo['nombre']} seleccionado como origen de arista.")
            else:
                if nodo != self.nodo_seleccionado_arista:
                    self.agregar_arista(self.nodo_seleccionado_arista, nodo)
                self.canvas.itemconfig(self.nodo_seleccionado_arista["circulo"], outline="black", width=2)
                self.nodo_seleccionado_arista = None
                self.info.config(text="Clic izquierdo para crear/mover nodos o arrastrar colores. Clic derecho para crear aristas.")

    def esta_en_paleta(self, x, y):
        return 430 <= y <= 470

    def obtener_color_paleta(self, x, y):
        for circ, color in self.color_circulos.items():
            coords = self.canvas.coords(circ)
            cx = (coords[0] + coords[2]) / 2
            cy = (coords[1] + coords[3]) / 2
            radio = (coords[2] - coords[0]) / 2
            if (x - cx) ** 2 + (y - cy) ** 2 <= radio ** 2:
                return color
        return None

    def agregar_nodo(self, x, y):
        nombre = f"N{self.contador}"
        self.contador += 1
        
        circulo = self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="white", outline="black", width=2)
        texto = self.canvas.create_text(x, y, text=nombre, font=("Cooper Black", 12, "bold"))
        
        nodo = {
            "x": x,
            "y": y,
            "nombre": nombre,
            "color": "white",
            "circulo": circulo,
            "texto": texto
        }
        self.nodos.append(nodo)
        self.adyacencia[nombre] = []
        self.info.config(text=f"Nodo {nombre} agregado en ({int(x)},{int(y)})")

    def agregar_arista(self, n1, n2):
        if n2["nombre"] not in self.adyacencia[n1["nombre"]]:
            linea = self.canvas.create_line(n1["x"], n1["y"], n2["x"], n2["y"], width=2)
            self.aristas.append({
                "nodo1": n1,
                "nodo2": n2,
                "linea": linea
            })
            self.adyacencia[n1["nombre"]].append(n2["nombre"])
            self.adyacencia[n2["nombre"]].append(n1["nombre"])
            self.info.config(text=f"Arista creada: {n1['nombre']} ↔ {n2['nombre']}")
        else:
            messagebox.showinfo("Arista duplicada", "Esta arista ya existe")

    def obtener_nodo_en_pos(self, x, y):
        for nodo in self.nodos:
            distancia = math.sqrt((nodo["x"] - x) ** 2 + (nodo["y"] - y) ** 2)
            if distancia <= 20:
                return nodo
        return None

    def obtener_nodo_por_nombre(self, nombre):
        for nodo in self.nodos:
            if nodo["nombre"] == nombre:
                return nodo
        return None

    # Aquí puedes incluir los métodos de coloreo, verificar_coloreo, auto_colorear y cargar_grafo_predefinido que ya tenías, sin modificaciones

    def verificar_coloreo(self):
        errores = []
        colores_usados = set()
        
        for nodo in self.nodos:
            color = nodo["color"]
            colores_usados.add(color)
            
            for vecino_nombre in self.adyacencia[nodo["nombre"]]:
                vecino = self.obtener_nodo_por_nombre(vecino_nombre)
                if vecino and vecino["color"] == color and color != "white":
                    errores.append(f"{nodo['nombre']} y {vecino['nombre']} tienen el mismo color ({color}).")
        
        colores_usados = {c for c in colores_usados if c != "white"}
        num_colores = len(colores_usados)
        
        minimo_estimo = self.coloreo_goloso()
        
        if errores:
            mensaje = "Error en el coloreado:\n" + "\n".join(errores)
            messagebox.showerror("Coloreado Incorrecto", mensaje)
        elif "white" in [nodo["color"] for nodo in self.nodos]:
            messagebox.showwarning("Coloreado Incompleto", "Algunos nodos aún no están coloreados")
        else:
            if num_colores == minimo_estimo:
                messagebox.showinfo("¡Perfecto!", f"✅ ¡Coloreado correcto y mínimo con {num_colores} colores!")
            else:
                messagebox.showinfo("Correcto pero no óptimo",
                                    f"✅ El coloreado es válido, pero puedes usar menos colores.\n"
                                    f"Usaste {num_colores}, mínimo estimado: {minimo_estimo}")

    def coloreo_goloso(self):
        asignacion = {}
        nodos_ordenados = sorted(self.adyacencia.keys(), key=lambda n: len(self.adyacencia[n]), reverse=True)
        
        for nodo in nodos_ordenados:
            usado = set()
            for vecino in self.adyacencia[nodo]:
                if vecino in asignacion:
                    usado.add(asignacion[vecino])
            color = 0
            while color in usado:
                color += 1
            asignacion[nodo] = color
        
        return max(asignacion.values()) + 1 if asignacion else 0

    def auto_colorear(self):
        asignacion = {}
        nodos_ordenados = sorted(self.adyacencia.keys(), key=lambda n: len(self.adyacencia[n]), reverse=True)
        
        for nodo in nodos_ordenados:
            usado = set()
            for vecino in self.adyacencia[nodo]:
                if vecino in asignacion:
                    usado.add(asignacion[vecino])
            color_idx = 0
            while color_idx < len(self.COLORES):
                if self.COLORES[color_idx] not in usado:
                    asignacion[nodo] = self.COLORES[color_idx]
                    break
                color_idx += 1
        
        for nombre, color in asignacion.items():
            nodo = self.obtener_nodo_por_nombre(nombre)
            if nodo:
                nodo["color"] = color
                self.canvas.itemconfig(nodo["circulo"], fill=color)
        
        self.info.config(text="Coloreado automático aplicado con éxito")

    def cargar_grafo_predefinido(self, dificultad):
        self.limpiar_todo()
        
        if dificultad == "facil":
            self.agregar_nodo(200, 200)
            self.agregar_nodo(400, 200)
            self.agregar_nodo(300, 400)
            n1 = self.obtener_nodo_por_nombre("N1")
            n2 = self.obtener_nodo_por_nombre("N2")
            n3 = self.obtener_nodo_por_nombre("N3")
            self.agregar_arista(n1, n2)
            self.agregar_arista(n2, n3)
            self.agregar_arista(n3, n1)
            self.info.config(text="Grafo fácil cargado: Triángulo")
            
        elif dificultad == "normal":
            for i in range(5):
                x = 200 + 150 * math.cos(2 * math.pi * i / 5)
                y = 250 + 150 * math.sin(2 * math.pi * i / 5)
                self.agregar_nodo(x, y)
            
            for i in range(1, 6):
                n1 = self.obtener_nodo_por_nombre(f"N{i}")
                n2 = self.obtener_nodo_por_nombre(f"N{(i % 5) + 1}")
                self.agregar_arista(n1, n2)
            
            n1 = self.obtener_nodo_por_nombre("N1")
            n3 = self.obtener_nodo_por_nombre("N3")
            self.agregar_arista(n1, n3)
            self.info.config(text="Grafo normal cargado: Pentágono con diagonales")
            
        elif dificultad == "dificil":
            for i in range(5):
                x = 200 + 150 * math.cos(2 * math.pi * i / 5)
                y = 250 + 150 * math.sin(2 * math.pi * i / 5)
                self.agregar_nodo(x, y)
            
            nodos = [self.obtener_nodo_por_nombre(f"N{i+1}") for i in range(5)]
            for i in range(len(nodos)):
                for j in range(i+1, len(nodos)):
                    self.agregar_arista(nodos[i], nodos[j])
            
            self.info.config(text="Grafo difícil cargado: Grafo completo K5")

    def limpiar_todo(self):
        self.canvas.delete("all")
        self.nodos = []
        self.aristas = []
        self.adyacencia = {}
        self.contador = 1
        self.nodo_seleccionado_arista = None
        self.color_actual = None
        self.drag_rect = None
        self.arrastrando_color = False
        self.nodo_en_movimiento = None
        self.crear_paleta_colores()
        self.info.config(text="Lienzo limpiado. Clic izquierdo para crear/mover nodos o arrastrar colores. Clic derecho para crear aristas.")


class BFSDFSApp:
    def __init__(self, root, volver_callback):
        self.root = root
        self.root.title("BFS/DFS")
        self.volver_callback = volver_callback
        self.nodos = []
        self.aristas = []
        self.aristas_regreso = []

        self.canvas = tk.Canvas(root, width=700, height=500, bg="white",
                                highlightthickness=1, highlightbackground="black")
        self.canvas.pack(padx=20, pady=20)

        # Frame principal para botones (fila 1)
        self.frame_botones = tk.Frame(root, bg=BACKGROUND_COLOR, padx=10, pady=10)
        self.frame_botones.pack(fill=tk.X)

        # Sub-frame centrado para botones principales (BFS, DFS, Limpiar, Menú)
        botones_principales = tk.Frame(self.frame_botones, bg=BACKGROUND_COLOR)
        botones_principales.pack(anchor="center")

        button_style = {"font": ("Britannic Bold", 11, "bold"),
                        "bd": 0, "fg": "black", "width": 15, "height": 2}

        self.btn_bfs = tk.Button(botones_principales, text="BFS", bg=GREEN, **button_style, command=self.ejecutar_bfs)
        self.btn_bfs.pack(side=tk.LEFT, padx=6)

        self.btn_dfs = tk.Button(botones_principales, text="DFS", bg=BLUE, **button_style, command=self.ejecutar_dfs)
        self.btn_dfs.pack(side=tk.LEFT, padx=6)

        self.btn_limpiar = tk.Button(botones_principales, text="Limpiar", bg=PURPLE, **button_style, command=self.limpiar)
        self.btn_limpiar.pack(side=tk.LEFT, padx=6)

        self.btn_menu = tk.Button(botones_principales, text="Menú Principal", bg=DARK_RED, **button_style,
                                  command=self.volver_callback)
        self.btn_menu.pack(side=tk.LEFT, padx=6)

        # Frame para presets (fila 2) centrado
        self.frame_presets = tk.Frame(root, bg=BACKGROUND_COLOR, padx=10, pady=5)
        self.frame_presets.pack(fill=tk.X)

        presets_centrados = tk.Frame(self.frame_presets, bg=BACKGROUND_COLOR)
        presets_centrados.pack(anchor="center")

        tk.Label(presets_centrados, text="Grafos:", font=("Britannic Bold", 11), bg=BACKGROUND_COLOR).pack(side=tk.LEFT, padx=(0, 10))

        self.btn_facil = tk.Button(presets_centrados, text="Fácil", bg="#90EE90", fg="black", width=15,
                                  command=lambda: self.cargar_grafo_predefinido("facil"))
        self.btn_facil.pack(side=tk.LEFT, padx=6)

        self.btn_normal = tk.Button(presets_centrados, text="Normal", bg="#FFD700", fg="black", width=15,
                                   command=lambda: self.cargar_grafo_predefinido("normal"))
        self.btn_normal.pack(side=tk.LEFT, padx=6)

        self.btn_dificil = tk.Button(presets_centrados, text="Difícil", bg="#FF6347", fg="black", width=15,
                                    command=lambda: self.cargar_grafo_predefinido("dificil"))
        self.btn_dificil.pack(side=tk.LEFT, padx=6)

        # Etiqueta de información (fila 3)
        self.info = tk.Label(root,
                             text="Clic izquierdo para crear/mover nodos. Clic derecho para crear aristas.",
                             font=("Britannic Bold", 12), bg=BACKGROUND_COLOR)
        self.info.pack(fill=tk.X)

        # Eventos y variables
        self.canvas.bind("<Button-1>", self.click_canvas)
        self.canvas.bind("<Button-3>", self.click_derecho_canvas)
        self.canvas.bind("<B1-Motion>", self.mover_nodo)
        self.nodo_seleccionado = None
        self.offset = (0, 0)

        self.res_bfs = {}
        self.res_dfs = []
        self.modo = "add"
        self.dibujar_grafo()
    def cargar_grafo_predefinido(self, dificultad):
        """Carga un grafo predefinido según la dificultad seleccionada"""
        self.limpiar()
        
        if dificultad == "facil":
            # Grafo simple (línea)
            self.nodos = [
                {"x": 200, "y": 250, "nombre": "A"},
                {"x": 350, "y": 250, "nombre": "B"},
                {"x": 500, "y": 250, "nombre": "C"}
            ]
            self.aristas = [
                (self.nodos[0], self.nodos[1]),
                (self.nodos[1], self.nodos[2])
            ]
            self.info.config(text="Grafo fácil cargado: Línea de 3 nodos")
            
        elif dificultad == "normal":
            # Grafo con 5 nodos en estrella
            centro = {"x": 350, "y": 250, "nombre": "Centro"}
            self.nodos = [centro]
            
            for i in range(4):
                ang = i * math.pi / 2
                x = centro["x"] + 150 * math.cos(ang)
                y = centro["y"] + 150 * math.sin(ang)
                self.nodos.append({"x": x, "y": y, "nombre": f"N{i+1}"})
                self.aristas.append((centro, self.nodos[-1]))
            
            # Añadir una arista adicional
            self.aristas.append((self.nodos[1], self.nodos[3]))
            self.info.config(text="Grafo normal cargado: Estrella con 4 puntas")
            
        elif dificultad == "dificil":
            # Grafo más complejo (árbol binario completo)
            self.nodos = [
                {"x": 350, "y": 100, "nombre": "Raíz"},
                {"x": 250, "y": 200, "nombre": "H1"},
                {"x": 450, "y": 200, "nombre": "H2"},
                {"x": 200, "y": 300, "nombre": "H3"},
                {"x": 300, "y": 300, "nombre": "H4"},
                {"x": 400, "y": 300, "nombre": "H5"},
                {"x": 500, "y": 300, "nombre": "H6"}
            ]
            self.aristas = [
                (self.nodos[0], self.nodos[1]),
                (self.nodos[0], self.nodos[2]),
                (self.nodos[1], self.nodos[3]),
                (self.nodos[1], self.nodos[4]),
                (self.nodos[2], self.nodos[5]),
                (self.nodos[2], self.nodos[6])
            ]
            self.info.config(text="Grafo difícil cargado: Árbol binario completo")
        
        self.dibujar_grafo()

    def click_canvas(self, event):
        # Manejar clic izquierdo en el lienzo
        x, y = event.x, event.y
        nodo = self.obtener_nodo_cerca(x, y)
        if nodo is None:
            # Crear nuevo nodo si no hay uno cercano
            self.nodos.append({"x": x, "y": y, "nombre": chr(65 + len(self.nodos))})
            self.dibujar_grafo()
        else:
            # Seleccionar nodo existente para mover
            self.nodo_seleccionado = nodo
            self.offset = (x - nodo["x"], y - nodo["y"])

    def click_derecho_canvas(self, event):
        # Manejar clic derecho para crear aristas
        x, y = event.x, event.y
        nodo1 = self.obtener_nodo_cerca(x, y)
        if nodo1:
            self.canvas.bind("<ButtonRelease-3>", lambda e: self.terminar_arista(nodo1, e))
            self.info.config(text="Arrastra y suelta sobre otro nodo para crear arista.")

    def terminar_arista(self, nodo1, event):
        # Completar la creación de una arista
        x, y = event.x, event.y
        nodo2 = self.obtener_nodo_cerca(x, y)
        if nodo2 and nodo2 != nodo1 and (nodo1, nodo2) not in self.aristas and (nodo2, nodo1) not in self.aristas:
            self.aristas.append((nodo1, nodo2))
            self.dibujar_grafo()
        self.canvas.unbind("<ButtonRelease-3>")
        self.info.config(text="Clic izquierdo para crear/mover nodos. Clic derecho para crear aristas.")

    def mover_nodo(self, event):
        # Mover un nodo seleccionado
        if self.nodo_seleccionado:
            self.nodo_seleccionado["x"] = event.x - self.offset[0]
            self.nodo_seleccionado["y"] = event.y - self.offset[1]
            self.dibujar_grafo()

    def obtener_nodo_cerca(self, x, y):
        # Encontrar nodo cercano a las coordenadas
        for nodo in self.nodos:
            if (nodo["x"] - x) ** 2 + (nodo["y"] - y) ** 2 < 400:
                return nodo
        return None

    def ejecutar_bfs(self):
        # Ejecutar algoritmo BFS
        if not self.nodos: return
        inicio = self.nodos[0]
        visitado = set()
        cola = deque([(inicio, 0)])
        res = {}
        self.aristas_regreso = []
        while cola:
            actual, nivel = cola.popleft()
            if actual["nombre"] in visitado:
                continue
            visitado.add(actual["nombre"])
            res[actual["nombre"]] = nivel
            vecinos = [b if a == actual else a for a, b in self.aristas if a == actual or b == actual]
            for v in vecinos:
                if v["nombre"] not in visitado:
                    cola.append((v, nivel + 1))
        self.res_bfs = res
        self.res_dfs = []
        self.dibujar_grafo()
        messagebox.showinfo("BFS", f"Niveles: {res}")

    def ejecutar_dfs(self):
        # Ejecutar algoritmo DFS
        if not self.nodos: return
        inicio = self.nodos[0]
        visitado = set()
        res = []
        self.aristas_regreso = []
        def dfs(nodo):
            visitado.add(nodo["nombre"])
            res.append(nodo["nombre"])
            vecinos = [b if a == nodo else a for a, b in self.aristas if a == nodo or b == nodo]
            for v in vecinos:
                if v["nombre"] not in visitado:
                    dfs(v)
                else:
                    # Detectar aristas de regreso
                    if (nodo["nombre"], v["nombre"]) not in self.aristas_regreso and (v["nombre"], nodo["nombre"]) not in self.aristas_regreso:
                        self.aristas_regreso.append((nodo, v))
        dfs(inicio)
        self.res_bfs = {}
        self.res_dfs = res
        self.dibujar_grafo()
        messagebox.showinfo("DFS", f"Orden: {res}")

    def limpiar(self):
        # Limpiar todo el grafo
        self.nodos.clear()
        self.aristas.clear()
        self.aristas_regreso.clear()
        self.res_bfs = {}
        self.res_dfs = []
        self.dibujar_grafo()
        self.info.config(text="Clic izquierdo para crear/mover nodos. Clic derecho para crear aristas.")

    def dibujar_grafo(self):
        # Dibujar el grafo completo
        self.canvas.delete("all")
        # Dibujar aristas
        for a, b in self.aristas:
            x1, y1 = a["x"], a["y"]
            x2, y2 = b["x"], b["y"]
            color = "#444"
            width = 2
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
        
        # Dibujar aristas de regreso para DFS
        if self.res_dfs:
            for a, b in self.aristas_regreso:
                x1, y1 = a["x"], a["y"]
                x2, y2 = b["x"], b["y"]
                self.canvas.create_line(x1, y1, x2, y2, fill=PURPLE, width=2, arrow=tk.LAST)
                px, py = (x1 + x2) // 2, (y1 + y2) // 2
                self.canvas.create_text(px, py, text="Regreso", fill=PURPLE, font=("Cooper Black", 9, "bold"))

        # Dibujar nodos
        for nodo in self.nodos:
            x, y, nombre = nodo["x"], nodo["y"], nodo["nombre"]
            fill = "white"
            outline = "black"
            ancho = 2
            texto = nombre
            if self.res_bfs and nombre in self.res_bfs:
                fill = GREEN
                texto = f"{nombre}\nL{self.res_bfs[nombre]}"
            elif self.res_dfs and nombre in self.res_dfs:
                idx = self.res_dfs.index(nombre) + 1
                fill = ORANGE
                texto = f"{nombre}\nD{idx}"
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=fill, outline=outline, width=ancho)
            self.canvas.create_text(x, y, text=texto, font=("Cooper Black", 14, "bold"))

class DijkstraApp:
    def __init__(self, root, volver_callback):
        self.root = root
        self.root.title("Juego de Dijkstra")
        self.volver_callback = volver_callback
        self.nodos = []
        self.aristas = []
        self.pesos = {}

        # Canvas idéntico
        self.canvas = tk.Canvas(root, width=700, height=500, bg="white",
                                highlightthickness=1, highlightbackground="black")
        self.canvas.pack(padx=20, pady=20)

        # Frame principal para botones (fila 1)
        self.frame_botones = tk.Frame(root, bg=BACKGROUND_COLOR, padx=10, pady=10)
        self.frame_botones.pack(fill=tk.X)

        # Sub-frame centrado para botones principales (Elegir origen, destino, Dijkstra, Limpiar, Menú)
        botones_principales = tk.Frame(self.frame_botones, bg=BACKGROUND_COLOR)
        botones_principales.pack(anchor="center")

        button_style = {"font": ("Britannic Bold", 11, "bold"),
                        "bd": 0, "fg": "black", "width": 15, "height": 2}

        self.btn_origen = tk.Button(botones_principales, text="Elegir origen", bg=GREEN, **button_style, command=self.elegir_origen)
        self.btn_origen.pack(side=tk.LEFT, padx=6)

        self.btn_destino = tk.Button(botones_principales, text="Elegir destino", bg=BLUE, **button_style, command=self.elegir_destino)
        self.btn_destino.pack(side=tk.LEFT, padx=6)

        self.btn_dijkstra = tk.Button(botones_principales, text="Calcular Dijkstra", bg=ORANGE, **button_style, command=self.calcular_dijkstra)
        self.btn_dijkstra.pack(side=tk.LEFT, padx=6)

        self.btn_limpiar = tk.Button(botones_principales, text="Limpiar", bg=PURPLE, **button_style, command=self.limpiar)
        self.btn_limpiar.pack(side=tk.LEFT, padx=6)

        self.btn_menu = tk.Button(botones_principales, text="Menú Principal", bg=DARK_RED, **button_style, command=self.volver_callback)
        self.btn_menu.pack(side=tk.LEFT, padx=6)

        # Frame para presets (fila 2), centrado
        self.frame_presets = tk.Frame(root, bg=BACKGROUND_COLOR, padx=10, pady=5)
        self.frame_presets.pack(fill=tk.X)

        presets_centrados = tk.Frame(self.frame_presets, bg=BACKGROUND_COLOR)
        presets_centrados.pack(anchor="center")

        tk.Label(presets_centrados, text="Grafos:", font=("Britannic Bold", 11), bg=BACKGROUND_COLOR).pack(side=tk.LEFT, padx=(0, 10))

        self.btn_facil = tk.Button(presets_centrados, text="Fácil", bg="#90EE90", fg="black", width=15,
                                  command=lambda: self.cargar_grafo_predefinido("facil"))
        self.btn_facil.pack(side=tk.LEFT, padx=6)

        self.btn_normal = tk.Button(presets_centrados, text="Normal", bg="#FFD700", fg="black", width=15,
                                   command=lambda: self.cargar_grafo_predefinido("normal"))
        self.btn_normal.pack(side=tk.LEFT, padx=6)

        self.btn_dificil = tk.Button(presets_centrados, text="Dificil", bg="#FF6347", fg="white", width=15,
                                    command=lambda: self.cargar_grafo_predefinido("dificil"))
        self.btn_dificil.pack(side=tk.LEFT, padx=6)

        # Etiqueta de información (fila 3)
        self.info = tk.Label(root,
                             text="Clic izquierdo para crear/mover nodos. Clic derecho para crear aristas.",
                             font=("Britannic Bold", 12), bg=BACKGROUND_COLOR)
        self.info.pack(fill=tk.X)

        # Eventos y variables
        self.canvas.bind("<Button-1>", self.click_canvas)
        self.canvas.bind("<Button-3>", self.click_derecho_canvas)
        self.canvas.bind("<B1-Motion>", self.mover_nodo)
        self.nodo_seleccionado = None
        self.offset = (0, 0)

        self.modo = "add"
        self.origen = None
        self.destino = None
        self.camino = []

        self.dibujar_grafo()

    def cargar_grafo_predefinido(self, dificultad):
        """Carga un grafo predefinido según la dificultad seleccionada"""
        self.limpiar()
        
        if dificultad == "facil":
            # Grafo simple con 3 nodos
            self.nodos = [
                {"x": 200, "y": 250, "nombre": "A"},
                {"x": 400, "y": 250, "nombre": "B"},
                {"x": 300, "y": 400, "nombre": "C"}
            ]
            self.aristas = [
                (self.nodos[0], self.nodos[1]),
                (self.nodos[1], self.nodos[2]),
                (self.nodos[2], self.nodos[0])
            ]
            self.pesos = {
                ("A", "B"): 3,
                ("B", "A"): 3,
                ("B", "C"): 4,
                ("C", "B"): 4,
                ("C", "A"): 5,
                ("A", "C"): 5
            }
            self.info.config(text="Grafo fácil cargado: Triángulo con pesos")
            
        elif dificultad == "normal":
            # Grafo con 5 nodos
            posiciones = [
                (350, 150), (200, 300), (500, 300), (150, 450), (550, 450)
            ]
            nombres = ["A", "B", "C", "D", "E"]
            
            for i, (x, y) in enumerate(posiciones):
                self.nodos.append({"x": x, "y": y, "nombre": nombres[i]})
            
            conexiones = [
                ("A", "B", 2), ("A", "C", 4), ("B", "D", 3),
                ("C", "E", 5), ("D", "E", 1), ("B", "C", 2)
            ]
            
            for a, b, w in conexiones:
                nodo_a = next(n for n in self.nodos if n["nombre"] == a)
                nodo_b = next(n for n in self.nodos if n["nombre"] == b)
                self.aristas.append((nodo_a, nodo_b))
                self.pesos[(a, b)] = w
                self.pesos[(b, a)] = w
            
            self.info.config(text="Grafo normal cargado: 5 nodos con diferentes pesos")
            
        elif dificultad == "dificil":
            # Grafo más complejo (grid 3x3)
            for i in range(3):
                for j in range(3):
                    x = 200 + j * 150
                    y = 150 + i * 150
                    nombre = f"{i}{j}"
                    self.nodos.append({"x": x, "y": y, "nombre": nombre})
            
            # Conexiones horizontales
            for i in range(3):
                for j in range(2):
                    a = f"{i}{j}"
                    b = f"{i}{j+1}"
                    w = random.randint(1, 5)
                    nodo_a = next(n for n in self.nodos if n["nombre"] == a)
                    nodo_b = next(n for n in self.nodos if n["nombre"] == b)
                    self.aristas.append((nodo_a, nodo_b))
                    self.pesos[(a, b)] = w
                    self.pesos[(b, a)] = w
            
            # Conexiones verticales
            for i in range(2):
                for j in range(3):
                    a = f"{i}{j}"
                    b = f"{i+1}{j}"
                    w = random.randint(1, 5)
                    nodo_a = next(n for n in self.nodos if n["nombre"] == a)
                    nodo_b = next(n for n in self.nodos if n["nombre"] == b)
                    self.aristas.append((nodo_a, nodo_b))
                    self.pesos[(a, b)] = w
                    self.pesos[(b, a)] = w
            
            self.info.config(text="Grafo difícil cargado: Grid 3x3 con pesos aleatorios")
        
        self.dibujar_grafo()

    def click_canvas(self, event):
        # Manejar clic en el lienzo según el modo
        x, y = event.x, event.y
        nodo = self.obtener_nodo_cerca(x, y)
        if self.modo == "add":
            if nodo is None:
                # Crear nuevo nodo
                self.nodos.append({"x": x, "y": y, "nombre": chr(65 + len(self.nodos))})
                self.dibujar_grafo()
            else:
                # Seleccionar nodo para mover
                self.nodo_seleccionado = nodo
                self.offset = (x - nodo["x"], y - nodo["y"])
        elif self.modo == "origen":
            if nodo:
                # Seleccionar nodo origen
                self.origen = nodo
                self.info.config(text=f"Origen: {nodo['nombre']}")
                self.modo = "add"
                self.dibujar_grafo()
        elif self.modo == "destino":
            if nodo:
                # Seleccionar nodo destino
                self.destino = nodo
                self.info.config(text=f"Destino: {nodo['nombre']}")
                self.modo = "add"
                self.dibujar_grafo()

    def click_derecho_canvas(self, event):
        # Manejar clic derecho para crear aristas
        x, y = event.x, event.y
        nodo1 = self.obtener_nodo_cerca(x, y)
        if nodo1:
            self.canvas.bind("<ButtonRelease-3>", lambda e: self.terminar_arista(nodo1, e))
            self.info.config(text="Arrastra y suelta sobre otro nodo para crear arista.")

    def terminar_arista(self, nodo1, event):
        # Completar la creación de una arista
        x, y = event.x, event.y
        nodo2 = self.obtener_nodo_cerca(x, y)
        if nodo2 and nodo2 != nodo1 and (nodo1, nodo2) not in self.aristas and (nodo2, nodo1) not in self.aristas:
            # Solicitar peso de la arista
            peso = simpledialog.askinteger("Peso", f"Peso de {nodo1['nombre']} a {nodo2['nombre']}:", minvalue=1, initialvalue=1, parent=self.root)
            if peso is not None:
                self.aristas.append((nodo1, nodo2))
                self.pesos[(nodo1['nombre'], nodo2['nombre'])] = peso
                self.pesos[(nodo2['nombre'], nodo1['nombre'])] = peso
                self.dibujar_grafo()
        self.canvas.unbind("<ButtonRelease-3>")
        self.info.config(text="Clic izquierdo para crear/mover nodos. Clic derecho para crear aristas.")

    def mover_nodo(self, event):
        # Mover nodo seleccionado
        if self.nodo_seleccionado:
            self.nodo_seleccionado["x"] = event.x - self.offset[0]
            self.nodo_seleccionado["y"] = event.y - self.offset[1]
            self.dibujar_grafo()

    def obtener_nodo_cerca(self, x, y):
        # Encontrar nodo cercano a las coordenadas
        for nodo in self.nodos:
            if (nodo["x"] - x) ** 2 + (nodo["y"] - y) ** 2 < 400:
                return nodo
        return None

    def elegir_origen(self):
        # Cambiar al modo de selección de origen
        self.modo = "origen"
        self.info.config(text="Haz clic en un nodo para elegir el origen.")

    def elegir_destino(self):
        # Cambiar al modo de selección de destino
        self.modo = "destino"
        self.info.config(text="Haz clic en un nodo para elegir el destino.")

    def calcular_dijkstra(self):
        # Calcular camino mínimo con Dijkstra
        if not self.origen or not self.destino:
            messagebox.showwarning("Faltan nodos", "Debes seleccionar origen y destino.")
            return
        
        # Ejecutar algoritmo de Dijkstra
        dist, prev = self.dijkstra(self.origen["nombre"])
        nombre_dest = self.destino["nombre"]
        
        if dist[nombre_dest] == float("inf"):
            messagebox.showinfo("Sin camino", "No hay camino entre los nodos seleccionados.")
            self.camino = []
        else:
            # Reconstruir camino
            camino = []
            n = nombre_dest
            while n:
                camino.append(n)
                n = prev[n]
            camino.reverse()
            self.camino = camino
            messagebox.showinfo("Dijkstra", f"Distancia mínima: {dist[nombre_dest]}\nCamino: {' → '.join(camino)}")
        self.dibujar_grafo()

    def dijkstra(self, origen):
        # Implementación del algoritmo de Dijkstra
        dist = {n["nombre"]: float("inf") for n in self.nodos}
        prev = {n["nombre"]: None for n in self.nodos}
        dist[origen] = 0
        cola = [(0, origen)]
        while cola:
            d, u = heapq.heappop(cola)
            if d > dist[u]:
                continue
            for v in [b if a["nombre"] == u else a for a, b in self.aristas if a["nombre"] == u or b["nombre"] == u]:
                if dist[u] + self.pesos[(u, v["nombre"])] < dist[v["nombre"]]:
                    dist[v["nombre"]] = dist[u] + self.pesos[(u, v["nombre"])]
                    prev[v["nombre"]] = u
                    heapq.heappush(cola, (dist[v["nombre"]], v["nombre"]))
        return dist, prev

    def limpiar(self):
        # Limpiar todo el grafo
        self.nodos.clear()
        self.aristas.clear()
        self.pesos.clear()
        self.origen = None
        self.destino = None
        self.camino = []
        self.dibujar_grafo()
        self.info.config(text="Clic izquierdo para crear/mover nodos. Clic derecho para crear aristas.")

    def dibujar_grafo(self):
        # Dibujar el grafo completo
        self.canvas.delete("all")
        # Dibujar aristas con pesos
        for a, b in self.aristas:
            x1, y1 = a["x"], a["y"]
            x2, y2 = b["x"], b["y"]
            color = "#444"
            width = 2
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
            px, py = (x1 + x2)//2, (y1 + y2)//2
            w = self.pesos.get((a["nombre"], b["nombre"]), 1)
            self.canvas.create_text(px, py, text=str(w), font=("Cooper Black", 12, "bold"), fill="black")
        
        # Dibujar nodos
        for nodo in self.nodos:
            x, y, nombre = nodo["x"], nodo["y"], nodo["nombre"]
            fill = "white"
            outline = "black"
            ancho = 2
            if self.origen == nodo:
                fill = GREEN
                outline = "black"
                ancho = 3
            elif self.destino == nodo:
                fill = ORANGE
                outline = "black"
                ancho = 3
            if nombre in self.camino:
                fill = "#FFD700"
                outline = "red"
                ancho = 4
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=fill, outline=outline, width=ancho)
            self.canvas.create_text(x, y, text=nombre, font=("Cooper Black", 14, "bold"))

class DirectedGraphApp:
    def __init__(self, root, volver_callback):
        self.root = root
        self.root.title("Grafos Dirigidos")
        self.volver_callback = volver_callback

        # Canvas para dibujar el grafo
        self.canvas = tk.Canvas(root, width=700, height=500, bg="white", highlightthickness=1, highlightbackground="black")
        self.canvas.pack(padx=20, pady=20)

        # Frame botones
        self.frame_botones = tk.Frame(root, bg=BACKGROUND_COLOR, padx=10, pady=10)
        self.frame_botones.pack(fill=tk.X)

        botones_centrados = tk.Frame(self.frame_botones, bg=BACKGROUND_COLOR)
        botones_centrados.pack(anchor="center")

        button_style = {"font": ("Cooper Black", 11, "bold"), "bd": 0, "fg": "black", "width": 15, "height": 2}

        self.btn_bidireccional = tk.Button(botones_centrados, text="Arista Bidireccional", bg=ORANGE, **button_style, command=self.modo_crear_aristas_bidireccionales)
        self.btn_bidireccional.pack(side=tk.LEFT, padx=5)

        self.btn_ciclo = tk.Button(botones_centrados, text="Verificar Ciclo", bg=GREEN, **button_style, command=self.verificar_ciclo)
        self.btn_ciclo.pack(side=tk.LEFT, padx=5)

        self.btn_caminos = tk.Button(botones_centrados, text="Mostrar Caminos", bg="#32CD32", **button_style, command=self.mostrar_caminos)
        self.btn_caminos.pack(side=tk.LEFT, padx=5)

        self.btn_limpiar = tk.Button(botones_centrados, text="Limpiar Todo", bg=RED, **button_style, command=self.limpiar)
        self.btn_limpiar.pack(side=tk.LEFT, padx=5)

        self.btn_menu = tk.Button(botones_centrados, text="Menú Principal", bg=DARK_RED, **button_style, command=self.volver_callback)
        self.btn_menu.pack(side=tk.LEFT, padx=5)

        # Frame presets
        self.frame_presets = tk.Frame(root, bg=BACKGROUND_COLOR)
        self.frame_presets.pack(fill=tk.X, padx=10, pady=5)

        presets_centrado = tk.Frame(self.frame_presets, bg=BACKGROUND_COLOR)
        presets_centrado.pack(anchor="center")

        tk.Label(presets_centrado, text="Grafos:", font=("Britannic Bold", 11), bg=BACKGROUND_COLOR).pack(side=tk.LEFT, padx=(10, 5))

        self.btn_facil = tk.Button(presets_centrado, text="Fácil", bg="#90EE90", fg="black", width=6,
                                   command=lambda: self.cargar_grafo_predefinido("facil"))
        self.btn_facil.pack(side=tk.LEFT, padx=6)

        self.btn_normal = tk.Button(presets_centrado, text="Normal", bg="#FFD700", fg="black", width=6,
                                    command=lambda: self.cargar_grafo_predefinido("normal"))
        self.btn_normal.pack(side=tk.LEFT, padx=6)

        self.btn_dificil = tk.Button(presets_centrado, text="Dificil", bg="#FF6347", fg="black", width=6,
                                     command=lambda: self.cargar_grafo_predefinido("dificil"))
        self.btn_dificil.pack(side=tk.LEFT, padx=6)

        # Etiqueta info
        self.info = tk.Label(root, text="Clic izquierdo para crear/mover nodos. Clic derecho para crear aristas dirigidas.",
                             font=("Cooper Black", 12), bg=BACKGROUND_COLOR)
        self.info.pack(fill=tk.X)

        # Variables grafo
        self.nodos = []
        self.aristas = []
        self.grafo = {}
        self.estado = "crear_nodos"  # Usamos para saber si arista bidireccional está activo
        self.nodo_seleccionado = None
        self.contador_nodos = 1

        # Eventos mouse
        self.canvas.bind("<Button-1>", self.click_canvas)
        self.canvas.bind("<Button-3>", self.click_derecho_canvas)
        self.canvas.bind("<B1-Motion>", self.mover_nodo)

    def modo_crear_aristas_bidireccionales(self):
        self.estado = "crear_aristas_bidireccionales"
        self.nodo_seleccionado = None
        self.info.config(text="Modo: Crear Aristas Bidireccionales - Selecciona dos nodos")

    def click_canvas(self, event):
        nodo = self.obtener_nodo_en_pos(event.x, event.y)
        if nodo:
            # Si hay nodo, seleccionar para mover
            self.nodo_seleccionado = nodo
        else:
            # Sino crear nuevo nodo
            self.agregar_nodo(event.x, event.y)

    def click_derecho_canvas(self, event):
        nodo = self.obtener_nodo_en_pos(event.x, event.y)
        if nodo:
            if not self.nodo_seleccionado:
                # Seleccionar nodo origen para arista
                self.nodo_seleccionado = nodo
            else:
                # Crear arista entre nodo seleccionado y nodo clic derecho actual
                if nodo != self.nodo_seleccionado:
                    self.agregar_arista(self.nodo_seleccionado, nodo)
                    if self.estado == "crear_aristas_bidireccionales":
                        self.agregar_arista(nodo, self.nodo_seleccionado)
                self.nodo_seleccionado = None
            self.dibujar_grafo()

    def mover_nodo(self, event):
        if self.nodo_seleccionado:
            self.nodo_seleccionado["x"] = event.x
            self.nodo_seleccionado["y"] = event.y
            self.dibujar_grafo()

    def agregar_nodo(self, x, y):
        nombre = f"N{self.contador_nodos}"
        self.contador_nodos += 1
        nodo = {"x": x, "y": y, "nombre": nombre}
        self.nodos.append(nodo)
        self.grafo[nombre] = []
        self.dibujar_grafo()
        self.info.config(text=f"Nodo {nombre} agregado en ({x},{y})")

    def obtener_nodo_en_pos(self, x, y):
        for nodo in self.nodos:
            if (nodo["x"] - x) ** 2 + (nodo["y"] - y) ** 2 < 400: 
                return nodo
        return None

    def agregar_arista(self, origen, destino):
        if destino["nombre"] not in self.grafo[origen["nombre"]]:
            self.grafo[origen["nombre"]].append(destino["nombre"])
            self.aristas.append((origen, destino))
            self.dibujar_grafo()
            self.info.config(text=f"Arista dirigida agregada: {origen['nombre']} → {destino['nombre']}")
        else:
            messagebox.showinfo("Info", "La arista dirigida ya existe.")

    def dibujar_grafo(self):
        self.canvas.delete("all")

        # Dibujar aristas dirigidas
        for origen, destino in self.aristas:
            x1, y1 = origen["x"], origen["y"]
            x2, y2 = destino["x"], destino["y"]
            dx = x2 - x1
            dy = y2 - y1
            dist = (dx**2 + dy**2)**0.5
            if dist > 0:
                dx /= dist
                dy /= dist
                x2 = x1 + dx * (dist - 20)
                y2 = y1 + dy * (dist - 20)
            self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, width=2, fill="blue")
            px, py = (x1 + x2) // 2, (y1 + y2) // 2
            self.canvas.create_text(px, py, text="→", font=("Cooper Black", 12, "bold"), fill="blue")

        # Dibujar nodos
        for nodo in self.nodos:
            x, y, nombre = nodo["x"], nodo["y"], nodo["nombre"]
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="lightblue", outline="black", width=2)
            self.canvas.create_text(x, y, text=nombre, font=("Cooper Black", 12, "bold"))

        # Resaltar nodo seleccionado
        if self.nodo_seleccionado:
            x, y = self.nodo_seleccionado["x"], self.nodo_seleccionado["y"]
            self.canvas.create_oval(x - 25, y - 25, x + 25, y + 25, outline="red", width=3)

    def verificar_ciclo(self):
        if self.hay_ciclo():
            messagebox.showwarning("Ciclo Detectado", "¡El grafo dirigido tiene al menos un ciclo!")
        else:
            messagebox.showinfo("Sin Ciclos", "El grafo dirigido no tiene ciclos.")

    def hay_ciclo(self):
        visitados = set()
        for nodo in self.grafo:
            if nodo not in visitados:
                pila = set()
                if self.dfs_ciclo(nodo, visitados, pila):
                    return True
        return False

    def dfs_ciclo(self, nodo, visitados, pila):
        visitados.add(nodo)
        pila.add(nodo)

        for vecino in self.grafo.get(nodo, []):
            if vecino not in visitados:
                if self.dfs_ciclo(vecino, visitados, pila):
                    return True
            elif vecino in pila:
                return True

        pila.remove(nodo)
        return False

    def mostrar_caminos(self):
        if not self.nodos:
            messagebox.showinfo("Sin nodos", "No hay nodos en el grafo.")
            return

        ventana_caminos = tk.Toplevel(self.root)
        ventana_caminos.title("Mostrar Caminos")
        ventana_caminos.geometry("400x300")
        ventana_caminos.configure(bg=LIGHT_BLUE)

        tk.Label(ventana_caminos, text="Nodo inicio:", font=("Cooper Black", 12), bg=LIGHT_BLUE).grid(row=0, column=0, padx=10, pady=10)
        inicio_entry = tk.Entry(ventana_caminos, font=("Cooper Black", 12))
        inicio_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(ventana_caminos, text="Nodo destino:", font=("Cooper Black", 12), bg=LIGHT_BLUE).grid(row=1, column=0, padx=10, pady=10)
        destino_entry = tk.Entry(ventana_caminos, font=("Cooper Black", 12))
        destino_entry.grid(row=1, column=1, padx=10, pady=10)

        txt_resultado = tk.Text(ventana_caminos, width=40, height=10, font=("Cooper Black", 10))
        txt_resultado.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        def buscar_caminos():
            inicio = inicio_entry.get().strip()
            destino = destino_entry.get().strip()
            if inicio not in self.grafo or destino not in self.grafo:
                messagebox.showerror("Error", "Uno o ambos nodos no existen en el grafo.")
                return
            caminos = self.caminos_desde(inicio, destino)
            txt_resultado.delete("1.0", tk.END)
            if caminos:
                txt_resultado.insert(tk.END, f"Caminos desde {inicio} hasta {destino}:\n\n")
                for c in caminos:
                    txt_resultado.insert(tk.END, " → ".join(c) + "\n\n")
            else:
                txt_resultado.insert(tk.END, f"No hay caminos desde {inicio} hasta {destino}.")

        btn_buscar = tk.Button(ventana_caminos, text="Buscar caminos", command=buscar_caminos,
                               bg=BLUE, fg="white", font=("Cooper Black", 10, "bold"))
        btn_buscar.grid(row=2, column=0, columnspan=2, pady=10)

    def caminos_desde(self, inicio, destino, camino=None):
        if camino is None:
            camino = []
        camino = camino + [inicio]
        if inicio == destino:
            return [camino]
        caminos = []
        for vecino in self.grafo.get(inicio, []):
            if vecino not in camino:
                nuevos_caminos = self.caminos_desde(vecino, destino, camino)
                for c in nuevos_caminos:
                    caminos.append(c)
        return caminos

    def cargar_grafo_predefinido(self, dificultad):
        self.limpiar()

        if dificultad == "facil":
            self.agregar_nodo(300, 200)
            self.agregar_nodo(200, 350)
            self.agregar_nodo(400, 350)

            n1 = self.obtener_nodo_por_nombre("N1")
            n2 = self.obtener_nodo_por_nombre("N2")
            n3 = self.obtener_nodo_por_nombre("N3")

            self.agregar_arista(n1, n2)
            self.agregar_arista(n1, n3)
            self.info.config(text="Grafo fácil cargado: Estrella de 3 nodos")

        elif dificultad == "normal":
            for i in range(4):
                ang = i * math.pi / 2
                x = 350 + 150 * math.cos(ang)
                y = 250 + 150 * math.sin(ang)
                self.agregar_nodo(x, y)

            for i in range(4):
                actual = self.obtener_nodo_por_nombre(f"N{i+1}")
                siguiente = self.obtener_nodo_por_nombre(f"N{(i % 4) + 1}")
                self.agregar_arista(actual, siguiente)

            n1 = self.obtener_nodo_por_nombre("N1")
            n3 = self.obtener_nodo_por_nombre("N3")
            self.agregar_arista(n1, n3)

            self.info.config(text="Grafo normal cargado: Ciclo con arista adicional")

        elif dificultad == "dificil":
            for i in range(5):
                ang = i * 2 * math.pi / 5
                x = 350 + 150 * math.cos(ang)
                y = 250 + 150 * math.sin(ang)
                self.agregar_nodo(x, y)

            nombres = [f"N{i+1}" for i in range(5)]

            conexiones = [
                (0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
                (0, 2), (1, 3), (2, 4), (3, 0), (4, 1)
            ]

            for i, j in conexiones:
                origen = self.obtener_nodo_por_nombre(nombres[i])
                destino = self.obtener_nodo_por_nombre(nombres[j])
                self.agregar_arista(origen, destino)

            self.info.config(text="Grafo difícil cargado: Grafo completo dirigido")

        self.dibujar_grafo()

    def limpiar(self):
        self.nodos.clear()
        self.aristas.clear()
        self.grafo.clear()
        self.contador_nodos = 1
        self.nodo_seleccionado = None
        self.estado = "crear_nodos"
        self.canvas.delete("all")
        self.info.config(text="Clic izquierdo para crear/mover nodos. Clic derecho para crear aristas dirigidas.")

    def obtener_nodo_por_nombre(self, nombre):
        for nodo in self.nodos:
            if nodo["nombre"] == nombre:
                return nodo
        return None


# Función principal para iniciar la aplicación
def main():
    root = tk.Tk()
    PantallaBienvenida(root)
    root.mainloop()

if __name__ == "__main__":
    main()