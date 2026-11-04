# Tercera entrega: mapa de alcaldías verificado

## Alcance y estado

La rama `mapa-alcaldias` contiene el rediseño visual previo, la preparación
territorial y el explorador interactivo. Esta entrega sustituye las fuentes
pendientes por archivos oficiales identificables y deja el mapa listo para
revisión de publicación.

La interfaz muestra el perfil demográfico del Censo 2020 de INEGI. No
interpreta pertenecer a un grupo etario como necesidad de cuidado y no muestra
infraestructura, CACI, ENUT ni discapacidad como hechos publicados.

## Fuentes verificadas

### Cartografía

Se descargó el recurso oficial **Límite de Alcaldías (áreas geoestadísticas
municipales)** del Portal de Datos Abiertos de CDMX, mantenido con referencia
al Marco Geoestadístico:

<https://datos.cdmx.gob.mx/dataset/alcaldias/resource/8648431b-4f34-4f1a-a4b1-19142f944300>

Archivo conservado: `data/raw/limites_alcaldias_cdmx_oficial.zip`.
El ZIP contiene 16 polígonos con `CVEGEO`, `CVE_ENT`, `CVE_MUN` y `NOMGEO`.
Se normalizó la clave como texto `09 002` a `09 017`, se conservaron los
nombres oficiales del catálogo local y se transformó a EPSG:4326. No se
aplicó simplificación adicional. Las 16 geometrías resultantes son válidas y
no vacías.

El shapefile histórico
`visualizacion/Equipamiento_de_asistencia_social.*` representa equipamiento
por colonia, no límites territoriales. Se conserva sólo en la auditoría y no
se utiliza para dibujar el mapa público.

### Población

Se descargó el paquete oficial **Censo de Población y Vivienda 2020, ITER por
localidad** de INEGI:

<https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/iter/iter_00_cpv2020_csv.zip>

Archivo conservado: `data/raw/iter_00_cpv2020_csv.zip`. El pipeline agrega las
localidades de entidad `09` por `MUN` y conserva las claves como texto.
Variables originales:

- `POBTOT` → población total.
- `P_0A4` → población de 0 a 4 años.
- `P_5A9` a `P_85YMAS` → grupos quinquenales.

`Edad no especificada` se calcula como `POBTOT - suma de los grupos de edad
publicados`; no se redistribuye. La suma de los grupos publicados y ese
residual concilia exactamente con `POBTOT` en las 16 alcaldías.

La población de 60 años o más se calcula en la interfaz como suma exacta de
`P_60A64`, `P_65A69`, `P_70A74`, `P_75A79`, `P_80A84` y `P_85YMAS`. El cálculo
es descriptivo y no es una categoría exclusiva de necesidad de cuidado.

## Contrato de salida

El comando genera `data/processed/mapa_alcaldias/`:

- `alcaldias.geojson`: 16 polígonos oficiales, claves de texto, EPSG:4326.
- `indicadores_alcaldia.parquet`: formato largo, clave, indicador, valor,
  unidad, periodo 2020, fuente, tipo y estado.
- `catalogo_indicadores.csv`: definición, variable, fórmula, población,
  limitaciones y autorización explícita.
- `fuentes.json`: institución, URL exacta, descarga, cobertura, archivo y
  SHA-256.
- `calidad_mapa.json`: geometrías, uniones, faltantes, conciliación,
  transformaciones y exclusiones.

Reproducción:

```powershell
.\.venv\Scripts\python.exe -m cuidado.pipelines.mapa_alcaldias
```

La interfaz sólo lee estos artefactos mediante caché; no descarga ni ejecuta
el pipeline durante una interacción. La caché incluye firma de ruta, tamaño y
`mtime_ns` de los archivos tabulares y cartográficos, por lo que se invalida
al regenerar cualquiera de ellos.

## Indicadores publicados

El servicio aplica `catalogo_indicadores.csv` y sólo expone filas con
`publicable` iniciado por `sí`:

