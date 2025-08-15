import tkinter as tk
from tkinter import colorchooser, messagebox, ttk
import random

class Polygon:
    def __init__(self, points):
        self.points = tuple(points) 
        self.vertex_colors = [(255, 255, 255)] * len(points)  # Branco como padrão para todos os vértices
        self.filled = False 

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("FillPoly")
        self.temp_points = []  # Lista de pontos temporários
        self.temp_colors = []  # Lista de cores temporárias para pontos
        self.polygon_list = [] 
        self.selected_polygon = None  
        self.selected_vertex = None
        self.show_edges = tk.BooleanVar(value=True) 
        self.mode = tk.StringVar(value="draw")  

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.main_frame, width=600, height=600, bg="black")
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
        self.control_frame = tk.Frame(self.main_frame, width=200)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        self.toolbar = tk.Frame(self.control_frame, bd=1, relief=tk.RAISED)
        self.toolbar.pack(fill=tk.X, pady=5)

        self.mode_button = tk.Button(self.toolbar, text="Draw", command=self.toggle_mode)
        self.mode_button.pack(side=tk.TOP, fill=tk.X)

        self.clear_button = tk.Button(self.toolbar, text="Clear Canvas", command=self.clear_canvas)
        self.clear_button.pack(side=tk.TOP, fill=tk.X)
        
        self.remove_button = tk.Button(self.toolbar, text="Remove Polygon", command=self.remove_polygon)
        self.remove_button.pack(side=tk.TOP, fill=tk.X)
        self.remove_button.config(state=tk.DISABLED)

        self.vertex_color_button = tk.Button(self.toolbar, text="Change Vertex Color", command=self.change_vertex_color)
        self.vertex_color_button.pack(side=tk.TOP, fill=tk.X)
        self.vertex_color_button.config(state=tk.DISABLED)

        self.fill_button = tk.Button(self.toolbar, text="Fill Polygon", command=self.fill_selected_polygon)
        self.fill_button.pack(side=tk.TOP, fill=tk.X)
        self.fill_button.config(state=tk.DISABLED)

        self.random_colors_button = tk.Button(
            self.toolbar, 
            text="Randomize Vertex Colors",
            command=self.randomize_vertex_colors
        )
        self.random_colors_button.pack(side=tk.TOP, fill=tk.X)
        self.random_colors_button.config(state=tk.DISABLED)

        self.current_vertex_color = (255, 255, 255)  # Cor padrão de vértice

        self.info_frame = tk.Frame(self.control_frame)
        self.info_frame.pack(fill=tk.X, pady=5)

        self.label = tk.Label(self.info_frame, text="Left click to add points, right click to close polygon", wraplength=180)
        self.label.pack()

        self.coordinates_label = tk.Label(self.info_frame, text="Mouse Coordinates: (0, 0)", wraplength=180)
        self.coordinates_label.pack()

        self.lists_frame = tk.Frame(self.control_frame)
        self.lists_frame.pack(fill=tk.BOTH, expand=True)

        self.poly_frame = tk.Frame(self.lists_frame)
        self.poly_frame.pack(fill=tk.BOTH, expand=True)

        # Lista de poligonos
        tk.Label(self.poly_frame, text="Polygons").pack()
        self.polygon_list_ui = tk.Listbox(self.poly_frame, height=8)
        self.polygon_list_ui.pack(fill=tk.BOTH, expand=True)
        self.polygon_list_ui.bind('<<ListboxSelect>>', self.select_polygon_ui)

        self.vertex_frame = tk.Frame(self.lists_frame)
        self.vertex_frame.pack(fill=tk.BOTH, expand=True)

        # Lista de vertices
        tk.Label(self.vertex_frame, text="Vertices").pack()
        self.vertex_list_ui = tk.Listbox(self.vertex_frame, height=8)
        self.vertex_list_ui.pack(fill=tk.BOTH, expand=True)
        self.vertex_list_ui.bind('<<ListboxSelect>>', self.select_vertex_ui)

        self.color_frame = tk.Frame(self.control_frame)
        self.color_frame.pack(fill=tk.X, pady=5)

        #Previa de cores
        self.color_preview = tk.Label(self.color_frame, text="Vertex Color", bg="#ffffff", width=20, height=2)
        self.color_preview.pack(fill=tk.X)

        self.canvas.bind("<Button-1>", self.handle_clicks)  # Clique esquerdo
        self.canvas.bind("<Button-3>", self.close_polygon) # Clique direito
        self.canvas.bind("<Motion>", self.update_coordinates)

    def update_coordinates(self, event):
        x, y = event.x, event.y
        self.coordinates_label.config(text=f"Mouse Coordinates: ({x}, {y})")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.polygon_list.clear()
        self.temp_points.clear()
        self.temp_colors.clear()
        self.polygon_list_ui.delete(0, tk.END)
        self.vertex_list_ui.delete(0, tk.END)
        self.selected_polygon = None
        self.selected_vertex = None
        self.remove_button.config(state=tk.DISABLED)
        self.fill_button.config(state=tk.DISABLED)
        self.vertex_color_button.config(state=tk.DISABLED)
        self.random_colors_button.config(state=tk.DISABLED)
        self.draw()

    def add_point(self, event):
        x, y = event.x, event.y
        self.temp_points.append((x, y))
        self.temp_colors.append(self.current_vertex_color)
        self.label.config(text=f"Current points: {self.temp_points}")
        self.draw()

    def close_polygon(self, event):
        if len(self.temp_points) >= 3:
            polygon = Polygon(self.temp_points)
            polygon.vertex_colors = self.temp_colors.copy()
            self.polygon_list.append(polygon)
            self.update_polygon_list_ui()
            self.temp_points.clear()
            self.temp_colors.clear()
            self.label.config(text="Polygon closed. Left click to start a new one.")
            self.draw()
        else:
            messagebox.showerror("Error", "At least 3 points are needed to form a polygon.")

    def update_polygon_list_ui(self):
        self.polygon_list_ui.delete(0, tk.END)
        for i, polygon in enumerate(self.polygon_list, 1):
            self.polygon_list_ui.insert(tk.END, f"Polygon {i}")

    def handle_clicks(self, event):
        if self.mode.get() == "draw":
            self.add_point(event)  
        elif self.mode.get() == "select":
            self.select_polygon_by_click(event)  

    def toggle_mode(self):
        if self.mode.get() == "draw":
            self.mode.set("select")
            self.mode_button.config(text="Select")
            self.label.config(text="Click to select a polygon.")
        else:
            self.mode.set("draw")
            self.mode_button.config(text="Draw")
            self.label.config(text="Left click to add points, right click to close polygon.")

    def remove_polygon(self):
        if self.selected_polygon:
            index = self.polygon_list.index(self.selected_polygon)
            del self.polygon_list[index]
            
            self.update_polygon_list_ui()
            
            self.vertex_list_ui.delete(0, tk.END)
            self.selected_polygon = None
            self.selected_vertex = None
            self.fill_button.config(state=tk.DISABLED)
            self.remove_button.config(state=tk.DISABLED)
            self.vertex_color_button.config(state=tk.DISABLED)
            self.random_colors_button.config(state=tk.DISABLED)
            self.draw()

    def select_polygon_by_click(self, event):
        x, y = event.x, event.y
        selected_polygon = None
        
        for polygon in reversed(self.polygon_list):
            if self.point_in_polygon(x, y, polygon.points):
                selected_polygon = polygon
                break
                
        if selected_polygon:
            self.select_polygon(selected_polygon)

    def select_polygon_ui(self, event):
        selection = self.polygon_list_ui.curselection()
        if selection:
            index = selection[0]
            self.select_polygon(self.polygon_list[index])

    def select_polygon(self, polygon):
        self.selected_polygon = polygon
        index = self.polygon_list.index(polygon)
        self.polygon_list_ui.selection_clear(0, tk.END)
        self.polygon_list_ui.selection_set(index)
        self.polygon_list_ui.activate(index)
        self.random_colors_button.config(state=tk.NORMAL)
        
        # Atualizar lista de vértices
        self.vertex_list_ui.delete(0, tk.END)
        for i, (x, y) in enumerate(polygon.points):
            self.vertex_list_ui.insert(tk.END, f"Vertex {i+1} ({x}, {y})")
        
        self.fill_button.config(state=tk.NORMAL)
        self.remove_button.config(state=tk.NORMAL)
        self.vertex_color_button.config(state=tk.NORMAL)
        self.draw()

    def select_vertex_ui(self, event):
        if not self.selected_polygon:
            return
            
        selection = self.vertex_list_ui.curselection()
        if selection:
            self.selected_vertex = selection[0]
            r, g, b = self.selected_polygon.vertex_colors[self.selected_vertex]
            self.color_preview.config(bg=f"#{r:02x}{g:02x}{b:02x}")

    def change_vertex_color(self):
        if self.selected_polygon is None or self.selected_vertex is None:
            return
            
        color = colorchooser.askcolor()[0]
        if color:
            r, g, b = tuple(int(c) for c in color)
            self.selected_polygon.vertex_colors[self.selected_vertex] = (r, g, b)
            # Atualizar prévia de cores
            self.color_preview.config(bg=f"#{r:02x}{g:02x}{b:02x}")
            self.draw()

    def point_in_polygon(self, x, y, points):
        n = len(points)
        inside = False
        x0, y0 = points[0]
        
        for i in range(n + 1):
            x1, y1 = points[i % n]
            if (y > min(y0, y1)) and (y <= max(y0, y1)):
                intersection_result = (y - y0) * (x1 - x0) / (y1 - y0) + x0
                if x <= intersection_result:
                    inside = not inside
            x0, y0 = x1, y1
        return inside

    def fill_selected_polygon(self):
        if self.selected_polygon:
            self.selected_polygon.filled = True
            self.draw()
    
    def randomize_vertex_colors(self):
        if self.selected_polygon is None:
            return
        
        # Gerar cores aleatorias para cada vertice
        for i in range(len(self.selected_polygon.vertex_colors)):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            self.selected_polygon.vertex_colors[i] = (r, g, b)
        
        # Atualizar previa de cores
        if self.selected_vertex is not None:
            r, g, b = self.selected_polygon.vertex_colors[self.selected_vertex]
            self.color_preview.config(bg=f"#{r:02x}{g:02x}{b:02x}")
        
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        if hasattr(self.canvas, '_raster_images'):
            del self.canvas._raster_images
        # Desenha os polígonos existentes
        for polygon in self.polygon_list:
            # Preenche o polígono se estiver marcado como preenchido
            if polygon.filled:
                rasterize(polygon, self.canvas)
            # Desenha o contorno do polígono
            if self.show_edges.get():
                points = polygon.points
                for i in range(len(points)):
                    x1, y1 = points[i]
                    x2, y2 = points[(i + 1) % len(points)]
                    color1 = polygon.vertex_colors[i]
                    color2 = polygon.vertex_colors[(i + 1) % len(points)]
                    self.draw_line_with_interpolation(x1, y1, x2, y2, color1, color2)

            # Destacar polígono selecionado e vértices
            if polygon == self.selected_polygon:
                for i, (x, y) in enumerate(polygon.points):
                    if i == self.selected_vertex:
                        # Desenhar vértice selecionado com um círculo maior
                        self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="red", outline="white")
                    else:
                        # Desenhar vértices regular
                        r, g, b = polygon.vertex_colors[i]
                        self.canvas.create_oval(x-3, y-3, x+3, y+3, fill=f"#{r:02x}{g:02x}{b:02x}", outline="white")

        # Desenha as linhas temporárias do polígono em construção
        if len(self.temp_points) > 1:
            for i in range(len(self.temp_points) - 1):
                x1, y1 = self.temp_points[i]
                x2, y2 = self.temp_points[i + 1]
                color1 = self.temp_colors[i]
                color2 = self.temp_colors[i + 1]
                self.draw_line_with_interpolation(x1, y1, x2, y2, color1, color2)

        # Desenha os pontos com suas cores
        for i, (x, y) in enumerate(self.temp_points):
            color = self.temp_colors[i]
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="#%02x%02x%02x" % color, outline="")

    #Desenha uma linha com interpolação de cores entre dois pontos
    def draw_line_with_interpolation(self, x1, y1, x2, y2, color1, color2):

        if x1 == x2 and y1 == y2:
            return

        steps = max(abs(x2 - x1), abs(y2 - y1))
        if steps == 0:
            return

        # Pré-cálculo dos incrementos 
        delta_x = (x2 - x1) / steps
        delta_y = (y2 - y1) / steps
        delta_r = (color2[0] - color1[0]) / steps
        delta_g = (color2[1] - color1[1]) / steps
        delta_b = (color2[2] - color1[2]) / steps

        # Valores iniciais
        x, y = x1, y1
        r, g, b = color1[0], color1[1], color1[2]

        for _ in range(steps + 1):
            self.canvas.create_line(
                int(x), int(y), int(x)+1, int(y), 
                fill=f"#{int(r):02x}{int(g):02x}{int(b):02x}"
            )
            x += delta_x
            y += delta_y
            r += delta_r
            g += delta_g
            b += delta_b
            self.canvas.create_line(x, y, x+1, y, fill="#%02x%02x%02x" % (int(r), int(g), int(b)))

