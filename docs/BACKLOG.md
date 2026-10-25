# Backlog priorizado

**Convención:** P0 imprescindible, P1 extensión sujeta a tiempo, P2 futuro. Estado: `TODO`, `IN_PROGRESS`, `DONE`, `BLOCKED`. Una tarea se cierra solo con evidencia.

| ID | Prioridad | Tarea | Dependencia | Definición de terminado | Estado |
|---|---|---|---|---|---|
| RFA-001 | P2 | Entrevistas y comparación de 3 soluciones | — | Problema, perfil y hallazgos documentados | TODO |
| RFA-002 | P0 | Cerrar criterios de éxito MVP de portafolio | — | PRD y alcance técnico aprobados | DONE |
| RFA-003 | P0 | Esqueleto de repo, entorno y CI | RFA-002 | App mínima y tests corren localmente | DONE |
| RFA-004 | P0 | Adaptador OpenAlex con normalización | RFA-003 | Casos 200, timeout, 429, sin abstract cubiertos | DONE |
| RFA-005 | P0 | GET /papers/search | RFA-004 | Contrato, filtros y paginación comprobados | DONE |
| RFA-006 | P0 | Esquema y migraciones PostgreSQL | RFA-003 | Migración up/down verificada | DONE |
| RFA-007 | P0 | Proyectos y artículos guardados | RFA-005/006 | CRUD y deduplicación testados | IN_PROGRESS |
| RFA-008 | P0 | Interfaz buscar/guardar | RFA-005/007 | Flujo E2E navegable | IN_PROGRESS |
| RFA-009 | P0 | Matriz editable y exportación CSV | RFA-007/008 | CSV con UTF-8, escape y celdas correctas | DONE |
| RFA-010 | P0 | Spike gratuito de IA/fallback | RFA-004 | Decisión basada en límites/costo/calidad | TODO |
| RFA-011 | P0 | Extracción estructurada con evidencia | RFA-010 | `unknown` y fragmento de apoyo correctos | TODO |
| RFA-012 | P0 | Watchlists + API de novedades | RFA-007 | Consulta y deduplicación registradas | TODO |
| RFA-013 | P0 | Workflow n8n + mail de prueba | RFA-012 | Reintentos, idempotencia y logs probados | TODO |
| RFA-014 | P0 | Evaluación y reporte de límites | RFA-011/013 | Dataset y resultados reproducibles | TODO |
| RFA-015 | P0 | Docker, README, demo y presentación | RFA-014 | Otro usuario puede reproducir demo | TODO |
| RFA-016 | P1 | Semantic Scholar | RFA-005 | Evaluación comparativa de cobertura | TODO |
| RFA-017 | P1 | Ranking semántico | RFA-014 | Mejora demostrada frente a baseline | TODO |
| RFA-018 | P2 | Chatbot sobre corpus | RFA-014 | Diseño específico y evaluación | TODO |

## Inicio técnico: 5 tareas
- [x] Congelar el MVP de portafolio y registrar la decisión (RFA-002).
- [ ] Crear estructura de backend y frontend.
- [ ] Configurar entorno local, variables de ejemplo y pruebas mínimas.
- [ ] Implementar una ruta de estado de la API y verificarla.
- [ ] Preparar CI para ejecutar las pruebas.

RFA-001 se conserva como mejora opcional posterior; no bloquea el desarrollo del MVP de portafolio.
