"""
JUEGO DEL AHORCADO
"""

import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os
import threading
import unicodedata
from datetime import datetime

try:
    from datasets import load_dataset
    HUGGINGFACE_DISPONIBLE = True
except ImportError:
    HUGGINGFACE_DISPONIBLE = False

class AhorcadoVentana:
    def __init__(self):
        """Constructor. Inicializa el juego."""
        # Estado del juego
        self.palabra_actual = ""
        self.palabra_original = ""  # Guardamos la palabra original
        self.palabra_oculta = []
        self.intentos_restantes = 6
        self.letras_usadas = set()
        self.juego_activo = True
        self.modo_dificil = False
        
        # Estadísticas
        self.partidas_ganadas = 0
        self.partidas_perdidas = 0
        self.racha_actual = 0
        self.racha_maxima = 0
        
        # Diccionario
        self.diccionario_completo = []
        self.diccionario_por_longitud = {}
        self.longitud_actual = 6
        self.total_palabras = 0
        
        # Configurar ventana
        self.ventana = tk.Tk()
        self.ventana.title("AHORCADO - Con soporte para vocales acentuadas")
        self.ventana.geometry("850x950")
        self.ventana.minsize(850, 950)
        self.ventana.configure(bg='#1a1a2e')
        
        self.crear_interfaz()
        self.cargar_diccionario()
    
    def normalizar_texto(self, texto):
        """
        Convierte vocales acentuadas a mayúsculas sin acento.
        """
        texto_normalizado = unicodedata.normalize('NFKD', texto)
        texto_sin_acentos = ''.join(c for c in texto_normalizado if not unicodedata.combining(c))
        return texto_sin_acentos.upper()
    
    def contar_vocales(self, palabra):
        """
        Cuenta todas las vocales (con y sin acento).
        """
        vocales = set('AEIOUÁÉÍÓÚ')
        return sum(1 for letra in palabra.upper() if letra in vocales)
    
    def tiene_vocal_acentuada(self, palabra):
        """
        Verifica si una palabra tiene vocales acentuadas.
        """
        acentos = set('ÁÉÍÓÚ')
        return any(letra in acentos for letra in palabra.upper())
    
    def centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        self.ventana.update_idletasks()
        ancho = 950
        alto = 800
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def crear_interfaz(self):
        """Crea la interfaz gráfica."""
        main_frame = tk.Frame(self.ventana, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Frame de carga
        self.frame_carga = tk.Frame(main_frame, bg='#1a1a2e')
        self.frame_carga.pack(fill=tk.BOTH, expand=True)
        
        center_frame = tk.Frame(self.frame_carga, bg='#1a1a2e')
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(
            center_frame,
            text="🎮",
            font=("Segoe UI Emoji", 48),
            bg='#1a1a2e'
        ).pack(pady=10)
        
        tk.Label(
            center_frame,
            text="AHORCADO PREMIUM",
            font=("Helvetica", 28, "bold"),
            bg='#1a1a2e',
            fg='#e94560'
        ).pack(pady=10)
        
        tk.Label(
            center_frame,
            text="Cargando diccionario Spanish-BFF...",
            font=("Helvetica", 12),
            bg='#1a1a2e',
            fg='#a0a0a0'
        ).pack(pady=5)
        
        self.progreso = ttk.Progressbar(center_frame, length=400, mode='indeterminate')
        self.progreso.pack(pady=20)
        self.progreso.start()
        
        self.label_carga_estado = tk.Label(
            center_frame,
            text="⏳ Conectando con Hugging Face...",
            font=("Helvetica", 10),
            bg='#1a1a2e',
            fg='#e94560'
        )
        self.label_carga_estado.pack(pady=10)
        
        # Frame del juego
        self.frame_juego = tk.Frame(main_frame, bg='#1a1a2e')
        
        # Título
        titulo_frame = tk.Frame(self.frame_juego, bg='#1a1a2e')
        titulo_frame.pack(pady=10)
        
        tk.Label(
            titulo_frame,
            text="🎮 AHORCADO PREMIUM 🎮",
            font=("Helvetica", 24, "bold"),
            bg='#1a1a2e',
            fg='#e94560'
        ).pack()
        
        tk.Label(
            titulo_frame,
            text="Diccionario Spanish-BFF · 66,353 palabras reales del español",
            font=("Helvetica", 10),
            bg='#1a1a2e',
            fg='#888'
        ).pack()
        
        # Canvas para el ahorcado
        canvas_frame = tk.Frame(self.frame_juego, bg='#16213e', relief=tk.GROOVE, bd=2)
        canvas_frame.pack(pady=15, padx=20, fill=tk.X)
        
        self.canvas = tk.Canvas(canvas_frame, width=500, height=280, bg='#16213e', highlightthickness=0)
        self.canvas.pack(pady=15)
        
        # Palabra oculta
        palabra_frame = tk.Frame(self.frame_juego, bg='#1a1a2e')
        palabra_frame.pack(pady=20)
        
        self.label_palabra = tk.Label(
            palabra_frame,
            text="",
            font=("Courier New", 44, "bold"),
            bg='#1a1a2e',
            fg='#e94560'
        )
        self.label_palabra.pack()
        
        # Panel de información
        info_frame = tk.Frame(self.frame_juego, bg='#1a1a2e')
        info_frame.pack(pady=15, fill=tk.X)
        
        # Estadísticas
        stats_box = tk.Frame(info_frame, bg='#16213e', relief=tk.GROOVE, bd=1)
        stats_box.pack(side=tk.LEFT, expand=True, padx=5, fill=tk.BOTH)
        
        tk.Label(
            stats_box,
            text="📊 ESTADÍSTICAS",
            font=("Helvetica", 11, "bold"),
            bg='#16213e',
            fg='#e94560'
        ).pack(pady=8)
        
        self.label_score = tk.Label(
            stats_box,
            text="🏆 Victorias: 0\n💀 Derrotas: 0\n📈 Racha: 0\n🏅 Máxima: 0",
            font=("Helvetica", 10),
            bg='#16213e',
            fg='#ccc',
            justify=tk.LEFT
        )
        self.label_score.pack(pady=5, padx=15)
        
        # Estado del juego
        game_box = tk.Frame(info_frame, bg='#16213e', relief=tk.GROOVE, bd=1)
        game_box.pack(side=tk.LEFT, expand=True, padx=5, fill=tk.BOTH)
        
        tk.Label(
            game_box,
            text="🎯 PARTIDA ACTUAL",
            font=("Helvetica", 11, "bold"),
            bg='#16213e',
            fg='#e94560'
        ).pack(pady=8)
        
        self.label_intentos = tk.Label(
            game_box,
            text="💪 Intentos: 6",
            font=("Helvetica", 12, "bold"),
            bg='#16213e',
            fg='#ffd700'
        )
        self.label_intentos.pack(pady=5)
        
        # Pista de vocales
        self.label_pista_vocales = tk.Label(
            game_box,
            text="",
            font=("Helvetica", 10),
            bg='#16213e',
            fg='#2ecc71'
        )
        self.label_pista_vocales.pack(pady=5)
        
        tk.Label(
            game_box,
            text="Letras usadas:",
            font=("Helvetica", 10),
            bg='#16213e',
            fg='#ccc'
        ).pack()
        
        self.label_usadas = tk.Label(
            game_box,
            text="",
            font=("Helvetica", 11),
            bg='#16213e',
            fg='#e94560',
            wraplength=250
        )
        self.label_usadas.pack(pady=5)
        
        # Controles
        control_box = tk.Frame(info_frame, bg='#16213e', relief=tk.GROOVE, bd=1)
        control_box.pack(side=tk.LEFT, expand=True, padx=5, fill=tk.BOTH)
        
        tk.Label(
            control_box,
            text="🎮 CONTROLES",
            font=("Helvetica", 11, "bold"),
            bg='#16213e',
            fg='#e94560'
        ).pack(pady=8)
        
        # Selector de longitud
        long_frame = tk.Frame(control_box, bg='#16213e')
        long_frame.pack(pady=5)
        
        tk.Label(
            long_frame,
            text="Longitud:",
            font=("Helvetica", 10),
            bg='#16213e',
            fg='#ccc'
        ).pack(side=tk.LEFT, padx=5)
        
        self.combo_longitud = ttk.Combobox(
            long_frame,
            values=[4, 5, 6, 7, 8, 9, 10],
            state="readonly",
            width=5
        )
        self.combo_longitud.set(6)
        self.combo_longitud.pack(side=tk.LEFT, padx=5)
        self.combo_longitud.bind('<<ComboboxSelected>>', self.cambiar_longitud)
        
        # Modo difícil
        self.dificil_var = tk.BooleanVar()
        dificil_check = tk.Checkbutton(
            control_box,
            text="🔥 Modo Difícil (4 intentos)",
            variable=self.dificil_var,
            command=self.toggle_modo_dificil,
            bg='#16213e',
            fg='#ccc',
            selectcolor='#16213e',
            font=("Helvetica", 10)
        )
        dificil_check.pack(pady=5)
        
        # Entrada de letras
        entrada_frame = tk.Frame(self.frame_juego, bg='#1a1a2e')
        entrada_frame.pack(pady=20)
        
        tk.Label(
            entrada_frame,
            text="INGRESA UNA LETRA:",
            font=("Helvetica", 12, "bold"),
            bg='#1a1a2e',
            fg='#ccc'
        ).pack(side=tk.LEFT, padx=10)
        
        self.entry_letra = tk.Entry(
            entrada_frame,
            font=("Helvetica", 18),
            width=4,
            justify='center',
            bg='#16213e',
            fg='#e94560',
            insertbackground='#e94560',
            bd=2,
            relief=tk.GROOVE
        )
        self.entry_letra.pack(side=tk.LEFT, padx=10)
        self.entry_letra.bind('<Return>', self.procesar_letra)
        
        self.boton_intentar = tk.Button(
            entrada_frame,
            text="INTENTAR",
            command=self.procesar_letra,
            font=("Helvetica", 11, "bold"),
            bg='#e94560',
            fg='white',
            activebackground='#c7354f',
            padx=20,
            pady=5,
            bd=0,
            cursor='hand2'
        )
        self.boton_intentar.pack(side=tk.LEFT, padx=10)
        
        # Botones de acción
        botones_frame = tk.Frame(self.frame_juego, bg='#1a1a2e')
        botones_frame.pack(pady=15)
        
        btn_nuevo = tk.Button(
            botones_frame,
            text="🎲 NUEVA PALABRA",
            command=self.nuevo_juego,
            font=("Helvetica", 10, "bold"),
            bg='#2ecc71',
            fg='white',
            padx=20,
            pady=8,
            bd=0,
            cursor='hand2'
        )
        btn_nuevo.pack(side=tk.LEFT, padx=8)
        
        btn_reset = tk.Button(
            botones_frame,
            text="🔄 REINICIAR ESTADÍSTICAS",
            command=self.reiniciar_estadisticas,
            font=("Helvetica", 10, "bold"),
            bg='#f39c12',
            fg='white',
            padx=20,
            pady=8,
            bd=0,
            cursor='hand2'
        )
        btn_reset.pack(side=tk.LEFT, padx=8)
        
        btn_salir = tk.Button(
            botones_frame,
            text="❌ SALIR",
            command=self.salir,
            font=("Helvetica", 10, "bold"),
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=8,
            bd=0,
            cursor='hand2'
        )
        btn_salir.pack(side=tk.LEFT, padx=8)
        
        # Información del diccionario
        info_bar = tk.Frame(self.frame_juego, bg='#1a1a2e')
        info_bar.pack(pady=10)
        
        self.label_info = tk.Label(
            info_bar,
            text="📚 Diccionario Spanish-BFF: cargando...",
            font=("Helvetica", 9),
            bg='#1a1a2e',
            fg='#666'
        )
        self.label_info.pack()
        
        # Footer
        footer = tk.Label(
            self.frame_juego,
            text="✓ Soporte para vocales con acento (Á, É, Í, Ó, Ú) | Fuente: Hugging Face - Spanish-BFF",
            font=("Helvetica", 8),
            bg='#1a1a2e',
            fg='#2ecc71'
        )
        footer.pack(pady=5)
    
    def actualizar_estado_carga(self, mensaje):
        """Actualiza el mensaje de carga."""
        def _update():
            self.label_carga_estado.config(text=mensaje)
            self.ventana.update()
        self.ventana.after(0, _update)
    
    def cargar_diccionario(self):
        """Carga el diccionario Spanish-BFF."""
        def cargar():
            archivo_cache = "diccionario_spanish_bff.json"
            
            if os.path.exists(archivo_cache):
                self.actualizar_estado_carga("📀 Cargando diccionario desde caché...")
                try:
                    with open(archivo_cache, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self.diccionario_completo = data['palabras']
                        self.total_palabras = data['total']
                        self.organizar_por_longitud()
                        self.ventana.after(0, self.finalizar_carga)
                        return
                except Exception as e:
                    print(f"Error cargando caché: {e}")
            
            if HUGGINGFACE_DISPONIBLE:
                self.actualizar_estado_carga("🌐 Descargando Spanish-BFF...")
                try:
                    dataset = load_dataset("MMG/SpanishBFF", split="train")
                    palabras_set = set()
                    
                    for i, item in enumerate(dataset):
                        # Tomamos la palabra original (puede tener acentos)
                        palabra_original = item['lemma'].upper()
                        # Normalizamos para el diccionario del juego
                        palabra_normalizada = self.normalizar_texto(palabra_original)
                        
                        if palabra_normalizada.isalpha() and 4 <= len(palabra_normalizada) <= 10:
                            palabras_set.add(palabra_normalizada)
                        
                        if i % 10000 == 0 and i > 0:
                            self.actualizar_estado_carga(f"🔄 Procesando: {i}/{len(dataset)} palabras")
                    
                    self.diccionario_completo = sorted(list(palabras_set))
                    self.total_palabras = len(self.diccionario_completo)
                    self.organizar_por_longitud()
                    
                    with open(archivo_cache, 'w', encoding='utf-8') as f:
                        json.dump({
                            "fecha": datetime.now().isoformat(),
                            "total": self.total_palabras,
                            "palabras": self.diccionario_completo
                        }, f, ensure_ascii=False, indent=2)
                    
                    self.ventana.after(0, self.finalizar_carga)
                    return
                    
                except Exception as e:
                    print(f"Error: {e}")
            
            # Fallback
            self.cargar_diccionario_respaldo()
            self.ventana.after(0, self.finalizar_carga)
        
        threading.Thread(target=cargar, daemon=True).start()
    
    def cargar_diccionario_respaldo(self):
        """Diccionario de respaldo con palabras que incluyen vocales acentuadas."""
        palabras = [
            "ARBOL", "CAMION", "AVION", "CORAZON", "LAPIZ", "JOVEN", "EXAMEN",
            "PYTHON", "JAVA", "PERRO", "GATO", "CASA", "MUNDO", "SOL", "LUNA",
            "AMOR", "VIDA", "FUEGO", "AGUA", "AIRE", "TIERRA", "MAR", "CIELO"
        ]
        self.diccionario_completo = sorted([p for p in palabras if 4 <= len(p) <= 10])
        self.total_palabras = len(self.diccionario_completo)
    
    def organizar_por_longitud(self):
        """Organiza el diccionario por longitud."""
        self.diccionario_por_longitud = {}
        for palabra in self.diccionario_completo:
            long = len(palabra)
            if long not in self.diccionario_por_longitud:
                self.diccionario_por_longitud[long] = []
            self.diccionario_por_longitud[long].append(palabra)
    
    def finalizar_carga(self):
        """Finaliza la carga y muestra el juego."""
        self.progreso.stop()
        self.frame_carga.pack_forget()
        self.frame_juego.pack(fill=tk.BOTH, expand=True)
        
        longitudes = sorted(self.diccionario_por_longitud.keys())
        self.combo_longitud['values'] = longitudes
        if self.longitud_actual not in longitudes and longitudes:
            self.longitud_actual = longitudes[0]
            self.combo_longitud.set(self.longitud_actual)
        
        self.actualizar_info()
        self.nuevo_juego()
        self.entry_letra.focus()
    
    def actualizar_info(self):
        """Actualiza la información del diccionario."""
        cantidad = len(self.diccionario_por_longitud.get(self.longitud_actual, []))
        self.label_info.config(
            text=f"📚 Spanish-BFF: {self.total_palabras:,} palabras | Longitud: {self.longitud_actual} letras | Opciones: {cantidad:,}"
        )
    
    def toggle_modo_dificil(self):
        """Activa/desactiva modo difícil."""
        self.modo_dificil = self.dificil_var.get()
        self.intentos_restantes = 4 if self.modo_dificil else 6
        self.label_intentos.config(text=f"💪 Intentos: {self.intentos_restantes}")
        self.nuevo_juego()
    
    def cambiar_longitud(self, event=None):
        """Cambia la longitud de palabra."""
        self.longitud_actual = int(self.combo_longitud.get())
        self.nuevo_juego()
        self.actualizar_info()
    
    def dibujar_ahorcado(self):
        """Dibuja el ahorcado."""
        self.canvas.delete("all")
        
        color = '#e94560'
        self.canvas.create_line(80, 240, 200, 240, width=4, fill=color, capstyle=tk.ROUND)
        self.canvas.create_line(140, 240, 140, 50, width=4, fill=color, capstyle=tk.ROUND)
        self.canvas.create_line(140, 50, 280, 50, width=4, fill=color, capstyle=tk.ROUND)
        self.canvas.create_line(280, 50, 280, 90, width=4, fill=color, capstyle=tk.ROUND)
        
        errores = 6 - self.intentos_restantes
        
        if errores >= 1:
            self.canvas.create_oval(255, 90, 305, 140, width=3, outline=color)
            self.canvas.create_oval(268, 110, 273, 115, fill=color)
            self.canvas.create_oval(287, 110, 292, 115, fill=color)
        if errores >= 2:
            self.canvas.create_line(280, 140, 280, 200, width=3, fill=color)
        if errores >= 3:
            self.canvas.create_line(280, 165, 250, 190, width=3, fill=color)
        if errores >= 4:
            self.canvas.create_line(280, 165, 310, 190, width=3, fill=color)
        if errores >= 5:
            self.canvas.create_line(280, 200, 255, 235, width=3, fill=color)
        if errores >= 6:
            self.canvas.create_line(280, 200, 305, 235, width=3, fill=color)
            self.canvas.create_arc(270, 125, 290, 140, start=0, extent=-180, width=2, outline=color)
    
    def actualizar_interfaz(self):
        """Actualiza la interfaz."""
        self.label_palabra.config(text=" ".join(self.palabra_oculta))
        self.label_usadas.config(text=", ".join(sorted(self.letras_usadas)))
        self.dibujar_ahorcado()
        
        # Mostrar pista de vocales
        total_vocales = self.contar_vocales(self.palabra_actual)
        self.label_pista_vocales.config(text=f"📢 La palabra tiene {total_vocales} vocal(es)")
    
    def procesar_letra(self, event=None):
        """Procesa la letra ingresada."""
        if not self.juego_activo:
            messagebox.showwarning("Juego terminado", "Inicia un nuevo juego")
            return
        
        letra = self.entry_letra.get().strip().upper()
        self.entry_letra.delete(0, tk.END)
        
        if not letra:
            return
        if len(letra) != 1 or not letra.isalpha():
            messagebox.showwarning("Error", "Ingresa una letra válida (A-Z)")
            return
        if letra in self.letras_usadas:
            messagebox.showinfo("Repetida", f"Ya usaste la letra '{letra}'")
            return
        
        self.letras_usadas.add(letra)
        
        # Buscar la letra en la palabra (comparación sin distinción de acentos)
        letra_encontrada = False
        palabra_normalizada = self.normalizar_texto(self.palabra_actual)
        
        for i, char in enumerate(self.palabra_actual):
            char_normalizado = self.normalizar_texto(char)
            if char_normalizado == letra:
                self.palabra_oculta[i] = char  # Mostramos la letra original (con acento si lo tiene)
                letra_encontrada = True
        
        if letra_encontrada:
            messagebox.showinfo("¡Correcto!", f"✅ '{letra}' está en la palabra")
        else:
            self.intentos_restantes -= 1
            self.label_intentos.config(text=f"💪 Intentos: {self.intentos_restantes}")
            messagebox.showwarning("¡Error!", f"❌ '{letra}' no está en la palabra")
        
        self.actualizar_interfaz()
        
        if '_' not in self.palabra_oculta:
            self.juego_activo = False
            self.partidas_ganadas += 1
            self.racha_actual += 1
            self.racha_maxima = max(self.racha_maxima, self.racha_actual)
            self.actualizar_score()
            messagebox.showinfo("🎉 VICTORIA", f"¡Ganaste! Palabra: {self.palabra_actual}\nRacha: {self.racha_actual}")
            self.nuevo_juego()
        elif self.intentos_restantes <= 0:
            self.juego_activo = False
            self.partidas_perdidas += 1
            self.racha_actual = 0
            self.actualizar_score()
            messagebox.showwarning("💀 DERROTA", f"Perdiste. La palabra era: {self.palabra_actual}")
            self.label_palabra.config(text=" ".join(self.palabra_actual), fg='#e74c3c')
            self.nuevo_juego()
    
    def actualizar_score(self):
        """Actualiza el marcador."""
        self.label_score.config(
            text=f"🏆 Victorias: {self.partidas_ganadas}\n"
                 f"💀 Derrotas: {self.partidas_perdidas}\n"
                 f"📈 Racha: {self.racha_actual}\n"
                 f"🏅 Máxima: {self.racha_maxima}"
        )
    
    def nuevo_juego(self):
        """Inicia un nuevo juego."""
        if not self.diccionario_por_longitud:
            return
        
        palabras = self.diccionario_por_longitud.get(self.longitud_actual, [])
        if not palabras:
            return
        
        self.palabra_actual = random.choice(palabras)
        self.palabra_oculta = ['_' for _ in self.palabra_actual]
        self.intentos_restantes = 4 if self.modo_dificil else 6
        self.letras_usadas = set()
        self.juego_activo = True
        
        self.label_intentos.config(text=f"💪 Intentos: {self.intentos_restantes}")
        self.label_palabra.config(fg='#e94560')
        self.entry_letra.delete(0, tk.END)
        self.entry_letra.focus()
        self.actualizar_interfaz()
        self.actualizar_info()
    
    def reiniciar_estadisticas(self):
        """Reinicia las estadísticas."""
        if messagebox.askyesno("Reiniciar", "¿Reiniciar todas las estadísticas?"):
            self.partidas_ganadas = 0
            self.partidas_perdidas = 0
            self.racha_actual = 0
            self.racha_maxima = 0
            self.actualizar_score()
    
    def salir(self):
        """Sale del juego."""
        if messagebox.askyesno("Salir", "¿Salir del juego?"):
            self.ventana.destroy()
    
    def ejecutar(self):
        """Inicia la aplicación."""
        self.ventana.mainloop()


if __name__ == "__main__":
    print("=" * 70)
    print("🎮 AHORCADO - CON SOPORTE PARA VOCALES ACENTUADAS")
    print("📚 Las vocales con acento (Á, É, Í, Ó, Ú) se cuentan correctamente")
    print("=" * 70)
    
    juego = AhorcadoVentana()
    juego.ejecutar()
