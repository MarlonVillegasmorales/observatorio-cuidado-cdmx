# Análisis del problema prototípico

## A. Identificación y método de lectura

**Título:** *Problema prototípico: Observatorio de datos para el diseño de
programas de innovación social en la economía del cuidado*. **Institución:**
Universidad Nacional Rosario Castellanos (UNRC), Gobierno de México /
Secretaría de Ciencia y Tecnología. **Programa y periodo:** Licenciatura en
Ciencias de Datos para los Negocios, 7.º semestre, 2026-2. **Fecha visible:**
2026-2. El archivo local tiene 18 páginas y metadatos de creación del 8 de
septiembre de 2026; se usa la numeración impresa del PDF.

El PDF está escaneado. Las páginas citadas fueron comprobadas visualmente; no
se presentan como transcripción automática. Las comillas indican el texto
visible del documento; las paráfrasis e interpretaciones del equipo se
identifican como tales. Las referencias a cifras de ENASIC, ENUT o trabajo no
remunerado se mantienen como fuentes del PDF, no como mediciones propias de
este repositorio.

## B. Problema central

El documento define el cuidado como actividades, relaciones, servicios y
recursos para atender necesidades físicas, emocionales y cotidianas, y señala
que se realiza en hogares, comunidades, instituciones y mercado. Explica que
se distribuye de forma desigual por género, edad, condición socioeconómica,
discapacidad, territorio y disponibilidad de servicios (p. 1).

La justificación sostiene que la información está fragmentada entre hogares,
instituciones, organizaciones y fuentes de datos. Esa fragmentación dificulta
identificar quién necesita cuidado, quién lo proporciona, qué servicios están
disponibles, dónde hay brechas y cuáles son sus costos sociales y económicos
(p. 2). El problema incluye pobreza de tiempo, barreras para empleo,
educación y participación social, y diferencias en la posibilidad de resolver
necesidades de cuidado (p. 2).

La respuesta académica no es “hacer una aplicación”: propone un observatorio
que integre, organice, analice y visualice información para producir
hallazgos, y desde ellos un programa de innovación social (p. 3). Las
consecuencias para cuidadoras y receptoras deben analizarse con población,
ámbito, año y fuente explícitos. El repositorio todavía no demuestra una
medición propia de impacto social, empleo o tiempo liberado.

## C. Caso didáctico: Renata y “Manos que Cuidan”

El caso pertenece a la UCA de Práctica Profesional I; no describe un
participante real de este repositorio.

- **Protagonista e institución:** Renata realiza su práctica profesional y
  debe entregar a una institución un diagnóstico y plan acotado (pp. 8–10).
  “Manos que Cuidan” aparece como el proyecto comunitario/caso de referencia,
  no como convenio de nuestro equipo.
- **Necesidad y diagnóstico:** Renata realiza diagnóstico social y análisis
  FODA. El diagnóstico indica que el problema principal no es solo la falta de
  personas, sino la ausencia de un mecanismo confiable para vincular oferta
  disponible con familias que requieren cuidado (p. 9).
- **Intervención didáctica:** se plantea un piloto con dos colonias, 15
  familias y 6 cuidadoras disponibles; esos números son del caso, no del
  observatorio (p. 9).
- **Restricciones y dilema:** la coordinación pide conectar de inmediato con
  187 familias registradas, pero ampliar el alcance comprometería calidad del
  registro y verificación. En la semana 8 se reportan 4 vinculaciones exitosas
  de 15 solicitudes y 2 incidencias por datos incompletos; son resultados
  narrados del caso didáctico, no resultados de este proyecto (p. 9).
- **Decisión:** comunicar resultados parciales con honestidad y defender un
  alcance delimitado, sin generar expectativas que la práctica no pueda
  sostener (pp. 9–10).

La adaptación del equipo cambia el énfasis de perfiles individuales a
vinculación institucional con centros comunitarios. Los perfiles “Necesito
cuidado” y “Puedo cuidar” son orientaciones funcionales del PDF (p. 5), no
una autorización para operar un mercado informal ni una base de personas.

## D. Objetivos académicos verificados

El objetivo general visible es: **“Diseñar y validar un Observatorio de Datos
que genere inteligencia para comprender la economía del cuidado y sustente el
desarrollo de un programa prototípico de innovación social orientado a
vincular necesidades de cuidado con servicios, personas u organizaciones,
mediante analítica, herramientas avanzadas, protección responsable de datos y
evaluación de impacto”** (p. 4).

