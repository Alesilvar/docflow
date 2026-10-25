# Automatizaciones n8n

## Flujo A: Alertas de publicaciones (MVP)
1. `Schedule Trigger` (semanal al principio, configurable).
2. `HTTP Request` al backend interno protegido: obtener watchlists activas.
3. `HTTP Request` al endpoint de revisión de novedades / o una llamada por watchlist.
4. `IF` si existen registros nuevos y válidos.
5. Preparar resumen y enviar email de prueba al usuario autorizado.
6. Registrar resultado por artículo y watchlist para evitar duplicados.

## Idempotencia y fallos
La fuente de verdad de `seen_watchlist_papers` y `notification_events` es PostgreSQL, no n8n. Al reintentar, comprobar estado; almacenar idempotency key `watchlist_id:paper_id:channel`. Distinguir pendiente, enviado, fallido y reintento. Evitar pérdida de eventos si el envío y la actualización de base de datos fallan entre sí; documentar semántica de entrega (at least once y deduplicación lógica).

## Desarrollo S/ 0
Iniciar n8n local en Docker. No garantizar funcionamiento continuo si la máquina está apagada. Usar correos propios de prueba; solicitar autorización antes de mensajes a terceros. No exportar credenciales junto al workflow.

## Entregables
`automations/watchlist-alerts.json` solo después de implementación; capturas de pruebas y registro de ejecución.
