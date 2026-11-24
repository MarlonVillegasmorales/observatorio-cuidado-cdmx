# Protección de datos en el Observatorio del Cuidado
Guía de revisión docente · Grupo 702 · 18 de noviembre de 2026

**Qué demostrar en pantalla.** Abrir el mapa y seleccionar Iztapalapa. Se pueden consultar 42 centros y 37 horarios documentados sin introducir datos de una familia. Abrir una ficha y distinguir la dirección del centro, el año del horario y la fecha de disponibilidad. El mapa usa coordenadas institucionales. Las cifras de INEGI describen México en 2022.

| Disposición | Decisión del proyecto | Evidencia o pendiente |
|---|---|---|
| Constitución, arts. 1, 4, 6 y 16 | Evitar discriminación, proteger a la niñez y respetar la privacidad y la protección de datos. | El directorio se consulta sin registro de familias. La selección territorial utiliza la alcaldía elegida. |
| Ley General de los Derechos de Niñas, Niños y Adolescentes, art. 76 | Proteger la intimidad personal y familiar. | Se publican nombres y domicilios de centros. La lista de columnas permitidas excluye campos de identidad, salud y domicilio familiar. Revisar manualmente el contenido de los campos de texto antes de incorporar fuentes nuevas. |
| Ley General de Protección de Datos Personales en Posesión de Sujetos Obligados | Si una institución pública determina las finalidades del tratamiento, debe justificar atribuciones, finalidad, proporcionalidad, información, seguridad y atención de derechos. | El importador selecciona campos institucionales. Antes del piloto, identificar al responsable público y documentar la base de tratamiento. |
| Ley de Protección de Datos Personales en Posesión de Sujetos Obligados de la Ciudad de México, publicada el 13 de julio de 2026 | Aplica al tratamiento a cargo de sujetos obligados locales, por ejemplo una alcaldía. | Si la alcaldía recibe solicitudes identificables, definir aviso, unidad que atiende derechos, plazos, accesos y transferencias. |
| Ley Federal de Protección de Datos Personales en Posesión de los Particulares | Si una empresa o centro privado decide para qué utilizar datos personales, le corresponde el régimen privado. | Para futuras inscripciones, documentar finalidades, aviso, consentimiento cuando proceda, conservación y mecanismo de derechos ARCO: acceso, rectificación, cancelación y oposición. |
| Ley Federal del Trabajo, arts. 2 y 3 | El análisis empresarial debe respetar trabajo digno y no discriminación. | El directorio carece de perfiles laborales individuales. Para el piloto, comunicar métricas agregadas y controlar el riesgo de identificar personas en equipos pequeños. |
| ISO/IEC 27001, 27002 y 27701 | Referencias voluntarias para gestionar seguridad, controles y privacidad. | El documento del equipo las propone para diseñar el piloto. No se ha acreditado certificación. |

**Incidente crítico.** Saber dónde está un centro y en qué horario atiende ayuda a planear el cuidado. Asociar la ubicación de una niña con el turno y las ausencias de su madre permitiría reconstruir una rutina familiar y podría facilitar discriminación laboral. Por eso la consulta pública trabaja con sedes e indicadores agregados.

**Control comprobable.** El importador permite únicamente campos definidos para la ficha pública. La prueba del directorio recorre todas las unidades y verifica las claves publicadas. Este control revisa la estructura. Una dirección o nota de texto requiere además revisión humana de su contenido. La información breve de privacidad explica la consulta del directorio. Para captar datos del piloto se requiere su propio aviso con responsable y medio de contacto efectivos.

**Pendientes antes del piloto.** Designar responsables por flujo, acordar las transferencias, establecer acceso por rol y cifrado, atender ARCO, definir retención, eliminación y respuesta ante incidentes, y evaluar el riesgo de reidentificación. La participación del gobierno o su financiamiento por sí solos no fijan el régimen de una empresa privada. El alcance de esta revisión es el directorio público. Falta revisar por separado los registros técnicos y las condiciones de los proveedores de alojamiento.

**Fuentes oficiales**
- [Constitución](https://www.diputados.gob.mx/LeyesBiblio/pdf/CPEUM.pdf)
- [Ley de derechos de la niñez](https://www.diputados.gob.mx/LeyesBiblio/pdf/LGDNNA.pdf)
- [Ley general de datos en el sector público](https://www.diputados.gob.mx/LeyesBiblio/pdf/LGPDPPSO.pdf)
- [Ley local de CDMX](https://paot.org.mx/centro/leyes-normas-htmls/ley-de-protecci-n-3052.html)
- [Ley federal de datos en el sector privado](https://www.diputados.gob.mx/LeyesBiblio/pdf/LFPDPPP.pdf)
- [Ley Federal del Trabajo](https://www.diputados.gob.mx/LeyesBiblio/pdf/LFT.pdf)
- [INEGI, ENASIC 2022](https://www.inegi.org.mx/programas/enasic/2022/)

Documento de trabajo consultado: Protección de datos personales y seguridad de la información, Observatorio de la Economía del Cuidado CDMX, grupo 702, noviembre de 2026, pp. 2–5.

## Aviso del piloto y revisión de publicaciones

Ambas aplicaciones leen `cliente_flutter/assets/privacidad/aviso.json` y el PDF indicado en su campo `archivo`. Para incorporar retroalimentación, sustituir el PDF, actualizar título, fecha, versión y estado en el JSON y comprobar ambas descargas después de reconstruir y desplegar. Git conserva las versiones anteriores. El informe académico de Karla, «Protección de datos personales y seguridad de la información», respalda la matriz y el protocolo y se conserva en el expediente del equipo.

| Riesgo | Revisión antes de publicar | Evidencia |
| --- | --- | --- |
| Un contacto personal entra al directorio | Revisar columnas, texto libre y una muestra de fichas contra la fuente institucional. Retirar teléfonos particulares. | Fuente y versión revisadas. |
| Una captura identifica a una familia | Inspeccionar la captura completa, ocultar identificadores y revisar el resultado exportado. | Captura revisada, fecha y persona revisora. |
| Un cruce de indicadores identifica a una persona | Revisar grupos pequeños y agregar o suprimir resultados identificables. | Decisión y justificación. |
| Un resultado sintético se interpreta como reserva | Recorrer la búsqueda hasta el resultado y comprobar la leyenda. | Pantalla y versión probadas. |

En la mesa de revisión registrar responsable, hallazgo, corrección y evidencia antes de marcar el control como verificado. Si se detecta exposición, detener esa publicación, limitar el acceso, preservar evidencia restringida y escalar a quien corresponda.

**Alcance técnico revisado.** El mapa principal usa cartografía preparada. Flutter envía criterios de ejemplo a `/api/matching` y parámetros del escenario a `/api/simular` cuando se ejecutan esas acciones. Streamlit mantiene filtros y resultados de búsqueda en la sesión; su configuración desactiva el envío de estadísticas de uso de Streamlit. Los registros de alojamiento, retención y configuración de analítica de producción requieren verificación del operador.
