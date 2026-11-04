# Rendimiento y diagnóstico del mapa

## Alcance y entorno

Las comprobaciones se realizaron el 3 de noviembre de 2026 en Windows,
con Python 3.12.3, Streamlit 1.52.1, `streamlit-folium` 0.25.3, Folium
0.20.0 y el entorno `.venv` del repositorio. La aplicación local quedó
ejecutándose en `http://127.0.0.1:8503/`.

No se modificaron dependencias, permisos, configuración de seguridad,
rama ni despliegue. La rama de trabajo se conserva como
`optimizacion-carga`.

## Instrumentación corregida

Las mediciones de navegador se cerraron con Playwright y esperas por
condiciones observables. Cada espera tiene un máximo de 10 a 30 segundos;
si vence, la muestra se registra como fallo y no como un tiempo válido.

- **Inicio:** comienza antes de recargar o navegar y termina cuando el
  encabezado de Inicio y el botón `Explorar mapa` están visibles y el botón
  está habilitado.
- **Mapa:** comienza antes de pulsar `Explorar mapa` desde un Inicio ya
  cargado. Termina sólo cuando el iframe
  `streamlit_folium.st_folium` está visible, su documento contiene un
  contenedor Leaflet visible y existen 16 elementos
  `.leaflet-interactive` visibles. La carga del fondo cartográfico se
  registra por separado esperando `.leaflet-tile`.
- **Cambio de alcaldía:** la muestra comienza inmediatamente antes de
  pulsar la opción de la alcaldía alternativa. Termina cuando el selector,
  el encabezado del panel y el polígono seleccionado (borde
  `#6D28D9`) corresponden a la misma alcaldía. Las alcaldías se alternaron
  para evitar medir una selección repetida.
- **Regreso al mapa:** comienza con Inicio ya cargado, inmediatamente antes
  de pulsar `Explorar mapa`, y usa el mismo criterio observable del mapa.

No se usaron pausas fijas como condición de finalización. Los fallos de
iframe, Leaflet, polígonos, panel o selector se consideran fallos de carga y
no se sustituyen por un número.

El mapa actualmente se construye con `tiles=None`; por eso la medición
separada del fondo cartográfico es **no aplicable**: se observaron
`0` elementos `.leaflet-tile` y no se solicitó una tesela. Esto no se
presenta como carga rápida del fondo.

## Mediciones locales actuales

Todas estas muestras se tomaron con el servidor local activo y una sesión
de navegador ya establecida. Las muestras de recarga no son arranque en
frío: son recargas del navegador con el proceso de Streamlit activo. No se
obtuvo una línea base comparable de la versión anterior, así que no se
afirman porcentajes de mejora.

| Escenario | Muestras (ms) | Condición de término |
|---|---:|---|
| Recarga hasta Inicio utilizable | 1,603; 1,078; 981 | Encabezado y `Explorar mapa` visibles y habilitado |
| Inicio cargado → Mapa utilizable | 958; 1,145; 1,271 | Iframe visible, Leaflet visible y 16 polígonos interactuables |
| Cambio alternado de alcaldía | 1,093; 993; 1,042 | Selector, panel y un polígono seleccionado coinciden |
| Inicio cargado → Regreso a Mapa | 958; 1,145; 1,271 | Iframe visible, Leaflet visible y 16 polígonos interactuables |
| Fondo cartográfico | N/A (0 teselas) | No hay capa de fondo configurada |

El cambio alternó Coyoacán, Iztapalapa y Milpa Alta. La condición
cartográfica verificó un único polígono con el estilo de selección y 16
polígonos totales. No se midió una sesión de navegador nueva aislada con
tres muestras, por lo que esa dimensión queda distinguida de la sesión con
caché disponible y no se infiere a partir de una recarga.

Como evidencia de proceso y archivos, una carga local de los datos preparados
con caché disponible permanece separada de la experiencia de navegador. El
GeoJSON contiene 16 geometrías y ocupa 773,483 bytes; no se presenta esa
carga como tiempo de interacción.

## Diagnóstico de la aplicación pública

URL comprobada:
`https://observatorio-cuidado-cdmx-9tklh8utkwwfn6kgsjwtsf.streamlit.app/`

La captura de consola y red se inició antes de navegar. En la primera
observación, durante 15 segundos:

- el documento y los recursos de la interfaz alojada de Streamlit cargaron;
- no se observó un WebSocket de la aplicación abierto antes de que terminara
  la ventana de espera;
