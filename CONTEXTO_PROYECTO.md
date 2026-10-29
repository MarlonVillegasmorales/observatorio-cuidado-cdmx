# Contexto maestro del proyecto

## Identidad y propósito

**Nombre:** Observatorio de la Economía del Cuidado CDMX y Sistema de
Vinculación B2B2C.

**Problema:** las necesidades y responsabilidades de cuidado se distribuyen de
forma desigual; la información sobre demanda, oferta, recursos y brechas está
fragmentada y existen barreras territoriales, sociales y económicas. El PDF
académico describe este problema y pide convertir datos en evidencia para
decidir (pp. 2–4). No se reduce a la ausencia de una aplicación.

**Propósito:** integrar evidencia sobre cuidado en CDMX y apoyar decisiones y
una futura vinculación con centros comunitarios, complementada con escenarios
B2B/B2G cuando existan datos y métodos validados. La intervención social debe
derivarse de hallazgos, no de una solución preconcebida (pp. 3–5).

La secuencia de trabajo es **datos → evidencia → decisión → programa de
innovación social**. El análisis académico completo está en
[docs/ANALISIS_PROBLEMA_PROTOTIPICO.md](docs/ANALISIS_PROBLEMA_PROTOTIPICO.md);
la matriz que gobierna el estado está en
[docs/REQUISITOS_Y_AVANCES.md](docs/REQUISITOS_Y_AVANCES.md).

## Fundamento académico

El documento *Problema prototípico: Observatorio de datos para el diseño de
programas de innovación social en la economía del cuidado*, de la Universidad
Nacional Rosario Castellanos, Licenciatura en Ciencias de Datos para los
Negocios, 7.º semestre, periodo 2026-2, articula seis UCA y una ruta de
observar, proteger, analizar, comprender, modelar, intervenir, evaluar y
documentar (pp. 1, 4–6 y 18).

El proyecto adopta operativamente: integrar fuentes para CDMX; analizar
necesidades y brechas con indicadores interpretables; ofrecer un observatorio
usable en computadora y celular; explorar vinculación con centros
comunitarios; diseñar una intervención sustentada en hallazgos; definir
protección y seguimiento; y explorar B2B/B2G solo con fuentes y supuestos
explícitos. Estos son compromisos del equipo, no resultados ya demostrados.

## Alcance territorial y etapa

- El observatorio y el ETL cubren las 16 alcaldías de CDMX.
- Iztapalapa es un piloto territorial propuesto, no un piloto ejecutado.
- La aplicación actual es una demostración sintética local.
- Un piloto real y una expansión futura requieren centros, participantes,
  autorizaciones, seguimiento y evaluación verificables.
- No existen en este repositorio pruebas de convenios, centros participantes,
  familias inscritas, empleo generado, tiempo liberado o impacto causal.
- La expansión a otros estados no es un compromiso vigente.

## Usuarios y necesidades previstas

| Usuario | Necesidad delimitada |
|---|---|
| Familias | Entender necesidades y explorar opciones de cuidado. |
| Comunidad | Conocer servicios y brechas de su zona. |
| Empresas | Explorar apoyo al personal y escenarios B2B. |
| Instituciones | Analizar brechas y escenarios B2G. |
| Administradores autorizados | Gestionar una operación privada cuando exista. |

En el caso didáctico, Renata, “Manos que Cuidan”, 15 familias y 6 cuidadoras
son elementos narrativos del PDF (pp. 8–10), no participantes ni resultados de
este proyecto.

## Funciones actuales y evidencia

| Función | Código y acceso | Estado comprobable |
|---|---|---|
| Conocer mi zona | `cuidado/ui/app.py`, opción de Streamlit y `cuidado/ui/territorial.py` | Implementada localmente; indicadores y límites requieren auditoría analítica. |
| Comparar zonas | `cuidado/ui/app.py` y `mostrar_comparativo_cuidado` | Implementada localmente; no es evaluación de impacto. |
| Probar una búsqueda | `_render_busqueda` en `cuidado/ui/app.py` | Implementada como demo sintética de cuatro pasos; conserva valores y marca resultados pendientes al cambiar filtros. |
| Información del proyecto | `cuidado/ui/app.py` e `INTEGRACIONES` | Visible; muestra entregas pendientes, no las convierte en módulos recibidos. |
| ETL y datos preparados | `cuidado/pipelines/`, `data/processed/` | Código y artefactos versionados; la procedencia y comparabilidad de cada fuente siguen requiriendo validación. |
| Matching demostrativo | `cuidado/domain/centros.py`, `cuidado/services/simulacion.py` | Implementado y probado localmente; greedy por orden de solicitudes, no modelo predictivo entrenado. |
| Persistencia y confirmación interna | `cuidado/database/`, `cuidado/services/vinculacion.py` | Código y pruebas locales; no está expuesto en la interfaz pública ni validado con PostgreSQL o personas reales. |

