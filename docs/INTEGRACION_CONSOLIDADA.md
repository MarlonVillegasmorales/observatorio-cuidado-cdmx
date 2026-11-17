# Integración consolidada

## Rama y commits incorporados

La integración se preparó sobre `integracion/base-consolidada`, creada desde
`origin/main` en `a016a25`. Se conservaron los respaldos Flutter existentes.

| Aportación | Commit incorporado | Procedencia |
|---|---|---|
| ETL de CONAPO, movilidad y empresas sintéticas | `4c46b39` | `origin/entrega/karla-etl` |
| Parámetros y notebook de simuladores | `00c8c91` | `origin/entrega/azael-simuladores` |
| Cliente Flutter | `80ca9b5` | `feature/flutter-mobile-mvp` |

La documentación Flutter de `d8fa8d4` no agregó cambios porque ya estaba
incorporada en la base. Las ramas de navegación, mapa, comparación y
rediseño no se copiaron de nuevo: sus cambios útiles ya eran ancestros de la
base. Se omitieron diagnósticos y versiones históricas que duplicaban esa
funcionalidad.

## Correcciones y procedencia

- `ETL_Datos/` conserva los CSV y scripts originales de Karla. El nuevo
  [cargador canónico](../cuidado/pipelines/entregas.py) valida los procesados
  disponibles antes de consumirlos.
- CONAPO se marca como proyección 2021–2030; movilidad conserva relaciones
  ruta-parada y no las convierte en tiempos de viaje; las empresas se marcan
  como sintéticas y los códigos postales se leen como texto.
- La relación TR13/SEMOVI no se corrige silenciosamente. Si aparece en una
  fuente futura, la validación falla y exige revisar el origen.
- `simulador_b2b_b2g_parametros.csv` conserva el original recibido. La copia
  [canónica](../data/processed/simulador_b2b_b2g_parametros.csv) repara su
  estructura sin inventar valores y deja `costo_intervencion` vacío.
- [simulador_b2b_b2g.py](../cuidado/services/simulador_b2b_b2g.py) es la única
  implementación reutilizable. Separa ahorro bruto, impuestos ISN y
  aportaciones patronales; no calcula beneficio neto sin costo de intervención.
- Flutter recupera sus 34 archivos fuente y consume
  [alcaldias.json](../cliente_flutter/assets/data/alcaldias.json), derivado
  del GeoParquet territorial existente. No se versionan `build`, `.dart_tool`,
  configuración local ni secretos.

## Arquitectura resultante

Streamlit continúa siendo la aplicación principal y usa `cuidado/ui`,
`cuidado/services`, `cuidado/domain`, `cuidado/database` y
`cuidado/pipelines`. La integración de entregas ocurre mediante loaders
explícitos; no se ejecutan ETL ni notebooks durante una visita.

Flutter Web es un cliente independiente. Para esta fase usa archivos estáticos
preparados, no Streamlit como API y no un servicio HTTP adicional. El matching
y los simuladores permanecen en Python; una API futura requerirá contrato,
validación y CORS propios.

## Ejecución local

Desde `D:\git\observatorio-cuidado-cdmx`:

```powershell
python -m streamlit run app_dashboard.py
```

```powershell
cd cliente_flutter
flutter pub get
flutter run -d chrome
```

El ETL integrado solo puede regenerar los procesados cuando se incorporen las
fuentes originales no incluidas en esta copia:

```powershell
python ETL_Datos\03_Scripts_Python\etl_movilidad_conapo.py
```

La aplicación no ejecuta ese comando automáticamente.

## Validación y límites

Las pruebas focalizadas validan 16 alcaldías, 22.532 relaciones de movilidad,
50 empresas sintéticas y 30 escenarios financieros. También se comprueban
valores finitos, rangos y ausencia de beneficio neto sin costo de intervención.

Los procesados no sustituyen la revisión de las fuentes originales. Las
proyecciones no son conteos observados, las empresas son sintéticas y una
relación ruta-parada no representa tiempo de viaje ni disponibilidad de
servicio. Flutter conserva pantallas demostrativas de búsqueda y comparación;
no ofrece reservas, centros verificados ni impacto social.

La publicación requiere revisar los resultados en Streamlit y Flutter Web,
confirmar accesibilidad, incorporar fuentes originales con autorización y
ejecutar las pruebas completas en el entorno de publicación. No se hizo push,
despliegue ni integración a `main`.
