# ResearchFlow AI

Aplicación web para descubrir, organizar y analizar literatura científica de distintas disciplinas. Está diseñada como un proyecto de portafolio con una demostración local, reproducible y honesta sobre sus límites.

> **Estado:** Sprint 1 — preparación técnica. **Prioridad:** portafolio profesional. **Dedicación:** 10–12 h/semana. **Presupuesto:** S/ 0. **Última actualización:** 2026-10-25.

## Estado del proyecto

| Área | Estado |
|---|---|
| Plan, análisis y diseño | Listos |
| Repositorio Git local | Inicializado; remoto configurado |
| Backend y frontend | Pendientes de implementación |
| Búsqueda OpenAlex | Pendiente de implementación |
| Base de datos, matriz y CSV | Pendientes de implementación |
| IA y alertas | Extensiones opcionales, posteriores al núcleo |

### Siguiente hito

Crear la estructura ejecutable del backend y frontend, configurar pruebas mínimas y exponer una ruta de estado de la API. Consulta `docs/BACKLOG.md` (RFA-003) para el criterio de terminado.

## Resultado demostrable

El MVP permite crear un proyecto de investigación, buscar publicaciones académicas en OpenAlex, revisar resultados, guardar artículos, corregir una matriz de literatura y exportarla a CSV. El análisis asistido por IA y las alertas con n8n se incorporarán solo si el núcleo está terminado y su viabilidad sin costo queda comprobada.

## Principios
- Multidisciplinario desde el MVP: búsquedas por texto libre; nunca codificar categorías propias de CS.
- No atribuir al texto completo lo inferido únicamente del abstract.
- Primero establecer una línea base sin IA; el proveedor de IA gratuito y fiable se decidirá tras un spike.
- S/ 0 **sin suponer** que los límites gratis de terceros permanezcan estables.
- Mantener secretos fuera del repositorio, controlar cuotas y proteger datos.
- Alcance de una sola persona: entregar verticales funcionales, recortar antes que acumular deuda.

## Cómo se construirá

1. Seguir las tareas en orden desde `docs/BACKLOG.md`.
2. Usar `docs/SPRINT_PLAN.md` para proteger el alcance del MVP.
3. Cerrar cada tarea contra `docs/ACCEPTANCE_TESTS.md` con evidencia real.
4. Registrar decisiones, avances y riesgos en `docs/DECISIONS.md` y `docs/WORK_LOG.md`.

## Estructura
- `PROJECT_INSTRUCTIONS.md`: instrucciones para ChatGPT Project y Work.
- `docs/PRD.md`: producto, usuario y alcance.
- `docs/PROJECT_PLAN.md`: plan formal, alcance, recursos, riesgos y entregables.
- `docs/ANALYSIS_AND_DESIGN.md`: análisis funcional y diseño técnico del sistema.
- `docs/ARCHITECTURE.md`: diseño técnico.
- `docs/BACKLOG.md`: tareas priorizadas.
- `docs/ROADMAP.md`: cronograma y hitos.
- `docs/SPRINT_PLAN.md`: objetivos, entregables y recortes por sprint.
- `docs/DATA_MODEL.md`, `docs/API_SPEC.md`: contratos y persistencia.
- `docs/AI_POLICY.md`, `docs/EVALUATION.md`: guardrails y métricas.
- `docs/N8N_AUTOMATIONS.md`: automatizaciones.
- `docs/ACCEPTANCE_TESTS.md`, `docs/SECURITY.md`: calidad y seguridad.
- `docs/DECISIONS.md`, `docs/WORK_LOG.md`: decisiones y continuidad.

## Estado actual
No existe aún implementación de la aplicación. Todos los endpoints, componentes y estructuras descritos en la documentación son propuestas hasta que se implementen y prueben.

## Mantenimiento de esta guía

Este README se actualizará en cada avance relevante: cambio de sprint, funcionalidad terminada, requisito modificado, decisión técnica importante o nueva forma de ejecutar el proyecto. El historial detallado se conserva en `docs/WORK_LOG.md`.
