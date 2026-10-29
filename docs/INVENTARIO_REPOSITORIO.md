# Inventario del repositorio

Inventario de la copia migrada al repositorio privado
`MarlonVillegasmorales/observatorio-cuidado-cdmx`. No se reorganiza ni elimina
código histórico en esta entrega; las decisiones son propuestas para una
limpieza posterior.

| Carpeta o archivo | Función | ¿Lo utiliza la aplicación actual? | Referencias o imports encontrados | Decisión propuesta | Evidencia |
|---|---|---|---|---|---|
| `cuidado/` | Arquitectura modular: UI, servicios, dominio, persistencia y ETL | Sí | `app_dashboard.py` importa `cuidado.ui.app`; los servicios importan dominio, base y datos preparados | Conservar | `docs/ARQUITECTURA.md`, `tests/` y los imports del paquete |
| `cuidado/ui/` | Cuatro secciones actuales y estilos de Streamlit | Sí | `cuidado.ui.app` importa `evidencia`, `simulacion`, `integraciones` y `territorial` | Conservar | `cuidado/ui/app.py` define `TAREAS` con cuatro secciones |
| `cuidado/services/` | Evidencia, simulación, integraciones y vinculación | Sí | Importado por `cuidado/ui/app.py` y `cuidado/ui/territorial.py` | Conservar | `tests/test_evidencia.py`, `tests/test_matching.py` |
| `cuidado/domain/` | Reglas de matching y entidades de centros | Sí | `cuidado/services/simulacion.py` y `vinculacion.py` | Conservar | `tests/test_matching.py`, `docs/CONTRATOS.md` |
| `cuidado/database/` | Conexión, modelos e inicialización aditiva | Sí, en pruebas y operación futura | `tests/test_database.py`, `cuidado/services/vinculacion.py` | Conservar | `docs/ARQUITECTURA.md` documenta el esquema v2 |
| `cuidado/pipelines/` | Preparación del dataset territorial y reporte de calidad | Sí, al regenerar datos | `cuidado/pipelines/preparar.py`; `cuidado/services/evidencia.py` consume el resultado | Conservar | `README.md` y `data/processed/` |
| `app_dashboard.py` | Punto de entrada principal | Sí | Importa `cuidado.ui.app.main`; Dockerfile y pruebas lo ejecutan | Conservar | `tests/test_app.py`, `Dockerfile` |
| `programas webapp/` | Scripts y entrada histórica compatibles | No como entrada principal; sí como compatibilidad | `programas webapp/etl_pipeline.py` delega a `cuidado.pipelines`; `database_setup.py` importa `cuidado.database` | Conservar por ahora | `README.md`, `docs/CONTRATOS.md` y sus imports |
| `dashboard/` | Marcador del área histórica de dashboard | No | Sólo `.gitkeep`; no hay imports | Archivar en una limpieza futura | La carpeta no contiene código ejecutable |
| `visualizacion/` | Fuentes cartográficas y script de visualización | Sí, ETL usa el `.shp` | `cuidado/pipelines/territorial.py` referencia el shapefile; `vizuai.py` es legado | Conservar sin separar componentes | El shapefile requiere `.shp`, `.shx`, `.dbf`, `.prj` y archivos auxiliares juntos |
| `data/raw/` | Fuentes CSV originales | Sí, para regenerar el dataset | `cuidado/pipelines/territorial.py` lee indicadores y fuentes territoriales | Conservar | El ETL documenta las rutas y procedencia |
| `data/processed/` | Dataset GeoParquet y metadatos preparados | Sí, la UI carga `observatorio.parquet` | `cuidado/services/evidencia.py` y `README.md` | Conservar | `calidad.json` y `observatorio.metadata.json` acompañan el parquet |
| `notebooks/` | Exploración y limpieza reproducible | No durante el arranque | `01_limpieza.ipynb`; no hay imports de runtime | Conservar | Es fuente de análisis y documentación del ETL |
| `docs/` | Arquitectura, contratos, avance, despliegue e inventario | Indirectamente | Enlaces desde `README.md` | Conservar | Documenta límites, fuentes, permisos y validación |
| `tests/` | Pruebas unitarias, de integración y AppTest | No en runtime; sí en validación | Importa todos los módulos principales | Conservar | `README.md` ejecuta `pytest`; `docs/SEGUNDO_AVANCE.md` resume cobertura |
| `Dockerfile` | Imagen reproducible de Streamlit | Sólo al desplegar con Docker | Ejecuta `app_dashboard.py` | Conservar | Coincide con el punto de entrada actual |
| `requirements.txt` y `requirements-dev.txt` | Dependencias runtime y de pruebas | Sí | Streamlit, pandas, SQLAlchemy y Pytest | Conservar | Comandos de instalación del `README.md` |
| `.streamlit/` | Configuración pública y plantilla de secretos | Sí, configuración; no secretos | Streamlit carga `config.toml`; `secrets.toml.example` es plantilla | Conservar; excluir secretos reales | `.gitignore` excluye `.streamlit/secrets.toml` |
| `.venv/`, `.pytest_cache/`, `__pycache__/`, `.ipynb_checkpoints/` | Entornos y cachés locales | No | Sin imports válidos | Excluir del control de versiones | `.gitignore`; los checkpoints rastreados fueron retirados de esta copia |

## Limpieza pendiente

Antes de reorganizar, confirmar con el equipo si `dashboard/` y
`visualizacion/vizuai.py` todavía se usan en entregas externas. También conviene
separar adaptadores históricos de `programas webapp/` sólo después de verificar
sus consumidores. No mover componentes del shapefile individualmente.
