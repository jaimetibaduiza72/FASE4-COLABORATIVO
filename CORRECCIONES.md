Software FJ - Fase 4 / Actividad 4
Nombre: Fabián Domínguez
Archivo que corregí: fase4.py
Grupo: FASE4-COLABORATIVO

Buenas, estas son las correcciones que yo hice al código base que estaba subido en GitHub. El código base era el que tenía los errores, yo lo revisé, lo probé y lo dejé corregido. Aquí explico qué tenía mal y qué le puse.

Lo que tenía mal el código base
Cuando lo abrí me di cuenta que:

Cliente solo pedía nombre y correo, no pedía documento ni teléfono.
El correo solo revisaba que tuviera un @, entonces pasaba "@@@" o "a@" como si fuera válido.
Servicio no heredaba de Entidad, solo Cliente lo hacía.
El precio se podía cambiar desde fuera, yo le puse precio = -999 y lo dejó.
El cálculo de costo no tenía impuesto ni descuento, era solo precio * horas.
Reserva se rompía si le pasaba "dos" en duración, salía un TypeError feo.
Se podía confirmar dos veces sin que dijera nada.
No tenía simulación de 10 operaciones, había que probar todo a mano.
Lo que yo corregí
1. Cliente - correo, documento y teléfono
Lo que hice fue ponerle regex al correo. Antes era solo "@" in correo, ahora sí valida que sea un correo de verdad. Ya no pasa "@@@", "a@" ni "ana@", pero sí pasa "ana@example.com".

También le agregué documento y teléfono que no estaban:

Documento: le quito espacios, puntos y guiones con re.sub y solo acepto entre 6 y 12 dígitos. Si ponen "12AB" ya no pasa.
Teléfono: le quito espacios y paréntesis, acepta con +57 como +573001234567 y solo acepto entre 7 y 15 dígitos. Si ponen "123" ya no pasa.
Y dejé nombre, correo, documento y teléfono privados con __ y con @property para leerlos.

2. Servicio - herencia y precio
Yo me di cuenta que Servicio decía class Servicio(ABC) y no heredaba de Entidad. Lo cambié a class Servicio(Entidad) y le puse su propio mostrar_info() para que quedara bien la herencia.

El precio también lo dejé privado. Antes era self.precio_base = precio_base y cualquiera lo podía cambiar. Ahora es self.__precio_base con @property, si intentan ponerle -999 da error y no deja.

También le puse validación al precio con math.isfinite, para que no acepte True, inf ni números menores o iguales a 0.

3. Cálculo de costo - sobrecarga e impuesto
Antes cada servicio tenía su propio calcular_costo sin impuesto ni descuento. Yo le puse a todos calcular_costo(duracion, impuesto=0, descuento=0) y creé un helper _calcular_costo() para no repetir el código.

Ahí valido que duración, impuesto y descuento sean números, que no sean bool, que duración sea mayor que 0, y que impuesto y descuento estén entre 0 y 1. Antes el impuesto aceptaba 5, o sea 500%, y daba 1200. Ahora si ponen impuesto=5 ya lo bloquea.

Ejemplo que yo probé:

calcular_costo(2) = 200
calcular_costo(2, 0.19) = 238.0
calcular_costo(2, 0.19, 0.1) = 214.2
4. Cada servicio con su atributo
ReservaSala: le puse capacidad, tiene que ser entero mayor que 0. Si ponen 0 ya no pasa.
AlquilerEquipo: le puse stock, tiene que ser entero mayor o igual a 0. Si ponen -1 ya no pasa.
AsesoriaEspecializada: le puse tema, no puede quedar vacío ni con solo espacios. Si ponen " " ya no pasa.
5. Reserva - validación y confirmar
Esto era lo que más se rompía. Antes el __init__ solo revisaba duracion <= 0.

Yo le puse:

Que cliente tiene que ser instancia de Cliente, si ponen None ya no lo acepta.
Que servicio tiene que ser instancia de Servicio.
Que duración tiene que ser número, no bool, finito y mayor que 0. Si ponen "dos" ya no sale TypeError, sale ReservaError que sí es nuestro error.
Y en confirmar() le puse que si ya está Confirmada no deje confirmar otra vez, y si está Cancelada tampoco deje confirmarla. En cancelar() ya estaba que no dejaba cancelar dos veces, eso lo dejé igual. Y en procesar() dejé el try / except / else / finally con raise ... from e.

6. Menú y simulación
En el menú arreglé lo de los índices. Antes si ponían 0 en seleccionar cliente, cogía el último por el -1. Ahora valido 0 <= cli < len(clientes) y lo mismo para servicios.

También cambié los except Exception genéricos por except ClienteError, except ServicioError, except ReservaError, except ValueError por separado.

Y agregué la simulación de 10 operaciones en la opción 8, para no probar todo a mano:

Cliente válido
Documento inválido
Teléfono inválido
Sala y costo válidos
Capacidad inválida
Equipo y costo válidos
Stock inválido
Asesoría y costo válidos
Tema inválido
Cancelación repetida
Cada una tiene su try/except y queda en logs.txt con inicio y fin. Yo la corrí y las 10 salieron bien.

Cómo lo probé yo
Yo lo probé corriendo el código y poniéndole casos malos a propósito:

Correo "@@@" -> bloqueado
Documento "12AB" -> bloqueado
Precio -999 desde fuera -> bloqueado
Impuesto 5 -> bloqueado
Duración "dos" -> bloqueado con ReservaError
Confirmar dos veces -> bloqueado
Simulación opción 8 -> 10/10 en logs.txt
— Fabián
