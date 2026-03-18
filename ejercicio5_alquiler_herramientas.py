# =============================================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# Curso: Programación - 213023_344
# Fase 2: Diseño y Programación Orientada a Objetos
# Ejercicio 5: Sistema de Alquiler de Herramientas
#
# Autor: Luz Alejandra Hincapie Cortes
# Fecha: Marzo 2026
#
# Descripción general:
#   Sistema de alquiler de herramientas con POO y encapsulamiento.
#   Interfaz gráfica en Tkinter, completamente en idioma inglés.
#   Módulo de login con validación de credenciales antes de acceder
#   al sistema principal.
#
#   Clases:
#     - Usuario:             gestiona las credenciales de acceso al sistema.
#     - HerramientaAlquiler: representa cada herramienta dentro del sistema.
#     - VentanaLogin:        pantalla de inicio de sesión (Tkinter).
#     - VentanaPrincipal:    sistema principal de alquiler (Tkinter).
#
#   Paleta de colores:
#     - Rojo:       #C0392B   (botones de acción principal)
#     - Dorado:     #F39C12   (acentos y encabezados)
#     - Gris oscuro:#2C3E50   (fondo principal)
#     - Blanco roto:#ECF0F1   (textos sobre fondo oscuro)
# =============================================================================

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime


# =============================================================================
# CONSTANTES DEL SISTEMA
# Centralizar los valores fijos facilita cambiarlos en un solo lugar.
# =============================================================================
USUARIO_VALIDO    = "programacion"  # Credencial de usuario aceptada
CONTRASENA_VALIDA = "programacion"  # Credencial de contraseña aceptada

HORA_MINIMA    = 0    # Hora mínima permitida en formato 24 horas
HORA_MAXIMA    = 23   # Hora máxima permitida en formato 24 horas
MINUTO_MINIMO  = 0    # Minuto mínimo permitido
MINUTO_MAXIMO  = 59   # Minuto máximo permitido
TARIFA_MINIMA  = 10000  # La tarifa debe ser mayor a este valor

ANIO_MINIMO = 2020    # Año mínimo aceptado para fechas
ANIO_MAXIMO = 2030    # Año máximo aceptado para fechas

# Colores de la interfaz
COLOR_FONDO          = "#2C3E50"   # Gris oscuro: fondo de ventanas
COLOR_PANEL          = "#34495E"   # Gris medio: fondo de secciones
COLOR_ACENTO         = "#F39C12"   # Dorado: títulos y bordes destacados
COLOR_BOTON_ACCION   = "#C0392B"   # Rojo: botones principales
COLOR_BOTON_RETORNO  = "#E67E22"   # Naranja dorado: botón de retorno
COLOR_BOTON_SALIR    = "#7F8C8D"   # Gris: botón de salida
COLOR_TEXTO_CLARO    = "#ECF0F1"   # Blanco roto: texto sobre fondo oscuro
COLOR_EXITO          = "#2ECC71"   # Verde: confirmaciones de éxito
COLOR_ENTRADA        = "#ECF0F1"   # Fondo de campos de texto
COLOR_TEXTO_ENTRADA  = "#2C3E50"   # Texto dentro de los campos


# =============================================================================
# CLASE: Usuario
# Propósito: almacenar las credenciales del sistema y validarlas.
# =============================================================================
class Usuario:
    """
    Representa al usuario autorizado para acceder al sistema.
    Usa encapsulamiento para proteger las credenciales.
    """

    def __init__(self, usuario, password):
        """
        Constructor de la clase Usuario.

        Parámetros:
            usuario  (str): nombre de usuario del sistema.
            password (str): contraseña del sistema.
        """
        # Atributo privado: nombre de usuario
        self._usuario = usuario

        # Atributo privado: contraseña del sistema
        self._password = password

    def validar(self, usuario_ingresado, password_ingresada):
        """
        Compara las credenciales ingresadas en el formulario
        con las credenciales almacenadas en el objeto.

        Parámetros:
            usuario_ingresado  (str): usuario digitado por el usuario.
            password_ingresada (str): contraseña digitada por el usuario.

        Retorna:
            bool: True si ambas credenciales coinciden, False en caso contrario.
        """
        usuario_correcto  = self._usuario  == usuario_ingresado
        password_correcta = self._password == password_ingresada
        return usuario_correcto and password_correcta

    def __str__(self):
        """
        Representación en texto del objeto.
        NUNCA expone la contraseña para proteger la seguridad.
        """
        return "Usuario: {}".format(self._usuario)


