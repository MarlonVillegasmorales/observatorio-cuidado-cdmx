# Requisitos y avances verificables

Esta matriz es la fuente principal del estado documental. Los estados no
implican despliegue, uso con participantes ni validación docente.

**Estados de implementación:** `pendiente`, `parcial`, `implementado`,
`propuesta futura`. **Validación:** `pendiente`, `sintética/local` o
`real/piloto`.

| ID | Objetivo | Requisito y origen | Criterio de aceptación comprobable | Implementación | Validación | Responsable | Dependencias o bloqueo | Evidencia | Siguiente trabajo |
|---|---|---|---|---|---|---|---|---|---|
| DAT-01 | Integrar fuentes | Dataset para 16 alcaldías (PDF, pp. 3–5) | Cada fuente conserva origen, año, unidad, granularidad y limitaciones | implementado | real/piloto | Marlon / Karla | Validación de publicación y revisión docente | `cuidado/pipelines/mapa_alcaldias.py`, `docs/MAPA_ALCALDIAS.md` | Revisar PR y despliegue |
| DAT-02 | Analizar brechas | Indicadores interpretables (PDF, pp. 4–5, 16–18) | Toda cifra muestra fuente, año, población, ámbito y unidad | implementado | real/piloto | Marlon / Karla | No interpretar grupos como necesidad de cuidado | `data/processed/mapa_alcaldias/catalogo_indicadores.csv`, `cuidado/ui/mapa_alcaldias.py` | Validar uso académico |
| DAT-03 | Calidad | Reportar faltantes, duplicados y transformaciones (PDF, p. 17) | El reporte de calidad hace visibles nulos y decisiones del ETL | implementado | real/piloto | Marlon | Teléfono físico y lector pendientes | `data/processed/mapa_alcaldias/calidad_mapa.json` | Mantener controles |
| ACA-01 | Observatorio | Generar evidencia para decidir (PDF, pp. 3–4) | El observatorio integra datos y visualiza hallazgos, no solo registros | parcial | sintética/local | Marlon | Auditoría analítica y validación de usuarios | `app_dashboard.py`, `cuidado/ui/` | Documentar hallazgos priorizados |
| ACA-02 | Programa social | Derivar intervención de un hallazgo (PDF, pp. 5, 8–10) | El plan identifica población, necesidad, actores, recursos, riesgos y evaluación | pendiente | pendiente | Equipo | No hay diagnóstico/población real validada | PDF, `docs/ANALISIS_PROBLEMA_PROTOTIPICO.md` | Validar propuesta de Iztapalapa |
| UI-01 | Interfaz | Mapa por alcaldía y cuatro tareas de consulta | Se puede navegar a las cuatro tareas y consultar una clave territorial | implementado | real/piloto | Marlon | Teléfono físico y lector pendientes | `cuidado/ui/app.py`, `cuidado/ui/mapa_alcaldias.py`, `tests/test_app.py` | Revisar versión pública |
| UI-02 | Búsqueda | Conservar valores entre pasos | Al volver o avanzar se conservan filtros y respuestas | implementado | sintética/local | Marlon | Ninguno conocido | `_render_busqueda`, `tests/test_app.py` | Probar más combinaciones |
| UI-03 | Actualización | Marcar resultados obsoletos | Al cambiar filtros, los resultados anteriores aparecen como pendientes de actualizar | implementado | sintética/local | Marlon | Ninguno conocido | `_render_busqueda`, `tests/test_app.py` | Verificar mensajes con usuarios |
| UI-04 | Accesibilidad | Teclado, foco, contraste, ampliación, alternativas y estados (PDF, pp. 5, 8) | Una evaluación documentada cubre teclado, foco, lector, móvil y estados no cromáticos | pendiente | pendiente | Equipo | No hay evaluación completa | `cuidado/ui/estilos.py`, AppTest parcial | Ejecutar auditoría de accesibilidad |
| ALG-01 | Vinculación | Matching por servicio, días, horario, distancia y cupo | Cada recomendación expone motivo, distancia geográfica y versión | implementado | sintética/local | Marlon | Falta referencia experimental | `cuidado/domain/centros.py`, `tests/test_matching.py` | Comparar cobertura y errores |
| ALG-02 | Vinculación | Modelo avanzado validado (PDF, pp. 6, 16–18) | Se reportan métricas, errores, capacidad, cobertura y diferencias territoriales | parcial | pendiente | Marlon / Azael | Datos y método validados pendientes | `docs/ARQUITECTURA.md`, contratos | Definir protocolo de evaluación |
| ALG-03 | Operación | Separar recomendación de confirmación | Una recomendación nunca se presenta como plaza o atención recibida | implementado | sintética/local | Marlon | Centros institucionalmente verificados | `cuidado/ui/app.py`, `vinculacion.py` | Diseñar flujo autorizado |
| PRI-01 | Privacidad | Minimización y gobernanza desde diseño (PDF, pp. 13–16) | Existe inventario, finalidad, base jurídica, riesgos, acceso, retención y eliminación | pendiente | pendiente | Equipo / Azael | Revisión jurídica y protocolo | `docs/ARQUITECTURA.md`, PDF | Preparar dictamen y matriz |
| PRI-02 | Demo | No registrar personas en la demostración | La aplicación pública funciona con datos sintéticos y sin base compartida | implementado | sintética/local | Marlon | No usar datos reales sin autorización | `cuidado/ui/app.py`, `docs/ARQUITECTURA.md` | Mantener separación |
| OPE-01 | Centros | Directorio verificado con cupos y requisitos | Cada centro tiene verificación, horarios, accesibilidad, cupos y fecha de actualización | propuesta futura | pendiente | Equipo | Centros y procedimiento institucional | `docs/CONTRATOS.md` | Definir contrato y piloto |
| OPE-02 | Seguimiento | Solicitud, confirmación, cancelación, incidencias y liberación | Cada transición queda autorizada y auditable | parcial | sintética/local | Marlon | Roles, privacidad, PostgreSQL y piloto | `cuidado/services/vinculacion.py`, `tests/test_database.py` | Diseñar operación privada |
| INT-01 | Integración | Recibir entregas de Karla y Azael por contrato | Cada módulo tiene entradas, salidas, fuentes, pruebas y revisión registrada | pendiente | pendiente | Karla / Azael / Marlon | Entregas pendientes | `docs/CONTRATOS.md`, `cuidado/services/integraciones.py` | Recibir y revisar módulos |
| DAT-04 | Movilidad | Movilidad/CONAPO con granularidad y CRS explícitos | Se distingue proyección de observación y no se confunde distancia con viaje | propuesta futura | pendiente | Karla | Entrega de Karla | `docs/CONTRATOS.md` | Incorporar solo tras validación |
| B2B-01 | Escenarios | B2B/B2G con fuentes, unidades y supuestos | Cada salida incluye resultado, unidad, periodo, supuestos, fuentes y método | propuesta futura | pendiente | Azael | Entrega de Azael y fuentes | `docs/CONTRATOS.md`, PDF, pp. 11–13 | No publicar cifras financieras aún |
| DEP-01 | Despliegue | Ejecutar Streamlit desde repositorio activo | Existe evidencia de aplicación y configuración verificable | parcial | pendiente | Marlon | Cuenta, configuración y comprobación Cloud | `docs/STREAMLIT.md`, `Dockerfile` | Desplegar solo cuando se autorice |
| ACA-03 | Entrega | Observatorio, programa, informe, presentación y referencias (PDF, pp. 4–5, 18) | Cada entregable tiene archivo, responsable, revisión y evidencia | parcial | pendiente | Equipo | Integración de UCA y revisión docente | PDF, `docs/`, README | Consolidar informe y presentación |

