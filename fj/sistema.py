"""
LANZAR APLICACION CON EJECUTAR.py
sistema.py
"""

from .cliente import Cliente
from .registro import logger


class SistemaFJ:
    """Gestión de clientes en memoria."""

    def __init__(self, empresa: str = "Software FJ"):
        self.empresa = empresa
        self.clientes: list = []
        logger.info("=== Sistema %s iniciado ===", empresa)

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
