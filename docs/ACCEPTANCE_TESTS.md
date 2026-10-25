# Pruebas y criterios de aceptación

## Búsqueda
- Consulta válida muestra título, año, autores, fuente y vínculo original cuando existan.
- Resumen ausente aparece como 'No disponible'.
- 429/timeout del proveedor devuelve error controlado; sin congelar UI.
- Filtros de años inválidos producen 400 y mensaje claro.

## Persistencia
- Un mismo artículo puede estar en varios proyectos sin duplicarse globalmente.
- Dos guardados repetidos en un proyecto no generan dos filas.
- Editar una fila de matriz y exportar CSV conserva cambios y caracteres acentuados.

## IA
- Sin abstract: no inventa objetivos ni hallazgos.
- Campos relevantes incluyen evidencia textual o `unknown`.
- JSON inválido se rechaza/reintenta de forma controlada.
- Un fragmento con 'ignore previous instructions' no altera directivas del sistema.

## Automatización
- Dos ejecuciones consecutivas sin nuevos artículos no envían alertas duplicadas.
- Un error de correo queda registrado y permite reintento seguro.
- La ruta interna no admite llamadas sin credenciales.

## Demo
- Instalación desde instrucciones sin credenciales reales en repo.
- Flujo completo en navegador, API documentada y tests automatizados reproducibles.
