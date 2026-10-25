import { FormEvent, StrictMode, useState } from "react";
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

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Paper[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

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

      {error && <p className="message error" role="alert">{error}</p>}
      {!isLoading && !error && results.length === 0 && <p className="message">Aún no hay resultados. Inicia una búsqueda para explorar publicaciones.</p>}
      <section className="results" aria-live="polite">
        {results.map((paper) => (
          <article className="paper" key={paper.openalex_id}>
            <p className="paper-meta">{paper.year ?? "Año no disponible"} · {paper.authors.join(", ") || "Autor no disponible"}</p>
            <h2>{paper.title}</h2>
            <p>{paper.abstract ?? "Resumen no disponible."}</p>
            <a href={paper.source_url} target="_blank" rel="noreferrer">Ver fuente original</a>
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
