import customtkinter as ctk
from Config.user_config import guardar_configuracion

class WelcomeWindow(ctk.CTkToplevel):
    def __init__(self, parent, on_success_callback):
        super().__init__(parent)
        self.parent = parent
        self.on_success_callback = on_success_callback  # Función que se ejecutará al guardar
        
        self.title("Bienvenido a VisionCore")
        self.geometry("500x520")
        self.attributes("-topmost", True)  # Siempre al frente
        
        # Hacer que la ventana no se pueda cerrar con la X (obligar a configurar)
        self.protocol("WM_DELETE_WINDOW", lambda: None)
        
        ctk.CTkLabel(self, text="🔐 Configuración de Inteligencia Artificial", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        ctk.CTkLabel(self, text="VisionCore necesita un 'cerebro' para explicar los comandos.\nSelecciona tu proveedor e ingresa la API Key correspondiente.", wraplength=450).pack(pady=5)
        
        # Selector de Proveedor
        ctk.CTkLabel(self, text="Proveedor de IA:", anchor="w").pack(fill="x", padx=20, pady=(10, 0))
        self.provider_select = ctk.CTkOptionMenu(
            self, 
            values=["Groq (Recomendado)", "OpenAI", "Ollama (Local)", "Personalizado"],
            command=self.cambiar_proveedor
        )
        self.provider_select.pack(fill="x", padx=20, pady=5)
        
        # Campo de Endpoint
        ctk.CTkLabel(self, text="URL del Endpoint:", anchor="w").pack(fill="x", padx=20, pady=(10, 0))
        self.entry_endpoint = ctk.CTkEntry(self)
        self.entry_endpoint.pack(fill="x", padx=20, pady=5)
        
        # Campo de API Key
        self.lbl_api_key = ctk.CTkLabel(self, text="API Key:", anchor="w")
        self.lbl_api_key.pack(fill="x", padx=20, pady=(10, 0))
        self.entry_api_key = ctk.CTkEntry(self, placeholder_text="gsk-...")
        self.entry_api_key.pack(fill="x", padx=20, pady=5)
        
        self.btn_save = ctk.CTkButton(self, text="Guardar y Comenzar", command=self.guardar_y_cerrar)
        self.btn_save.pack(pady=25)
        
        self.lbl_status = ctk.CTkLabel(self, text="", text_color="orange")
        self.lbl_status.pack()

        # Establecer proveedor inicial por defecto
        self.provider_select.set("Groq (Recomendado)")
        self.cambiar_proveedor("Groq (Recomendado)")

    def cambiar_proveedor(self, valor):
        if valor == "Groq (Recomendado)":
            self.entry_endpoint.configure(state="normal")
            self.entry_endpoint.delete(0, "end")
            self.entry_endpoint.insert(0, "https://api.groq.com/openai/v1")
            self.entry_endpoint.configure(state="readonly")
            self.entry_api_key.configure(state="normal", placeholder_text="gsk_...")
            self.lbl_api_key.configure(text="API Key (Requerido para Groq):")
        elif valor == "OpenAI":
            self.entry_endpoint.configure(state="normal")
            self.entry_endpoint.delete(0, "end")
            self.entry_endpoint.insert(0, "https://api.openai.com/v1")
            self.entry_endpoint.configure(state="readonly")
            self.entry_api_key.configure(state="normal", placeholder_text="sk-...")
            self.lbl_api_key.configure(text="API Key (Requerido para OpenAI):")
        elif valor == "Ollama (Local)":
            self.entry_endpoint.configure(state="normal")
            self.entry_endpoint.delete(0, "end")
            self.entry_endpoint.insert(0, "http://localhost:11434/v1")
            self.entry_endpoint.configure(state="readonly")
            self.entry_api_key.delete(0, "end")
            self.entry_api_key.configure(state="normal", placeholder_text="No se necesita API Key")
            self.lbl_api_key.configure(text="API Key (Opcional):")
        elif valor == "Personalizado":
            self.entry_endpoint.configure(state="normal")
            self.entry_endpoint.delete(0, "end")
            self.entry_endpoint.configure(placeholder_text="https://tu-endpoint-compatible-con-openai/v1")
            self.entry_api_key.configure(state="normal", placeholder_text="api-key")
            self.lbl_api_key.configure(text="API Key:")

    def guardar_y_cerrar(self):
        # Obtenemos el valor de la caja de texto (aunque esté en modo readonly)
        endpoint = self.entry_endpoint.get().strip()
        api_key = self.entry_api_key.get().strip()
        
        if not endpoint:
            self.lbl_status.configure(text="Error: Debes ingresar una URL de Endpoint.", text_color="red")
            return
            
        # Guardar en el JSON
        guardar_configuracion(api_key, endpoint)
        self.lbl_status.configure(text="✅ Configuración guardada. Iniciando...", text_color="green")
        
        # Esperar un momento y cerrar la ventana
        self.after(1000, self.destroy)
        # Ejecutar la función de la app principal para desbloquear la interfaz
        self.after(1000, self.on_success_callback)