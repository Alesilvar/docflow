# Product Requirements Document (PRD)

## Problema e hipótesis
Quienes revisan literatura académica invierten tiempo en búsquedas, selección, extracción, organización y seguimiento. **Hipótesis**: una herramienta que combina APIs verificables, IA con evidencia y automatizaciones disminuye el trabajo manual sin degradar la calidad.

## Usuario y alcance
**Usuario primario:** estudiante universitario de cualquier disciplina que prepara una revisión bibliográfica o proyecto. **MVP:** un usuario sin colaboración; búsqueda multidisciplinaria por consulta textual. **No promete** cubrir todas las fuentes académicas.

## Jobs to be done
1. Encontrar artículos candidatos sobre una pregunta o tema.
2. Revisar metadatos y resúmenes de manera eficiente.
3. Guardar artículos en un proyecto y construir una matriz editable.
4. Exportar el trabajo y detectar nuevas publicaciones.

## Historias y criterios de valor
- US-01: Buscar por palabra/frase y filtrar por años; recibir lista con fuente y URL original.
- US-02: Guardar en proyecto sin duplicados; poder quitar y revisar registros.
- US-03: Extraer de abstracts disponibles objetivos, enfoque, hallazgos y límites **solo cuando estén explícitos**; indicar `unknown` en lo demás.
- US-04: Corregir manualmente una matriz y exportar CSV de manera fiel.
- US-05: Crear una watchlist y recibir alertas de nuevas publicaciones sin duplicados.

## Requisitos no funcionales
- Despliegue reproducible localmente; presupuesto de operación de S/ 0.
- Errores comprensibles y estados vacíos bien definidos.
- Seguridad básica de secretos y datos; trazabilidad de ejecuciones.
- Tests automatizados para adaptador OpenAlex, API, deduplicación y exportación.
- Accesibilidad básica de UI: navegación por teclado, labels, contraste, mensajes de error.

## Fuera de alcance del MVP
Chatbot conversacional, lectura de PDF completo, búsqueda federada multi-API, colaboración, cuentas multitenant, embeddings propios, recomendaciones avanzadas, redacción automática de papers, publicación científica.

## Validación temprana
Entrevistar 3–5 potenciales usuarios; medir qué pasos actuales causan fricción y comparar al menos 3 alternativas existentes. Decidir si se mantiene la propuesta antes de ampliar UI.

## Métricas del MVP
Tasa de flujos completos en prueba con 3 usuarios; porcentaje de campos de IA respaldados por fragmentos verificables; errores y duplicados en alertas; tiempo total de tarea contra proceso manual en una pequeña prueba exploratoria. No establecer umbrales artificiales sin línea base.
