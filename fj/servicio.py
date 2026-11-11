"""
Módulo de servicios de Software FJ

Define la clase abstracta Servicio y tres servicios
ReservaSala
AlquilerEquipo
Asesoria
"""

from abc import ABC, abstractmethod


def pesos(valor):
    """Formatea un valor en pesos colombianos"""
    return f"${valor:,.0f}".replace(",", ".")


class ServicioError(ValueError):
    """Error propio para problemas con los servicios"""
    pass


class Servicio(ABC):
    """Clase abstracta base para todos los servicios"""

    def __init__(self, codigo, nombre, precio_base):
        if not codigo or not nombre:
            raise ServicioError("El código y el nombre del servicio son obligatorios")
        if precio_base <= 0:
            raise ServicioError("El precio base debe ser mayor que cero")
        self._codigo = codigo
        self._nombre = nombre
        self._precio_base = precio_base
        self._disponible = True

    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre(self):
        return self._nombre

    @property
    def precio_base(self):
        return self._precio_base

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, estado):
        self._disponible = bool(estado)

    @abstractmethod
    def calcular_costo(self, horas, descuento=0):
        """Cada servicio calcula su costo de forma diferente"""
        pass

    @abstractmethod
    def describir(self):
        """Devuelve una descripción del servicio"""
        pass

    def _validar_horas(self, horas):
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise ServicioError("Las horas deben ser un número mayor que cero")

    def _aplicar_descuento(self, costo, descuento):
        if descuento < 0 or descuento > 0.5:
            raise ServicioError("El descuento debe estar entre 0% a 50%")
        return costo * (1 - descuento)

    def __str__(self):
        estado = "Disponible" if self._disponible else "No disponible"
        return f"[{self._codigo}] {self._nombre} - {pesos(self._precio_base)}/h ({estado})"


class ReservaSala(Servicio):
    """Reserva de salas de reuniones."""

    def __init__(self, codigo, nombre, precio_base, capacidad):
        super().__init__(codigo, nombre, precio_base)
        if capacidad <= 0:
            raise ServicioError("La capacidad de la sala debe ser mayor que cero")
        self._capacidad = capacidad

    def calcular_costo(self, horas, descuento=0):
        self._validar_horas(horas)
        costo = self._precio_base * horas
        if self._capacidad > 20:
            costo += 50000  # recargo por sala grande
        return self._aplicar_descuento(costo, descuento)

    def describir(self):
        return f"Sala '{self._nombre}' para {self._capacidad} personas."


class AlquilerEquipo(Servicio):
    """Alquiler de equipos"""

    def __init__(self, codigo, nombre, precio_base, tipo_equipo, deposito=0):
        super().__init__(codigo, nombre, precio_base)
        self._tipo_equipo = tipo_equipo
        self._deposito = deposito

    def calcular_costo(self, horas, descuento=0):
        self._validar_horas(horas)
        costo = self._precio_base * horas + self._deposito
        return self._aplicar_descuento(costo, descuento)

    def describir(self):
        return f"Alquiler de {self._tipo_equipo} (depósito: {pesos(self._deposito)})."


class Asesoria(Servicio):
    """Asesorías especializadas"""

    def __init__(self, codigo, nombre, precio_base, especialidad):
        super().__init__(codigo, nombre, precio_base)
        self._especialidad = especialidad

    def calcular_costo(self, horas, descuento=0):
        self._validar_horas(horas)
        costo = self._precio_base * horas
        if horas >= 5:
            costo *= 0.9  # 10% menos por asesorías largas
        return self._aplicar_descuento(costo, descuento)

    def describir(self):
        return f"Asesoría en {self._especialidad}."
