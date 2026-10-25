import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import "./styles.css";

function App() {
  return (
    <main>
      <p className="eyebrow">ResearchFlow AI</p>
      <h1>Tu espacio para organizar literatura académica.</h1>
      <p>
        La búsqueda, la matriz bibliográfica y la exportación CSV estarán disponibles
        en los próximos incrementos.
      </p>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
