# Work log — continuidad entre sesiones

## 2026-10-25 — Planificación
- **Decisiones del usuario:** 10–12 h/semana; empleabilidad/portafolio; S/ 0; alcance multidisciplinario.
- **Hecho:** paquete documental inicial (plan y contratos propuestos, sin implementación).
- **Pruebas ejecutadas:** ninguna; no existe aún código aplicativo.
- **Bloqueos:** validar problema con usuarios; confirmar proveedor gratuito de IA; revisar límites vigentes de APIs.
- **Próximo paso:** RFA-001 — entrevistas rápidas y análisis comparativo de soluciones existentes.

## 2026-10-25 — Organización de ejecución
- **Objetivo:** convertir el roadmap semanal en entregas controlables para una persona.
- **Cambios/archivos:** añadido `docs/SPRINT_PLAN.md`; actualizado `docs/ROADMAP.md` y `README.md`.
- **Evidencia y comandos de prueba:** revisión documental; no existe código aplicativo que probar.
- **Decisiones:** cuatro sprints de dos semanas; el núcleo búsqueda → guardar → matriz → CSV tiene prioridad. IA es la extensión preferida y alertas solo se abordan si existe margen.
- **Riesgos/bloqueos:** siguen pendientes las entrevistas, la validación de límites de OpenAlex y el spike de IA.
- **Próxima tarea (ID):** RFA-001.

## 2026-10-25 — Documentación formal del proyecto
- **Objetivo:** consolidar el plan y el análisis/diseño para orientar la implementación y servir como evidencia de portafolio.
- **Cambios/archivos:** añadidos `docs/PROJECT_PLAN.md` y `docs/ANALYSIS_AND_DESIGN.md`; actualizado `README.md`.
- **Evidencia y comandos de prueba:** revisión de consistencia documental; no existe código aplicativo que probar.
- **Decisiones:** el núcleo sigue siendo búsqueda, organización y exportación; IA y alertas permanecen condicionales.
- **Riesgos/bloqueos:** validar problema, límites de proveedores y viabilidad de IA gratuita.
- **Próxima tarea (ID):** RFA-001.

## 2026-10-25 — Cambio de enfoque a portafolio
- **Objetivo:** eliminar la validación con entrevistas como requisito previo de desarrollo.
- **Cambios/archivos:** actualizados `BACKLOG.md`, `DECISIONS.md`, `SPRINT_PLAN.md` y `PROJECT_PLAN.md`.
- **Evidencia y comandos de prueba:** decisión explícita del responsable del proyecto.
- **Decisiones:** RFA-001 pasa a prioridad P2 y deja de bloquear el MVP; RFA-002 se completa como definición del alcance de portafolio.
- **Riesgos/bloqueos:** no se podrá afirmar validación de mercado o de usuarios en la presentación; quedan por validar límites de OpenAlex e IA.
- **Próxima tarea (ID):** RFA-003 — esqueleto de repositorio, entorno y CI.

## 2026-10-25 — README como guía viva
- **Objetivo:** convertir el README en una portada clara para el repositorio de portafolio.
- **Cambios/archivos:** actualizado `README.md` con estado, siguiente hito y política de mantenimiento.
- **Evidencia y comandos de prueba:** revisión de contenido Markdown; no existe código aplicativo que probar.
- **Decisiones:** el README se actualizará con cada avance relevante y `WORK_LOG.md` conservará el detalle histórico.
- **Riesgos/bloqueos:** ninguno nuevo.
- **Próxima tarea (ID):** RFA-003 — esqueleto de repositorio, entorno y CI.

## 2026-10-25 — Flujo de control de versiones
- **Objetivo:** conservar avances verificables en GitHub durante el desarrollo.
- **Cambios/archivos:** actualizado `PROJECT_INSTRUCTIONS.md` con el flujo de commits y publicación remota.
- **Evidencia y comandos de prueba:** commit inicial local creado: `65ffeca`.
- **Decisiones:** realizar commits pequeños y descriptivos al finalizar avances relevantes; subirlos al remoto cuando estén listos.
- **Riesgos/bloqueos:** la publicación remota requiere que GitHub acepte la autenticación de esta máquina.
- **Próxima tarea (ID):** publicar el commit inicial y continuar con RFA-003.

## 2026-10-25 — RFA-003: base técnica y CI
- **Objetivo:** crear una aplicación mínima ejecutable que permita comenzar el desarrollo vertical.
- **Cambios/archivos:** añadido backend FastAPI con `GET /api/v1/health`, prueba de estado, frontend React/TypeScript con Vite, `.env.example`, configuración de CI y guía de ejecución en `README.md`.
- **Evidencia y comandos de prueba:** `pytest -q` en `backend` → 1 prueba aprobada; `npm run lint && npm run build` en `frontend` → correcto.
- **Decisiones:** dependencias de backend acotadas a FastAPI 0.115.x y Uvicorn 0.32.x por compatibilidad de pruebas; el endpoint HTTP se probará de forma integral al añadir la siguiente integración.
- **Riesgos/bloqueos:** ninguno para continuar. El entorno de ejecución aislado no permite comprobar una conexión HTTP entre procesos, aunque la aplicación inicia y la función de estado está probada.
- **Próxima tarea (ID):** RFA-004 — adaptador OpenAlex con normalización.

## 2026-10-25 — RFA-004: adaptador OpenAlex
- **Objetivo:** aislar OpenAlex del resto de la aplicación y convertir su respuesta externa a un formato estable.
- **Cambios/archivos:** añadido `app/integrations/openalex.py`, modelos internos de resultado, reconstrucción de `abstract_inverted_index`, validación de parámetros y pruebas de adaptación.
- **Evidencia y comandos de prueba:** `pytest -q` en `backend` → 6 pruebas aprobadas; consulta mínima con `OpenAlexClient.search_works('climate change', per_page=1)` → artículo normalizado y abstract disponible.
- **Decisiones:** búsqueda usa `search`, paginación `page`/`per-page` y filtros de fecha de publicación; se tratan 429, timeout y errores upstream como errores tipados. OpenAlex no requiere clave para el prototipo, pero su cuota compartida limita el uso sin clave.
- **Riesgos/bloqueos:** una clave gratuita de OpenAlex podría ser necesaria antes de una demo con uso intensivo; no se almacena ni se solicita todavía.
- **Próxima tarea (ID):** RFA-005 — endpoint `GET /papers/search`.

## Plantilla para sesiones futuras
### AAAA-MM-DD — Sesión
- Objetivo:
- Cambios/archivos:
- Evidencia y comandos de prueba:
- Decisiones:
- Riesgos/bloqueos:
- Próxima tarea (ID):
