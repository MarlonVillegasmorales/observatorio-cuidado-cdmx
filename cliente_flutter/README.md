# Cliente Flutter

Primera fase visual del Observatorio de la Economía del Cuidado CDMX. La
aplicación contiene cinco destinos navegables: Inicio, Mapa, Comparar,
Búsqueda demo y Proyecto.

Esta fase usa Material 3, navegación inferior en pantallas estrechas y
navegación lateral desde 900 px. El mapa consume un archivo JSON estático
derivado del GeoParquet territorial preparado; no ejecuta ETL, no usa
Streamlit como API y no recoge datos personales. La búsqueda y comparación
siguen siendo demostrativas, sin API, persistencia ni reservas.

## Regenerar datos territoriales

Desde la raíz del proyecto:

```powershell
python scripts/generar_json_flutter.py
flutter build web
```

El comando lee `data/processed/mapa_alcaldias/indicadores_alcaldia.parquet`,
valida 16 alcaldías únicas y genera
`cliente_flutter/assets/data/alcaldias.json` de forma determinista.

## Funciones y límites

- Inicio: navegación y presentación del proyecto.
- Mapa: datos territoriales observados del Censo 2020.
- Comparar: proporciones observadas 0–14 y 60+ derivadas del Censo 2020.
- Búsqueda: demostración sintética; no realiza matching ni crea reservas.
- Proyecto: límites y procedencia.
- Simuladores: no están implementados en Flutter; no deben presentarse como
  conectados hasta contar con una API Python validada.

```powershell
flutter analyze
flutter test
flutter run -d chrome
```
