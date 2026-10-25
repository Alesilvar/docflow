# Modelo de datos inicial (propuesta)

## Tablas
- `research_projects`: `id (uuid pk)`, `name`, `research_question`, `created_at`, `updated_at`.
- `papers`: `id (uuid pk)`, `openalex_id (unique)`, `doi (nullable index)`, `title`, `publication_year`, `publication_date`, `landing_url`, `abstract_text (nullable)`, `source_payload`, `created_at`.
- `paper_authors`: `paper_id`, `display_name`, `author_position` (opcional para MVP).
- `project_papers`: `project_id`, `paper_id`, `notes`, `status`, `added_at`; unique (`project_id`, `paper_id`).
- `paper_analyses`: `id`, `paper_id`, `model_name`, `prompt_version`, `input_scope`, `output_json`, `review_status`, `created_at`.
- `watchlists`: `id`, `project_id`, `query`, `filters_json`, `active`, `last_checked_at`.
- `seen_watchlist_papers`: `watchlist_id`, `paper_id`, `first_seen_at`; unique pair.
- `notification_events`: `id`, `watchlist_id`, `paper_id`, `channel`, `status`, `sent_at`, `attempts`; unique (`watchlist_id`, `paper_id`, `channel`).
- `automation_runs`: `id`, `workflow_name`, `started_at`, `finished_at`, `status`, `error_code`.
- `evaluation_labels`: `id`, `query`, `paper_id`, `relevance_grade`, `annotator`, `notes`.

## Invariantes
Un artículo puede estar en muchos proyectos. DOI puede faltar o tener variantes; priorizar ID OpenAlex normalizado y reconciliar duplicados. Un abstract ausente no debe transformarse en texto vacío interpretado como contenido. Los análisis siempre registran `input_scope` y versión del modelo/prompt.

## Migraciones
Usar Alembic. Esquema no final; registrar cambios incompatibles en `DECISIONS.md`.
