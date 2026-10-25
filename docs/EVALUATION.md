# Plan de evaluación

## Preguntas
- ¿Ayuda el producto a encontrar y organizar literatura más rápidamente que un flujo manual?
- ¿Con qué frecuencia la extracción asistida por IA contiene afirmaciones no respaldadas?
- ¿Con qué frecuencia las alertas duplican o pierden novedades?

## Línea base
Usar búsqueda directa OpenAlex + organización manual. Para ranking, usar el orden de OpenAlex antes de introducir un reranker.

## Conjuntos de prueba
- 10 consultas de al menos 3 disciplinas (propuesta ajustable) y artículos etiquetados por dos evaluadores cuando sea viable.
- 30 abstracts heterogéneos y algunos registros sin abstract para evaluar extracción.
- 10 escenarios automatizados de fallos/reintentos/deduplicación.

## Métricas
- Relevancia: Precision@10; NDCG@10 solo si hay etiquetas ordinales fiables; no reportar recall sin universo de relevantes definido.
- Extracción: exactitud por campo, tasa de afirmaciones sin evidencia, tasa de `unknown` correcto, concordancia de evaluadores.
- Operación: latencia p50/p95 (si volumen permite), errores, solicitudes API, consumo/costo, duplicados de alertas.
- UX: finalización de tareas y tiempo de búsqueda → matriz → exportación con usuarios piloto.

## Reporte
Describir muestra, fechas, método de anotación, intervalos de incertidumbre cuando se justifique, sesgos, ejemplos de errores y límites de generalización. Nunca presentar métricas objetivo como resultados obtenidos.
