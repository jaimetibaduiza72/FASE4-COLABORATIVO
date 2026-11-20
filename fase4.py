# ==================================================
# SOFTWARE FJ - FASE 4 / ACTIVIDAD 4
# Archivo: fase4.py
# Descripción: Sistema de reservas, alquiler y asesorías
# Documentado línea por línea para el Anexo 3
# ==================================================

# --- IMPORTACIONES ---
# Importa ABC para crear clases abstractas y abstractmethod para obligar a implementar métodos
from abc import ABC, abstractmethod
# Importa datetime para poner fecha y hora en los logs
from datetime import datetime
# Importa math para usar isfinite y validar que un número no sea infinito ni NaN
import math
# Importa re para usar expresiones regulares en correo, documento y teléfono
import re

# ==================================================
# LOGS - Función para guardar eventos en logs.txt
# ==================================================
# Define la función registrar_log que recibe un mensaje de texto
def registrar_log(mensaje):
    # Abre el archivo logs.txt en modo "a" (agregar, no borrar lo anterior), con tildes en español
    with open("logs.txt", "a", encoding="utf-8") as archivo:
        # Guarda la fecha y hora actual en formato Año-Mes-Día Hora:Minuto:Segundo
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Escribe en el archivo la fecha entre corchetes + el mensaje + salto de línea
        archivo.write(f"[{fecha}] {mensaje}\n")

# ==================================================
# EXCEPCIONES PERSONALIZADAS - Errores propios del sistema
# ==================================================
# Crea la excepción ClienteError, hereda de Exception, para errores de cliente
class ClienteError(Exception):
    pass # No necesita código extra, solo sirve para identificar el tipo de error
# Crea la excepción ServicioError para errores de servicio
class ServicioError(Exception):
    pass # Solo marca el tipo de error
# Crea la excepción ReservaError para errores de reserva
class ReservaError(Exception):
    pass # Solo marca el tipo de error

# ==================================================
# CLASE ABSTRACTA ENTIDAD - Base para Cliente y Servicio
# ==================================================
# Define Entidad como clase abstracta, no se puede crear un objeto Entidad directo
class Entidad(ABC):
    # Declara mostrar_info como método abstracto, obliga a las hijas a crearlo
    @abstractmethod
    def mostrar_info(self):
        pass # Las clases hijas deben poner su propio código aquí

