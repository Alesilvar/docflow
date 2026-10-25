import { FormEvent, StrictMode, useEffect, useState } from "react";
import { createRoot } from "react-dom/client";

import "./styles.css";

type Paper = {
  openalex_id: string;
  title: string;
  year: number | null;
  authors: string[];
  doi: string | null;
  abstract: string | null;
  source_url: string;
};

type SearchResponse = { items: Paper[]; page: number; has_next: boolean; total_count: number | null };
type ApiError = { error?: { message?: string } };
type Project = { id: string; name: string; research_question: string | null };

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Paper[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState("");
  const [projectName, setProjectName] = useState("");

  useEffect(() => {
    void loadProjects();
  }, []);

  async function loadProjects() {
    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/projects`);
      if (!response.ok) return;
      const body = (await response.json()) as Project[];
      setProjects(body);
      setSelectedProjectId((current) => current || body[0]?.id || "");
    } catch {
      // Searching remains available if the project service is not reachable.
    }
  }

  async function createProject(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!projectName.trim()) return;
    const response = await fetch(`${apiBaseUrl}/api/v1/projects`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ name: projectName.trim() }) });
    if (!response.ok) { setError("No se pudo crear el proyecto."); return; }
    const project = (await response.json()) as Project;
    setProjects((current) => [project, ...current]);
    setSelectedProjectId(project.id);
    setProjectName("");
  }

  async function savePaper(paper: Paper) {
    if (!selectedProjectId) { setError("Crea o selecciona un proyecto antes de guardar."); return; }
    const response = await fetch(`${apiBaseUrl}/api/v1/projects/${selectedProjectId}/papers`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(paper) });
    if (!response.ok) { setError("No se pudo guardar el artículo."); return; }
    setError(null);
  }

  async function search(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const normalizedQuery = query.trim();
    if (!normalizedQuery) {
      setError("Escribe un tema, una pregunta o palabras clave para buscar.");
      return;
    }

    setIsLoading(true);
    setError(null);
    try {
      const parameters = new URLSearchParams({ query: normalizedQuery, per_page: "10" });
      const response = await fetch(`${apiBaseUrl}/api/v1/papers/search?${parameters}`);
      if (!response.ok) {
        const body = (await response.json().catch(() => ({}))) as ApiError;
        throw new Error(body.error?.message ?? "No se pudo completar la búsqueda.");
      }
      const body = (await response.json()) as SearchResponse;
      setResults(body.items);
    } catch (requestError) {
      setResults([]);
      setError(requestError instanceof Error ? requestError.message : "Ocurrió un error inesperado.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="page">
      <header>
        <p className="eyebrow">ResearchFlow AI</p>
        <h1>Encuentra literatura para tu investigación.</h1>
        <p className="intro">Busca en OpenAlex y revisa los metadatos disponibles antes de guardar un artículo.</p>
      </header>

      <form className="search-form" onSubmit={search}>
        <label htmlFor="query">Tema de investigación</label>
        <div className="search-controls">
          <input id="query" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Ej.: cambio climático y salud pública" />
          <button type="submit" disabled={isLoading}>{isLoading ? "Buscando…" : "Buscar"}</button>
        </div>
      </form>

      <section className="project-bar" aria-label="Proyecto actual">
        <form onSubmit={createProject} className="project-create"><input value={projectName} onChange={(event) => setProjectName(event.target.value)} placeholder="Nuevo proyecto" aria-label="Nombre del nuevo proyecto" /><button type="submit">Crear proyecto</button></form>
        <select value={selectedProjectId} onChange={(event) => setSelectedProjectId(event.target.value)} aria-label="Proyecto para guardar artículos"><option value="">Selecciona un proyecto</option>{projects.map((project) => <option key={project.id} value={project.id}>{project.name}</option>)}</select>
      </section>

      {error && <p className="message error" role="alert">{error}</p>}
      {!isLoading && !error && results.length === 0 && <p className="message">Aún no hay resultados. Inicia una búsqueda para explorar publicaciones.</p>}
      <section className="results" aria-live="polite">
        {results.map((paper) => (
          <article className="paper" key={paper.openalex_id}>
            <p className="paper-meta">{paper.year ?? "Año no disponible"} · {paper.authors.join(", ") || "Autor no disponible"}</p>
            <h2>{paper.title}</h2>
            <p>{paper.abstract ?? "Resumen no disponible."}</p>
            <a href={paper.source_url} target="_blank" rel="noreferrer">Ver fuente original</a>
            <button className="save" type="button" onClick={() => void savePaper(paper)}>Guardar en proyecto</button>
          </article>
        ))}
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
