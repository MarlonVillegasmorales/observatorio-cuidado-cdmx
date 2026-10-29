# Despliegue en Streamlit Community Cloud

## Repositorios y permisos

El repositorio de trabajo para esta copia es
`MarlonVillegasmorales/observatorio-cuidado-cdmx`. El repositorio original se
conserva como `upstream` para documentar el origen y las contribuciones:
`KarlaKsanova/ECONOMIA-DEL-CUIDADO`. Los cambios deben publicarse en `origin`;
no se debe hacer push a `upstream`.

La cuenta propietaria de Marlon tiene permisos suficientes para crear y
administrar el despliegue inicial de Community Cloud desde el repositorio
activo. Las personas colaboradoras pueden aportar código según sus permisos
de GitHub, pero no es necesario que Karla cree el despliegue.

## Procedimiento posterior al rediseño visual

La tercera entrega se prepara en la rama `mapa-alcaldias`; no se publica
automáticamente. Después de revisar el resultado local:

1. Revisar y aprobar las cuatro secciones en computadora y celular.
2. Crear el commit de los cambios pertinentes.
3. Subir `mapa-alcaldias` al repositorio propio.
4. Crear y revisar un pull request hacia `main`.
5. Integrar el PR después de las comprobaciones.
6. Verificar que Streamlit procese la nueva revisión de `main`.
7. Revisar logs y comprobar las cuatro secciones publicadas.
8. Comprobar acceso sin sesión y desde celular con datos móviles.

El despliegue conserva Python 3.12 y `app_dashboard.py`; un cambio visual no
requiere eliminar ni recrear la aplicación. Si una regresión aparece después de
integrar, revertir el commit de integración con un commit nuevo (`git revert
<commit>`), revisar y publicar ese revert; no reescribir el historial
compartido.

## Validación local del rediseño

La revisión del rediseño se realiza con el intérprete propio:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m streamlit run app_dashboard.py
```

Se deben revisar las cuatro secciones en anchos de 360, 390, 768 y 1440 px,
incluidas orientación horizontal y zoom de 200 %. La revisión debe comprobar
el recorrido completo de búsqueda, los estados de resultados pendientes, el
mapa, las tablas, las etiquetas y el foco de teclado, así como que no exista
desplazamiento horizontal general. Las capturas de navegador son evidencia de
emulación de ancho, no certificación de un teléfono real ni de accesibilidad
completa. La URL pública no cambia hasta integrar el PR en `main`.

La navegación del rediseño se mantiene en el flujo de la página mediante un
radio nativo horizontal que se adapta y envuelve en pantallas estrechas. No se
fija al borde inferior: así evita tapar el mapa, tablas, atribuciones y el
contenido final, y conserva un único control accesible para computadora y
celular.

### Comprobaciones del mapa `mapa-alcaldias`

Realizadas el 29 de octubre de 2026 con Python 3.12 y el servidor local
`http://localhost:8501`:

- Se recorrieron **Mapa por alcaldía**, **Comparar**, **Búsqueda demo** y
  **Proyecto**.
- Se revisaron 360, 390, 768 y 1440 px; en todos los casos
  `scrollWidth == clientWidth`, sin desplazamiento horizontal general.
- Se generaron capturas de las cuatro secciones a 1440 px y 390 px.
- Se comprobó que la navegación se envuelve en celular, conserva etiquetas
  legibles y que los controles de búsqueda permanecen operables.
- Se verificó que el mapa y los gráficos permanecen dentro del contenedor y
  que las tablas se muestran dentro de su componente propio.
- Se completó la búsqueda con clics normales hasta resultados y se verificó el
  estado de resultado sintético.
- Se recorrieron controles con teclado; los campos, radios y botones mostraron
  foco visible con el esquema de foco de la interfaz.
- Se aplicó zoom real del navegador al 200 % (`devicePixelRatio` 2.0) y no
  apareció overflow horizontal (`scrollWidth == clientWidth`).
- La suite existente pasó: `17 passed`; también pasó `git diff --check`.
- Se verificaron tres alcaldías, incluida Iztapalapa, por lista y mediante
  clic normal en un polígono; se confirmó la clave esperada y el nombre del
  panel en cada selección.
- El comparativo sólo ofrece población total y 0–4 años del conjunto oficial.
- La regeneración ejecutada fue
  `.\.venv\Scripts\python.exe -m cuidado.pipelines.mapa_alcaldias`.

### Limitaciones y pruebas pendientes

- Las capturas son emulación del navegador, no una prueba en teléfonos físicos.
- No se certificó con hardware real el área segura inferior ni lectores de
  pantalla.
- El componente de tabla conserva controles propios de Streamlit; su
  interacción completa con teclado y ampliación debe revisarse manualmente en
  cada navegador objetivo.
- Las advertencias de Vega-Lite, deprecación de `use_container_width` y
  `DtypeWarning` del ITER son advertencias de dependencias o lectura de la
  fuente; no invalidaron los resultados, pero deben revisarse si se actualizan
  dependencias.
- No se probó teléfono físico ni lector de pantalla.

## Configuración inicial

En https://share.streamlit.io/ → Create app, desde un repositorio existente:

| Campo | Valor |
|---|---|
| Repository | MarlonVillegasmorales/observatorio-cuidado-cdmx |
| Branch de revisión | main |
| Main file path | app_dashboard.py |
| Python en Advanced settings | 3.12 |
| Secrets | Ninguno para este demo público |

`main` contiene la versión completa del segundo avance y la mejora de
experiencia de usuario. `requirements.txt` está en la raíz. Community Cloud no
necesita el Dockerfile. El dataset preparado público viaja con el código.

El demo no persiste información operativa y no necesita Neon ni otra base.
Cuando exista operación privada, configurar PostgreSQL y validar acceso,
privacidad y persistencia; no usar un archivo SQLite del alojamiento como
registro duradero. No introducir credenciales en requirements, Git o el PR.

## Diagnóstico

- Repositorio no disponible o error de permisos: verificar la cuenta
  propietaria de Marlon, el repositorio activo y el permiso de administración;
  no modificar Python para resolverlo.
- ModuleNotFoundError: comprobar ruta raíz y requirements.txt.
- Falta dataset: ejecutar `python -m cuidado.pipelines.preparar` localmente
  y publicar data/processed/observatorio.parquet y sus JSON.
- Error al instalar: revisar log y Python 3.12 antes de cambiar versiones.
- Sin entrega B2B/B2G: estado previsto, no error de despliegue.

## Fuentes oficiales consultadas el 27 de octubre de 2026

https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started/connect-your-github-account
https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
https://docs.github.com/account-and-profile/concepts/personal-repository-access-and-collaboration

No se ha creado una aplicación ni configurado una cuenta de Streamlit desde
esta migración. El error anterior de Google Cloud no fue diagnosticado porque
no se dispone de su mensaje ni sus logs.
