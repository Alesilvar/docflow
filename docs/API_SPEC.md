# API REST propuesta — v1

Base path: `/api/v1`. Contratos sujetos a evolución antes del código.

| Método | Ruta | Uso |
|---|---|---|
| GET | `/papers/search?query=...&from_year=2022&to_year=2026&page=1` | Buscar en OpenAlex |
| GET | `/papers/{id}` | Ver papel persistido |
| POST | `/projects` | Crear proyecto |
| GET | `/projects` | Listar proyectos |
| POST | `/projects/{id}/papers` | Guardar artículo |
| GET | `/projects/{id}/papers` | Listar matriz |
| PATCH | `/projects/{id}/papers/{paper_id}` | Editar notas/campos revisados |
| GET | `/projects/{id}/export.csv` | Exportar CSV |
| POST | `/papers/{id}/analyze` | Analizar abstract disponible |
| POST | `/watchlists` | Crear seguimiento |
| POST | `/internal/watchlists/check` | Ejecución autenticada desde n8n |

## Respuesta de búsqueda ejemplo (datos ficticios)
```json
{
  "items": [{
    "openalex_id": "https://openalex.org/W0000000000",
    "title": "Example title",
    "year": 2024,
    "authors": ["Example Author"],
    "doi": null,
    "abstract": null,
    "source_url": "https://openalex.org/W0000000000"
  }],
  "page": 1,
  "has_next": false,
  "total_count": 1
}
```

## Errores y validaciones
`400` consulta/filtros inválidos; `404` inexistente; `409` duplicado manejado; `429` límite de frecuencia; `503` dependencia upstream no disponible; `504` timeout upstream; `500` error interno sin secretos. Usar respuestas JSON consistentes con `error.code`, `message`, `request_id`.

## Seguridad
Proteger `/internal/*` con token o autenticación de servicio y mínimo privilegio. No exponer API keys ni configuración de proveedor al cliente.
