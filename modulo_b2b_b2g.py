"""Compatibilidad histórica para el simulador consolidado."""

from cuidado.services.simulador_b2b_b2g import (
    cargar_escenarios,
    ejecutar_escenarios,
    simular_b2b,
    simular_b2g,
    simular_escenario,
    validar_escenario,
)

__all__ = [
    "cargar_escenarios",
    "ejecutar_escenarios",
    "simular_b2b",
    "simular_b2g",
    "simular_escenario",
    "validar_escenario",
]
