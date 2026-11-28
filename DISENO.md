# Diseño del README de perfil — decisiones tomadas

## Noviembre de 2026

- **Base elegida:** boceto C «vitrina» (cabecera con línea de terminal animada y proyectos en filas alternas con captura), adaptado a la estética del portfolio.
- **Paleta:** la monocroma del portfolio: negros `#06070a` y `#0c0e13`, superficie `#14171e`, textos `#ffffff`, `#cbd2de`, `#8b95a7` y `#4f5868`, bordes blancos con poca opacidad. Sin colores de acento.
- **Cabecera (`assets/banner.svg`):** solo versión oscura (decidido así aunque GitHub esté en tema claro). Rejilla tenue, brillo blanco arriba a la derecha, «PORTFOLIO · DESARROLLADOR FULL-STACK» en monoespaciada, el nombre en degradado de blanco a plata y una línea `>` que escribe tres frases sacadas de la descripción. Animación con CSS dentro del SVG; con `prefers-reduced-motion` se queda la primera frase escrita.
- **Tipografía:** Outfit y JetBrains Mono, como el portfolio, con fuentes del sistema de respaldo. No se incrustan en el SVG: en GitHub se verá la de respaldo.
- **Proyectos:** tabla HTML con captura y texto alternados (DistribuTech Pro, Agente de citas, Portfolio y Shenron). Capturas en color, guardadas en `assets/`. Etiquetas de tecnología con shields.io en `#14171e` y logotipos en `#cbd2de`.
- **Contenido:** el mismo que el README anterior (descripción, proyectos con sus enlaces, stack por áreas y contacto con correo).
- **Sin párrafo de descripción:** repetía la bio del perfil y las frases del banner. Se queda solo la bio.
- **Stack:** cada área de la tabla con insignias de shields.io `for-the-badge` en el color de cada marca (excepción a la paleta monocroma, a propósito). Lo que no tiene logotipo (SQL, LLM con herramientas, Pest) va sin icono.
- **Lenguajes (`assets/lenguajes.svg`):** tarjeta propia generada por `scripts/lenguajes.py`, que suma los bytes por lenguaje de los repositorios públicos propios (sin forks) con la API de GitHub. Linguist ya excluye `vendor/`. Es estática: para ponerla al día se vuelve a ejecutar el script y se hace commit. Se descartó gitskins.com por la misma razón que github-readme-stats (servicio externo) y una Action con commits automáticos a `main`.
- **Contacto (`assets/contacto-*.svg`):** cápsulas monocromas con icono redondo, etiqueta y dato, generadas por `scripts/contacto.py`. El enlace va en el README, alrededor de cada imagen.
- **Descartado:** estadísticas de github-readme-stats (poco fiables y cifras que no aportan), gráfico de contribuciones con serpiente (GitHub ya lo muestra en el perfil), versión clara de la cabecera, bocetos A (tarjetas 2×2) y B (solo texto y tabla) y la paleta azul y violeta del primer boceto C.