# ==================================================
# CLASE CLIENTE - Hereda de Entidad
# ==================================================
# Define Cliente que hereda de Entidad, por eso debe tener mostrar_info
class Cliente(Entidad):
    # Constructor: recibe nombre, correo, documento y teléfono al crear un cliente
    def __init__(self, nombre, correo, documento, telefono):
        # Valida que nombre sea texto y que al quitar espacios no quede vacío
        if not isinstance(nombre, str) or not nombre.strip():
            # Si falla, lanza ClienteError con mensaje claro
            raise ClienteError("El nombre no puede estar vacío")
        # Define el patrón regex para el correo: usuario + @ + dominio + punto + extensión
        patron_correo = (
            r"[A-Za-z0-9_%+-]+(?:\.[A-Za-z0-9_%+-]+)*@"
            r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
            r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+"
        )
        # Valida que correo sea texto y que cumpla completo el patrón, si no, error
        if not isinstance(correo, str) or not re.fullmatch(patron_correo, correo):
            raise ClienteError("Correo electrónico inválido")
        # Valida que documento sea texto, si es número u otro tipo, error
        if not isinstance(documento, str):
            raise ClienteError("El documento debe ser texto")
        # Limpia el documento: quita espacios, puntos y guiones, deja solo dígitos
        documento_normalizado = re.sub(r"[\s.-]", "", documento)
        # Valida que el documento tenga entre 6 y 12 dígitos, solo números
        if not re.fullmatch(r"[0-9]{6,12}", documento_normalizado):
            raise ClienteError("El documento debe contener entre 6 y 12 dígitos")
        # Valida que teléfono sea texto
        if not isinstance(telefono, str):
            raise ClienteError("El teléfono debe ser texto")
        # Limpia el teléfono: quita espacios, paréntesis, puntos y guiones, deja + y dígitos
        telefono_normalizado = re.sub(r"[\s().-]", "", telefono)
        # Quita el + del inicio para validar solo los dígitos
        numero_telefono = telefono_normalizado.removeprefix("+")
        # Valida teléfono: 7 a 15 dígitos, máximo un + y si tiene + debe ir al inicio
        if (
            not re.fullmatch(r"[0-9]{7,15}", numero_telefono)
            or telefono_normalizado.count("+") > 1
            or ("+" in telefono_normalizado and not telefono_normalizado.startswith("+"))
        ):
            raise ClienteError("El teléfono debe contener entre 7 y 15 dígitos")
        # Guarda el nombre en atributo privado __nombre, nadie lo cambia desde fuera
        self.__nombre = nombre
        # Guarda el correo en atributo privado __correo
        self.__correo = correo
        # Guarda el documento ya limpio en atributo privado __documento
        self.__documento = documento_normalizado
        # Guarda el teléfono ya limpio en atributo privado __telefono
        self.__telefono = telefono_normalizado
    # Property para leer el nombre sin poder cambiarlo desde fuera
    @property
    def nombre(self):
        return self.__nombre # Devuelve el nombre privado
    # Property para leer el correo
    @property
    def correo(self):
        return self.__correo # Devuelve el correo privado
    # Property para leer el documento
    @property
    def documento(self):
        return self.__documento # Devuelve el documento privado
    # Property para leer el teléfono
    @property
    def telefono(self):
        return self.__telefono # Devuelve el teléfono privado
    # Implementa mostrar_info obligatorio de Entidad, devuelve los datos en una línea
    def mostrar_info(self):
        return (
            f"Nombre: {self.__nombre} | Correo: {self.__correo} | "
            f"Documento: {self.__documento} | Teléfono: {self.__telefono}"
        )

# ==================================================
# CLASE ABSTRACTA SERVICIO - Hereda de Entidad
# ==================================================
# Define Servicio abstracto, hereda de Entidad, base para sala, equipo y asesoría
class Servicio(Entidad):
    # Constructor: recibe nombre y precio_base
    def __init__(self, nombre, precio_base):
        # Valida precio: debe ser número, no bool, finito y mayor que 0
        if (
            not isinstance(precio_base, (int, float))
            or isinstance(precio_base, bool)
            or not math.isfinite(precio_base)
            or precio_base <= 0
        ):
            raise ServicioError("El precio debe ser mayor que 0")
        # Valida que nombre sea texto y no quede vacío al quitar espacios
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioError("El nombre del servicio no puede estar vacío")
        # Guarda el nombre como público, se usa en el menú para mostrarlo
        self.nombre = nombre
        # Guarda el precio en privado __precio_base, solo se lee con @property
        self.__precio_base = precio_base
    # Property para leer el precio sin poder cambiarlo desde fuera
    @property
    def precio_base(self):
        return self.__precio_base # Devuelve el precio privado
    # Implementa mostrar_info de Entidad, muestra nombre, tipo y precio
    def mostrar_info(self):
        return (
            f"Nombre: {self.nombre} | Tipo: {self.descripcion()} | "
            f"Precio base: ${self.precio_base:,.0f}"
        )
    # Método abstracto calcular_costo, cada servicio debe crearlo a su manera
    @abstractmethod
    def calcular_costo(
        self, duracion: float, impuesto: float = 0, descuento: float = 0
    ) -> float:
        pass # Las hijas ponen la fórmula
    # Método helper para calcular costo, evita repetir validaciones en cada servicio
    def _calcular_costo(
        self, duracion: float, impuesto: float, descuento: float
    ) -> float:
        # Agrupa los 3 valores para validarlos juntos
        valores = (duracion, impuesto, descuento)
        # Valida que los 3 sean números, no bool y finitos
        if any(
            not isinstance(valor, (int, float))
            or isinstance(valor, bool)
            or not math.isfinite(valor)
            for valor in valores
        ):
            raise ServicioError("Duración, impuesto y descuento deben ser números")
        # Valida que duración sea mayor que 0
        if duracion <= 0:
            raise ServicioError("La duración debe ser mayor que cero")
        # Valida que impuesto esté entre 0 y 1 (0% a 100%), antes aceptaba 5 = 500%
        if not 0 <= impuesto <= 1:
            raise ServicioError("El impuesto debe estar entre 0 y 1")
        # Valida que descuento esté entre 0 y 1
        if not 0 <= descuento <= 1:
            raise ServicioError("El descuento debe estar entre 0 y 1")
        # Calcula subtotal: precio_base * duración
        subtotal = self.precio_base * duracion
        # Aplica impuesto y descuento: subtotal * (1+impuesto) * (1-descuento)
        return subtotal * (1 + impuesto) * (1 - descuento)
    # Método abstracto descripcion, cada servicio dice qué tipo es
    @abstractmethod
    def descripcion(self):
        pass # Las hijas devuelven su texto