- Población total.
- Grupos exactos de edad de 0–4 a 85 años y más.
- Edad no especificada, como residual documentado.
- Derivado descriptivo 0–14 y 60 años o más.

Cada tarjeta identifica valor, unidad, periodo 2020, fuente y limitaciones.

## Indicadores omitidos

Se excluyen del panel y del comparativo:

- `guarderias_conteo`: el histórico no tiene procedencia y definición
  verificadas; no representa cupos ni disponibilidad.
- Cobertura CACI e infantes sin cobertura.
- Estimación territorial ENUT.
- Guarderías por 1,000 habitantes.
- Discapacidad hasta validar definición y denominador.

El archivo histórico de equipamiento y los CSV heredados permanecen como
auditoría; no se usan para llenar faltantes con cero.

## Comparación territorial

**Comparar** usa sólo los artefactos tabulares y no construye Folium ni carga
geometrías. Presenta dos indicadores verificables del Censo 2020:

- Personas de 0 a 4 años por cada 100 habitantes: `pob_0_4 /
  poblacion_total * 100`.
- Personas de 60 años o más por cada 100 habitantes: suma de
  `pob_60_64` a `pob_85_plus`, dividida entre `poblacion_total`, por 100.

La referencia de CDMX se calcula como suma de numeradores dividida entre suma
de denominadores de las 16 alcaldías, nunca como promedio simple. La
diferencia se expresa en puntos porcentuales y sólo se calcula con valores
completos y denominadores positivos.

No se habilitaron servicios registrados ni acceso territorial: el directorio
histórico de equipamiento no tiene fecha, definición de servicio, población
atendida, cobertura territorial ni deduplicación verificables. Tampoco hay un
método validado de origen-destino o ruta; no se usa el centroide de una
alcaldía como sustituto de sus habitantes.

## Interfaz y validación

El apartado **Mapa por alcaldía** permite selección por lista o clic normal,
sin selección inicial, restablecimiento a CDMX y panel inferior sincronizado.
El mapa usa la clave territorial y destaca la geometría elegida. **Comparar**
permite elegir dos alcaldías distintas, usa la selección del mapa sólo como
valor inicial de A, y conserva después su propia selección de sesión.

Pruebas automatizadas:

- 16 claves sin duplicados y consultas exactas.
- Clave vacía y desconocida.
- Selección y cálculo de 60+.
- Valores oficiales de Iztapalapa revisados contra el ITER: población total
  `1,835,486` y 0–4 años `103,148`.
- Exclusión del conteo de guarderías y ENUT.
- Geometrías, uniones, faltantes, rangos y conciliación etaria.
- Suite completa y `git diff --check`.

La revisión de navegador cubre selección por lista y polígono, cambio
A→B→A, Iztapalapa, restablecimiento, anchos 360/390/768/1440, overflow y
zoom local al 200 %. Teléfono físico, lector de pantalla y validación del
despliegue público siguen siendo pendientes.

### Auditoría de cifras

La señal inicial (`3,670,972` para Iztapalapa y `2,346,702` para Gustavo
A. Madero) era exactamente el doble de los valores oficiales del ITER
(`1,835,486` y `1,173,351`). El archivo fuente contiene, para cada alcaldía,
una fila `LOC=0` titulada “Total del Municipio” y las filas de localidades;
el pipeline sumaba ambas. La corrección excluye `LOC=0`, conserva las
localidades y regenera `indicadores_alcaldia.parquet`, `catalogo_indicadores.csv`,
`calidad_mapa.json` y `fuentes.json`. Las 16 claves siguen siendo únicas, no
hay duplicados por alcaldía/indicador/periodo, y la conciliación de grupos de
edad permanece exacta.

## Condiciones de publicación

La cartografía y población ya tienen fuentes oficiales y checksums. Antes de
integrar se debe comprobar en navegador la versión final local, revisar el
diff que se incluirá, ejecutar las pruebas y verificar el PR. La URL pública
no se considera actualizada hasta comprobar una nueva revisión de `main`.