def rasterize(polygon, canvas):
    if len(polygon.points) < 3:
        return

    # Procurar os limites do polígono
    min_y = min(y for x, y in polygon.points)
    max_y = max(y for x, y in polygon.points)

    # Número de linhas de varredura
    N_s = max_y - min_y

    # Inicializar a tabela de arestas como um dicionário 
    edge_table = {i: [] for i in range(N_s + 1)}

    # Processar cada aresta do polígono
    n = len(polygon.points)
    for i in range(n):
        # Vertice atual
        x1, y1 = polygon.points[i]
        color1 = polygon.vertex_colors[i]
        
        # Proximo vertice ou primeiro vertice se for o ultimo
        if i < n - 1:
            x2, y2 = polygon.points[i + 1]
            color2 = polygon.vertex_colors[i + 1]
        else:
            # Conectar o último vértice ao primeiro
            x2, y2 = polygon.points[0]
            color2 = polygon.vertex_colors[0]
        # Pular arestas horizontais
        if y1 == y2:
            continue

        # Garantir que y1 < y2
        if y1 > y2:
            x1, y1, x2, y2 = x2, y2, x1, y1
            color1, color2 = color2, color1

        # Calcular a inclinação (Tx) e as diferenças de cor
        dy = y2 - y1
        Tx = (x2 - x1) / dy
        delta_r = (color2[0] - color1[0]) / dy
        delta_g = (color2[1] - color1[1]) / dy
        delta_b = (color2[2] - color1[2]) / dy

        # Valores iniciais
        current_x = x1
        current_r, current_g, current_b = color1

        # Processar de y_min a y_max-1 (coordenadas da linha de varredura)
        y_min_scanline = int(y1 - min_y)
        y_max_scanline = int(y2 - min_y)
        
        for scanline in range(y_min_scanline, y_max_scanline):
            if scanline >= 0 and scanline <= N_s:
                # Armazenar interseção com informações de cor
                edge_table[scanline].append({
                    'x': current_x,
                    'color': (int(current_r), int(current_g), int(current_b))
                })

            # Atualização incremental
            current_x += Tx
            current_r += delta_r
            current_g += delta_g
            current_b += delta_b

    # Processar cada linha de varredura
    for scanline in range(N_s + 1):
        intersections = edge_table[scanline]
        
        # Ordenar as interseções por x
        intersections.sort(key=lambda item: item['x'])

        # Preencher entre pares de interseções
        for i in range(0, len(intersections), 2):
            if i + 1 >= len(intersections):
                break
                
            x1 = intersections[i]['x']
            x2 = intersections[i + 1]['x']
            color1 = intersections[i]['color']
            color2 = intersections[i + 1]['color']
            if x2 > x1:
                # Criar linha de gradiente
                width = int(x2) - int(x1)
                if width <= 0:
                    continue
                    
                img = tk.PhotoImage(width=width, height=1)
                delta_r = (color2[0] - color1[0]) / width
                delta_g = (color2[1] - color1[1]) / width
                delta_b = (color2[2] - color1[2]) / width
                
                r, g, b = color1[0], color1[1], color1[2]
                for x_pixel in range(width):
                    img.put(f"#{int(r):02x}{int(g):02x}{int(b):02x}", (x_pixel, 0))
                    r += delta_r
                    g += delta_g
                    b += delta_b
                
                canvas.create_image(int(x1), scanline + min_y, image=img, anchor=tk.NW)
                if not hasattr(canvas, '_raster_images'):
                    canvas._raster_images = []
                canvas._raster_images.append(img)
   
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()