# ==================================================
# SERVICIO RESERVA DE SALAS - Hereda de Servicio
# ==================================================
class ReservaSala(Servicio):
    # Constructor: recibe nombre, precio y capacidad
    def __init__(self, nombre, precio_base, capacidad):
        # Llama al constructor del padre Servicio para validar nombre y precio
        super().__init__(nombre, precio_base)
        # Valida capacidad: debe ser entero, no bool y mayor que 0
        if (
            not isinstance(capacidad, int)
            or isinstance(capacidad, bool)
            or capacidad <= 0
        ):
            raise ServicioError("La capacidad debe ser un entero mayor que cero")
        # Guarda la capacidad
        self.capacidad = capacidad
    # Sobrescribe calcular_costo, usa el helper del padre (sobrecarga con impuesto/descuento)
    def calcular_costo(
        self, duracion: float, impuesto: float = 0, descuento: float = 0
    ) -> float:
        return self._calcular_costo(duracion, impuesto, descuento)
    # Devuelve el texto del tipo de servicio
    def descripcion(self):
        return "Reserva de sala"

# ==================================================
# SERVICIO ALQUILER EQUIPOS - Hereda de Servicio
# ==================================================
class AlquilerEquipo(Servicio):
    # Constructor: recibe nombre, precio y stock
    def __init__(self, nombre, precio_base, stock):
        # Llama al padre para validar nombre y precio
        super().__init__(nombre, precio_base)
        # Valida stock: debe ser entero, no bool y mayor o igual a 0
        if not isinstance(stock, int) or isinstance(stock, bool) or stock < 0:
            raise ServicioError("El stock debe ser un entero igual o mayor que cero")
        # Guarda el stock
        self.stock = stock
    # Sobrescribe calcular_costo con el helper del padre
    def calcular_costo(
        self, duracion: float, impuesto: float = 0, descuento: float = 0
    ) -> float:
        return self._calcular_costo(duracion, impuesto, descuento)
    # Devuelve el texto del tipo
    def descripcion(self):
        return "Alquiler de equipos"

# ==================================================
# SERVICIO ASESORIA - Hereda de Servicio
# ==================================================
class AsesoriaEspecializada(Servicio):
    # Constructor: recibe nombre, precio y tema
    def __init__(self, nombre, precio_base, tema):
        # Llama al padre para validar nombre y precio
        super().__init__(nombre, precio_base)
        # Valida tema: debe ser texto y no quedar vacío al quitar espacios
        if not isinstance(tema, str) or not tema.strip():
            raise ServicioError("El tema de la asesoría no puede estar vacío")
        # Guarda el tema ya sin espacios al inicio y al final
        self.tema = tema.strip()
    # Sobrescribe calcular_costo con el helper del padre
    def calcular_costo(
        self, duracion: float, impuesto: float = 0, descuento: float = 0
    ) -> float:
        return self._calcular_costo(duracion, impuesto, descuento)
    # Devuelve el texto del tipo
    def descripcion(self):
        return "Asesoría especializada"

