"""
EJECUTAR.py
Interfaz gráfica del Software FJ
Ejecución:
    python EJECUTAR.py
"""

import tkinter as tk
from tkinter import messagebox, ttk

from fj import ARCHIVO_LOG, TIPOS_SERVICIO, SistemaFJ, logger

"""Tema del Software"""

COLORES = {
  
    "fondo": "#cfd6de",
    "superficie": "#dde3e9",
    "campo": "#eef2f6",
    "borde": "#a7b1bc",
    "texto": "#1c2530",
    "texto_suave": "#4a5664",
    "acento": "#34404d",
    "acento_hover": "#46535f",
    "exito": "#1e7a3c",
    "error": "#b42318",
    "tarjeta": "#bcc5cf",
    "tarjeta_borde": "#9aa5b1",
    "gris_1": "#1c2530",
    "gris_2": "#34404d",
    "gris_3": "#566472",
    "gris_4": "#7b8896",
}

SECCIONES = ["Clientes", "Servicios", "Reservas", "Registro"]

class AppSoftwareFJ(tk.Tk):
    """Ventana principal"""

    def __init__(self):
        super().__init__()
        self.sistema = SistemaFJ()
        self.title("Software FJ")
        self.geometry("1050x650")
        self.minsize(900, 560)

        self.ultimo_calculo = None

        self._aplicar_tema_oscuro()

        self._crear_encabezado()
        self._crear_tarjetas()
        self.pestanas = ttk.Notebook(self, style="Oculto.TNotebook")
        self.pestanas.pack(fill="both", expand=True, padx=12, pady=(0, 6))
        self._crear_pestana_clientes()
        self._crear_pestana_servicios()
        self._crear_pestana_reservas()
        self._crear_pestana_log()
        self._crear_barra_estado()
        self.mostrar_seccion("Clientes")
        self.refrescar()

    """Tema global"""

    def _aplicar_tema_oscuro(self):
        c = COLORES
        self.configure(bg=c["fondo"])
        self.option_add("*Background", c["superficie"])
        self.option_add("*Foreground", c["texto"])
        self.option_add("*TCombobox*Listbox.background", c["campo"])
        self.option_add("*TCombobox*Listbox.foreground", c["texto"])
        self.option_add("*TCombobox*Listbox.selectBackground", c["acento"])

        estilo = ttk.Style(self)
        estilo.theme_use("clam") 
        estilo.configure(".", background=c["fondo"], foreground=c["texto"],
                         bordercolor=c["borde"], lightcolor=c["superficie"],
                         darkcolor=c["superficie"], troughcolor=c["fondo"],
                         fieldbackground=c["campo"], insertcolor=c["texto"],
                         selectbackground=c["acento"], selectforeground="#ffffff",
                         font=("Segoe UI", 10))

        estilo.configure("TFrame", background=c["fondo"])
        estilo.configure("TLabel", background=c["fondo"], foreground=c["texto"])
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 15, "bold"))
        estilo.configure("Sub.TLabel", foreground=c["texto_suave"])
        estilo.configure("TLabelframe", background=c["fondo"], bordercolor=c["borde"])
        estilo.configure("TLabelframe.Label", background=c["fondo"], foreground=c["texto_suave"])

        estilo.configure("TEntry", fieldbackground=c["campo"], foreground=c["texto"],
                         insertcolor=c["texto"], bordercolor=c["borde"], padding=4)
        estilo.map("TEntry", bordercolor=[("focus", c["acento"])],
                   lightcolor=[("focus", c["acento"])])

        estilo.configure("TButton", background=c["superficie"], foreground=c["texto"],
                         bordercolor=c["borde"], focuscolor=c["superficie"], padding=6)
        estilo.map("TButton", background=[("pressed", c["campo"]), ("active", c["campo"])])
        estilo.configure("Accion.TButton", background=c["acento"], foreground="#ffffff",
                         bordercolor=c["acento"], focuscolor=c["acento"],
                         font=("Segoe UI", 10, "bold"))
        estilo.map("Accion.TButton", background=[("pressed", c["acento"]), ("active", c["acento_hover"])])

        estilo.configure("TNotebook", background=c["fondo"], bordercolor=c["borde"])
        estilo.configure("TNotebook.Tab", background=c["superficie"], foreground=c["texto_suave"],
                         bordercolor=c["borde"], padding=(12, 6))
        estilo.map("TNotebook.Tab",
                   background=[("selected", c["fondo"])],
                   foreground=[("selected", c["texto"])],
                   lightcolor=[("selected", c["acento"])])

        estilo.configure("Treeview", background=c["superficie"], fieldbackground=c["superficie"],
                         foreground=c["texto"], bordercolor=c["borde"], rowheight=26)
        estilo.map("Treeview", background=[("selected", c["acento"])],
                   foreground=[("selected", "#ffffff")])
        estilo.configure("Treeview.Heading", background=c["campo"], foreground=c["texto"],
                         bordercolor=c["borde"], relief="flat", font=("Segoe UI", 10, "bold"))
        estilo.map("Treeview.Heading", background=[("active", c["borde"])])

    
        estilo.configure("TCombobox", fieldbackground=c["campo"], background=c["campo"],
                         foreground=c["texto"], arrowcolor=c["texto"], bordercolor=c["borde"],
                         lightcolor=c["campo"], darkcolor=c["campo"], padding=4)
        estilo.map("TCombobox",
                   fieldbackground=[("readonly", c["campo"]), ("disabled", c["campo"])],
                   background=[("readonly", c["campo"]), ("active", c["borde"])],
                   foreground=[("readonly", c["texto"]), ("disabled", c["texto_suave"])],
                   selectbackground=[("readonly", c["campo"])],
                   selectforeground=[("readonly", c["texto"])],
                   bordercolor=[("focus", c["texto_suave"])],
                   arrowcolor=[("disabled", c["texto_suave"])])
        self.option_add("*TCombobox*Listbox.selectForeground", "#ffffff")

        estilo.layout("Oculto.TNotebook.Tab", [])
        estilo.configure("Oculto.TNotebook", background=c["fondo"], borderwidth=0)

        estilo.configure("Vertical.TScrollbar", background=c["campo"], troughcolor=c["fondo"],
                         bordercolor=c["fondo"], arrowcolor=c["texto_suave"])
        estilo.map("Vertical.TScrollbar", background=[("active", c["borde"])])

    """"Un error muestra un aviso y la app sigue abierta"""
    
    def ejecutar(self, accion: str, funcion, *args, **kwargs):
        try:
            resultado = funcion(*args, **kwargs)
        except (ValueError, TypeError) as error:
            logger.error("%s falló: %s", accion, error)
            self.mostrar_estado(f"✗ No se pudo {accion}: {error}", error=True)
            messagebox.showerror(f"No se pudo {accion}", str(error), parent=self)
            return None
        finally:
            self.refrescar()
        return resultado

    def _crear_encabezado(self):
        """Encabezado: menú a la izquierda, título + sección actual a la derecha."""
        c = COLORES
        marco = tk.Frame(self, bg=c["fondo"], padx=14, pady=10)
        marco.pack(fill="x")
        tk.Frame(self, bg=c["tarjeta_borde"], height=1).pack(fill="x")

        titulo = tk.Frame(marco, bg=c["fondo"])
        titulo.pack(side="right")
        tk.Label(titulo, text="Software FJ", bg=c["fondo"], fg=c["texto"],
                 font=("Segoe UI", 15, "bold")).pack(side="left")
        self.lbl_seccion = tk.Label(titulo, text="", bg=c["fondo"], fg=c["gris_3"],
                                    font=("Segoe UI", 11))
        self.lbl_seccion.pack(side="left", padx=(6, 0), pady=(4, 0))

        menu = tk.Frame(marco, bg=c["fondo"])
        menu.pack(side="left")
        self.menu_items = {}
        for nombre in SECCIONES:
            item = tk.Frame(menu, bg=c["fondo"], cursor="hand2")
            item.pack(side="left", padx=(0, 20))
            texto = tk.Label(item, text=nombre, bg=c["fondo"], fg=c["gris_2"],
                             font=("Segoe UI", 10), cursor="hand2")
            texto.pack()
            linea = tk.Frame(item, height=2, bg=c["fondo"])
            linea.pack(fill="x", pady=(3, 0))
            for w in (item, texto):
                w.bind("<Button-1>", lambda _e, n=nombre: self.mostrar_seccion(n))
                w.bind("<Enter>", lambda _e, n=nombre: self._hover_menu(n, True))
                w.bind("<Leave>", lambda _e, n=nombre: self._hover_menu(n, False))
            self.menu_items[nombre] = (texto, linea)

    def mostrar_seccion(self, nombre: str):
        self.seccion_actual = nombre
        self.pestanas.select(SECCIONES.index(nombre))
        self.lbl_seccion.config(text=f"/  {nombre}")
        for n, (texto, linea) in self.menu_items.items():
            activo = n == nombre
            texto.config(fg=COLORES["gris_1"] if activo else COLORES["gris_2"],
                         font=("Segoe UI", 10, "bold" if activo else "normal"))
            linea.config(bg=COLORES["gris_1"] if activo else COLORES["fondo"])
        if nombre == "Registro":
            self.cargar_log()

    def _hover_menu(self, nombre: str, dentro: bool):
        if nombre == getattr(self, "seccion_actual", None):
            return
        texto, _ = self.menu_items[nombre]
        texto.config(fg=COLORES["gris_1"] if dentro else COLORES["gris_2"])

    def _crear_tarjetas(self):
        """Fila de tarjetas con los totales del sistema"""
        c = COLORES
        fila = tk.Frame(self, bg=c["fondo"], padx=12, pady=6)
        fila.pack(fill="x")
        datos = [
            ("clientes", "Clientes", c["gris_1"]),
            ("servicios", "Servicios", c["gris_2"]),
            ("reservas", "Reservas", c["gris_3"]),
            ("calculo", "Último cálculo", c["gris_4"]),
        ]
        self.tarjetas = {}
        for i, (clave, titulo, franja) in enumerate(datos):
            tarjeta = tk.Frame(fila, bg=c["tarjeta"], highlightthickness=1,
                               highlightbackground=c["tarjeta_borde"])
            tarjeta.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 10, 0))
            fila.columnconfigure(i, weight=1, uniform="tarjetas")
            tk.Frame(tarjeta, bg=franja, width=3).pack(side="left", fill="y")
            cuerpo = tk.Frame(tarjeta, bg=c["tarjeta"], padx=10, pady=3)
            cuerpo.pack(side="left", fill="both", expand=True)
            tk.Label(cuerpo, text=titulo.upper(), bg=c["tarjeta"], fg=c["gris_3"],
                     font=("Segoe UI", 7, "bold")).pack(anchor="w")
            valor = tk.Label(cuerpo, text="0", bg=c["tarjeta"], fg=c["gris_1"],
                             font=("Segoe UI", 13, "bold"))
            valor.pack(anchor="w")
            self.tarjetas[clave] = valor

    def _crear_barra_estado(self):
        self.lbl_estado = tk.Label(self, anchor="w", padx=12, pady=6,
                                   bg=COLORES["superficie"], fg=COLORES["texto_suave"])
        self.lbl_estado.pack(fill="x", side="bottom")

    def mostrar_estado(self, texto: str, error: bool = False):
        self.lbl_estado.config(text=texto, fg=COLORES["error"] if error else COLORES["exito"])

    @staticmethod
    def _tabla(padre, columnas):

        """Crea una tabla con barra de desplazamiento"""

        marco = ttk.Frame(padre)
        tabla = ttk.Treeview(marco, columns=[c[0] for c in columnas], show="headings",
                             selectmode="browse")
        for cid, titulo, ancho in columnas:
            tabla.heading(cid, text=titulo)
            tabla.column(cid, width=ancho, anchor="w")
        barra = ttk.Scrollbar(marco, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=barra.set)
        tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        return marco, tabla

    def _campo(self, padre, fila, etiqueta, ancho=28, solo_numeros=False, mayusculas=False):
        """
        Crea una etiqueta con su casilla de texto, solo permite parametros establecidos en desarrollo
        """
        ttk.Label(padre, text=etiqueta).grid(row=fila, column=0, sticky="w", pady=3)
        variable = tk.StringVar()
        entrada = ttk.Entry(padre, textvariable=variable, width=ancho)
        entrada.grid(row=fila, column=1, sticky="ew", pady=3)

        if solo_numeros:
       
            solo_digitos = self.register(lambda texto: texto == "" or texto.isdigit())
            entrada.configure(validate="key", validatecommand=(solo_digitos, "%P"))

        if mayusculas:
            def a_mayusculas(*_):
                texto = variable.get()
                if texto != texto.upper():
                    posicion = entrada.index("insert")
                    variable.set(texto.upper())
                    entrada.icursor(posicion)
            variable.trace_add("write", a_mayusculas)

        return variable

    """"Pestaña clientes"""
    def _crear_pestana_clientes(self):
        pestana = ttk.Frame(self.pestanas, padding=(0, 4))
        self.pestanas.add(pestana, text="  Clientes  ")

        formulario = ttk.LabelFrame(pestana, text="Nuevo cliente", padding=10)
        formulario.pack(side="left", fill="y", padx=(0, 10))
        self.cli_doc = self._campo(formulario, 0, "Documento", solo_numeros=True)
        self.cli_nombre = self._campo(formulario, 1, "Nombre completo", mayusculas=True)
        self.cli_email = self._campo(formulario, 2, "Email")
        self.cli_tel = self._campo(formulario, 3, "Teléfono", solo_numeros=True)
        ttk.Button(formulario, text="Registrar cliente", style="Accion.TButton",
                   command=self.registrar_cliente).grid(row=4, column=0, columnspan=2, sticky="ew", pady=(12, 4))
        ttk.Button(formulario, text="Limpiar", command=self._limpiar_cliente)\
            .grid(row=5, column=0, columnspan=2, sticky="ew")

        marco, self.tabla_clientes = self._tabla(pestana, [
            ("nombre", "Nombre", 200), ("doc", "Documento", 130),
            ("email", "Email", 240), ("tel", "Teléfono", 140),
        ])
        marco.pack(side="left", fill="both", expand=True)

    def registrar_cliente(self):
        cliente = self.ejecutar("registrar el cliente", self.sistema.registrar_cliente,
                                self.cli_doc.get(), self.cli_nombre.get(),
                                self.cli_email.get(), self.cli_tel.get())
        if cliente:
            self.mostrar_estado(f"Cliente registrado: {cliente.describir()}")
            self._limpiar_cliente()

    def _limpiar_cliente(self):
        for variable in (self.cli_doc, self.cli_nombre, self.cli_email, self.cli_tel):
            variable.set("")

    """"Pestañas SERVICIOS y RESERVAS"""

    DETALLE_POR_TIPO = {
        "Reserva de sala": "Capacidad (personas)",
        "Alquiler de equipo": "Tipo de equipo",
        "Asesoría": "Especialidad",
    }

    def _crear_pestana_servicios(self):
        pestana = ttk.Frame(self.pestanas, padding=(0, 4))
        self.pestanas.add(pestana, text="  Servicios  ")

        lateral = ttk.Frame(pestana)
        lateral.pack(side="left", fill="y", padx=(0, 10))

        
        formulario = ttk.LabelFrame(lateral, text="Nuevo servicio", padding=10)
        formulario.pack(fill="x")
        ttk.Label(formulario, text="Tipo").grid(row=0, column=0, sticky="w", pady=3)
        self.srv_tipo = tk.StringVar(value="Reserva de sala")
        combo = self.srv_combo = ttk.Combobox(formulario, textvariable=self.srv_tipo, state="readonly",
                             values=list(TIPOS_SERVICIO), width=26)
        combo.grid(row=0, column=1, sticky="ew", pady=3)
        combo.bind("<<ComboboxSelected>>", self._cambiar_etiqueta_detalle)

        self.srv_codigo = self._campo(formulario, 1, "Código", mayusculas=True)
        self.srv_nombre = self._campo(formulario, 2, "Nombre")
        self.srv_precio = self._campo(formulario, 3, "Precio por hora", solo_numeros=True)
        self.srv_detalle = self._campo(formulario, 4, "Detalle")
        self.lbl_detalle = formulario.grid_slaves(row=4, column=0)[0]
        self._cambiar_etiqueta_detalle()

        ttk.Button(formulario, text="Registrar servicio", style="Accion.TButton",
                   command=self.registrar_servicio).grid(row=5, column=0, columnspan=2,
                                                         sticky="ew", pady=(12, 4))
        ttk.Button(formulario, text="Limpiar", command=self._limpiar_servicio)\
            .grid(row=6, column=0, columnspan=2, sticky="ew")
 
        calculo = ttk.LabelFrame(lateral, text="Calcular costo (seleccione en la tabla)", padding=10)
        calculo.pack(fill="x", pady=(10, 0))
        self.srv_horas = self._campo(calculo, 0, "Horas", ancho=10, solo_numeros=True)
        self.srv_descuento = self._campo(calculo, 1, "Descuento %", ancho=10, solo_numeros=True)
        ttk.Button(calculo, text="Calcular", command=self.calcular_costo_servicio)\
            .grid(row=2, column=0, columnspan=2, sticky="ew", pady=(8, 0))

        marco, self.tabla_servicios = self._tabla(pestana, [
            ("codigo", "Código", 70), ("nombre", "Nombre", 170), ("tipo", "Tipo", 130),
            ("precio", "Precio/hora", 100), ("detalle", "Detalle", 230),
        ])
        marco.pack(side="left", fill="both", expand=True)

    def _cambiar_etiqueta_detalle(self, *_):
        self.srv_combo.selection_clear()  
        self.lbl_detalle.config(text=self.DETALLE_POR_TIPO.get(self.srv_tipo.get(), "Detalle"))

    def registrar_servicio(self):
        servicio = self.ejecutar("registrar el servicio", self.sistema.registrar_servicio,
                                 self.srv_tipo.get(), self.srv_codigo.get(), self.srv_nombre.get(),
                                 self.srv_precio.get(), self.srv_detalle.get())
        if servicio:
            self.mostrar_estado(f"Servicio registrado: {servicio}")
            self._limpiar_servicio()

    def _limpiar_servicio(self):
        for variable in (self.srv_codigo, self.srv_nombre, self.srv_precio, self.srv_detalle):
            variable.set("")

    def calcular_costo_servicio(self):
        seleccion = self.tabla_servicios.selection()
        if not seleccion:
            messagebox.showwarning("Calcular costo", "Seleccione un servicio en la tabla.", parent=self)
            return
        codigo = self.tabla_servicios.item(seleccion[0], "values")[0]
        resultado = self.ejecutar("calcular el costo", self.sistema.calcular_costo,
                                  codigo, self.srv_horas.get(), self.srv_descuento.get() or "0")
        if resultado:
            servicio, costo = resultado
            self.ultimo_calculo = costo
            self.tarjetas["calculo"].config(text=f"${costo:,.0f}")
            texto = f"{servicio.nombre}: {self.srv_horas.get()} h = ${costo:,.0f}"
            self.mostrar_estado(texto)
            messagebox.showinfo("Costo del servicio", texto, parent=self)

    def _crear_pestana_reservas(self):
        pestana = ttk.Frame(self.pestanas, padding=10)
        self.pestanas.add(pestana, text="  Reservas  ")

    """"Registros"""""

    def _crear_pestana_log(self):
        pestana = ttk.Frame(self.pestanas, padding=10)
        self.pestanas.add(pestana, text="  Registro de eventos  ")
        barra = ttk.Frame(pestana)
        barra.pack(fill="x", pady=(0, 6))
        ttk.Label(barra, text=f"Archivo: {ARCHIVO_LOG}", style="Sub.TLabel").pack(side="left")
        ttk.Button(barra, text="Actualizar", command=self.cargar_log).pack(side="right")

        marco = ttk.Frame(pestana)
        marco.pack(fill="both", expand=True)
        self.txt_log = tk.Text(marco, wrap="none", font=("Consolas", 9), state="disabled",
                               bg=COLORES["superficie"], fg=COLORES["texto"],
                               insertbackground=COLORES["texto"], relief="flat",
                               highlightthickness=1, highlightbackground=COLORES["borde"],
                               padx=8, pady=6)
        barra_y = ttk.Scrollbar(marco, orient="vertical", command=self.txt_log.yview)
        self.txt_log.configure(yscrollcommand=barra_y.set)
        self.txt_log.pack(side="left", fill="both", expand=True)
        barra_y.pack(side="right", fill="y")
        self.txt_log.tag_configure("ERROR", foreground=COLORES["error"])
        self.txt_log.tag_configure("INFO", foreground=COLORES["exito"])

    def cargar_log(self):
        try:
            with open(ARCHIVO_LOG, encoding="utf-8") as archivo:
                lineas = archivo.readlines()[-400:]
        except OSError:
            lineas = []
        self.txt_log.config(state="normal")
        self.txt_log.delete("1.0", "end")
        for linea in lineas:
            if "| DEBUG" in linea:
                continue
            nivel = "ERROR" if "| ERROR" in linea else "INFO"
            self.txt_log.insert("end", linea, nivel)
        self.txt_log.config(state="disabled")
        self.txt_log.see("end")

    def refrescar(self):
        self.tabla_clientes.delete(*self.tabla_clientes.get_children())
        for c in self.sistema.clientes:
            self.tabla_clientes.insert("", "end", values=(c.nombre, c.documento, c.email, c.telefono))

        nombres_tipo = {clase: nombre for nombre, clase in TIPOS_SERVICIO.items()}
        self.tabla_servicios.delete(*self.tabla_servicios.get_children())
        for s in self.sistema.servicios:
            self.tabla_servicios.insert("", "end", values=(
                s.codigo, s.nombre, nombres_tipo.get(type(s), "-"),
                f"${s.precio_base:,.0f}", s.describir()))

        self.tarjetas["clientes"].config(text=str(len(self.sistema.clientes)))
        self.tarjetas["servicios"].config(text=str(len(self.sistema.servicios)))
        self.tarjetas["reservas"].config(text=str(len(getattr(self.sistema, "reservas", []))))
        self.tarjetas["calculo"].config(
            text="—" if self.ultimo_calculo is None else f"${self.ultimo_calculo:,.0f}")

if __name__ == "__main__":
    AppSoftwareFJ().mainloop()
