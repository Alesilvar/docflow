# Seguridad y privacidad

- Nunca commitear API keys, tokens de correo, `.env` ni datos personales.
- `.env.example` debe contener nombres de variables y valores de ejemplo inofensivos.
- Sanitizar logs y errores de API; utilizar identificadores de solicitud.
- Validar query params y tamaño de respuestas; limitar llamadas costosas a IA.
- Token dedicado para integración n8n → backend, guardado como credencial, con rotación.
- Evitar inyección de prompt desde abstracts y otras fuentes externas.
- Verificar licencias y condiciones de uso de APIs y publicaciones; almacenar metadatos necesarios, no republicar full texts sin permiso.
- Añadir autenticación/limitación de uso antes de exponer endpoints públicamente.
- Definir borrado local de proyectos y datos antes de considerar cuentas multiusuario.
- El uso del proveedor de IA y envíos de correos reales requiere consentimiento y revisión del destino.
