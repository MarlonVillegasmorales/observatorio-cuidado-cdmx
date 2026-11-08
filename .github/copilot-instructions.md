# Instrucciones de Copilot — Observatorio Economía del Cuidado

## Contexto
Proyecto académico de análisis territorial de la economía del cuidado en las 16 alcaldías de CDMX, desarrollado principalmente con Python y Streamlit.

Antes de modificar código, consultar los documentos relevantes:
- CONTEXTO_PROYECTO.md
- docs/ARQUITECTURA.md
- docs/CONTRATOS.md
- docs/REQUISITOS_Y_AVANCES.md

## Reglas de desarrollo
1. Reutilizar componentes y funciones existentes.
2. No reescribir módulos completos si basta un cambio localizado.
3. Conservar la arquitectura por capas.
4. Mantener compatibilidad con escritorio y dispositivos móviles.
5. Respetar el diseño visual y la navegación por tareas.
6. No inventar datos, estadísticas, pilotos ni resultados de impacto social.
7. Distinguir datos reales, simulaciones y funcionalidades pendientes.
8. No introducir dependencias sin justificarlo.
9. No modificar archivos ajenos a la tarea sin necesidad.
10. No incluir credenciales ni información personal en Git.

## Ejecución y pruebas
- Aplicación: `python -m streamlit run app_dashboard.py`
- Pruebas: `python -m pytest -q`
- Documentar fallos y limitaciones de validación.

## Flujo de trabajo
- Para tareas sencillas, implementar directamente.
- Para cambios estructurales, presentar primero un plan breve.
- Realizar cambios mínimos y verificables.
- Revisar el diff antes de crear el commit.
- No fusionar cambios a main sin revisión.

## Respuesta final
Informar únicamente:
- Archivos modificados.
- Qué cambió.
- Pruebas realizadas y resultados.
- Problemas pendientes.

Evitar explicaciones extensas y repetir el contexto del proyecto.