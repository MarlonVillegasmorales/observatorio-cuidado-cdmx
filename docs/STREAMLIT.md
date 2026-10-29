# Despliegue en Streamlit Community Cloud

## Permisos comprobados

Al preparar esta migración, GitHub reportó push=true y admin=false para la
conexión usada en KarlaKsanova/ECONOMIA-DEL-CUIDADO. El repositorio pertenece
a una cuenta personal. Ser colaborador permite aportar código; el despliegue
inicial de Community Cloud exige permisos de administración.

El repositorio de trabajo para esta copia es
`MarlonVillegasmorales/observatorio-cuidado-cdmx`. El repositorio original se
conserva como `upstream`:
`KarlaKsanova/ECONOMIA-DEL-CUIDADO`. Los cambios deben publicarse en `origin`;
no se debe hacer push a `upstream`.

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

- Repositorio no disponible o error de permisos: verificar cuenta GitHub
  vinculada, propietario y permiso admin; no modificar Python para resolverlo.
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