La existencia de código o una prueba local no demuestra uso con participantes,
accesibilidad completa ni despliegue.

## Funciones previstas y límites

Son ampliaciones sujetas a evidencia y contratos: directorio verificado de
centros; horarios, requisitos, costos, accesibilidad y cupos; solicitudes,
recomendaciones, confirmación, cancelación y seguimiento; acceso privado por
rol; movilidad y proyecciones demográficas; B2B/B2G; y evaluación del modelo y
del piloto. El alcance necesario para la versión final se controla en la
[matriz de requisitos](docs/REQUISITOS_Y_AVANCES.md); no todas las
posibilidades son compromisos obligatorios.

## Experiencia, accesibilidad y arquitectura

La interfaz comparte lógica para computadora y celular, usa navegación por
tareas y lenguaje explicativo, y comunica que distancia geográfica no es
tiempo de viaje. La aplicación ya conserva valores de búsqueda y explica
motivos de compatibilidad o rechazo. Persisten por comprobar de manera
sistemática teclado, foco, contraste, ampliación, alternativas textuales,
estados no dependientes del color y accesibilidad móvil; AppTest o un health
check aislado no bastan.

La arquitectura es un monolito modular: `cuidado/ui` presenta,
`cuidado/services` coordina, `cuidado/domain` aplica reglas,
`cuidado/database` contiene persistencia y `cuidado/pipelines` prepara datos.
`app_dashboard.py` es la entrada principal. `data/raw`, `data/processed`,
`tests`, `docs` y `notebooks` tienen funciones documentadas en el
[inventario](docs/INVENTARIO_REPOSITORIO.md). `programas webapp/` y
`visualizacion/` conservan compatibilidad y fuentes históricas; no se declara
obsoleto un archivo solo por su nombre.

La conexión usa `DATABASE_URL`; el entorno `.venv` es local. El ETL se ejecuta
explícitamente fuera del ciclo de interacción de Streamlit. La arquitectura
detallada está en [docs/ARQUITECTURA.md](docs/ARQUITECTURA.md).

## Fuentes, vinculación y privacidad

El dataset preparado combina fuentes territoriales, cartográficas, CACI, ENUT
y datos macroeconómicos con años, poblaciones y granularidades distintas.
`data/processed/observatorio.metadata.json` y `calidad.json` acompañan el
resultado. Se distinguen observaciones, estimaciones, proyecciones y datos
sintéticos; la procedencia de algunos insumos debe confirmarse con el equipo.
No se debe confundir centroide de CP con domicilio, infraestructura con cupos,
distancia con tiempo de viaje ni recomendación con atención recibida.

El matching recibe tipo, días, horario, coordenadas, radio y cupos; filtra
ofertas verificadas, calcula distancia haversiana y asigna greedy por orden de
entrada. Devuelve recomendación o motivo de incompatibilidad y versión del
modelo. No optimiza globalmente ni prueba impacto laboral. La confirmación
transaccional es interna y consume cupo; recomendación no equivale a
confirmación institucional.

La demo no recoge personas ni escribe simulaciones en una base compartida.
Antes de datos reales se requieren minimización, seudonimización,
autorización, seguridad, conservación/eliminación, auditoría, verificación
institucional, atención de incidencias y evaluación jurídica. Un UUID no
anonimiza ubicaciones. No se afirma cumplimiento legal completo.

## Equipo, entregas y continuidad

- **Marlon:** arquitectura, interfaz, matching, integración y despliegue.
- **Karla:** datos/GIS, movilidad/CONAPO y plantilla empresarial simulada.
- **Azael:** simuladores financieros y documentación académica.

La ausencia de un módulo no elimina a su responsable. Las entregas deben
distinguir recepción, revisión, integración y validación; los contratos están
en [docs/CONTRATOS.md](docs/CONTRATOS.md). Las dos entregas de Karla y las de
Azael siguen pendientes de recepción e integración según la evidencia local.

El repositorio activo es
[MarlonVillegasmorales/observatorio-cuidado-cdmx](https://github.com/MarlonVillegasmorales/observatorio-cuidado-cdmx),
en `D:\git\observatorio-cuidado-cdmx`. Se conservan el origen y créditos de
[KarlaKsanova/ECONOMIA-DEL-CUIDADO](https://github.com/KarlaKsanova/ECONOMIA-DEL-CUIDADO)
como `upstream`; los cambios de esta copia se publican en `origin`. Marlon
puede administrar el despliegue desde la cuenta propietaria del repositorio
activo; no se afirma que exista una aplicación desplegada. El procedimiento
está en [docs/STREAMLIT.md](docs/STREAMLIT.md).

Reglas permanentes: revisar estado Git antes de editar, conservar cambios y
responsabilidades, mantener separación de capas, no fabricar fuentes o
resultados, no borrar históricos sin revisar consumidores y actualizar la
documentación cuando cambie el alcance.