# ==================================================
# CLASE RESERVA - Une Cliente + Servicio + Duración
# ==================================================
class Reserva:
    # Constructor: recibe cliente, servicio y duración
    def __init__(self, cliente, servicio, duracion):
        # Valida que cliente sea realmente un objeto Cliente, si es None o texto, error
        if not isinstance(cliente, Cliente):
            raise ReservaError("El cliente debe ser una instancia de Cliente")
        # Valida que servicio sea realmente un objeto Servicio
        if not isinstance(servicio, Servicio):
            raise ReservaError("El servicio debe ser una instancia de Servicio")
        # Valida que duración sea número, no bool y finito
        if (
            not isinstance(duracion, (int, float))
            or isinstance(duracion, bool)
            or not math.isfinite(duracion)
        ):
            raise ReservaError("La duración debe ser un número")
        # Valida que duración sea mayor que 0
        if duracion <= 0:
            raise ReservaError("La duración debe ser mayor que cero")
        # Guarda el cliente
        self.cliente = cliente
        # Guarda el servicio
        self.servicio = servicio
        # Guarda la duración
        self.duracion = duracion
        # Estado inicial siempre Pendiente
        self.estado = "Pendiente"
    # Método para confirmar la reserva
    def confirmar(self):
        # Si ya está Confirmada, no deja confirmar otra vez
        if self.estado == "Confirmada":
            raise ReservaError("La reserva ya está confirmada")
        # Si está Cancelada, no deja confirmarla
        if self.estado == "Cancelada":
            raise ReservaError("No se puede confirmar una reserva cancelada")
        # Intenta cambiar estado y guardar log
        try:
            # Cambia el estado a Confirmada
            self.estado = "Confirmada"
            # Guarda en logs.txt que se confirmó
            registrar_log(f"Reserva confirmada para {self.cliente.nombre}")
        # Si falla el archivo, captura OSError
        except OSError as e:
            # Lanza ReservaError encadenado con from e, para no perder el error original
            raise ReservaError("Error confirmando reserva") from e
    # Método para cancelar la reserva
    def cancelar(self):
        # Si ya está Cancelada, no deja cancelar otra vez
        if self.estado == "Cancelada":
            raise ReservaError("La reserva ya está cancelada")
        # Cambia el estado a Cancelada
        self.estado = "Cancelada"
        # Guarda en logs.txt que se canceló
        registrar_log(f"Reserva cancelada para {self.cliente.nombre}")
    # Método para procesar la reserva y calcular el costo
    def procesar(self):
        # Si está Cancelada, no deja procesarla
        if self.estado == "Cancelada":
            raise ReservaError("No se puede procesar una reserva cancelada")
        # Intenta calcular el costo con el servicio
        try:
            # Llama a calcular_costo del servicio con la duración
            costo = self.servicio.calcular_costo(self.duracion)
        # Si hay error de servicio o de archivo, lo captura
        except (ServicioError, OSError) as e:
            # Guarda el error en logs
            registrar_log(f"Error de procesamiento: {e}")
            # Lanza ReservaError encadenado
            raise ReservaError("Error procesando reserva") from e
        # Si no hubo error, entra al else
        else:
            # Guarda en logs que se procesó bien
            registrar_log("Reserva procesada correctamente")
            # Devuelve el costo calculado
            return costo
        # Finally siempre se ejecuta, haya error o no
        finally:
            # Guarda en logs que terminó el proceso
            registrar_log("Finalización del proceso de reserva")

