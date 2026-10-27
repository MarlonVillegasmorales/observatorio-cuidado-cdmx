"""Escenario sintético reproducible, aislado de cualquier base operativa."""
from datetime import time
from dataclasses import replace
from cuidado.domain.centros import Necesidad, Oferta, recomendar

def escenario():
    dias=frozenset({'lun','mar'})
    ofertas=[Oferta('demo-servicio-1','demo-centro-1','infantil',19.35,-99.06,time(8),time(14),dias,3),
             Oferta('demo-servicio-2','demo-centro-2','infantil',19.36,-99.07,time(9),time(17),dias,2)]
    solicitudes=[Necesidad(f'demo-{i:02}','infantil',19.35+i*.002,-99.06,time(9),time(12),dias) for i in range(8)]
    solicitudes += [Necesidad('demo-horario','infantil',19.35,-99.06,time(18),time(20),dias),
                    Necesidad('demo-tipo','mayores',19.35,-99.06,time(9),time(12),dias),
                    Necesidad('demo-lejana','infantil',19.8,-99.06,time(9),time(12),dias)]
    return solicitudes,ofertas

def ejecutar_demo(radio_km=10):
    solicitudes,ofertas=escenario()
    return recomendar(solicitudes,ofertas,radio_km)

def ejecutar_busqueda(tipo, inicio, fin, dias, radio_km=10):
    """Evalúa una solicitud sintética con el mismo motor explicable del dominio."""
    solicitudes, ofertas = escenario()
    solicitud = replace(
        solicitudes[0],
        solicitud_id="demo-usuario",
        tipo=tipo,
        inicio=inicio,
        fin=fin,
        dias=frozenset(dias),
    )
    return recomendar([solicitud], ofertas, radio_km)
