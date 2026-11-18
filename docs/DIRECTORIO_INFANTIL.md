# Directorio documental de oferta infantil en la Ciudad de México

Edición del 18 de noviembre de 2026. Se reunieron registros identificables de las 16 alcaldías. El año de edición indica cuándo se integraron los archivos. Cada fuente conserva su propio periodo. La cobertura de redes es parcial, especialmente en prestadores privados, comunitarios, ISSSTE y DIF.

## Archivos para el portal

- **matriz_16_alcaldias.csv** presenta las redes y los indicadores por alcaldía.
- **detalle_por_red.csv** permite desglosar los indicadores por institución dentro de cada alcaldía.
- **sedes.csv** tiene una fila por ubicación documental. Los indicadores con prefijo con_ valen 1 cuando al menos una de las unidades en ese domicilio tiene el dato. Para contar sedes en el portal se usa este archivo.
- **directorio.csv** conserva las unidades, sus nombres originales, domicilio, claves oficiales cuando se conocen, horarios ordinarios y extraordinarios, capacidad, periodo y enlaces. Conserva las coordenadas documentales del IMSS. Las demás ubicaciones se pueden consultar en una lista hasta verificar sus coordenadas.
- **fuentes.csv** reúne los enlaces usados para identificar unidades y capacidad. Las fichas de Advenio y Baby Star provienen de sus operadores. La contratación o acreditación de particulares requiere verificación adicional.

## Criterios de conteo

Una unidad requiere nombre institucional y ubicación identificable. Los totales agregados de una alcaldía nunca generan sedes. Se agruparon en un id_sede los domicilios coincidentes dentro de la misma demarcación tras uniformar mayúsculas, signos y acentos. Se revisaron turnos y reubicaciones expresas. El CENDI Arenal de Venustiano Carranza aparece dos veces por turno en el PDF y ocupa una sede. En Iztapalapa, el directorio de 2020 documenta la reubicación de Ignacio Zaragoza en el centro social Lucrecia Toriz. En Miguel Hidalgo, los registros de América y Carmen Serdán comparten calle y colonia con número exterior 0 en el padrón. Se contabilizaron conservadoramente como una ubicación pendiente de confirmar. La coincidencia documental no garantiza identidad catastral. Los domicilios escritos de forma distinta pueden requerir revisión adicional. No comparar la suma de capacidades de diferentes periodos como si fuera el aforo actual.

Horario requiere apertura y cierre por centro. Se conservan los horarios históricos y los anunciados por el operador con su periodo. Un turno matutino sin horas precisas queda vacío. Capacidad exacta admite la cifra de capacidad física, máxima o de atención publicada por unidad. En Azcapotzalco se sumaron capacidades por nivel del mismo centro y ejercicio. En Tlalpan se conservaron los intervalos y topes como tales. Vacantes requiere un número explícito de plazas abiertas y su fecha de corte para esa unidad. Una celda vacía significa sin evidencia incorporada. Un 0 en la matriz cuenta sedes que reúnen un indicador. Por ejemplo, 0 en vacantes fechadas significa que ninguna sede aportó ese dato. El expediente contiene exclusivamente información institucional. Se omitieron nombres, teléfonos particulares y padrones de personas usuarias.

## Comprobaciones y pendientes

- Iztapalapa: 30 unidades de alcaldía en el directorio de 2020. La auditoría del ejercicio 2023 identifica 28 centros y una capacidad física total de 1,643. Las coincidencias por nombre se vincularon individualmente. Ignacio Zaragoza y Yunuén quedan sin cifra propia de capacidad. Los horarios de 2020 y las capacidades de 2023 se deben mostrar con sus respectivas fechas. La alcaldía también informa una red de 28 centros: https://www.iztapalapa.cdmx.gob.mx/principal/alcaldiaApartado/Contenido/Cendi.html
- Iztacalco: las 14 cifras de capacidad física suman 661 en 2023. Milpa Alta: siete CENDI con clave de centro de trabajo y capacidad total de 772 en 2023. Xochimilco: seis cifras que suman 598 en 2023. El directorio incluye por separado la estancia de la Utopía Tecómitl inaugurada en 2026.
- Venustiano Carranza: la lista municipal sin fecha y la auditoría de 2023 corresponden a universos distintos. Conciliar sedes históricas, posibles bajas y las unidades Ernestina Lattour y Leona Vicario con domicilio actualizado. Mantener separado el total agregado de capacidad de la auditoría. https://ascm.gob.mx/Informes/CP2023/InformeGeneral/ASCM-164-23.pdf
- El padrón CACI se recuperó parcialmente mediante registros indexados con nombre, domicilio y demarcación. La consulta directa devolvió un error del servidor. Las redes se incorporaron cuando pudo identificarse su adscripción. Se reservaron para revisión el CENDI PEMEX Azcapotzalco y el CADI Tlazocihualpilli por discordancias territoriales. En Tláhuac, tres centros documentados en un cuadro legislativo conservan la adscripción pendiente.
- Completar cada red con un directorio nominal fechado y conciliar altas, bajas y cambios de domicilio. Para ISSSTE se identificó la ficha oficial con capacidad y horarios. La descarga directa no permitió verificar el archivo durante esta revisión. https://www.datos.gob.mx/dataset/estancias_bienestar_desarrollo_infantil_ebdi
- Para actualizar disponibilidad, solicitar únicamente la clave de sede, grupo de edad, turno, plazas abiertas y fecha de corte. El IMSS administra las disponibilidades por guardería. https://siag.imss.gob.mx/instalacionsiag/Guarderias/Manual/Archivos/SIAG%20Control%20de%20Poblacion%20Ninos%20Autoriza%20Disponibilidad%20Lugares.html

## Uso público

Mostrar por defecto nombre, red, alcaldía y periodo de la evidencia. Al abrir la ficha, desplegar domicilio, horario, capacidad y enlace de procedencia. Cuando falte un valor, mostrar «Sin dato documentado». Para el piloto de Iztapalapa, las posibles zonas de inversión requieren contrastar oferta vigente por edad y turno, demanda territorial, elegibilidad y tiempos de traslado. Una alcaldía con menos registros puede tener menor cobertura documental.

## Actualización de las aplicaciones

Desde la raíz del repositorio, ejecutar python scripts/importar_directorio_infantil.py archivo.zip. El archivo compartido se encuentra en cliente_flutter/assets/data/directorio_infantil.json. Streamlit lo lee al abrir el explorador. Flutter lo incluye en la compilación. Para actualizar la web móvil hay que compilar y publicar una nueva versión.