# ==================================================
# SIMULACIÓN - 10 operaciones automáticas
# ==================================================
# Define la función que corre las 10 operaciones sin pedir datos al usuario
def ejecutar_simulacion():
    # Crea la lista vacía donde van las 10 operaciones
    operaciones = []
    # Define helper interno para correr una operación y registrar si fue válida o inválida
    def ejecutar_operacion(numero, descripcion, accion, espera_error=False):
        # Intenta ejecutar la acción (crear cliente, sala, etc.)
        try:
            resultado = accion()
        # Si lanza ClienteError, ServicioError, ReservaError o ValueError, lo captura
        except (ClienteError, ServicioError, ReservaError, ValueError) as error:
            # Si NO esperábamos error pero pasó, lo marca como error inesperado
            if not espera_error:
                registrar_log(f"SIMULACIÓN {numero}/10 ERROR inesperado en {descripcion}: {error}")
                return # Sale sin seguir
            # Si SÍ esperábamos error, lo marca como caso inválido esperado, que está bien
            registrar_log(f"SIMULACIÓN {numero}/10 CASO INVÁLIDO esperado ({descripcion}): {error}")
        # Si no hubo excepción, entra al else
        else:
            # Si esperábamos error pero no pasó, es un error porque aceptó algo inválido
            if espera_error:
                registrar_log(f"SIMULACIÓN {numero}/10 ERROR: se aceptó un caso inválido ({descripcion})")
                return
            # Si era caso válido y pasó, lo registra como válido con su resultado
            registrar_log(f"SIMULACIÓN {numero}/10 CASO VÁLIDO ({descripcion}): {resultado}")
    # Función para crear un cliente válido de ejemplo
    def crear_cliente():
        # Crea cliente Ana Pérez con datos válidos
        cliente = Cliente("Ana Pérez", "ana@example.com", "12345678", "+573001234567")
        # Devuelve su info para el log
        return cliente.mostrar_info()
    # Función para crear sala válida y calcular costo con impuesto y descuento
    def crear_sala():
        # Crea sala Norte, precio 100, capacidad 12
        sala = ReservaSala("Sala Norte", 100, 12)
        # Calcula costo 2 horas, impuesto 19%, descuento 10% -> 214.20
        costo = sala.calcular_costo(2, 0.19, 0.1)
        # Devuelve texto para el log
        return f"{sala.descripcion()}, capacidad {sala.capacidad}, costo {costo:.2f}"
    # Función para crear equipo válido
    def crear_equipo():
        # Crea proyector, precio 50, stock 4
        equipo = AlquilerEquipo("Proyector", 50, 4)
        # Calcula costo 3 días con descuento 10%
        costo = equipo.calcular_costo(3, descuento=0.1)
        # Devuelve texto para el log
        return f"{equipo.descripcion()}, stock {equipo.stock}, costo {costo:.2f}"
    # Función para crear asesoría válida
    def crear_asesoria():
        # Crea consultoría, precio 200, tema Finanzas
        asesoria = AsesoriaEspecializada("Consultoría", 200, "Finanzas")
        # Calcula costo 1 hora sin impuesto ni descuento
        costo = asesoria.calcular_costo(1)
        # Devuelve texto para el log
        return f"{asesoria.descripcion()}, tema {asesoria.tema}, costo {costo:.2f}"
    # Función para probar cancelar dos veces, la segunda debe fallar
    def cancelar_dos_veces():
        # Crea cliente y sala de ejemplo
        cliente = Cliente("Ana Pérez", "ana@example.com", "12345678", "+573001234567")
        sala = ReservaSala("Sala simulada", 100, 10)
        # Crea reserva de 1 hora
        reserva = Reserva(cliente, sala, 1)
        # Primera cancelación, debe pasar
        reserva.cancelar()
        # Segunda cancelación, debe lanzar ReservaError
        reserva.cancelar()
    # Agrega las 10 operaciones a la lista: (descripción, función, ¿espera error?)
    operaciones.extend([
        ("cliente con datos válidos", crear_cliente, False),
        ("documento inválido", lambda: Cliente("Ana", "ana@example.com", "12AB", "3001234567"), True),
        ("teléfono inválido", lambda: Cliente("Ana", "ana@example.com", "12345678", "123"), True),
        ("sala y cálculo de costo válidos", crear_sala, False),
        ("capacidad inválida", lambda: ReservaSala("Sala", 100, 0), True),
        ("equipo y cálculo de costo válidos", crear_equipo, False),
        ("stock inválido", lambda: AlquilerEquipo("Proyector", 50, -1), True),
        ("asesoría y cálculo de costo válidos", crear_asesoria, False),
        ("tema de asesoría inválido", lambda: AsesoriaEspecializada("Consultoría", 200, " "), True),
        ("cancelación repetida", cancelar_dos_veces, True),
    ])
    # Guarda en logs que empezó la simulación
    registrar_log("Inicio de simulación de 10 operaciones")
    # Recorre las 10 operaciones con número del 1 al 10
    for numero, (descripcion, accion, espera_error) in enumerate(operaciones, 1):
        # Ejecuta cada operación con su helper
        ejecutar_operacion(numero, descripcion, accion, espera_error)
    # Guarda en logs que terminó la simulación
    registrar_log("Fin de simulación de 10 operaciones")
    # Muestra en pantalla que terminó
    print("Simulación completada. Resultados guardados en logs.txt")