# =============================================================================
# CLASE: HerramientaAlquiler
# Propósito: modelar cada herramienta que se registra en el sistema.
# Se usan datetime completos (fecha + hora + minutos) para calcular
# correctamente alquileres que abarcan varios días.
# =============================================================================
class HerramientaAlquiler:
    """
    Representa una herramienta dentro del sistema de alquiler.

    Registra el momento de salida y retorno como objetos datetime completos
    (fecha + hora + minutos), lo que permite calcular con precisión
    el tiempo total incluso cuando el alquiler abarca varios días.

    El ID se convierte y almacena siempre en MAYÚSCULAS para evitar
    duplicados por diferencias de capitalización.
    """

    def __init__(self, id_herramienta, tarifa_hora):
        """
        Constructor de la clase HerramientaAlquiler.

        Parámetros:
            id_herramienta (str):   identificador único de la herramienta.
                                    Se normaliza a mayúsculas automáticamente.
            tarifa_hora    (float): valor cobrado por cada hora de alquiler.
        """
        # Atributo privado: ID normalizado a mayúsculas sin espacios
        self._id_herramienta = id_herramienta.replace(" ", "").upper()

        # Atributo privado: momento de salida (datetime completo)
        self._hora_salida = None

        # Atributo privado: momento de retorno (datetime completo)
        self._hora_retorno = None

        # Atributo privado: tarifa por hora de alquiler
        self._tarifa_hora = tarifa_hora

    def registrar_salida(self, hora):
        """
        Guarda el momento en que la herramienta sale del establecimiento.

        Parámetros:
            hora (datetime): fecha y hora exacta de salida.
        """
        self._hora_salida = hora

    def registrar_retorno(self, hora):
        """
        Guarda el momento en que la herramienta es devuelta.

        Parámetros:
            hora (datetime): fecha y hora exacta de retorno.
        """
        self._hora_retorno = hora

    def calcular_costo(self, hora_retorno):
        """
        Calcula el costo total del alquiler.

        Resta los dos objetos datetime para obtener un timedelta,
        luego lo convierte a horas decimales y lo multiplica por la tarifa.

        Parámetros:
            hora_retorno (datetime): fecha y hora de devolución.

        Retorna:
            float: costo total redondeado a 2 decimales.
            None:  si no existe una hora de salida registrada.
        """
        if self._hora_salida is None:
            return None

        # timedelta = diferencia exacta entre los dos momentos
        diferencia_tiempo = hora_retorno - self._hora_salida

        # Convertir la diferencia total a horas decimales
        total_horas_decimales = diferencia_tiempo.total_seconds() / 3600

        costo_calculado = round(total_horas_decimales * self._tarifa_hora, 2)
        return costo_calculado

    def calcular_desglose_tiempo(self, hora_retorno):
        """
        Calcula el tiempo de uso desglosado en días, horas y minutos.

        timedelta almacena internamente:
          - .days:    días completos transcurridos.
          - .seconds: segundos del día parcial restante (0 a 86399).
        A partir de .seconds se extraen las horas y los minutos sobrantes.

        Parámetros:
            hora_retorno (datetime): fecha y hora de devolución.

        Retorna:
            dict con claves: dias, horas, minutos, total_horas_decimal.
            None: si no existe una hora de salida registrada.
        """
        if self._hora_salida is None:
            return None

        diferencia_tiempo = hora_retorno - self._hora_salida

        # Días completos
        dias_completos = diferencia_tiempo.days

        # Segundos del día parcial restante
        segundos_restantes = diferencia_tiempo.seconds

        # Horas y minutos dentro del día parcial
        horas_del_dia   = segundos_restantes // 3600
        minutos_del_dia = (segundos_restantes % 3600) // 60

        # Total en horas decimales (para la fórmula de cálculo en la interfaz)
        total_decimal = round(diferencia_tiempo.total_seconds() / 3600, 2)

        return {
            "dias"               : dias_completos,
            "horas"              : horas_del_dia,
            "minutos"            : minutos_del_dia,
            "total_horas_decimal": total_decimal
        }

    def esta_disponible(self):
        """
        Indica si la herramienta todavía no ha sido retornada.

        Retorna:
            bool: True si sigue activa (en uso), False si ya fue devuelta.
        """
        return self._hora_retorno is None

    # -------------------------------------------------------------------------
    # Métodos de acceso (getters)
    # -------------------------------------------------------------------------

    def obtener_id(self):
        """Retorna el ID de la herramienta (siempre en mayúsculas)."""
        return self._id_herramienta

    def obtener_hora_salida(self):
        """Retorna el datetime completo de salida."""
        return self._hora_salida

    def obtener_hora_retorno(self):
        """Retorna el datetime completo de retorno."""
        return self._hora_retorno

    def obtener_tarifa(self):
        """Retorna la tarifa por hora."""
        return self._tarifa_hora

    def obtener_resumen(self):
        """
        Construye y retorna un diccionario con los datos principales
        de la herramienta, listos para mostrarse en la interfaz.

        Las fechas se formatean como texto DD/MM/YYYY HH:MM.

        Retorna:
            dict con claves: id, salida_texto, retorno_texto, tarifa, estado.
        """
        estado_herramienta = "Active" if self.esta_disponible() else "Returned"

        if self._hora_salida is not None:
            texto_salida = self._hora_salida.strftime("%d/%m/%Y %H:%M")
        else:
            texto_salida = "N/A"

        if self._hora_retorno is not None:
            texto_retorno = self._hora_retorno.strftime("%d/%m/%Y %H:%M")
        else:
            texto_retorno = "Pending"

        return {
            "id"           : self._id_herramienta,
            "salida_texto" : texto_salida,
            "retorno_texto": texto_retorno,
            "tarifa"       : self._tarifa_hora,
            "estado"       : estado_herramienta
        }

    def __str__(self):
        """
        Representación en texto del objeto.
        Útil para depuración en consola durante el desarrollo.
        """
        datos = self.obtener_resumen()
        return "Tool ID: {} | Out: {} | Rate: ${}/hr | Status: {}".format(
            datos["id"],
            datos["salida_texto"],
            datos["tarifa"],
            datos["estado"]
        )


