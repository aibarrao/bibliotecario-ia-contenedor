# Bibliotecario IA — El Contenedor

Aplicación Streamlit independiente del catálogo público de Libib. Incluye 2.527 registros de la colección Consejo exportados por el responsable de la biblioteca.

## Cómo probar en tu equipo

1. Instala Python 3.11 o 3.12.
2. En esta carpeta ejecuta `python -m pip install -r requirements.txt`.
3. Ejecuta `streamlit run app.py`.
4. Sin clave API, podrás buscar en el catálogo. Para activar respuestas conversacionales, crea `.streamlit/secrets.toml` con `OPENAI_API_KEY = "tu_clave"`.

## Publicar en Streamlit Community Cloud

1. Crea un repositorio privado en GitHub y sube los archivos de esta carpeta (incluida la carpeta `.streamlit`, pero **no** el archivo real `secrets.toml`).
2. En https://share.streamlit.io/ crea una app, selecciona el repositorio, rama y `app.py`.
3. En **Advanced settings → Secrets**, pega `OPENAI_API_KEY = "tu_clave"` y despliega la aplicación.
4. Prueba consultas y verifica los libros recomendados. Si deseas una URL personalizada, consulta las opciones disponibles de Streamlit.

## Privacidad y limitaciones

- La app usa los metadatos del CSV; NO importa usuarios, préstamos ni fichas de lectores.
- El CSV queda incluido en el repositorio y en el despliegue. Comprueba que no contiene notas privadas o datos que no quieras publicar. Se recomienda limpiar el CSV antes de hacer público el repositorio.
- Las preguntas y los metadatos de los libros candidatos se envían al proveedor de IA al usar el modo conversacional.
- No existe sincronización en tiempo real con Libib: actualiza `catalogo.csv` exportando un CSV nuevo y vuelve a desplegar.
- No se garantiza disponibilidad de préstamo; el campo `copies` es una cantidad catalogada, no el estado de circulación.
- Los enlaces llevan al catálogo público general; no se ha verificado el formato de URL de fichas individuales.
- Búsqueda híbrida TF-IDF de palabras y caracteres, más expansión opcional de consulta y generación restringida a resultados del CSV. No es una búsqueda por embeddings todavía.
- Para uso público, añade control de gastos, límites de uso, política de privacidad y evaluación editorial de respuestas.
