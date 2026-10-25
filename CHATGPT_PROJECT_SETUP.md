# Configurar un Proyecto en ChatGPT y trabajar con Work

1. Crea un Proyecto llamado **ResearchFlow AI** en ChatGPT.
2. Copia el contenido de `PROJECT_INSTRUCTIONS.md` en las instrucciones del Proyecto, si tu interfaz permite instrucciones personalizadas; si no, adjunta el archivo y úsalo como referencia inicial.
3. Agrega `README.md` y los archivos de `docs/` como material de contexto. Según límites de adjuntos, puedes subir primero README, PRD, BACKLOG, DECISIONS y WORK_LOG, y después el resto.
4. Al iniciar una conversación nueva dentro del Proyecto, escribe: **«Lee PROJECT_INSTRUCTIONS.md, PRD.md, BACKLOG.md, DECISIONS.md y WORK_LOG.md. Propón el próximo paso sin escribir código todavía.»**
5. Usa **Work** para tareas con inspección de repositorio, edición de múltiples archivos, ejecución de comandos, pruebas y preparación de artefactos. Antes de pedir ediciones, asegúrate de que tenga acceso al repositorio o adjunta los archivos pertinentes.
6. Después de cada sesión, solicita actualizar `docs/WORK_LOG.md` y las tareas del backlog para mantener continuidad.
7. No asumas que adjuntar documentación a ChatGPT sincroniza cambios automáticamente con GitHub; mantén el repositorio como fuente de verdad del código y sincroniza los Markdown cuando se modifiquen.

## Primer prompt recomendado
> Trabajemos ResearchFlow AI en modo planificación. Revisa los Markdown del proyecto, detecta contradicciones o riesgos y guía la tarea RFA-001 de validación del problema. Prioriza empleabilidad, costo S/ 0, 10–12 horas semanales y búsqueda multidisciplinaria. No implementes nada todavía. Registra decisiones nuevas y preguntas imprescindibles.
