# ==========================================================
# SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS

# IMPORTACIÓN DE LIBRERÍAS
# ==========================================================
from abc import ABC, abstractmethod
from datetime import datetime

# FUNCION PARA REGISTRAR EL LOG
# ==================================================

def registrar_log(mensaje):
    with open("logs.txt", "a", encoding="utf-8") as archivo:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        archivo.write(f"[{fecha}] {mensaje}\n")


# EXCEPCIONES PERSONALIZADAS
# ==================================================

class ClienteError(Exception):
    pass


class ServicioError(Exception):
    pass


class ReservaError(Exception):
    pass



# CLASE ABSTRACTA ENTIDAD
# ==================================================

class Entidad(ABC):

    @abstractmethod
    def mostrar_info(self):
        pass


# CLASE CLIENTE
# ==================================================

class Cliente(Entidad):

    def __init__(self, nombre, correo):

        if not nombre.strip():
            raise ClienteError("El nombre no puede estar vacío")

        if "@" not in correo:
            raise ClienteError("Correo electrónico inválido")

        self.__nombre = nombre
        self.__correo = correo

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    def mostrar_info(self):
        return f"Nombre: {self.__nombre} | Correo: {self.__correo}"



# CLASE ABSTRACTA SERVICIO
# ==================================================

class Servicio(ABC):

    def __init__(self, nombre, precio_base):

        if precio_base <= 0:
            raise ServicioError(
                "El precio debe ser mayor que 0"
            )

        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self, duracion):
        pass

    @abstractmethod
    def descripcion(self):
        pass


# SERVICIO RESERVA DE SALAS
# ==================================================

class ReservaSala(Servicio):

    def calcular_costo(self, horas):
        return self.precio_base * horas

    def descripcion(self):
        return "Reserva de sala"



# SERVICIO ALQUILER EQUIPOS
# ==================================================

class AlquilerEquipo(Servicio):

    def calcular_costo(self, dias):
        return self.precio_base * dias

    def descripcion(self):
        return "Alquiler de equipos"

# SERVICIO ASESORIA
# ==================================================

class AsesoriaEspecializada(Servicio):

    def calcular_costo(self, horas):
        return self.precio_base * horas * 1.19

    def descripcion(self):
        return "Asesoría especializada"



# CLASE RESERVA
# ==================================================

class Reserva:

    def __init__(self, cliente, servicio, duracion):

        if duracion <= 0:
            raise ReservaError(
                "La duración debe ser mayor que cero"
            )

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def confirmar(self):

        try:

            self.estado = "Confirmada"

            registrar_log(
                f"Reserva confirmada para "
                f"{self.cliente.nombre}"
            )

        except Exception as e:

            raise ReservaError(
                "Error confirmando reserva"
            ) from e

    def procesar(self):

        try:

            costo = self.servicio.calcular_costo(
                self.duracion
            )

        except Exception as e:

            registrar_log(
                f"Error de procesamiento: {e}"
            )

            raise ReservaError(
                "Error procesando reserva"
            ) from e

        else:

            registrar_log(
                "Reserva procesada correctamente"
            )

            return costo

        finally:

            registrar_log(
                "Finalización del proceso de reserva"
            )



# LISTAS DEL SISTEMA
# ==================================================

clientes = []
servicios = []
reservas = []



# MENU PRINCIPAL
# ==================================================

