# pyrefly: ignore [missing-import]
import customtkinter as ctk
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Config.user_config import cargar_configuracion
from Gui.welcome_screen import WelcomeWindow
from Core.command_bank import COMANDOS_DISPONIBLES

# Configuración global del tema visual de CustomTkinter
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("dark-blue") 

# Colores personalizados de la interfaz
COLOR_ACENTO = "#5e5ce6" 
COLOR_BG_MENU = "#121212"

# =====================================================================
# CLASE PRINCIPAL: Ventana y controlador de VisionCore
# =====================================================================
class VisionCoreApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Configuración básica de la ventana principal
        self.title("VisionCore v1.0 - Agente de Aprendizaje")
        self.geometry("1300x850")
        self.ia_configurada = False
        
        # Configuración de la cuadrícula (Grid) para que la ventana sea responsiva
        self.grid_columnconfigure(0, weight=0) # Menú lateral con ancho fijo
        self.grid_columnconfigure(1, weight=1) # Área de trabajo se expande para llenar
        self.grid_rowconfigure(0, weight=1)

        # --- MENÚ LATERAL (Contenedor fijo: logo y buscador) ---
        self.menu_frame = ctk.CTkFrame(self, width=270, corner_radius=0, fg_color=COLOR_BG_MENU)
        self.menu_frame.grid(row=0, column=0, sticky="nsew")
        self.menu_frame.grid_propagate(False)
        # El menú lateral se estructura con grid internamente para controlar el espacio
        self.menu_frame.grid_rowconfigure(4, weight=1)  # La fila del scroll se expande
        self.menu_frame.grid_columnconfigure(0, weight=1)

        self.logo_label = ctk.CTkLabel(self.menu_frame, text="VISIONCORE", font=ctk.CTkFont(size=28, weight="bold"), text_color=COLOR_ACENTO)
        self.logo_label.grid(row=0, column=0, pady=(30, 15), padx=20)

        self.btn_ia_setup = ctk.CTkButton(
            self.menu_frame, 
            text="🧠 Configurar Agente", 
            fg_color="transparent", 
            border_width=1, border_color="#4c566a",
            hover_color="#2e3440", 
            command=self.abrir_ventana_ia
        )
        self.btn_ia_setup.grid(row=1, column=0, pady=(0, 10), padx=20, sticky="ew")

        # --- BARRA DE BÚSQUEDA ---
        self.search_entry = ctk.CTkEntry(
            self.menu_frame, 
            placeholder_text="🔍  Buscar comando...",
            fg_color="#1e1e1e", border_color="#3b4252",
            text_color="#d8dee9"
        )
        self.search_entry.grid(row=2, column=0, pady=(0, 8), padx=15, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.filtrar_comandos)

        ctk.CTkFrame(self.menu_frame, height=1, fg_color="#2e3440").grid(row=3, column=0, sticky="ew", padx=15, pady=0)

        # --- ÁREA DESPLAZABLE PARA LOS NIVELES Y COMANDOS ---
        self.scrollable_menu = ctk.CTkScrollableFrame(
            self.menu_frame, fg_color="transparent",
            scrollbar_button_color="#3b4252",
            scrollbar_button_hover_color="#4c566a"
        )
        self.scrollable_menu.grid(row=4, column=0, sticky="nsew", padx=0, pady=0)
        self.scrollable_menu.grid_columnconfigure(0, weight=1)

        # --- NIVELES DE AUDITORÍA (APRENDIZAJE) dentro del área scrollable ---
        
        # 1. Reconocimiento Básico (🟢)
        self.btn_basico_master = ctk.CTkButton(
            self.scrollable_menu, 
            text="🟢  1. Reconocimiento Básico", 
            anchor="w", fg_color="transparent", hover_color="#27272a",
            font=ctk.CTkFont(size=13, weight="bold"), text_color="#4c566a",
            command=self.toggle_basico_menu
        )
        self.btn_basico_master.pack(pady=(10, 2), padx=10, fill="x")
        
        self.basico_commands_frame = ctk.CTkFrame(self.scrollable_menu, fg_color="transparent")
        # NO hacemos pack aquí; el toggle lo maneja

        # 2. Enumeración Intermedia (🟡)
        self.btn_intermedio_master = ctk.CTkButton(
            self.scrollable_menu, 
            text="🟡  2. Enumeración Intermedia", 
            anchor="w", fg_color="transparent", hover_color="#27272a",
            font=ctk.CTkFont(size=13, weight="bold"), text_color="#4c566a",
            command=self.toggle_intermedio_menu
        )
        self.btn_intermedio_master.pack(pady=2, padx=10, fill="x")
        
        self.intermedio_commands_frame = ctk.CTkFrame(self.scrollable_menu, fg_color="transparent")
        # NO hacemos pack aquí; el toggle lo maneja

        # 3. Auditoría Avanzada (🔴)
        self.btn_avanzado_master = ctk.CTkButton(
            self.scrollable_menu, 
            text="🔴  3. Auditoría Avanzada", 
            anchor="w", fg_color="transparent", hover_color="#27272a",
            font=ctk.CTkFont(size=13, weight="bold"), text_color="#4c566a",
            command=self.toggle_avanzado_menu
        )
        self.btn_avanzado_master.pack(pady=2, padx=10, fill="x")
        
        self.avanzado_commands_frame = ctk.CTkFrame(self.scrollable_menu, fg_color="transparent")
        # NO hacemos pack aquí; el toggle lo maneja

        # Guardamos referencias a los botones individuales para el buscador
        self.botones_comando = []

        # Rellenar dinámicamente los comandos por nivel
        for cmd in COMANDOS_DISPONIBLES:
            if cmd["nivel"] == "Basico":
                target_frame = self.basico_commands_frame
            elif cmd["nivel"] == "Intermedio":
                target_frame = self.intermedio_commands_frame
            else:
                target_frame = self.avanzado_commands_frame

            # Solo el comando "nmap -sS" (Escaneo simple de puertos) es funcional por ahora.
            # Los demás comandos están vacíos (con marcadores para funciones futuras).
            es_funcional = (cmd["comando"] == "nmap -sS")

            if es_funcional:
                cmd_callback = lambda c=cmd: self.iniciar_comando_consola(c["comando"])
                btn_text = cmd["nombre"]
                text_color = "#81a1c1"  # Color azul para el comando activo
            else:
                cmd_callback = lambda c=cmd: self.ejecutar_comando_futuro_placeholder(c["nombre"])
                btn_text = f"{cmd['nombre']}"
                text_color = "#4c566a"  # Gris para indicar módulo pendiente

            btn = ctk.CTkButton(
                target_frame, 
                text=btn_text, 
                anchor="w", fg_color="transparent", hover_color="#1e222a",
                text_color=text_color, font=("Arial", 11),
                command=cmd_callback
            )
            btn.pack(pady=2, padx=(20, 10), fill="x")
            # Guardamos referencia para filtrar en la búsqueda
            self.botones_comando.append({"btn": btn, "nombre": cmd["nombre"].lower(), "nivel": cmd["nivel"], "frame": target_frame})

        # --- BARRA DE PROGRESO (parte inferior del menú, fija) ---
        self.progress_frame = ctk.CTkFrame(self.menu_frame, fg_color="#1a1a1a", height=55, corner_radius=0)
        self.progress_frame.grid(row=5, column=0, sticky="ew", padx=0, pady=0)
        self.progress_frame.grid_propagate(False)
        self.progress_frame.grid_columnconfigure(0, weight=1)

        self.progress_label = ctk.CTkLabel(self.progress_frame, text="Listo", text_color="#4c566a", font=("Consolas", 10))
        self.progress_label.grid(row=0, column=0, sticky="w", padx=12, pady=(6, 2))

        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, progress_color=COLOR_ACENTO, fg_color="#2e3440", height=6)
        self.progress_bar.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 8))
        self.progress_bar.set(0)

        # --- ÁREA DE TRABAJO ---
        self.workspace_frame = ctk.CTkFrame(self, fg_color="#000000")
        self.workspace_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.workspace_frame.grid_rowconfigure(0, weight=0)
        self.workspace_frame.grid_rowconfigure(1, weight=1)
        self.workspace_frame.grid_rowconfigure(2, weight=1)
        self.workspace_frame.grid_columnconfigure(0, weight=1)

        self.header_frame = ctk.CTkFrame(self.workspace_frame, fg_color="transparent", height=50)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 10))
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.btn_help = ctk.CTkButton(self.header_frame, text="❓ Ayuda", width=80, fg_color="transparent", border_width=1, border_color="#4c566a", hover_color="#2e3440", command=self.funcion_futura)
        self.btn_help.grid(row=0, column=1, padx=5)
        self.btn_settings = ctk.CTkButton(self.header_frame, text="⚙️ Config", width=80, fg_color="transparent", border_width=1, border_color="#4c566a", hover_color="#2e3440", command=self.funcion_futura)
        self.btn_settings.grid(row=0, column=2, padx=5)

        self.console_frame = ctk.CTkFrame(self.workspace_frame, fg_color="#0a0a0a", corner_radius=8, border_width=1, border_color="#2e3440")
        self.console_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.header_console = ctk.CTkFrame(self.console_frame, fg_color="transparent")
        self.header_console.pack(fill="x", padx=15, pady=(10, 5))
        self.console_label = ctk.CTkLabel(self.header_console, text="[ TERMINAL DE EJECUCIÓN ]", text_color="#d8dee9", font=("Consolas", 13, "bold"))
        self.console_label.pack(side="left")
        self.btn_clear_console = ctk.CTkButton(self.header_console, text="Limpiar", width=70, fg_color="transparent", border_width=1, border_color="#4c566a", hover_color="#2e3440", command=self.limpiar_consola)
        self.btn_clear_console.pack(side="right")
        self.console_output = ctk.CTkTextbox(self.console_frame, fg_color="#000000", text_color="#e5e9f0", font=("Consolas", 13), corner_radius=6, border_width=0, state="disabled")
        self.console_output.pack(expand=True, fill="both", padx=10, pady=(0, 10))

        # Contenedor del Motor de Análisis de IA (Consola de IA)
        self.ia_frame = ctk.CTkFrame(self.workspace_frame, fg_color="#0a0a0a", corner_radius=8, border_width=1, border_color="#2e3440")
        self.ia_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(10, 20))
        
        # Encabezado del Motor de Análisis de IA
        self.header_ia = ctk.CTkFrame(self.ia_frame, fg_color="transparent")
        self.header_ia.pack(fill="x", padx=15, pady=(10, 5))
        
        self.ia_label = ctk.CTkLabel(self.header_ia, text="[ MOTOR DE ANÁLISIS ]", text_color="#88C0D0", font=("Consolas", 13, "bold"))
        self.ia_label.pack(side="left")
        
        # Botón para guardar el resultado del análisis (función futura)
        self.btn_save_ia = ctk.CTkButton(
            self.header_ia, 
            text="💾 Guardar", 
            width=80, 
            fg_color="transparent", 
            border_width=1, 
            border_color="#4c566a", 
            hover_color="#2e3440", 
            command=self.guardar_resultado_ia
        )
        self.btn_save_ia.pack(side="right")
        
        # Caja de texto para el resultado del análisis de IA
        self.ia_output = ctk.CTkTextbox(self.ia_frame, fg_color="#000000", text_color="#e5e9f0", font=("Consolas", 13), corner_radius=6, border_width=0)
        self.ia_output.pack(expand=True, fill="both", padx=10, pady=(0, 10))
        
        # Configuración de tags de color para la IA (sin 'font' para evitar problemas de escalado de CustomTkinter)
        self.ia_output.tag_config("titulo", foreground="#88c0d0")      # Cyan
        self.ia_output.tag_config("parametro", foreground="#ebcb8b")   # Amarillo/Naranja
        self.ia_output.tag_config("clave", foreground="#a3be8c")       # Verde
        self.ia_output.tag_config("normal", foreground="#e5e9f0")      # Blanco

        self.after(500, self.verificar_estado_inicial)

    # --- LÓGICA ---
    def verificar_estado_inicial(self):
        config = cargar_configuracion()
        if config["endpoint"] != "":
            self.ia_configurada = True
            self.mostrar_bienvenida()
            self.actualizar_estado_menu()
        else:
            WelcomeWindow(self, self.on_ia_configured)
            self.mostrar_bienvenida_desde_python()

    def on_ia_configured(self):
        self.ia_configurada = True
        self.actualizar_estado_menu()
        self.mostrar_bienvenida()

    def actualizar_estado_menu(self):
        self.btn_basico_master.configure(text_color="#d8dee9", state="normal")
        self.btn_intermedio_master.configure(text_color="#d8dee9", state="normal")
        self.btn_avanzado_master.configure(text_color="#d8dee9", state="normal")
        self.btn_ia_setup.configure(fg_color="#2e3440", border_width=0)

    def limpiar_consola(self):
        self.console_output.configure(state="normal")
        self.console_output.delete("1.0", "end")
        self.console_output.configure(state="disabled")

    def toggle_basico_menu(self):
        if not self.ia_configurada:
            self.mostrar_aviso_ia_bloqueada()
            return
        if self.basico_commands_frame.winfo_ismapped():
            self.basico_commands_frame.pack_forget()
            self.btn_basico_master.configure(text="🟢  1. Reconocimiento Básico")
        else:
            # Insertamos en el orden correcto dentro del scrollable: después del btn_basico
            self.basico_commands_frame.pack(after=self.btn_basico_master, fill="x", padx=0, pady=(0, 4))
            self.btn_basico_master.configure(text="▼ 🟢  1. Reconocimiento Básico")

    def toggle_intermedio_menu(self):
        if not self.ia_configurada:
            self.mostrar_aviso_ia_bloqueada()
            return
        if self.intermedio_commands_frame.winfo_ismapped():
            self.intermedio_commands_frame.pack_forget()
            self.btn_intermedio_master.configure(text="🟡  2. Enumeración Intermedia")
        else:
            self.intermedio_commands_frame.pack(after=self.btn_intermedio_master, fill="x", padx=0, pady=(0, 4))
            self.btn_intermedio_master.configure(text="▼ 🟡  2. Enumeración Intermedia")

    def toggle_avanzado_menu(self):
        if not self.ia_configurada:
            self.mostrar_aviso_ia_bloqueada()
            return
        if self.avanzado_commands_frame.winfo_ismapped():
            self.avanzado_commands_frame.pack_forget()
            self.btn_avanzado_master.configure(text="🔴  3. Auditoría Avanzada")
        else:
            self.avanzado_commands_frame.pack(after=self.btn_avanzado_master, fill="x", padx=0, pady=(0, 4))
            self.btn_avanzado_master.configure(text="▼ 🔴  3. Auditoría Avanzada")

    def mostrar_aviso_ia_bloqueada(self):
        self.console_output.configure(state="normal")
        self.console_output.insert("end", "\n[!] Acción bloqueada. Configura el Agente IA.\n")
        self.console_output.see("end")
        self.console_output.configure(state="disabled")

    def filtrar_comandos(self, event=None):
        """
        Filtra los botones de comandos en el menú según el texto del campo de búsqueda.
        Si la búsqueda está vacía, colapsa todos los menús y los muestra normales.
        """
        query = self.search_entry.get().strip().lower()

        if not query:
            # Sin búsqueda: ocultar todos los frames de comandos
            self.basico_commands_frame.pack_forget()
            self.intermedio_commands_frame.pack_forget()
            self.avanzado_commands_frame.pack_forget()
            self.btn_basico_master.configure(text="🟢  1. Reconocimiento Básico")
            self.btn_intermedio_master.configure(text="🟡  2. Enumeración Intermedia")
            self.btn_avanzado_master.configure(text="🔴  3. Auditoría Avanzada")
            for item in self.botones_comando:
                item["btn"].pack(pady=2, padx=(20, 10), fill="x")
            return

        # Con búsqueda: expandir todo y mostrar solo los que coincidan
        for frame in [self.basico_commands_frame, self.intermedio_commands_frame, self.avanzado_commands_frame]:
            if not frame.winfo_ismapped():
                frame.pack(fill="x", padx=0, pady=(0, 4))
        self.btn_basico_master.configure(text="▼ 🟢  1. Reconocimiento Básico")
        self.btn_intermedio_master.configure(text="▼ 🟡  2. Enumeración Intermedia")
        self.btn_avanzado_master.configure(text="▼ 🔴  3. Auditoría Avanzada")

        for item in self.botones_comando:
            if query in item["nombre"]:
                item["btn"].pack(pady=2, padx=(20, 10), fill="x")
            else:
                item["btn"].pack_forget()

    def ejecutar_comando_futuro_placeholder(self, nombre_comando):
        """
        Manejador para comandos del plan de estudio que se implementarán en el futuro.
        """
        self.console_output.configure(state="normal")
        self.console_output.delete("1.0", "end")
        
        self.console_output.insert("end", "="*70 + "\n")
        self.console_output.insert("end", f" 🔒 MÓDULO PENDIENTE: {nombre_comando.upper()}\n")
        self.console_output.insert("end", "="*70 + "\n\n")
        self.console_output.insert("end", ">> Este comando forma parte del plan de estudios futuro de VisionCore.\n")
        self.console_output.insert("end", ">> La lógica de ejecución en Docker y análisis de IA se integrará próximamente.\n")
        self.console_output.insert("end", ">> Por ahora, puedes practicar con el 'Escaneo simple de puertos (TCP SYN)' en el Nivel 2.\n")
        
        self.console_output.see("end")
        self.console_output.configure(state="disabled")

    def mostrar_bienvenida_desde_python(self):
        self.console_output.configure(state="normal")
        self.console_output.delete("1.0", "end")
        ruta_ascii = "assets/VisionCore_ASCII.txt"
        ascii_text = ""
        if os.path.exists(ruta_ascii):
            with open(ruta_ascii, "r", encoding="utf-8") as f:
                ascii_text = f.read()
        else:
            ascii_text = "ERROR: No se encontró el archivo ASCII."
        
        self.console_output.insert("end", ascii_text + "\n\n")
        self.console_output.insert("end", ">> AVISO: Agente IA no configurado.\n")
        self.console_output.insert("end", ">> Acción requerida: Configurar Agente en el menú lateral.\n")
        self.console_output.see("end")
        self.console_output.configure(state="disabled")

    def mostrar_bienvenida(self):
        self.console_output.configure(state="normal")
        self.console_output.delete("1.0", "end")
        ruta_ascii = "assets/VisionCore_ASCII.txt"
        ascii_text = ""
        if os.path.exists(ruta_ascii):
            with open(ruta_ascii, "r", encoding="utf-8") as f:
                ascii_text = f.read()
        else:
            ascii_text = "ERROR: No se encontró el archivo ASCII."
        
        self.console_output.insert("end", ascii_text + "\n\n")
        self.console_output.insert("end", "[✓] Motor de IA conectado.\n")
        self.console_output.insert("end", "[>] Expande un nivel del menú izquierdo para ver los comandos disponibles.\n")
        self.console_output.see("end")
        self.console_output.configure(state="disabled")

    def abrir_ventana_ia(self):
        print("Función futura: Abrir ventana para cambiar de IA.")

    def funcion_futura(self):
        print("Botón presionado. Función futura pendiente de implementar.")

    def guardar_resultado_ia(self):
        # ==========================================================
        # FUNCIÓN FUTURA: Guardar resultado del análisis de IA
        # Aquí se implementará la lógica para guardar el contenido
        # de `self.ia_output` en un archivo de texto o base de datos.
        # ==========================================================
        print("Guardar resultado presionado. Lógica para guardar análisis pendiente.")
        
    def mostrar_analisis_ia(self, texto_ia):
        """
        Parsea la respuesta formateada de la IA (con etiquetas [TITULO], [PARAM], [CLAVE], [NORMAL])
        e inserta el texto con colores y estilos personalizados en la consola de IA.
        """
        self.ia_output.configure(state="normal")
        self.ia_output.delete("1.0", "end")
        
        lineas = texto_ia.split("\n")
        for linea in lineas:
            linea_strip = linea.strip()
            if not linea_strip:
                self.ia_output.insert("end", "\n")
                continue
                
            # Procesamos según la etiqueta
            if linea.startswith("[TITULO]"):
                contenido = linea.replace("[TITULO]", "").strip()
                self.ia_output.insert("end", "\n" + contenido + "\n", "titulo")
            elif linea.startswith("[PARAM]"):
                contenido = linea.replace("[PARAM]", "").strip()
                self.ia_output.insert("end", "  " + contenido + "\n", "parametro")
            elif linea.startswith("[CLAVE]"):
                contenido = linea.replace("[CLAVE]", "").strip()
                self.ia_output.insert("end", "  " + contenido + "\n", "clave")
            elif linea.startswith("[NORMAL]"):
                contenido = linea.replace("[NORMAL]", "").strip()
                self.ia_output.insert("end", contenido + "\n", "normal")
            else:
                # Fallback por si acaso la línea no trae etiqueta
                self.ia_output.insert("end", linea + "\n", "normal")
                
        self.ia_output.configure(state="disabled")
        self.ia_output.see("1.0") # Regresa al inicio del texto para leer desde el principio
        
    # ==========================================
    # NUEVO SISTEMA DE ENTRADA POR CONSOLA
    # ==========================================
    def iniciar_comando_consola(self, comando_base):
        # Limpiamos la consola
        self.console_output.configure(state="normal")
        self.console_output.delete("1.0", "end")
        
        # Mostramos una guía interactiva y explicativa de la terminal
        self.console_output.insert("end", "="*70 + "\n")
        self.console_output.insert("end", " 💻 TERMINAL INTERACTIVA - DEBIAN CONTAINER\n")
        self.console_output.insert("end", "="*70 + "\n")
        self.console_output.insert("end", f" Comando base seleccionado: {comando_base}\n\n")
        self.console_output.insert("end", " Para ejecutar este comando, necesitas ingresar un 'objetivo' (IP o dominio).\n")
        self.console_output.insert("end", " • Ejemplo de IP: 192.168.1.1  (IP privada / red local)\n")
        self.console_output.insert("end", " • Ejemplo de dominio: scanme.nmap.org  (Sitio de pruebas de Nmap)\n\n")
        self.console_output.insert("end", " 💡 ¿CÓMO HACERLO?\n")
        self.console_output.insert("end", f" Escribe la IP o dominio objetivo al final de la línea del prompt 'debian@orioncore:~#'.\n")
        self.console_output.insert("end", f" Por ejemplo, para escanear la IP '192.168.1.1', debes completarlo para que se vea así:\n")
        self.console_output.insert("end", f"   debian@orioncore:~$ {comando_base} 192.168.1.1\n")
        self.console_output.insert("end", " Y luego presiona la tecla [ENTER] para iniciar la ejecución.\n")
        self.console_output.insert("end", "="*70 + "\n\n")
        
        # El prompt de terminal simulado donde el usuario escribirá
        prompt_text = f"debian@orioncore:~$ {comando_base} "
        self.console_output.insert("end", prompt_text)
        
        # Guardamos el comando base para usarlo después
        self.comando_pendiente = comando_base
        self.consola_modo_entrada = True
        
        # Colocamos el cursor al final de la línea y enfocamos la consola
        self.console_output.see("end")
        self.console_output.focus_set()

    def ejecutar_comando_universal(self, comando_base, objetivo):
        # Esta función se llama desde el evento de teclado (Enter)
        self.console_output.configure(state="normal")
        self.console_output.insert("end", f"\n[>] Objetivo ingresado: {objetivo}\n")
        self.console_output.insert("end", "[*] Iniciando escaneo en el contenedor Debian...\n")
        self.console_output.see("end")
        self.console_output.configure(state="disabled")
        
        # Activar barra de progreso animada
        self.progress_label.configure(text=f"Escaneando: {objetivo}...", text_color="#88c0d0")
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()
        self.update()

        from Core.orchestrator import ejecutar_flujo_completo
        resultado = ejecutar_flujo_completo(comando_base, objetivo, max_intentos=2)

        self.console_output.configure(state="normal")
        
        if resultado["exito"]:
            self.console_output.insert("end", "\n" + "="*50 + "\n")
            self.console_output.insert("end", resultado["output_docker"])
            self.console_output.insert("end", "\n" + "="*50 + "\n")
            self.console_output.insert("end", "[✓] Escaneo completado.\n")
            
            self.mostrar_analisis_ia(resultado["output_ia"])
        else:
            self.console_output.insert("end", f"\n[!] Error: {resultado['error']}\n")
            if resultado["output_ia"]:
                self.mostrar_analisis_ia(
                    "[TITULO] Error de Análisis\n"
                    "[CLAVE] • El comando falló o la IA experimentó un error.\n"
                    f"[NORMAL] Detalles: {resultado['output_ia']}"
                )

        self.console_output.see("end")
        self.console_output.configure(state="disabled")
        
        # Detener y resetear la barra de progreso
        self.progress_bar.stop()
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.set(1 if resultado["exito"] else 0)
        self.progress_label.configure(
            text="✓ Escaneo completado" if resultado["exito"] else "[!] Error en el escaneo",
            text_color="#a3be8c" if resultado["exito"] else "#bf616a"
        )
        
        self.ia_output.configure(state="disabled")
        self.consola_modo_entrada = False

    # ==========================================
    # CAPTURADOR DE TECLADO (El truco para la entrada en la consola)
    # ==========================================
    def bind_consola_event(self):
        self.console_output.bind("<Return>", self.capturar_enter)

    def capturar_enter(self, event):
        if hasattr(self, 'consola_modo_entrada') and self.consola_modo_entrada:
            # Obtener el texto escrito por el usuario
            texto_completo = self.console_output.get("1.0", "end").strip()
            lineas = texto_completo.split("\n")
            
            if lineas:
                # Obtenemos la última línea donde el usuario interactuó
                ultima_linea = lineas[-1].strip()
                
                # Extraemos el objetivo restándole el prompt y el comando base
                prompt = f"debian@orioncore:~$ {self.comando_pendiente} "
                if ultima_linea.startswith(prompt.strip()):
                    objetivo = ultima_linea[len(prompt.strip()):].strip()
                elif self.comando_pendiente in ultima_linea:
                    parts = ultima_linea.split(self.comando_pendiente)
                    objetivo = parts[-1].strip()
                else:
                    objetivo = ultima_linea.strip()
                
                # Verificar si es un objetivo válido (mínimo 4 caracteres para dominios cortos o 7 para IPs)
                # Ejemplo: localhost (9) o un dominio corto como a.co (4)
                if len(objetivo) >= 4:
                    self.ejecutar_comando_universal(self.comando_pendiente, objetivo)
                else:
                    self.console_output.configure(state="normal")
                    self.console_output.insert("end", "\n[!] Entrada inválida. Escribe una IP o dominio válido.\n")
                    # Restauramos el prompt para volver a intentarlo
                    prompt_text = f"\ndebian@orioncore:~$ {self.comando_pendiente} "
                    self.console_output.insert("end", prompt_text)
                    self.console_output.see("end")
            
            # Retornamos 'break' para evitar que se inserte un salto de línea adicional en el Textbox
            return "break"

if __name__ == "__main__":
    app = VisionCoreApp()
    app.bind_consola_event() # Activamos el evento de teclado
    app.mainloop()