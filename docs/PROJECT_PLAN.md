# Plan de proyecto — ResearchFlow AI

## 1. Identificación

| Elemento | Definición |
|---|---|
| Proyecto | ResearchFlow AI |
| Propósito | Crear una aplicación local que ayude a descubrir, organizar y revisar literatura académica multidisciplinaria. |
| Prioridad | Portafolio profesional y aprendizaje aplicado. |
| Duración estimada | 8 semanas. |
| Dedicación | 10–12 horas por semana (80–96 horas estimadas). |
| Presupuesto | S/ 0 para el MVP local. |
| Responsable | Una persona desarrolladora. |

## 2. Problema y justificación

Una revisión bibliográfica exige buscar fuentes, seleccionar artículos, ordenar metadatos, registrar notas y seguir publicaciones recientes. Estas actividades suelen estar repartidas entre buscadores, hojas de cálculo y herramientas separadas. ResearchFlow AI busca centralizar el flujo mínimo de investigación sin afirmar conclusiones que no estén respaldadas por el abstract disponible.

El proyecto se justifica como pieza de portafolio porque combina consumo de APIs, backend, persistencia, interfaz web, pruebas, automatización y uso responsable de IA, manteniendo un problema concreto y demostrable.

## 3. Objetivo general

Diseñar e implementar un MVP local que permita crear un proyecto de investigación, buscar artículos académicos en OpenAlex, guardarlos sin duplicados, organizarlos en una matriz editable y exportar los resultados a CSV.

## 4. Objetivos específicos

1. Integrar una búsqueda textual multidisciplinaria basada en OpenAlex.
2. Persistir proyectos y artículos, garantizando deduplicación.
3. Ofrecer una matriz bibliográfica editable y una exportación CSV fiable.
4. Evaluar una extracción asistida desde abstracts solo si existe una alternativa gratuita y verificable.
5. Documentar instalación, pruebas, decisiones y limitaciones para una demostración reproducible.

## 5. Alcance

### Incluido en el MVP

- Proyectos de investigación locales para un único usuario.
- Búsqueda por texto y rango de años en OpenAlex.
- Visualización de título, autores, año, URL, fuente y abstract cuando esté disponible.
- Guardado de artículos en proyectos sin duplicación.
- Matriz de literatura editable.
- Exportación de la matriz a CSV con UTF-8.
- Manejo controlado de errores de la fuente externa.
- Pruebas automatizadas esenciales y documentación de ejecución local.

### Condicional

- Extracción de objetivo, metodología, hallazgos y limitaciones desde abstracts, con evidencia textual y revisión humana.
- Watchlists y alertas locales mediante n8n; solo si el núcleo ya está finalizado y existe capacidad disponible.

### Excluido

- Lectura y análisis de PDF completo.
- Chatbot, recomendaciones, embeddings o ranking semántico.
- Colaboración, cuentas, multitenencia o despliegue público.
- Búsqueda federada en múltiples fuentes para el MVP.
- Envíos reales a terceros sin autorización expresa.

## 6. Entregables

| Entregable | Criterio de aceptación |
|---|---|
| Alcance de portafolio | MVP, plan y diseño aprobados; no se presenta como producto validado por usuarios. |
| API de búsqueda | Búsqueda funcional con respuestas normalizadas y manejo de error. |
| Persistencia | Migraciones y deduplicación verificadas. |
| Interfaz MVP | Flujo crear proyecto → buscar → guardar → editar matriz → exportar CSV. |
| Extensión de IA, si procede | Campos estructurados con evidencia o `unknown`; modo manual disponible. |
| Documentación y demo | Instalación local, pruebas y límites claramente explicados. |

## 7. Plan de trabajo por sprints

| Sprint | Semanas | Objetivo | Resultado verificable |
|---|---:|---|---|
| 1 | 1–2 | Fundar el proyecto y habilitar búsqueda | Estructura ejecutable, API OpenAlex y pruebas de adaptación. |
| 2 | 3–4 | Construir el núcleo de organización | Flujo completo de búsqueda, guardado, matriz y CSV. |
| 3 | 5–6 | Incorporar una extensión de valor | IA con evidencia; alertas únicamente si hay margen. |
| 4 | 7–8 | Asegurar calidad y preparar portafolio | Evaluación, documentación, contenedor y demo reproducible. |

La planificación operativa, las tareas y las puertas de decisión se mantienen en `SPRINT_PLAN.md` y `BACKLOG.md`.

## 8. Recursos y tecnología

| Área | Propuesta | Propósito |
|---|---|---|
| Frontend | React + TypeScript | Interfaz de búsqueda y matriz. |
| Backend | Python + FastAPI | API, validación y reglas de negocio. |
| Datos | PostgreSQL + Alembic | Persistencia, integridad y migraciones. |
| Fuente académica | OpenAlex | Metadatos y abstracts disponibles. |
| Automatización | n8n local | Programación de alertas, si se implementa. |
| Entorno | Docker Compose | Reproducibilidad local. |
| Calidad | Pytest, pruebas de API y GitHub Actions | Verificación automatizada. |

## 9. Riesgos y respuestas

| Riesgo | Probabilidad | Impacto | Respuesta |
|---|---|---|---|
| Alcance excesivo | Alta | Alto | Proteger el flujo principal y postergar IA/alertas. |
| Límites o cambios de servicios gratuitos | Media | Alto | Verificar antes del uso; ofrecer modo manual y ejecución local. |
| Datos incompletos de OpenAlex | Alta | Medio | Mostrar ausencia de abstract como información desconocida. |
| Extracción de IA no fiable | Media | Alto | Exigir evidencia, `unknown` y revisión humana. |
| Tiempo disponible menor al previsto | Media | Alto | Reducir extensiones, no calidad del núcleo. |
| Duplicados en alertas | Media | Medio | Idempotencia y fuente de verdad en PostgreSQL. |

## 10. Calidad y aceptación final

El proyecto se considera terminado cuando una persona puede seguir la guía local, crear un proyecto, buscar artículos, guardar resultados, modificar la matriz y exportar un CSV correcto. Deben existir pruebas para integración OpenAlex, errores previsibles, deduplicación y exportación. Toda capacidad de IA debe identificar el alcance del texto analizado y proporcionar evidencia o marcar el dato como desconocido.

## 11. Seguimiento

- Registrar semanalmente horas, evidencia, riesgos y siguiente tarea en `WORK_LOG.md`.
- Cerrar tareas solo contra los criterios de `ACCEPTANCE_TESTS.md`.
- Registrar cambios de arquitectura o alcance en `DECISIONS.md`.
- Solicitar aprobación antes de gastos, despliegue público, borrados o envíos reales a terceros.
