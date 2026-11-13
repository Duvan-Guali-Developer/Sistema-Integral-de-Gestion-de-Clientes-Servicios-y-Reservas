"""
Módulo de reservas de Software FJ

Define la clase que une un cliente con un servicio,
una fecha y una duración, y controla su estado
"""

from datetime import date, datetime

from .servicio import pesos


class ReservaError(ValueError):
    """Error propio para problemas con las reservas"""
    pass


class Reserva:
    """Reserva de un servicio por parte de un cliente"""

    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"

    def __init__(self, codigo, cliente, servicio, fecha, horas, descuento=0):
        if cliente is None or servicio is None:
            raise ReservaError("La reserva necesita un cliente y un servicio")
        if not servicio.disponible:
            raise ReservaError(f"El servicio {servicio.nombre} no está disponible")
        if fecha < date.today():
            raise ReservaError("La fecha de la reserva no puede ser anterior a hoy")
        if horas <= 0:
            raise ReservaError("La duración debe ser mayor que cero (0) horas")

        self._codigo = codigo
        self._cliente = cliente
        self._servicio = servicio
        self._fecha = fecha
        self._horas = horas
        self._descuento = descuento
        self._estado = Reserva.PENDIENTE
        self._costo = servicio.calcular_costo(horas, descuento)

    @property
    def codigo(self):
        return self._codigo

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def fecha(self):
        return self._fecha

    @property
    def horas(self):
        return self._horas

    @property
    def costo(self):
        return self._costo

    @property
    def estado(self):
        return self._estado

    def confirmar(self):
        if self._estado == Reserva.CANCELADA:
            raise ReservaError("No se puede confirmar una reserva cancelada")
        if self._estado == Reserva.CONFIRMADA:
            raise ReservaError("La reserva está confirmada")
        self._estado = Reserva.CONFIRMADA

    def cancelar(self):
        if self._estado == Reserva.CANCELADA:
            raise ReservaError("La reserva está cancelada")
        self._estado = Reserva.CANCELADA

    def activa(self):
        return self._estado != Reserva.CANCELADA

    @staticmethod
    def leer_fecha(texto):
        """Convierte un texto AAAA-MM-DD en fecha"""
        try:
            return datetime.strptime(texto.strip(), "%Y-%m-%d").date()
        except ValueError as error:
            raise ReservaError("La fecha debe tener el formato AAAA-MM-DD") from error

    def describir(self):
        return (f"{self._codigo}: {self._cliente.nombre} - {self._servicio.nombre} "
                f"el {self._fecha.isoformat()} por {self._horas:g} h = {pesos(self._costo)} ({self._estado})")

    def __str__(self):
        return self.describir()