## Bloqueos separados

1. **Académico:** falta confirmar con docentes las adaptaciones a centros
   comunitarios, B2B/B2G, alcance de Iztapalapa y criterios de entrega.
2. **Datos:** falta confirmar procedencia, año, población, comparabilidad y
   granularidad de cada fuente; las estimaciones no son observaciones.
3. **Operación:** no hay centros verificados, participantes, convenio,
   autenticación, roles, protocolo completo ni seguimiento real.
4. **Algoritmo:** falta evaluación comparativa de cobertura, errores,
   capacidad, explicabilidad y diferencias territoriales.
5. **Privacidad:** falta dictamen, inventario de datos, base jurídica, matriz
   de riesgos, conservación/eliminación y controles de acceso.
6. **Integración:** están pendientes las entregas de movilidad/CONAPO y
   plantilla empresarial de Karla, y los simuladores/documentación de Azael.
7. **Despliegue:** no hay evidencia de aplicación Cloud, PostgreSQL remoto ni
   validación con usuarios.

## Evidencia local disponible

La documentación técnica está en
[docs/ARQUITECTURA.md](ARQUITECTURA.md), [docs/CONTRATOS.md](CONTRATOS.md),
[docs/INVENTARIO_REPOSITORIO.md](INVENTARIO_REPOSITORIO.md),
[docs/SEGUNDO_AVANCE.md](SEGUNDO_AVANCE.md) y
[docs/STREAMLIT.md](STREAMLIT.md). La prueba local previamente reportada es
evidencia de comportamiento sintético, no de piloto ni de impacto. El PDF
académico y su interpretación detallada están en
[ANALISIS_PROBLEMA_PROTOTIPICO.md](ANALISIS_PROBLEMA_PROTOTIPICO.md).