# ==================================================
# LISTAS DEL SISTEMA - Guardan todo en memoria
# ==================================================
# Lista vacía para guardar clientes creados
clientes = []
# Lista vacía para guardar servicios creados
servicios = []
# Lista vacía para guardar reservas creadas
reservas = []

# ==================================================
# MENU PRINCIPAL - Bucle infinito hasta salir con 7
# ==================================================
# Bucle infinito, solo sale con break en opción 7
while True:
    # Salto de línea para separar
    print("\n")
    # Línea de adorno
    print("=" * 50)
    # Título del sistema
    print("      SOFTWARE FJ")
    # Línea de adorno
    print("=" * 50)
    # Opción 1
    print("1. Registrar Cliente")
    # Opción 2
    print("2. Crear Servicio")
    # Opción 3
    print("3. Generar Reserva")
    # Opción 4
    print("4. Ver Clientes")
    # Opción 5
    print("5. Ver Servicios")
    # Opción 6
    print("6. Ver Reservas")
    # Opción 7
    print("7. Salir")
    # Opción 8
    print("8. Ejecutar simulación de 10 operaciones")
    # Pide la opción al usuario
    opcion = input("\nSeleccione una opción: ")
    # Si elige 1, registra cliente
    if opcion == "1":
        # Intenta crear el cliente
        try:
            # Pide nombre
            nombre = input("Ingrese nombre: ")
            # Pide correo
            correo = input("Ingrese correo: ")
            # Pide documento
            documento = input("Ingrese documento (6-12 dígitos): ")
            # Pide teléfono
            telefono = input("Ingrese teléfono (7-15 dígitos): ")
            # Crea el objeto Cliente con los datos, aquí se validan
            cliente = Cliente(nombre, correo, documento, telefono)
            # Lo agrega a la lista de clientes
            clientes.append(cliente)
            # Guarda en logs que se registró
            registrar_log(f"Cliente registrado: {nombre}")
            # Muestra mensaje de éxito
            print("Cliente registrado exitosamente")
        # Si hay error de cliente, lo muestra y lo guarda
        except ClienteError as e:
            print("ERROR:", e)
            registrar_log(str(e))
        # Si hay error de valor (ej: letra donde va número), lo muestra
        except ValueError as e:
            print("ERROR:", e)
            registrar_log(str(e))
    # Si elige 2, crea servicio
    elif opcion == "2":
        # Intenta crear el servicio
        try:
            # Muestra subtipos
            print("\n1. Reserva Sala")
            print("2. Alquiler Equipos")
            print("3. Asesoría")
            # Pide el tipo
            tipo = input("Seleccione servicio: ")
            # Pide nombre del servicio
            nombre_servicio = input("Nombre del servicio: ")
            # Pide precio y lo convierte a float
            precio = float(input("Precio base: "))
            # Si es 1, es sala
            if tipo == "1":
                # Pide capacidad y la convierte a entero
                capacidad = int(input("Capacidad de la sala: "))
                # Crea ReservaSala
                servicio = ReservaSala(nombre_servicio, precio, capacidad)
            # Si es 2, es equipo
            elif tipo == "2":
                # Pide stock
                stock = int(input("Stock disponible: "))
                # Crea AlquilerEquipo
                servicio = AlquilerEquipo(nombre_servicio, precio, stock)
            # Si es 3, es asesoría
            elif tipo == "3":
                # Pide tema
                tema = input("Tema de la asesoría: ")
                # Crea AsesoriaEspecializada
                servicio = AsesoriaEspecializada(nombre_servicio, precio, tema)
            # Si no es 1,2 ni 3, error
            else:
                raise ServicioError("Tipo inválido")
            # Agrega el servicio a la lista
            servicios.append(servicio)
            # Muestra éxito
            print("Servicio creado con éxito")
            # Guarda en logs
            registrar_log(f"Servicio creado: {nombre_servicio}")
        # Captura error de servicio
        except ServicioError as e:
            print("ERROR:", e)
            registrar_log(str(e))
        # Captura error de valor
        except ValueError as e:
            print("ERROR:", e)
            registrar_log(str(e))
    # Si elige 3, genera reserva
    elif opcion == "3":
        # Intenta crear la reserva
        try:
            # Si no hay clientes, no puede reservar
            if len(clientes) == 0:
                raise ReservaError("Primero debe registrar clientes")
            # Si no hay servicios, no puede reservar
            if len(servicios) == 0:
                raise ReservaError("Primero debe registrar servicios")
            # Muestra título clientes
            print("\nCLIENTES")
            # Muestra cada cliente con número
            for i, cliente in enumerate(clientes):
                print(f"{i+1}. {cliente.nombre}")
            # Pide cliente y resta 1 porque la lista empieza en 0
            cli = int(input("Seleccione cliente: ")) - 1
            # Valida que el índice esté dentro de la lista, antes el 0 cogía el último
            if not 0 <= cli < len(clientes):
                raise ReservaError("Selección de cliente inválida")
            # Muestra título servicios
            print("\nSERVICIOS")
            # Muestra cada servicio con número
            for i, servicio in enumerate(servicios):
                print(f"{i+1}. {servicio.nombre}")
            # Pide servicio y resta 1
            ser = int(input("Seleccione servicio: ")) - 1
            # Valida índice de servicio
            if not 0 <= ser < len(servicios):
                raise ReservaError("Selección de servicio inválida")
            # Pide duración y la convierte a entero
            duracion = int(input("Duración (horas o días): "))
            # Crea la reserva con cliente, servicio y duración
            reserva = Reserva(clientes[cli], servicios[ser], duracion)
            # Confirma la reserva
            reserva.confirmar()
            # Procesa la reserva y calcula el costo
            costo = reserva.procesar()
            # Agrega la reserva a la lista
            reservas.append(reserva)
            # Muestra que se creó bien
            print("Reserva creada correctamente.")
            # Muestra el costo total con formato
            print(f"Costo Total: ${costo:,.0f}")
        # Captura errores por tipo
        except ClienteError as e:
            print("ERROR:", e)
            registrar_log(str(e))
        except ServicioError as e:
            print("ERROR:", e)
            registrar_log(str(e))
        except ReservaError as e:
            print("ERROR:", e)
            registrar_log(str(e))
        except ValueError as e:
            print("ERROR:", e)
            registrar_log(str(e))
    # Si elige 4, ver clientes
    elif opcion == "4":
        # Título
        print("\nCLIENTES REGISTRADOS")
        # Si no hay clientes, avisa
        if len(clientes) == 0:
            print("No existen clientes")
        # Si sí hay, los muestra uno por uno
        else:
            for cliente in clientes:
                print(cliente.mostrar_info())
    # Si elige 5, ver servicios
    elif opcion == "5":
        # Título
        print("\nSERVICIOS REGISTRADOS")
        # Si no hay servicios, avisa
        if len(servicios) == 0:
            print("No existen servicios")
        # Si sí hay, los muestra
        else:
            for servicio in servicios:
                # Muestra nombre
                print(f"Nombre: {servicio.nombre}")
                # Muestra tipo con descripcion()
                print(f"Tipo: {servicio.descripcion()}")
                # Muestra precio base
                print(f"Precio Base: ${servicio.precio_base:,.0f}")
                # Si es sala, muestra capacidad
                if isinstance(servicio, ReservaSala):
                    print(f"Capacidad: {servicio.capacidad}")
                # Si es equipo, muestra stock
                elif isinstance(servicio, AlquilerEquipo):
                    print(f"Stock: {servicio.stock}")
                # Si es asesoría, muestra tema
                elif isinstance(servicio, AsesoriaEspecializada):
                    print(f"Tema: {servicio.tema}")
                # Línea de separación
                print("-" * 30)
    # Si elige 6, ver reservas
    elif opcion == "6":
        # Título
        print("\nRESERVAS REALIZADAS")
        # Si no hay reservas, avisa
        if len(reservas) == 0:
            print("No existen reservas")
        # Si sí hay, las muestra
        else:
            for reserva in reservas:
                # Muestra cliente de la reserva
                print(f"Cliente: {reserva.cliente.nombre}")
                # Muestra servicio
                print(f"Servicio: {reserva.servicio.nombre}")
                # Muestra duración
                print(f"Duración: {reserva.duracion}")
                # Muestra estado
                print(f"Estado: {reserva.estado}")
                # Línea de separación
                print("-" * 30)
    # Si elige 7, reporte final y salir
    elif opcion == "7":
        # Abre reporte_final.txt para escribir, borra lo anterior
        with open("reporte_final.txt", "w", encoding="utf-8") as reporte:
            # Escribe título
            reporte.write("REPORTE FINAL SOFTWARE FJ\n")
            # Escribe línea de adorno
            reporte.write("=" * 50 + "\n\n")
            # Escribe sección clientes
            reporte.write("CLIENTES REGISTRADOS\n")
            # Escribe cada cliente
            for cliente in clientes:
                reporte.write(f"{cliente.nombre} - {cliente.correo} - Documento: {cliente.documento} - Teléfono: {cliente.telefono}\n")
            # Salto de línea
            reporte.write("\n")
            # Escribe sección servicios
            reporte.write("SERVICIOS REGISTRADOS\n")
            # Escribe cada servicio
            for servicio in servicios:
                reporte.write(f"{servicio.nombre} - ${servicio.precio_base}\n")
                # Si es sala, escribe capacidad
                if isinstance(servicio, ReservaSala):
                    reporte.write(f"Capacidad: {servicio.capacidad}\n")
                # Si es equipo, escribe stock
                elif isinstance(servicio, AlquilerEquipo):
                    reporte.write(f"Stock: {servicio.stock}\n")
                # Si es asesoría, escribe tema
                elif isinstance(servicio, AsesoriaEspecializada):
                    reporte.write(f"Tema: {servicio.tema}\n")
            # Salto de línea
            reporte.write("\n")
            # Escribe sección reservas
            reporte.write("RESERVAS REALIZADAS\n")
            # Escribe cada reserva
            for reserva in reservas:
                reporte.write(f"Cliente: {reserva.cliente.nombre}\n")
                reporte.write(f"Servicio: {reserva.servicio.nombre}\n")
                reporte.write(f"Duración: {reserva.duracion}\n")
                reporte.write(f"Estado: {reserva.estado}\n")
                reporte.write("-" * 30 + "\n")
        # Muestra título de reporte en pantalla
        print("\n")
        print("=" * 50)
        print("REPORTE FINAL")
        print("=" * 50)
        # Muestra total clientes
        print(f"Total clientes: {len(clientes)}")
        # Muestra total servicios
        print(f"Total servicios: {len(servicios)}")
        # Muestra total reservas
        print(f"Total reservas: {len(reservas)}")
        # Avisa que se generó el archivo
        print("\nSe generó el archivo:")
        print("reporte_final.txt")
        # Guarda en logs que terminó
        registrar_log("Sistema finalizado correctamente.")
        # Sale del while True, termina el programa
        break
    # Si elige 8, ejecuta simulación
    elif opcion == "8":
        # Llama a la función de simulación de 10 operaciones
        ejecutar_simulacion()
    # Si no es 1-8, opción inválida
    else:
        # Muestra mensaje y vuelve al menú, sin salir del programa
        print("Opción inválida")
        break
    else:

        print("Opción inválida")
