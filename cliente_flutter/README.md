# Cliente Flutter

Primera fase visual del Observatorio de la Economía del Cuidado CDMX. La
aplicación contiene cinco destinos navegables: Inicio, Mapa, Comparar,
Búsqueda demo y Proyecto.

Esta fase usa Material 3, navegación inferior en pantallas estrechas y
navegación lateral desde 900 px. El mapa consume un archivo JSON estático
derivado del GeoParquet territorial preparado; no ejecuta ETL, no usa
Streamlit como API y no recoge datos personales. La búsqueda y comparación
siguen siendo demostrativas, sin API, persistencia ni reservas.

```powershell
flutter analyze
flutter test
flutter run -d chrome
```
