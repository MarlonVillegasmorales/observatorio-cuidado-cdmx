# API mínima del observatorio

La API separa transporte HTTP de las reglas de negocio. Matching y simuladores
usan los servicios existentes en `cuidado/services`.

## Ejecutar localmente

```powershell
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```

Health: `GET /api/health`

## Matching

`POST /api/matching`

```json
{
  "tipo": "infantil",
  "inicio": "09:00",
  "fin": "12:00",
  "dias": ["lun", "mar"],
  "radio_km": 10
}
```

Devuelve resultados explicables del servicio sintético y conserva motivos como
`compatible`, `sin_servicio_compatible`, `sin_compatibilidad_horaria`,
`fuera_de_radio` y `sin_cupo`.

## Simulador

`POST /api/simular`

Acepta las entradas numéricas validadas por el simulador canónico. Un
`costo_intervencion` ausente produce `beneficio_neto: null`; no se convierte en
ahorro cero.

## CORS y despliegue

La URL de Flutter se configura con `--dart-define=OBSERVATORIO_API_URL=<URL>`.
Los orígenes se separan con una variable `OBSERVATORIO_CORS_ORIGINS`.

`Dockerfile.api` prepara un contenedor Python. No existe un destino público
autorizado para este backend en la infraestructura disponible, por lo que
Flutter no se publica con una URL pública inexistente.
