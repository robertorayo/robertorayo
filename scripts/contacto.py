"""
==== Botones de contacto del README ====
Genera assets/contacto-*.svg: una cápsula monocroma con icono redondo,
etiqueta pequeña y el dato debajo. Los SVG no pueden llevar enlaces dentro
de un <img>, así que el enlace lo pone el README alrededor de cada imagen.

Uso:  python scripts/contacto.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

CARPETA = Path(__file__).resolve().parent.parent / "assets"

# Iconos dibujados a 24×24 con trazo blanco, centrados en el círculo
ICONOS = {
    "linkedin": '<text x="12" y="16.5" text-anchor="middle" class="sans" font-size="14" font-weight="800" fill="#ffffff">in</text>',
    "portfolio": '<g fill="none" stroke="#ffffff" stroke-width="1.6"><circle cx="12" cy="12" r="7.5"/>'
                 '<ellipse cx="12" cy="12" rx="3.2" ry="7.5"/><path d="M4.5 12h15"/></g>',
    "correo": '<g fill="none" stroke="#ffffff" stroke-width="1.6" stroke-linejoin="round">'
              '<rect x="4.5" y="6.5" width="15" height="11" rx="2"/><path d="m5 7.5 7 5.5 7-5.5"/></g>',
}

BOTONES = [
    ("linkedin", "LinkedIn", "roberto-borrallo-alvarez"),
    ("portfolio", "Portfolio", "roberto-borrallo.vercel.app"),
    ("correo", "Correo", "robertobamym@gmail.com"),
]

ALTO = 60
# Ancho estimado de cada letra a 13 px seminegrita; textLength corrige la diferencia real
ANCHAS, ESTRECHAS = set("mw@"), set("iljt.-r")


def ancho_texto(texto):
    return round(sum(11 if c in ANCHAS else 4.4 if c in ESTRECHAS else 7.4 for c in texto))


def svg(clave, etiqueta, dato):
    texto = ancho_texto(dato)
    ancho = 62 + texto + 26
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{ancho}" height="{ALTO}" viewBox="0 0 {ancho} {ALTO}" role="img" aria-label="{escape(f'{etiqueta}: {dato}', {'"': '&quot;'})}">
  <!-- Generado por scripts/contacto.py: no editar a mano -->
  <defs>
    <linearGradient id="fondo" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#14171e"/>
      <stop offset="1" stop-color="#0c0e13"/>
    </linearGradient>
    <linearGradient id="borde" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ffffff" stop-opacity=".55"/>
      <stop offset=".45" stop-color="#ffffff" stop-opacity=".08"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity=".35"/>
    </linearGradient>
    <radialGradient id="brillo" cx=".2" cy="0" r=".9">
      <stop offset="0" stop-color="#ffffff" stop-opacity=".12"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <style>
    .sans {{ font-family: 'Outfit', -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif; }}
    .mono {{ font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Consolas, 'Liberation Mono', monospace; }}
  </style>
  <rect x="1" y="1" width="{ancho - 2}" height="{ALTO - 2}" rx="{(ALTO - 2) / 2}" fill="url(#fondo)"/>
  <rect x="1" y="1" width="{ancho - 2}" height="{ALTO - 2}" rx="{(ALTO - 2) / 2}" fill="url(#brillo)"/>
  <rect x="1" y="1" width="{ancho - 2}" height="{ALTO - 2}" rx="{(ALTO - 2) / 2}" fill="none" stroke="url(#borde)" stroke-width="1.2"/>

  <circle cx="31" cy="30" r="19" fill="#06070a" stroke="#ffffff" stroke-opacity=".18"/>
  <g transform="translate(19 18)">{ICONOS[clave]}</g>

  <text x="62" y="25" class="mono" font-size="10.5" font-weight="600" letter-spacing="1.5" fill="#8b95a7">{escape(etiqueta.upper())}</text>
  <text x="62" y="43" class="sans" font-size="13" font-weight="600" fill="#ffffff" textLength="{texto}" lengthAdjust="spacingAndGlyphs">{escape(dato)}</text>
</svg>
"""


if __name__ == "__main__":
    for clave, etiqueta, dato in BOTONES:
        ruta = CARPETA / f"contacto-{clave}.svg"
        ruta.write_text(svg(clave, etiqueta, dato), encoding="utf-8")
        print(f"Guardado {ruta.name}")