Los objetivos específicos visibles son:

1. Analizar las necesidades y brechas de la economía del cuidado mediante
   datos e indicadores para generar evidencia útil en la toma de decisiones
   (p. 4).
2. Diseñar una intervención de innovación social basada en evidencia, evaluar
   sus posibles resultados y oportunidades de mejora (p. 4).

Su relación con el proyecto es:

| Eje académico | Interpretación delimitada |
|---|---|
| Observatorio | Integrar fuentes, indicadores, visualizaciones y metadatos; no solo almacenar datos. |
| Brechas | Comparar necesidades y recursos con unidades y limitaciones explícitas. |
| Programa social | Derivar una intervención de hallazgos; si no son suficientes, mantenerla como propuesta. |
| Técnicas avanzadas | Evaluar clasificación, predicción, recomendación, matching u optimización solo cuando el problema, las métricas y los datos lo permitan (pp. 16–17). |
| Protección | Minimizar, clasificar, proteger y gobernar datos desde el diseño (pp. 13–15). |
| Evaluación y documentación | Separar funcionamiento, desempeño, usabilidad, piloto e impacto; documentar método y límites. |

## E. Objetivos operativos adoptados

| Objetivo | Resultado esperado | Evidencia y dependencia | Límite actual |
|---|---|---|---|
| Integrar fuentes pertinentes para CDMX | Dataset territorial trazable para 16 alcaldías | ETL, GeoParquet, metadata y calidad; depende de confirmar procedencia y comparabilidad | No convierte estimaciones en observaciones. |
| Analizar necesidades y brechas | Indicadores interpretables con fuente, año, población y unidad | `cuidado/services/evidencia.py` y datos preparados; depende de auditoría de indicadores | No prueba causalidad ni abandono laboral. |
| Ofrecer observatorio accesible | Tareas de consulta en Streamlit para computadora y celular | `cuidado/ui/app.py` y AppTest local; depende de evaluación completa de accesibilidad | No hay validación con usuarios ni despliegue comprobado. |
| Explorar vinculación con centros | Recomendaciones explicables y separadas de confirmación | `cuidado/domain/centros.py`, simulación y pruebas; depende de centros verificados y piloto | Es sintético, greedy y usa distancia geográfica. |
| Diseñar intervención social | Propuesta derivada de un hallazgo priorizado | Programa social del PDF, pp. 5 y 8–10; depende de diagnóstico y actores reales | Iztapalapa es propuesta, no intervención ejecutada. |
| Definir protección y seguimiento | Protocolo de datos, roles, retención e incidencias | Contratos y requisitos del PDF, pp. 13–15; depende de revisión jurídica e institucional | No se afirma cumplimiento legal completo. |
| Explorar B2B/B2G | Escenarios con supuestos y fuentes explícitos | Contratos y pendientes de Azael; depende de entregas y métodos validados | No hay resultados financieros verificables. |

## F. Correspondencia entre documento y propuesta

| ID | Planteamiento del PDF | Página | Tipo | Respuesta del proyecto | Evidencia necesaria |
|---|---|---:|---|---|---|
| A-01 | Observatorio para integrar necesidades, oferta, demanda y brechas | 3–4 | Requisito académico | ETL, indicadores y cuatro tareas de consulta | Auditoría de fuentes y validación con usuarios |
| A-02 | Vincular cuidado con servicios, personas u organizaciones | 4–5 | Requisito académico | Adaptación hacia centros comunitarios verificados | Contratos, centros, autorización y piloto |
| A-03 | Perfiles “Necesito cuidado” y “Puedo cuidar” | 5 | Orientación didáctica | Se refleja como necesidad/oferta sintética, no como bolsa laboral | Validación docente y reglas de protección |
| A-04 | Programa derivado de un hallazgo | 5, 8–10 | Requisito académico | Iztapalapa queda como piloto propuesto | Diagnóstico, población, institución y seguimiento |
| A-05 | Analítica, matching, predicción u optimización con validación | 16–17 | Orientación técnica | Matching explicable greedy, no entrenado | Comparación experimental, cobertura y errores |
| A-06 | Proteger datos desde diseño y gobernar su ciclo | 13–15 | Requisito académico | Demo sin datos personales; protocolo pendiente | Dictamen, matriz de riesgos y controles |
| A-07 | Escenarios de valor compartido y decisiones empresariales | 11–13 | Orientación de UCA | B2B/B2G son decisiones de la propuesta, no requisito textual obligatorio | Datos, supuestos, responsables y validación |
| A-08 | Observar, proteger, analizar, comprender, modelar, intervenir, evaluar y documentar | 18 | Ruta integradora | Estructura documentación y matriz de avance | Entregables de todas las UCA |

