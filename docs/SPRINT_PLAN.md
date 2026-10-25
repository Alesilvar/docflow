# Plan de sprints

Cadencia: cuatro sprints de dos semanas, con 10–12 horas de trabajo por semana. Cada sprint termina con evidencia verificable; una funcionalidad incompleta no se considera entregada. El núcleo demostrable tiene prioridad sobre IA y alertas.

## Sprint 1 — Fundar y habilitar la búsqueda (semanas 1–2)

**Objetivo:** establecer el proyecto técnico y obtener una búsqueda reproducible desde OpenAlex.

| Trabajo | Backlog | Evidencia de cierre |
|---|---|---|
| Cerrar el alcance de portafolio | RFA-002 | PRD, plan y diseño aprobados para implementación |
| Crear esqueleto del repositorio, entorno y CI | RFA-003 | Aplicación mínima y pruebas ejecutables localmente |
| Implementar adaptador OpenAlex y búsqueda | RFA-004, RFA-005 | Casos 200, 429, timeout y abstract ausente cubiertos por pruebas |

**Demostración:** una consulta textual devuelve resultados normalizados con fuente, año, autores y enlace original.

**Fuera de este sprint:** entrevistas de usuarios, base de datos, interfaz completa, IA, automatizaciones y despliegue.

**Nota:** las entrevistas (RFA-001) se posponen como mejora opcional posterior. La demo debe presentarse como proyecto de portafolio, no como producto validado por usuarios.

## Sprint 2 — Completar el núcleo de organización (semanas 3–4)

**Objetivo:** permitir que una persona convierta resultados de búsqueda en una matriz bibliográfica exportable.

| Trabajo | Backlog | Evidencia de cierre |
|---|---|---|
| Modelo, migraciones y persistencia | RFA-006 | Migración aplicada y revertida en entorno local |
| Proyectos y artículos guardados sin duplicados | RFA-007 | CRUD y restricciones de deduplicación probados |
| Interfaz de búsqueda y guardado | RFA-008 | Flujo navegable en navegador local |
| Matriz editable y CSV | RFA-009 | Cambios manuales y caracteres UTF-8 se conservan en la exportación |

**Demostración:** crear proyecto → buscar → guardar → editar una fila → descargar CSV.

**Puerta de decisión:** si este flujo no está completo al terminar el sprint, se posponen IA y alertas para proteger la demo principal.

## Sprint 3 — Elegir una extensión de valor (semanas 5–6)

**Objetivo:** añadir una sola extensión principal sin comprometer el núcleo. La opción por defecto es IA con revisión humana; alertas pasan a ser segunda prioridad.

| Trabajo | Backlog | Evidencia de cierre |
|---|---|---|
| Spike de proveedor gratuito y modo manual | RFA-010 | Decisión documentada con costo, límites, calidad y fallback |
| Extracción desde abstracts, si el spike es viable | RFA-011 | JSON estructurado, citas de evidencia y `unknown` correctos |
| Watchlist y n8n, solo si RFA-011 se termina con margen | RFA-012, RFA-013 | Ejecución programada sin alertas duplicadas |

**Demostración por defecto:** análisis de un abstract con evidencia visible y corrección humana en la matriz.

**Regla de recorte:** si no existe una opción de IA fiable a coste cero, conservar el modo manual y documentar el resultado del spike; no reemplazarlo por una integración frágil.

## Sprint 4 — Calidad y portafolio (semanas 7–8)

**Objetivo:** convertir el producto local en una demostración honesta, reproducible y presentable.

| Trabajo | Backlog | Evidencia de cierre |
|---|---|---|
| Evaluación de búsqueda, extracción y errores | RFA-014 | Dataset, método, resultados y limitaciones documentados |
| Docker, guía de uso, demo y presentación | RFA-015 | Otra persona puede ejecutar la demo y seguir el flujo principal |

**Demostración final:** instalación local documentada, flujo completo del Sprint 2 y, si fue validada, la extensión del Sprint 3.

**No se hace en este sprint:** nuevas fuentes académicas, ranking semántico o chatbot. Corresponden a RFA-016–018 después de la demo.

## Ceremonias mínimas

- **Inicio de sprint (30 min):** confirmar objetivo, capacidad disponible, dependencias y criterio de cierre.
- **Revisión semanal (15 min):** actualizar `WORK_LOG.md`, horas reales, evidencia, riesgos y próxima tarea.
- **Cierre de sprint (30 min):** ejecutar criterios de `ACCEPTANCE_TESTS.md`, mostrar el resultado observable y decidir si se conserva o recorta alcance.

## Orden de prioridad innegociable

1. Búsqueda verificable.
2. Guardado, matriz y exportación CSV.
3. Calidad, reproducibilidad y demo.
4. IA con evidencia.
5. Alertas con n8n.