while True:

    print("\n")
    print("=" * 50)
    print("      SOFTWARE FJ")
    print("=" * 50)

    print("1. Registrar Cliente")
    print("2. Crear Servicio")
    print("3. Generar Reserva")
    print("4. Ver Clientes")
    print("5. Ver Servicios")
    print("6. Ver Reservas")
    print("7. Salir")

    opcion = input("\nSeleccione una opción: ")

    
    # REGISTRAR CLIENTE
    # ==================================================

    if opcion == "1":

        try:

            nombre = input("Ingrese nombre: ")
            correo = input("Ingrese correo: ")

            cliente = Cliente(nombre, correo)

            clientes.append(cliente)

            registrar_log(
                f"Cliente registrado: {nombre}"
            )

            print("Cliente registrado exitosamente")

        except Exception as e:

            print("ERROR:", e)

            registrar_log(str(e))

    
    # CREAR SERVICIO
    # ==================================================

    elif opcion == "2":

        try:

            print("\n1. Reserva Sala")
            print("2. Alquiler Equipos")
            print("3. Asesoría")

            tipo = input("Seleccione servicio: ")

            nombre_servicio = input(
                "Nombre del servicio: "
            )

            precio = float(
                input(
                    "Precio base: "
                )
            )

            if tipo == "1":

                servicio = ReservaSala(
                    nombre_servicio,
                    precio
                )

            elif tipo == "2":

                servicio = AlquilerEquipo(
                    nombre_servicio,
                    precio
                )

            elif tipo == "3":

                servicio = AsesoriaEspecializada(
                    nombre_servicio,
                    precio
                )

            else:

                raise ServicioError(
                    "Tipo inválido"
                )

            servicios.append(servicio)

            print("Servicio creado con éxito")

            registrar_log(
                f"Servicio creado: {nombre_servicio}"
            )

        except Exception as e:

            print("ERROR:", e)

            registrar_log(str(e))

    
    # CREAR RESERVA
    # ==================================================

    elif opcion == "3":

        try:

            if len(clientes) == 0:
                raise ReservaError(
                    "Primero debe registrar clientes"
                )

            if len(servicios) == 0:
                raise ReservaError(
                    "Primero debe registrar servicios"
                )

            print("\nCLIENTES")

            for i, cliente in enumerate(clientes):

                print(
                    f"{i+1}. {cliente.nombre}"
                )

            cli = int(
                input("Seleccione cliente: ")
            ) - 1

            print("\nSERVICIOS")

            for i, servicio in enumerate(servicios):

                print(
                    f"{i+1}. {servicio.nombre}"
                )

            ser = int(
                input("Seleccione servicio: ")
            ) - 1

            duracion = int(
                input(
                    "Duración (horas o días): "
                )
            )

            reserva = Reserva(
                clientes[cli],
                servicios[ser],
                duracion
            )

            reserva.confirmar()

            costo = reserva.procesar()

            reservas.append(reserva)

            print(
                f"Reserva creada "
                f"correctamente."
            )

            print(
                f"Costo Total: ${costo:,.0f}"
            )

        except Exception as e:

            print("ERROR:", e)

            registrar_log(str(e))

    
    # VER CLIENTES
    # ==================================================

    elif opcion == "4":

        print("\nCLIENTES REGISTRADOS")

        if len(clientes) == 0:

            print("No existen clientes")

        else:

            for cliente in clientes:

                print(
                    cliente.mostrar_info()
                )

    
    # VER SERVICIOS
    # ==================================================

    elif opcion == "5":

        print("\nSERVICIOS REGISTRADOS")

        if len(servicios) == 0:

            print("No existen servicios")

        else:

            for servicio in servicios:

                print(f"Nombre: {servicio.nombre}")

                print(f"Tipo: {servicio.descripcion()}")

                print(f"Precio Base: ${servicio.precio_base:,.0f}")

                print("-" * 30)

    
    # VER RESERVAS
    # ==================================================

    elif opcion == "6":

        print("\nRESERVAS REALIZADAS")

        if len(reservas) == 0:

            print("No existen reservas")

        else:

            for reserva in reservas:

                print(f"Cliente: {reserva.cliente.nombre}")

                print(f"Servicio: {reserva.servicio.nombre}")

                print(f"Duración: {reserva.duracion}")

                print(f"Estado: {reserva.estado}")

                print("-" * 30)

    
    # REPORTE FINAL Y SALIDA
    # ==================================================

    elif opcion == "7":

        with open(
            "reporte_final.txt",
            "w",
            encoding="utf-8"
        ) as reporte:

            reporte.write(
                "REPORTE FINAL SOFTWARE FJ\n"
            )

            reporte.write("=" * 50 + "\n\n")

            reporte.write(
                "CLIENTES REGISTRADOS\n"
            )

            for cliente in clientes:

                reporte.write(
                    f"{cliente.nombre} - "
                    f"{cliente.correo}\n"
                )

            reporte.write("\n")

            reporte.write(
                "SERVICIOS REGISTRADOS\n"
            )

            for servicio in servicios:

                reporte.write(
                    f"{servicio.nombre} - "
                    f"${servicio.precio_base}\n"
                )

            reporte.write("\n")

            reporte.write(
                "RESERVAS REALIZADAS\n"
            )

            for reserva in reservas:

                reporte.write(f"Cliente: {reserva.cliente.nombre}\n")

                reporte.write(f"Servicio: {reserva.servicio.nombre}\n")

                reporte.write(f"Duración: {reserva.duracion}\n")

                reporte.write(f"Estado: {reserva.estado}\n")

                reporte.write("-" * 30 + "\n")

        print("\n")
        print("=" * 50)
        print("REPORTE FINAL")
        print("=" * 50)

        print(
            f"Total clientes: {len(clientes)}"
        )

        print(
            f"Total servicios: {len(servicios)}"
        )

        print(
            f"Total reservas: {len(reservas)}"
        )

        print(
            "\nSe generó el archivo:"
        )

        print("reporte_final.txt")

        registrar_log(
            "Sistema finalizado correctamente."
        )

        break
    else:

        print("Opción inválida")