Las adaptaciones hacia centros comunitarios y B2B/B2G son decisiones del
equipo; el PDF permite servicios, personas u organizaciones, pero no impone
estas etiquetas. La validación docente de esas adaptaciones está pendiente.

## G. Programa de innovación social

Debe construirse después de priorizar un hallazgo del observatorio. La
propuesta vigente es un piloto territorial delimitado en Iztapalapa, sujeto a
validación. Su población objetivo serían familias con necesidades de cuidado y
centros comunitarios verificados, con criterios de acceso, consentimiento,
capacidad y no discriminación por definir con la institución.

El diseño deberá especificar necesidad priorizada, actores (familias,
centros, comunidad, instituciones y, si procede, empresas), flujo de
solicitud–recomendación–confirmación, recursos, sostenibilidad, verificación,
incidencias, seguimiento y evaluación. La solución técnica no sustituye la
evidencia para justificar la intervención. Sin hallazgo y población real
suficientes, el programa permanece como propuesta pendiente.

## H. Aportación de las UCA

El PDF articula: Práctica Profesional I, Inteligencia de Negocios, Seminario
de Titulación I, Analítica para los Negocios, Leyes para la Protección de
Datos y Herramientas y Técnicas Avanzadas para Ciencia de Datos (p. 1).

| UCA | Aportación indicada | Evidencia requerida |
|---|---|---|
| Práctica Profesional I | Diagnóstico situado, priorización, intervención y seguimiento | Diagnóstico, plan acotado, bitácora y evaluación (pp. 8–10) |
| Inteligencia de Negocios | KPIs operativos, sociales y de sostenibilidad para decisiones | Mapa de objetivos, indicadores, visualizaciones y hallazgos (pp. 7–8) |
| Seminario de Titulación I | Problematización, metodología, resultados y escritura | Informe académico con límites y líneas de continuidad (p. 10) |
| Analítica para los Negocios | Exploración, segmentación, patrones, relaciones y evaluación de demanda/oferta | Reporte analítico y hallazgos priorizados (p. 6) |
| Leyes para la Protección de Datos | Base jurídica, minimización, seguridad, anonimización y gobernanza | Dictamen, protocolo, matriz de riesgos y ciclo de datos (pp. 13–16) |
| Herramientas y Técnicas Avanzadas | Selección, implementación y validación de matching, predicción u optimización | Modelo documentado, métricas, errores, cobertura y diferencias (pp. 6 y 16–18) |

No se inventan ponderaciones ni acuerdos docentes. El PDF contiene una rúbrica
general orientativa y aclara que puede adaptarse a las UCA (pp. 6–7).

## I. Evaluación y entregables

Debe distinguirse:

- **Software:** ejecución, navegación y errores; las pruebas locales muestran
  comportamiento sintético.
- **Algoritmo:** compatibilidad, errores, capacidad, cobertura,
  explicabilidad y diferencias territoriales; aún falta comparación
  experimental.
- **Usabilidad y accesibilidad:** tareas, lenguaje, teclado, foco, contraste,
  ampliación y alternativas; no están validados con usuarios.
- **Piloto:** participantes, seguimiento, incidencias y resultados operativos;
  no existe en el repositorio.
- **Impacto social:** requiere diseño de evaluación, referencia y seguimiento;
  una prueba sintética o comparación simple antes/después no demuestra
  causalidad.

El PDF solicita observatorio documentado, programa social, protocolo de
protección y gobernanza, piloto de práctica profesional, informe académico,
presentación y demostración (pp. 4–5, 8–10, 13–16 y 18). El producto final
resumido es “Observatorio funcional + Programa social basado en la evidencia”
(p. 18). En este repositorio solo hay evidencia local de partes del
observatorio y documentación técnica; el resto está pendiente.
