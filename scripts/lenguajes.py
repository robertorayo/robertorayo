"""
==== Tarjeta de lenguajes del README ====
Suma los bytes por lenguaje de los repositorios públicos propios (sin forks)
con la API de GitHub y genera assets/lenguajes.svg.

Uso:  python scripts/lenguajes.py
Si existe la variable de entorno GITHUB_TOKEN se usa para no chocar con el
límite de 60 peticiones por hora de la API sin autenticar.
"""
import json
import os
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

USUARIO = "robertorayo"
MAXIMO = 6  # lenguajes que se muestran; el resto se agrupa en «Otros»
SALIDA = Path(__file__).resolve().parent.parent / "assets" / "lenguajes.svg"

# Colores de GitHub Linguist para los lenguajes habituales
COLORES = {
    "TypeScript": "#3178c6", "JavaScript": "#f1e05a", "HTML": "#e34c26",
    "CSS": "#663399", "SCSS": "#c6538c", "Python": "#3572a5", "Java": "#b07219",
    "PHP": "#4f5d95", "Blade": "#f7523f", "Vue": "#41b883", "Shell": "#89e051",
    "PowerShell": "#012456", "Dockerfile": "#384d54", "PLpgSQL": "#336790",
    "TSQL": "#e38c00", "Kotlin": "#a97bff", "C#": "#178600",
}
GRIS = "#8b95a7"


def pedir(url):
    cabeceras = {"Accept": "application/vnd.github+json", "User-Agent": "readme-lenguajes"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        cabeceras["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=cabeceras)) as r:
        return json.load(r)


def contar():
    repos = pedir(f"https://api.github.com/users/{USUARIO}/repos?per_page=100&type=owner")
    total = {}
    for repo in repos:
        if repo["fork"]:
            continue
        for lenguaje, bytes_ in pedir(repo["languages_url"]).items():
            total[lenguaje] = total.get(lenguaje, 0) + bytes_
    return total


def coma(pct):
    return f"{pct:.1f}".replace(".", ",")


def porcentajes(total):
    if not total:
        raise SystemExit("La API no ha devuelto ningún lenguaje; no se toca el SVG.")
    suma = sum(total.values())
    orden = sorted(total.items(), key=lambda par: par[1], reverse=True)
    filas = [(nombre, bytes_ / suma * 100) for nombre, bytes_ in orden[:MAXIMO]]
    resto = sum(bytes_ for _, bytes_ in orden[MAXIMO:])
    if resto:
        filas.append(("Otros", resto / suma * 100))
    return filas


def svg(filas):
    ancho, alto_fila, arriba = 860, 34, 118
    alto = arriba + alto_fila * len(filas) + 28
    barra_x, barra_ancho = 330, 470
    filas_svg = []
    for i, (nombre, pct) in enumerate(filas):
        y = arriba + i * alto_fila
        color = COLORES.get(nombre, GRIS)
        relleno = max(barra_ancho * pct / 100, 6)
        filas_svg.append(f"""
  <g transform="translate(0 {y})">
    <circle cx="66" cy="0" r="5" fill="{color}"/>
    <text x="84" y="5" class="sans" font-size="15" font-weight="600" fill="#ffffff">{escape(nombre)}</text>
    <text x="300" y="5" class="mono" font-size="14" font-weight="600" fill="#cbd2de" text-anchor="end">{coma(pct)} %</text>
    <rect x="{barra_x}" y="-4" width="{barra_ancho}" height="8" rx="4" fill="#ffffff" fill-opacity=".06"/>
    <rect x="{barra_x}" y="-4" width="{relleno:.1f}" height="8" rx="4" fill="{color}"/>
  </g>""")
    nombres = ", ".join(f"{n} {coma(p)} %" for n, p in filas)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{ancho}" height="{alto}" viewBox="0 0 {ancho} {alto}" role="img" aria-labelledby="t d">
  <title id="t">Lenguajes en mis repositorios públicos</title>
  <desc id="d">{escape(nombres)}</desc>
  <!-- Generado por scripts/lenguajes.py: no editar a mano -->
  <defs>
    <linearGradient id="fondo" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#06070a"/>
      <stop offset="1" stop-color="#0c0e13"/>
    </linearGradient>
    <radialGradient id="brillo" cx=".85" cy="0" r=".7">
      <stop offset="0" stop-color="#ffffff" stop-opacity=".07"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
    <pattern id="rejilla" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M32 0H0V32" fill="none" stroke="#ffffff" stroke-opacity=".03"/>
    </pattern>
    <clipPath id="marco"><rect width="{ancho}" height="{alto}" rx="16"/></clipPath>
  </defs>
  <style>
    .mono {{ font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Consolas, 'Liberation Mono', monospace; }}
    .sans {{ font-family: 'Outfit', -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif; }}
  </style>
  <g clip-path="url(#marco)">
    <rect width="{ancho}" height="{alto}" fill="url(#fondo)"/>
    <rect width="{ancho}" height="{alto}" fill="url(#rejilla)"/>
    <rect width="{ancho}" height="{alto}" fill="url(#brillo)"/>
  </g>
  <rect x=".5" y=".5" width="{ancho - 1}" height="{alto - 1}" rx="16" fill="none" stroke="#ffffff" stroke-opacity=".13"/>

  <text x="60" y="58" class="sans" font-size="26" font-weight="700" fill="#ffffff">Lenguajes</text>
  <text x="60" y="82" class="mono" font-size="13" fill="#8b95a7">por bytes de código en mis repositorios públicos</text>
  <text x="{ancho - 60}" y="58" class="mono" font-size="14" fill="#4f5868" text-anchor="end">&gt; linguist</text>
{''.join(filas_svg)}
</svg>
"""


if __name__ == "__main__":
    filas = porcentajes(contar())
    SALIDA.write_text(svg(filas), encoding="utf-8")
    for nombre, pct in filas:
        print(f"{nombre:<14}{pct:5.1f} %")
    print(f"Guardado en {SALIDA}")
