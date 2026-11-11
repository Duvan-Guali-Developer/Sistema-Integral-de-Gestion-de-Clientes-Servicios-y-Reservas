"""
LANZAR APLICACION CON EJECUTAR.py
sistema.py
"""

from .cliente import Cliente
from .registro import logger
from .servicio import AlquilerEquipo, Asesoria, ReservaSala, Servicio, ServicioError, pesos

TIPOS_SERVICIO = {
    "Reserva de sala": ReservaSala,
    "Alquiler de equipo": AlquilerEquipo,
    "Asesoría": Asesoria,
}


class SistemaFJ:
    """Gestión de clientes y servicios en memoria."""

    def __init__(self, empresa: str = "Software FJ"):
        self.empresa = empresa
        self.clientes: list = []
        self.servicios: list = []
        logger.info("=== Sistema %s iniciado ===", empresa)

    def buscar_servicio(self, codigo: str) -> Servicio:
        for servicio in self.servicios:
            if servicio.codigo == codigo:
                return servicio
        raise ServicioError(f"No existe un servicio con código {codigo}")

    def registrar_servicio(self, tipo, codigo, nombre, precio_texto, detalle) -> Servicio:
        if tipo not in TIPOS_SERVICIO:
            raise ServicioError("Seleccione un tipo de servicio válido")
        codigo = codigo.strip().upper()
        if any(s.codigo == codigo for s in self.servicios):
            raise ServicioError(f"Ya existe un servicio con código {codigo}")
        if not str(precio_texto).strip().isdigit():
            raise ServicioError("El precio por hora debe ser un número entero")
        if not detalle.strip():
            raise ServicioError("El campo de detalle es obligatorio")

        precio = int(precio_texto)
        clase = TIPOS_SERVICIO[tipo]
        if clase is ReservaSala:
            if not detalle.strip().isdigit():
                raise ServicioError("La capacidad de la sala debe ser un número")
            servicio = ReservaSala(codigo, nombre.strip(), precio, int(detalle))
        elif clase is AlquilerEquipo:
            servicio = AlquilerEquipo(codigo, nombre.strip(), precio, detalle.strip())
        else:
            servicio = Asesoria(codigo, nombre.strip(), precio, detalle.strip())

        self.servicios.append(servicio)
        logger.info("Servicio registrado: %s", servicio)
        return servicio

    def calcular_costo(self, codigo, horas_texto, descuento_texto="0"):
        servicio = self.buscar_servicio(codigo)
        try:
            horas = float(horas_texto)
            descuento = float(descuento_texto or 0) / 100
        except ValueError:
            raise ServicioError("Las horas y el descuento deben ser números")
        costo = servicio.calcular_costo(horas, descuento)
        logger.info("Costo calculado: %s x %s h (desc. %.0f%%) = %s",
                    servicio.codigo, horas, descuento * 100, pesos(costo))
        return servicio, costo

    def buscar_cliente(self, documento: str) -> Cliente:
        for cliente in self.clientes:
            if cliente.documento == documento:
                return cliente
        raise ValueError(f"No existe un cliente con documento {documento}")

    def registrar_cliente(self, documento, nombre, email, telefono) -> Cliente:
        if any(c.documento == documento for c in self.clientes):
            raise ValueError(f"Ya existe un cliente con documento {documento}")
        cliente = Cliente(documento, nombre, email, telefono)
        self.clientes.append(cliente)
        logger.info("Cliente registrado: %s", cliente.describir())
        return cliente
