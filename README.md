# Observatorio de la Economía del Cuidado CDMX

Proyecto académico y prototipo de observatorio de datos para comprender la
economía del cuidado en las 16 alcaldías de Ciudad de México. Su propósito es
convertir datos en evidencia para decisiones y explorar una vinculación B2B2C
con centros comunitarios; no es una plataforma de contratación ni demuestra
todavía un piloto social real.

La propuesta académica del PDF `PROBLEMA PROTOTÍPICO 7° SEM LCDN 2026-2.pdf`
plantea la secuencia datos → evidencia → decisión → programa de innovación
social (pp. 4–5 y 18).
El [análisis académico](docs/ANALISIS_PROBLEMA_PROTOTIPICO.md) distingue ese
caso didáctico de lo que ya está implementado en este repositorio.

## Alcance comprobado

- **Actual:** cuatro tareas en Streamlit: conocer la zona, comparar zonas,
  probar una búsqueda sintética y consultar información del proyecto.
- **Datos:** ETL reproducible y GeoParquet preparado para 16 alcaldías, con
  metadata y reporte de calidad.
- **Vinculación:** matching explicable por tipo, días, horario, distancia
  geográfica y cupo; las ofertas y solicitudes de la demostración son
  sintéticas.
- **Límites:** no hay centros verificados, personas participantes, convenio,
  confirmación pública, impacto social medido ni despliegue comprobado.

El estado verificable, los criterios de aceptación y los bloqueos están en
[Requisitos y avances](docs/REQUISITOS_Y_AVANCES.md). El propósito, la
arquitectura y las responsabilidades están en
[CONTEXTO_PROYECTO.md](CONTEXTO_PROYECTO.md).

## Ejecución local (Python 3.12)

Desde `D:\git\observatorio-cuidado-cdmx`:

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app_dashboard.py
```

Para validar cambios:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

La configuración del intérprete local está en
[.vscode/settings.json](.vscode/settings.json) y usa una ruta relativa a
`${workspaceFolder}`.

## Documentación relacionada

- [Análisis del problema prototípico](docs/ANALISIS_PROBLEMA_PROTOTIPICO.md)
- [Requisitos y avances](docs/REQUISITOS_Y_AVANCES.md)
- [Arquitectura y límites](docs/ARQUITECTURA.md)
- [Contratos de integración](docs/CONTRATOS.md)
- [Inventario del repositorio](docs/INVENTARIO_REPOSITORIO.md)
- [Evidencia del segundo avance](docs/SEGUNDO_AVANCE.md)
- [Despliegue en Streamlit](docs/STREAMLIT.md)

## Repositorio y procedencia

El repositorio activo es
[MarlonVillegasmorales/observatorio-cuidado-cdmx](https://github.com/MarlonVillegasmorales/observatorio-cuidado-cdmx).
Conserva el historial y los créditos del repositorio original
[KarlaKsanova/ECONOMIA-DEL-CUIDADO](https://github.com/KarlaKsanova/ECONOMIA-DEL-CUIDADO),
documentado como `upstream`. El despliegue, si se autoriza y verifica, puede
administrarlo Marlon desde la cuenta propietaria del repositorio activo.