# =============================================================================
# CLASE: VentanaLogin
# Propósito: mostrar el formulario de inicio de sesión.
# Solo cuando las credenciales son válidas se abre el sistema principal.
# =============================================================================
class VentanaLogin:
    """
    Pantalla de inicio de sesión del sistema.
    Valida las credenciales antes de dar acceso al menú principal.
    """

    def __init__(self, ventana_raiz):
        """
        Constructor de la ventana de login.

        Parámetros:
            ventana_raiz: ventana raíz de Tkinter.
        """
        self.__ventana = ventana_raiz
        self.__ventana.title("Login - Tool Rental System")
        self.__ventana.geometry("380x300")
        self.__ventana.resizable(False, False)
        self.__ventana.configure(bg=COLOR_FONDO)

        # Crear el objeto Usuario con las credenciales válidas del sistema
        self.__usuario_sistema = Usuario(USUARIO_VALIDO, CONTRASENA_VALIDA)

        self.__construir_interfaz()

    def __construir_interfaz(self):
        """Construye y organiza todos los elementos visuales del login."""

        tk.Label(
            self.__ventana,
            text="⚙  TOOL RENTAL SYSTEM",
            font=("Arial", 14, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_ACENTO
        ).pack(pady=(25, 4))

        tk.Label(
            self.__ventana,
            text="Please log in to continue",
            font=("Arial", 9),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO_CLARO
        ).pack(pady=(0, 20))

        tk.Label(
            self.__ventana,
            text="Username:",
            font=("Arial", 10),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO_CLARO
        ).pack()

        self.__campo_usuario = tk.Entry(
            self.__ventana,
            width=28,
            font=("Arial", 10),
            bg=COLOR_ENTRADA,
            fg=COLOR_TEXTO_ENTRADA
        )
        self.__campo_usuario.pack(pady=(3, 12))

        tk.Label(
            self.__ventana,
            text="Password:",
            font=("Arial", 10),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO_CLARO
        ).pack()

        self.__campo_password = tk.Entry(
            self.__ventana,
            width=28,
            font=("Arial", 10),
            show="*",
            bg=COLOR_ENTRADA,
            fg=COLOR_TEXTO_ENTRADA
        )
        self.__campo_password.pack(pady=(3, 22))

        tk.Button(
            self.__ventana,
            text="Log In",
            font=("Arial", 10, "bold"),
            bg=COLOR_BOTON_ACCION,
            fg=COLOR_TEXTO_CLARO,
            activebackground="#922B21",
            activeforeground=COLOR_TEXTO_CLARO,
            width=16,
            cursor="hand2",
            relief="flat",
            command=self.__validar_login
        ).pack()

        # Tecla Enter también activa el login
        self.__ventana.bind("<Return>", lambda evento: self.__validar_login())

        # El cursor inicia en el campo de usuario
        self.__campo_usuario.focus()

    def __validar_login(self):
        """
        Lee los campos del formulario y valida las credenciales.

        - Si los campos están vacíos: muestra advertencia.
        - Si las credenciales son incorrectas: muestra error y limpia contraseña.
        - Si son correctas: destruye esta ventana y abre el sistema principal.
        """
        usuario_digitado  = self.__campo_usuario.get().strip()
        password_digitada = self.__campo_password.get().strip()

        # Verificar que ningún campo esté vacío
        if usuario_digitado == "" or password_digitada == "":
            messagebox.showwarning(
                "Warning",
                "Please fill in all fields before logging in."
            )
            return

        # Usar el método validar() de la clase Usuario
        acceso_concedido = self.__usuario_sistema.validar(
            usuario_digitado, password_digitada
        )

        if acceso_concedido:
            # Credenciales correctas: abrir el sistema principal
            self.__ventana.destroy()
            ventana_sistema = tk.Tk()
            VentanaPrincipal(ventana_sistema)
            ventana_sistema.mainloop()
        else:
            # Credenciales incorrectas: bloquear acceso y mostrar error
            messagebox.showerror(
                "Access Denied",
                "Invalid username or password.\nPlease try again."
            )
            # Limpiar solo la contraseña y devolver el foco a ese campo
            self.__campo_password.delete(0, tk.END)
            self.__campo_password.focus()


# =============================================================================
# CLASE: VentanaPrincipal
# Propósito: sistema principal de alquiler de herramientas.
# Las herramientas se almacenan en una LISTA interna (lista_herramientas).
# =============================================================================
class VentanaPrincipal:
    """
    Ventana principal del sistema de alquiler de herramientas.

    Permite:
      1. Registrar una herramienta nueva con su fecha/hora de salida.
      2. Ver todas las herramientas registradas en una lista visual.
      3. Seleccionar una herramienta activa y registrar su retorno.
      4. Ver el desglose del tiempo usado y el costo total calculado.

    Estructura de datos:
      - lista_herramientas: lista de objetos HerramientaAlquiler.
        La búsqueda por ID se realiza con un bucle for.
    """

    def __init__(self, ventana_raiz):
        """
        Constructor de la ventana principal.

        Parámetros:
            ventana_raiz: ventana raíz de Tkinter.
        """
        self.__ventana = ventana_raiz
        self.__ventana.title("Tool Rental System - Main")
        self.__ventana.geometry("680x800")
        self.__ventana.resizable(False, False)
        self.__ventana.configure(bg=COLOR_FONDO)

        # Manejar el cierre con la X para pedir confirmación
        self.__ventana.protocol("WM_DELETE_WINDOW", self.__salir)

        # LISTA INTERNA de herramientas (requerida por la guía del curso).
        # Cada elemento es un objeto de tipo HerramientaAlquiler.
        self.__lista_herramientas = []

        self.__construir_interfaz()

    # -------------------------------------------------------------------------
    # CONSTRUCCIÓN DE LA INTERFAZ
    # -------------------------------------------------------------------------

    def __construir_interfaz(self):
        """Construye y organiza todos los elementos visuales de la ventana."""

        tk.Label(
            self.__ventana,
            text="⚙  TOOL RENTAL SYSTEM",
            font=("Arial", 15, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_ACENTO
        ).pack(pady=(15, 8))

        self.__construir_seccion_registro()
        self.__construir_seccion_lista()
        self.__construir_seccion_retorno()
        self.__construir_seccion_resultado()
        self.__construir_boton_salir()

    # =========================================================================
    # HELPER 1: __crear_campo
    # Elimina el duplicado de crear Label + Entry en cada fila de fecha/hora.
    # Se usaba 8 veces (Day, Month, Year, Hour, Min en registro y en retorno).
    # =========================================================================
    def __crear_campo(self, padre, etiqueta, ancho):
        """
        Crea y empaqueta una etiqueta de texto seguida de un campo de entrada.

        Este método evita repetir el mismo par Label + Entry en cada fila de
        fecha y hora. Se llama desde __construir_seccion_registro (5 veces)
        y desde __construir_seccion_retorno (5 veces).

        Parámetros:
            padre    (tk.Frame): frame contenedor donde se agregan los widgets.
            etiqueta (str):      texto descriptivo que aparece sobre el campo.
            ancho    (int):      número de caracteres de ancho del campo Entry.

        Retorna:
            tk.Entry: referencia al campo creado, para leer su valor luego.
        """
        tk.Label(
            padre,
            text=etiqueta,
            font=("Arial", 8),
            bg=COLOR_PANEL,
            fg=COLOR_ACENTO
        ).pack(side="left")

        campo = tk.Entry(
            padre,
            width=ancho,
            font=("Arial", 10),
            bg=COLOR_ENTRADA,
            fg=COLOR_TEXTO_ENTRADA
        )
        campo.pack(side="left", padx=(2, 8))
        return campo

    def __construir_seccion_registro(self):
        """Construye el panel de registro de nuevas herramientas."""

        marco_registro = tk.LabelFrame(
            self.__ventana,
            text="  Register New Tool  ",
            font=("Arial", 10, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_ACENTO,
            padx=12,
            pady=10
        )
        marco_registro.pack(fill="x", padx=20, pady=(0, 6))

        # --- Fila 1: Tool ID y Hourly Rate ---
        fila_id_tarifa = tk.Frame(marco_registro, bg=COLOR_PANEL)
        fila_id_tarifa.pack(fill="x", pady=3)

        tk.Label(
            fila_id_tarifa, text="Tool ID:",
            font=("Arial", 10), bg=COLOR_PANEL, fg=COLOR_TEXTO_CLARO,
            width=14, anchor="w"
        ).pack(side="left")

        self.__campo_id = tk.Entry(
            fila_id_tarifa, width=13,
            font=("Arial", 10), bg=COLOR_ENTRADA, fg=COLOR_TEXTO_ENTRADA
        )
        self.__campo_id.pack(side="left", padx=(0, 18))

        tk.Label(
            fila_id_tarifa, text="Hourly Rate ($):",
            font=("Arial", 10), bg=COLOR_PANEL, fg=COLOR_TEXTO_CLARO,
            width=15, anchor="w"
        ).pack(side="left")

        self.__campo_tarifa = tk.Entry(
            fila_id_tarifa, width=10,
            font=("Arial", 10), bg=COLOR_ENTRADA, fg=COLOR_TEXTO_ENTRADA
        )
        self.__campo_tarifa.pack(side="left")

        # --- Fila 2: Departure Date ---
        # __crear_campo reemplaza los 3 bloques Label+Entry duplicados
        fila_fecha_salida = tk.Frame(marco_registro, bg=COLOR_PANEL)
        fila_fecha_salida.pack(fill="x", pady=3)

        tk.Label(
            fila_fecha_salida, text="Departure Date:",
            font=("Arial", 10), bg=COLOR_PANEL, fg=COLOR_TEXTO_CLARO,
            width=14, anchor="w"
        ).pack(side="left")

        self.__campo_salida_dia   = self.__crear_campo(fila_fecha_salida, "Day",   4)
        self.__campo_salida_mes   = self.__crear_campo(fila_fecha_salida, "Month", 4)
        self.__campo_salida_anio  = self.__crear_campo(fila_fecha_salida, "Year",  6)

        # --- Fila 3: Departure Time ---
        # __crear_campo reemplaza los 2 bloques Label+Entry duplicados
        fila_hora_salida = tk.Frame(marco_registro, bg=COLOR_PANEL)
        fila_hora_salida.pack(fill="x", pady=3)

        tk.Label(
            fila_hora_salida, text="Departure Time:",
            font=("Arial", 10), bg=COLOR_PANEL, fg=COLOR_TEXTO_CLARO,
            width=14, anchor="w"
        ).pack(side="left")

        self.__campo_salida_hora   = self.__crear_campo(fila_hora_salida, "Hour (0-23)", 4)
        self.__campo_salida_minuto = self.__crear_campo(fila_hora_salida, "Min (0-59)",  4)

        # --- Botón Register Tool ---
        tk.Button(
            marco_registro,
            text="Register Tool",
            font=("Arial", 10, "bold"),
            bg=COLOR_BOTON_ACCION,
            fg=COLOR_TEXTO_CLARO,
            activebackground="#922B21",
            activeforeground=COLOR_TEXTO_CLARO,
            width=20,
            cursor="hand2",
            relief="flat",
            command=self.__registrar_herramienta
        ).pack(pady=(10, 2))

    def __construir_seccion_lista(self):
        """Construye el panel que muestra la lista de herramientas registradas."""

        marco_lista = tk.LabelFrame(
            self.__ventana,
            text="  Registered Tools  ",
            font=("Arial", 10, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_ACENTO,
            padx=12,
            pady=8
        )
        marco_lista.pack(fill="x", padx=20, pady=(0, 6))

        self.__listbox_herramientas = tk.Listbox(
            marco_lista,
            font=("Courier", 9),
            height=6,
            selectmode="single",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO_CLARO,
            selectbackground=COLOR_ACENTO,
            selectforeground=COLOR_FONDO
        )
        self.__listbox_herramientas.pack(fill="x")

        # Insertar el encabezado usando el helper reutilizable
        self.__insertar_encabezado_listbox()

    def __construir_seccion_retorno(self):
        """Construye el panel para registrar el retorno de una herramienta."""

        marco_retorno = tk.LabelFrame(
            self.__ventana,
            text="  Register Return  ",
            font=("Arial", 10, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_ACENTO,
            padx=12,
            pady=10
        )
        marco_retorno.pack(fill="x", padx=20, pady=(0, 6))

        # --- Selector de herramienta activa ---
        fila_selector = tk.Frame(marco_retorno, bg=COLOR_PANEL)
        fila_selector.pack(fill="x", pady=(0, 6))

        tk.Label(
            fila_selector, text="Select Tool:",
            font=("Arial", 10), bg=COLOR_PANEL, fg=COLOR_TEXTO_CLARO,
            width=14, anchor="w"
        ).pack(side="left")

        self.__combo_herramienta = ttk.Combobox(
            fila_selector, width=25,
            font=("Arial", 10), state="readonly"
        )
        self.__combo_herramienta.pack(side="left")
        self.__combo_herramienta.set("-- Select active tool --")

        estilo_combo = ttk.Style()
        estilo_combo.theme_use("clam")
        estilo_combo.configure(
            "TCombobox",
            fieldbackground=COLOR_ENTRADA,
            background=COLOR_PANEL,
            foreground=COLOR_TEXTO_ENTRADA
        )

        # --- Return Date ---
        # __crear_campo reemplaza los 3 bloques Label+Entry duplicados
        fila_fecha_retorno = tk.Frame(marco_retorno, bg=COLOR_PANEL)
        fila_fecha_retorno.pack(fill="x", pady=3)

        tk.Label(
            fila_fecha_retorno, text="Return Date:",
            font=("Arial", 10), bg=COLOR_PANEL, fg=COLOR_TEXTO_CLARO,
            width=14, anchor="w"
        ).pack(side="left")

        self.__campo_retorno_dia   = self.__crear_campo(fila_fecha_retorno, "Day",   4)
        self.__campo_retorno_mes   = self.__crear_campo(fila_fecha_retorno, "Month", 4)
        self.__campo_retorno_anio  = self.__crear_campo(fila_fecha_retorno, "Year",  6)

        # --- Return Time + botón Register Return ---
        # __crear_campo reemplaza los 2 bloques Label+Entry duplicados
        fila_hora_retorno = tk.Frame(marco_retorno, bg=COLOR_PANEL)
        fila_hora_retorno.pack(fill="x", pady=(3, 0))

        tk.Label(
            fila_hora_retorno, text="Return Time:",
            font=("Arial", 10), bg=COLOR_PANEL, fg=COLOR_TEXTO_CLARO,
            width=14, anchor="w"
        ).pack(side="left")

        self.__campo_retorno_hora   = self.__crear_campo(fila_hora_retorno, "Hour (0-23)", 4)
        self.__campo_retorno_minuto = self.__crear_campo(fila_hora_retorno, "Min (0-59)",  4)

        tk.Button(
            fila_hora_retorno,
            text="Register Return",
            font=("Arial", 10, "bold"),
            bg=COLOR_BOTON_RETORNO,
            fg=COLOR_TEXTO_CLARO,
            activebackground="#CA6F1E",
            activeforeground=COLOR_TEXTO_CLARO,
            width=16,
            cursor="hand2",
            relief="flat",
            command=self.__registrar_retorno
        ).pack(side="left", padx=(10, 0))

    def __construir_seccion_resultado(self):
        """Construye el panel que muestra el resultado del último retorno."""

        marco_resultado = tk.LabelFrame(
            self.__ventana,
            text="  Result  ",
            font=("Arial", 10, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_ACENTO,
            padx=12,
            pady=8
        )
        marco_resultado.pack(fill="x", padx=20, pady=(0, 8))

        # Línea 1: herramienta, fecha/hora de salida y retorno
        self.__etiqueta_resultado_linea1 = tk.Label(
            marco_resultado,
            text="No operations yet.",
            font=("Arial", 10),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO_CLARO,
            anchor="w",
            relief="sunken",
            padx=8,
            pady=4
        )
        self.__etiqueta_resultado_linea1.pack(fill="x")

        # Línea 2: tiempo desglosado (días, horas, minutos)
        self.__etiqueta_resultado_linea2 = tk.Label(
            marco_resultado,
            text="",
            font=("Arial", 10),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO_CLARO,
            anchor="w",
            padx=8,
            pady=2
        )
        self.__etiqueta_resultado_linea2.pack(fill="x")

        # Línea 3: fórmula de cálculo y costo total
        self.__etiqueta_resultado_linea3 = tk.Label(
            marco_resultado,
            text="",
            font=("Arial", 10, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_ACENTO,
            anchor="w",
            padx=8,
            pady=4
        )
        self.__etiqueta_resultado_linea3.pack(fill="x")

    def __construir_boton_salir(self):
        """Construye el botón de salida al final de la ventana."""

        tk.Button(
            self.__ventana,
            text="Exit",
            font=("Arial", 10, "bold"),
            bg=COLOR_BOTON_SALIR,
            fg=COLOR_TEXTO_CLARO,
            activebackground="#626567",
            activeforeground=COLOR_TEXTO_CLARO,
            width=12,
            cursor="hand2",
            relief="flat",
            command=self.__salir
        ).pack(pady=(0, 14))

    # -------------------------------------------------------------------------
    # MÉTODOS PRIVADOS DE VALIDACIÓN
    # -------------------------------------------------------------------------

    def __validar_entero_en_rango(self, valor_texto, minimo, maximo):
        """
        Valida que un texto represente un número entero dentro de un rango.
        Se reutiliza para validar hora, minutos, día, mes y año.

        Parámetros:
            valor_texto (str): texto ingresado por el usuario.
            minimo      (int): valor mínimo permitido (inclusive).
            maximo      (int): valor máximo permitido (inclusive).

        Retorna:
            int:  el valor convertido a entero si es válido.
            None: si el texto no es un entero o está fuera del rango.
        """
        try:
            numero = int(valor_texto)
            if minimo <= numero <= maximo:
                return numero
            return None
        except ValueError:
            return None

    def __construir_datetime(self, dia_texto, mes_texto, anio_texto,
                              hora_texto, minuto_texto):
        """
        Convierte los cinco campos separados (día, mes, año, hora, minuto)
        en un único objeto datetime de Python.

        El objeto datetime detecta automáticamente fechas imposibles
        como 30/02 o 31/11 y lanza ValueError en esos casos.

        Parámetros:
            dia_texto    (str): día ingresado.
            mes_texto    (str): mes ingresado.
            anio_texto   (str): año ingresado.
            hora_texto   (str): hora ingresada (0-23).
            minuto_texto (str): minuto ingresado (0-59).

        Retorna:
            (datetime, None): si todos los datos son válidos.
            (None, str):      si hay algún error; el str describe el problema.
        """
        campos_vacios = (
            dia_texto    == "" or
            mes_texto    == "" or
            anio_texto   == "" or
            hora_texto   == "" or
            minuto_texto == ""
        )
        if campos_vacios:
            return None, "Please fill in all date and time fields."

        try:
            dia  = int(dia_texto)
            mes  = int(mes_texto)
            anio = int(anio_texto)
        except ValueError:
            return None, "Day, month and year must be whole numbers."

        if anio < ANIO_MINIMO or anio > ANIO_MAXIMO:
            return None, "Year must be between {} and {}.".format(
                ANIO_MINIMO, ANIO_MAXIMO
            )

        hora = self.__validar_entero_en_rango(hora_texto, HORA_MINIMA, HORA_MAXIMA)
        if hora is None:
            return None, "Hour must be a whole number between 0 and 23."

        minuto = self.__validar_entero_en_rango(
            minuto_texto, MINUTO_MINIMO, MINUTO_MAXIMO
        )
        if minuto is None:
            return None, "Minutes must be a whole number between 0 and 59."

        try:
            fecha_hora_completa = datetime(anio, mes, dia, hora, minuto, 0)
            return fecha_hora_completa, None
        except ValueError:
            return None, "Invalid date. Please check day, month and year."

    # -------------------------------------------------------------------------
    # MÉTODOS PRIVADOS DE BÚSQUEDA EN LA LISTA
    # -------------------------------------------------------------------------

    def __buscar_herramienta_por_id(self, id_buscado):
        """
        Recorre la lista interna para encontrar una herramienta por su ID.
        El ID siempre se compara en mayúsculas.

        Parámetros:
            id_buscado (str): ID de la herramienta a buscar.

        Retorna:
            HerramientaAlquiler: si se encuentra.
            None: si no existe ninguna herramienta con ese ID.
        """
        id_normalizado = id_buscado.upper()
        for herramienta in self.__lista_herramientas:
            if herramienta.obtener_id() == id_normalizado:
                return herramienta
        return None

    def __existe_id_en_lista(self, id_buscado):
        """
        Verifica si ya existe una herramienta con el ID dado en la lista.

        Parámetros:
            id_buscado (str): ID a verificar.

        Retorna:
            bool: True si ya existe, False si no.
        """
        return self.__buscar_herramienta_por_id(id_buscado) is not None

    # -------------------------------------------------------------------------
    # MÉTODOS PRIVADOS DE ACTUALIZACIÓN DE LA INTERFAZ
    # -------------------------------------------------------------------------

    # =========================================================================
    # HELPER 2: __insertar_encabezado_listbox
    # Elimina el duplicado de las 2 líneas fijas del listbox que aparecían
    # copiadas en __construir_seccion_lista y en __actualizar_listbox.
    # =========================================================================
    def __insertar_encabezado_listbox(self):
        """
        Inserta las dos líneas fijas del encabezado de la tabla en el listbox.

        Este método evita duplicar el mismo par de inserciones en
        __construir_seccion_lista (al crear la interfaz) y en
        __actualizar_listbox (al refrescar los datos).
        """
        self.__listbox_herramientas.insert(
            tk.END,
            "  {:<14} {:<18} {:<10} {}".format(
                "Tool ID", "Departure", "Rate/hr", "Status"
            )
        )
        self.__listbox_herramientas.insert(tk.END, "  " + "-" * 54)

    def __actualizar_listbox(self):
        """
        Reconstruye completamente el listbox con los datos actuales
        de la lista interna de herramientas.
        Se llama después de cada registro o retorno.
        """
        # Borrar todo el contenido actual
        self.__listbox_herramientas.delete(0, tk.END)

        # Reescribir el encabezado usando el helper
        self.__insertar_encabezado_listbox()

        # Recorrer la lista e insertar una línea por herramienta
        for herramienta in self.__lista_herramientas:
            datos = herramienta.obtener_resumen()
            linea = "  {:<14} {:<18} ${:<9} {}".format(
                datos["id"],
                datos["salida_texto"],
                str(datos["tarifa"]),
                datos["estado"]
            )
            self.__listbox_herramientas.insert(tk.END, linea)

    def __actualizar_combo_retorno(self):
        """
        Actualiza el Combobox de retorno con solo las herramientas activas.
        Una herramienta activa es aquella que aún no ha sido devuelta.
        Se llama después de cada registro o retorno.
        """
        lista_ids_activos = []
        for herramienta in self.__lista_herramientas:
            if herramienta.esta_disponible():
                lista_ids_activos.append(herramienta.obtener_id())

        self.__combo_herramienta["values"] = lista_ids_activos
        self.__combo_herramienta.set("-- Select active tool --")

    def __formatear_desglose(self, desglose):
        """
        Convierte el diccionario de desglose de tiempo en un texto legible.
        Solo incluye las unidades que sean mayores a cero.

        Ejemplos:
          { dias:0, horas:3, minutos:30 } → "3 hrs, 30 min"
          { dias:1, horas:0, minutos:0  } → "1 day"
          { dias:0, horas:0, minutos:0  } → "0 min"

        Parámetros:
            desglose (dict): resultado de calcular_desglose_tiempo().

        Retorna:
            str: tiempo formateado de forma legible.
        """
        partes_tiempo = []

        if desglose["dias"] > 0:
            sufijo_dia = "day" if desglose["dias"] == 1 else "days"
            partes_tiempo.append("{} {}".format(desglose["dias"], sufijo_dia))

        if desglose["horas"] > 0:
            sufijo_hora = "hr" if desglose["horas"] == 1 else "hrs"
            partes_tiempo.append("{} {}".format(desglose["horas"], sufijo_hora))

        if desglose["minutos"] > 0:
            partes_tiempo.append("{} min".format(desglose["minutos"]))

        if len(partes_tiempo) == 0:
            partes_tiempo.append("0 min")

        return ", ".join(partes_tiempo)

    def __mostrar_resultado_retorno(self, herramienta, datetime_retorno,
                                     desglose, costo_total):
        """
        Actualiza las tres etiquetas del área de resultados con el detalle
        completo del retorno procesado.

        Parámetros:
            herramienta      (HerramientaAlquiler): herramienta devuelta.
            datetime_retorno (datetime):            momento de la devolución.
            desglose         (dict):                días, horas y minutos.
            costo_total      (float):               costo total calculado.
        """
        datetime_salida = herramienta.obtener_hora_salida()

        # Línea 1: identificación y rango de fechas
        self.__etiqueta_resultado_linea1.config(
            text="Tool: {}   |   Out: {}   |   In: {}".format(
                herramienta.obtener_id(),
                datetime_salida.strftime("%d/%m/%Y %H:%M"),
                datetime_retorno.strftime("%d/%m/%Y %H:%M")
            ),
            fg=COLOR_TEXTO_CLARO
        )

        # Línea 2: tiempo total desglosado en días, horas y minutos
        self.__etiqueta_resultado_linea2.config(
            text="Time used:  {}".format(self.__formatear_desglose(desglose)),
            fg=COLOR_EXITO
        )

        # Línea 3: fórmula explícita del cálculo (horas × tarifa = total)
        self.__etiqueta_resultado_linea3.config(
            text="Calculation:  {} hrs  x  ${}/hr  =  ${:.2f}".format(
                desglose["total_horas_decimal"],
                herramienta.obtener_tarifa(),
                costo_total
            ),
            fg=COLOR_ACENTO
        )

    # =========================================================================
    # HELPER 3: __limpiar_campos
    # Elimina el duplicado de campo.delete(0, tk.END) que se repetía
    # 7 veces en __registrar_herramienta y 5 veces en __registrar_retorno.
    # =========================================================================
    def __limpiar_campos(self, lista_campos):
        """
        Borra el contenido de cada campo Entry de la lista recibida.

        Este método evita repetir campo.delete(0, tk.END) individualmente
        en __registrar_herramienta (7 campos) y en __registrar_retorno
        (5 campos). Con el helper basta pasar la lista de campos a limpiar.

        Parámetros:
            lista_campos (list): lista de widgets tk.Entry a limpiar.
        """
        for campo in lista_campos:
            campo.delete(0, tk.END)

    # -------------------------------------------------------------------------
    # MÉTODOS PRIVADOS DE ACCIÓN (botones)
    # -------------------------------------------------------------------------

    def __registrar_herramienta(self):
        """
        Lee el formulario de registro, valida todos los campos
        y agrega la nueva herramienta a la lista interna.

        Validaciones aplicadas:
          - Tool ID no puede estar vacío.
          - No puede existir otra herramienta con el mismo ID.
          - La tarifa debe ser un número mayor a TARIFA_MINIMA.
          - La fecha de salida debe ser válida (día, mes, año, hora, minuto).
          - La fecha de salida no puede estar en el futuro.
        """
        # Leer y normalizar el ID (eliminar espacios y convertir a mayúsculas)
        id_ingresado     = self.__campo_id.get().strip().replace(" ", "").upper()
        tarifa_ingresada = self.__campo_tarifa.get().strip()

        # Validar que el ID no esté vacío
        if id_ingresado == "":
            messagebox.showwarning("Warning", "Please enter a Tool ID.")
            return

        # Validar que el ID no esté repetido en la lista
        if self.__existe_id_en_lista(id_ingresado):
            messagebox.showwarning(
                "Warning",
                "A tool with ID '{}' is already registered.".format(id_ingresado)
            )
            return

        # Validar que la tarifa sea un número mayor a TARIFA_MINIMA
        try:
            tarifa = float(tarifa_ingresada)
            if tarifa <= TARIFA_MINIMA:
                messagebox.showwarning(
                    "Warning",
                    "Hourly rate must be greater than {}.".format(TARIFA_MINIMA)
                )
                return
        except ValueError:
            messagebox.showerror(
                "Error",
                "Hourly rate must be a valid number.\nExample: 15000 or 25000.50"
            )
            return

        # Construir el datetime de salida desde los campos separados
        datetime_salida, mensaje_error = self.__construir_datetime(
            self.__campo_salida_dia.get().strip(),
            self.__campo_salida_mes.get().strip(),
            self.__campo_salida_anio.get().strip(),
            self.__campo_salida_hora.get().strip(),
            self.__campo_salida_minuto.get().strip()
        )

        if mensaje_error is not None:
            messagebox.showerror("Error - Departure Date", mensaje_error)
            return

        # La fecha de salida no puede ser en el futuro
        if datetime_salida > datetime.now():
            messagebox.showwarning(
                "Warning",
                "Departure date/time ({}) cannot be in the future.\n"
                "Please enter a past or current date/time.".format(
                    datetime_salida.strftime("%d/%m/%Y %H:%M")
                )
            )
            return

        # Crear el objeto y registrar la salida
        nueva_herramienta = HerramientaAlquiler(id_ingresado, tarifa)
        nueva_herramienta.registrar_salida(datetime_salida)

        # Agregar a la LISTA INTERNA
        self.__lista_herramientas.append(nueva_herramienta)

        # Actualizar la interfaz
        self.__actualizar_listbox()
        self.__actualizar_combo_retorno()

        # Mostrar confirmación en el área de resultados
        self.__etiqueta_resultado_linea1.config(
            text="Tool '{}' registered.  Departure: {}  |  Rate: ${}/hr".format(
                id_ingresado,
                datetime_salida.strftime("%d/%m/%Y %H:%M"),
                tarifa
            ),
            fg=COLOR_EXITO
        )
        self.__etiqueta_resultado_linea2.config(text="")
        self.__etiqueta_resultado_linea3.config(text="")

        # Limpiar los 7 campos del formulario usando el helper
        self.__limpiar_campos([
            self.__campo_id,
            self.__campo_tarifa,
            self.__campo_salida_dia,
            self.__campo_salida_mes,
            self.__campo_salida_anio,
            self.__campo_salida_hora,
            self.__campo_salida_minuto
        ])
        self.__campo_id.focus()

    def __registrar_retorno(self):
        """
        Lee el formulario de retorno, valida los campos
        y procesa la devolución de la herramienta seleccionada.

        Validaciones aplicadas:
          - Debe haber al menos una herramienta registrada.
          - Se debe haber seleccionado una herramienta del Combobox.
          - La herramienta debe estar activa (no devuelta anteriormente).
          - La fecha de retorno debe ser válida.
          - El retorno debe ser posterior a la salida.
        """
        # Verificar que haya herramientas en la lista
        if len(self.__lista_herramientas) == 0:
            messagebox.showwarning(
                "Warning", "There are no tools registered in the system."
            )
            return

        # Verificar que se haya seleccionado una herramienta
        id_seleccionado = self.__combo_herramienta.get()
        if id_seleccionado == "" or id_seleccionado == "-- Select active tool --":
            messagebox.showwarning(
                "Warning", "Please select an active tool from the dropdown."
            )
            return

        # Buscar la herramienta en la lista por su ID
        herramienta_seleccionada = self.__buscar_herramienta_por_id(id_seleccionado)

        if herramienta_seleccionada is None:
            messagebox.showerror(
                "Error",
                "Tool '{}' not found in the system.".format(id_seleccionado)
            )
            return

        # Verificar que la herramienta aún esté activa
        if not herramienta_seleccionada.esta_disponible():
            messagebox.showwarning(
                "Warning",
                "Tool '{}' has already been returned.".format(id_seleccionado)
            )
            self.__actualizar_combo_retorno()
            return

        # Construir el datetime de retorno desde los campos separados
        datetime_retorno, mensaje_error = self.__construir_datetime(
            self.__campo_retorno_dia.get().strip(),
            self.__campo_retorno_mes.get().strip(),
            self.__campo_retorno_anio.get().strip(),
            self.__campo_retorno_hora.get().strip(),
            self.__campo_retorno_minuto.get().strip()
        )

        if mensaje_error is not None:
            messagebox.showerror("Error - Return Date", mensaje_error)
            return

        # El retorno debe ser estrictamente posterior a la salida
        datetime_salida = herramienta_seleccionada.obtener_hora_salida()
        if datetime_retorno <= datetime_salida:
            messagebox.showwarning(
                "Warning",
                "Return date/time ({}) must be after\n"
                "departure date/time ({}).".format(
                    datetime_retorno.strftime("%d/%m/%Y %H:%M"),
                    datetime_salida.strftime("%d/%m/%Y %H:%M")
                )
            )
            return

        # Registrar retorno y calcular costo usando los métodos de la clase
        herramienta_seleccionada.registrar_retorno(datetime_retorno)
        costo_total = herramienta_seleccionada.calcular_costo(datetime_retorno)
        desglose    = herramienta_seleccionada.calcular_desglose_tiempo(datetime_retorno)

        # Actualizar la interfaz
        self.__actualizar_listbox()
        self.__actualizar_combo_retorno()

        # Mostrar el resultado en el área de resultados
        self.__mostrar_resultado_retorno(
            herramienta_seleccionada, datetime_retorno, desglose, costo_total
        )

        # Mostrar cuadro de diálogo con el resumen del retorno
        messagebox.showinfo(
            "Return Registered",
            "Tool: {}\nTime used: {}\nTotal cost: ${:.2f}".format(
                id_seleccionado,
                self.__formatear_desglose(desglose),
                costo_total
            )
        )

        # Limpiar los 5 campos del formulario de retorno usando el helper
        self.__limpiar_campos([
            self.__campo_retorno_dia,
            self.__campo_retorno_mes,
            self.__campo_retorno_anio,
            self.__campo_retorno_hora,
            self.__campo_retorno_minuto
        ])

    def __salir(self):
        """
        Solicita confirmación antes de cerrar la aplicación.
        Se activa tanto con el botón Exit como con el botón X de la ventana.
        """
        confirmacion = messagebox.askyesno(
            "Exit",
            "Are you sure you want to exit the system?"
        )
        if confirmacion:
            self.__ventana.destroy()


# =============================================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# El bloque if __name__ == "__main__" garantiza que el código solo se ejecute
# cuando el archivo se corre directamente, no cuando se importa como módulo.
# =============================================================================
if __name__ == "__main__":
    ventana_login = tk.Tk()
    VentanaLogin(ventana_login)
    ventana_login.mainloop()