- el cuerpo superior permaneció vacío para la aplicación y no existió un
  iframe de `streamlit_folium`;
- se registró `403` en
  `/api/v1/app/event/open`;
- se registraron `404` en `/api/v2/user/details` y en
  `https://cdn.heapanalytics.com/js/heap-.js`;
- `/~/+/_stcore/health` respondió `200` en una comprobación posterior.

Los recursos se clasificaron así:

- **Alojamiento/Streamlit:** los scripts y hojas de estilo de
  `/-/build/assets/` cargaron; el estado de la aplicación respondió `200`.
- **Aplicación:** `/api/v2/app/context`, `/api/v2/app/status`,
  `/api/v2/app/disambiguate` y `/api/v2/feature-flags` respondieron `200`.
- **Analítica:** Heap falló con `404`; las solicitudes Datadog observadas
  respondieron `202`.
- **Componente:** en una navegación posterior sí se creó el iframe
  `.../component/streamlit_folium.st_folium/index.html`; su Leaflet mostró
  16 polígonos. No se solicitaron teselas porque la aplicación no configura
  un fondo.
- **WebSocket:** no hay evidencia de apertura durante la primera ventana
  con spinner; no se atribuye ese hecho a un recurso del componente que aún
  no existía.

En una navegación posterior, la aplicación pública terminó mostrando Inicio
y, tras pulsar `Explorar mapa`, creó el iframe del componente en
aproximadamente 21.9 s hasta iframe visible. El iframe terminó mostrando
Leaflet y los 16 polígonos. Streamlit también mostró la advertencia de que
el componente tenía problemas de carga; la advertencia no impidió esa
creación posterior del iframe.

El endpoint público de desambiguación identificó:

- repositorio `marlonvillegasmorales/observatorio-cuidado-cdmx`;
- rama desplegada `main`;
- módulo `app_dashboard.py`;
- Python 3.12 y Streamlit 1.52.1.

Ese endpoint no proporcionó un SHA de revisión. No se afirma que el
`origin/main` local sea el commit ejecutado por Cloud.

### Causa confirmada e hipótesis pendientes

No hay una causa confirmada del spinner inicial. La evidencia confirma una
incidencia intermitente de inicialización o comunicación del runtime:
la primera ventana no mostró el canal de la aplicación y una navegación
posterior sí cargó la aplicación y el componente. El `403` de
`/api/v1/app/event/open` puede ser telemetría o un evento auxiliar; no se
demostró que bloquee la sesión. Los `404` de `user/details` y Heap tampoco
se relacionaron causalmente con el bloqueo.

No se tuvo acceso autorizado a logs de Streamlit Cloud. Falta, para cerrar
la causa, el log de despliegue y runtime de la instancia afectada, su SHA
real desplegado, el mensaje del servidor durante el primer intento, y la
secuencia de apertura/cierre del WebSocket o protocolo equivalente en esa
misma instancia. Sin esos datos no puede confirmarse si el problema fue
latencia, reinicio, error del componente, proxy o fallo del runtime.

## Validación local de escritorio, móvil y teclado

Se verificó la interacción pendiente sin forzar clics ni ejecutar JavaScript
para saltar controles:

- `Consultar sin mapa` tuvo etiqueta visible y caja visible en escritorio y
  ancho móvil de 390 px.
- Con Coyoacán seleccionada, la etiqueta se enfocó con el teclado y
  `Espacio` desactivó el mapa: desapareció el iframe, permanecieron el
  selector y el panel de Coyoacán.
- Otro `Espacio` reactivó el mapa y conservó Coyoacán; el iframe volvió a
  mostrar Leaflet.
- La medición de ancho dio `scrollWidth == clientWidth`: 876/876 px en
  escritorio y 390/390 px en móvil. No se observó desplazamiento
  horizontal ni contenido cortado.

La prueba anterior que no encontró el input no se interpreta como defecto:
la etiqueta visible y el acceso por teclado sí fueron comprobados.

## Validaciones y estado de entrega

- `git diff --check`: aprobado.
- No se repitieron las pruebas funcionales previamente aprobadas salvo la
  instrumentación de medición y la comprobación específica de móvil,
  teclado y conservación de selección.
- La reproducción mínima separada está en
  [`diagnostics/repro_mapa.py`](../diagnostics/repro_mapa.py).
- La aplicación local queda funcionando en
  `http://127.0.0.1:8503/`.
- No se hicieron commit, push, merge ni despliegue.
