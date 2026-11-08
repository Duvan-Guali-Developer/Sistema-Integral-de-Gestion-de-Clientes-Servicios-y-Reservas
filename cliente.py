"""
LANZAR APLICACION CON EJECUTAR.py
cliente.py
"""

import re


class Cliente:
    """Cliente de Software FJ."""

    def __init__(self, documento: str, nombre: str, email: str, telefono: str):
        campos = {"documento": documento, "nombre": nombre, "email": email, "teléfono": telefono}
        for campo, valor in campos.items():
            if not valor or not str(valor).strip():
                raise ValueError(f"El campo '{campo}' es obligatorio")

        if not documento.strip().isdigit():
            raise ValueError("El campo 'documento' solo puede contener números")
        if not telefono.strip().isdigit():
            raise ValueError("El campo 'teléfono' solo puede contener números")
        if not re.fullmatch(r"[\w.+-]+@[\w-]+(\.[\w-]+)+", email.strip()):
            raise ValueError("El campo 'email' no tiene un formato válido (ejemplo: nombre@correo.com)")

        self.documento = documento.strip()
        self.nombre = nombre.strip().upper()
        self.email = email.strip().lower()
        self.telefono = telefono.strip()

    def describir(self) -> str:
        return f"{self.nombre} (doc. {self.documento}, {self.email})"
