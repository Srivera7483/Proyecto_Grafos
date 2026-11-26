"""Adaptación de DirectedGraph a PyVis y resaltado de resultados (Issue #8).

La representación base del Issue #6 se conserva. Un arco bloqueado no
puede resaltarse como integrante de un camino o corte válido.
"""

from pyvis.network import Network

VISTA_RED = "Red original"
VISTA_BFS = "Camino mínimo"
VISTA_DISJUNTOS = "Caminos disjuntos"
VISTA_CORTE = "Corte mínimo"
VISTAS = (VISTA_RED, VISTA_BFS, VISTA_DISJUNTOS, VISTA_CORTE)

COLOR_ACTIVO = "#64748b"
COLOR_BLOQUEADO = "#dc2626"
COLOR_ATENUADO = "#aab3c2"
COLOR_BFS = "#d97706"
COLOR_CORTE = "#9333ea"
COLORES_CAMINOS = (
    "#0f766e", "#7c3aed", "#e11d48", "#2563eb", "#b45309", "#15803d",
    "#be185d", "#0891b2", "#4f46e5", "#a16207", "#0e7490", "#9f1239",
)


def grafo_a_datos_visualizacion(grafo) -> dict:
    """Extrae vértices y arcos de DirectedGraph sin modificarlo."""
    activos = {
        (str(origen), str(destino))
        for origen, destinos in grafo.active_edges.items()
        for destino in destinos
    }
    bloqueados = {
        (str(origen), str(destino))
        for origen, destino in grafo.blocked_edges
    }
    todos = activos | bloqueados

    return {
        "vertices": sorted((str(v) for v in grafo.vertices)),
        "arcos": [
            {
                "origen": origen,
                "destino": destino,
                "activo": (origen, destino) in activos,
            }
            for origen, destino in sorted(todos)
        ],
        "s": str(grafo.source),
        "t": str(grafo.sink),
    }


def estilos_arcos(datos: dict, vista: str = VISTA_RED, resultados: dict | None = None) -> dict:
    """Define color, grosor, trazo y descripción por arco, sin llamar a PyVis.

    resultados contiene las claves 'bfs', 'disjuntos', 'corte', tal como
    las devuelve la capa de coordinación de app.py.
    """
    if vista not in VISTAS:
        raise ValueError(f"Vista desconocida: {vista}")

    destacados: dict[tuple[str, str], tuple[str, str]] = {}
    if resultados is not None:
        if vista == VISTA_BFS:
            for u, v in resultados["bfs"]["path_edges"]:
                destacados[(str(u), str(v))] = (COLOR_BFS, "Camino mínimo (BFS)")
        elif vista == VISTA_DISJUNTOS:
            for indice, camino in enumerate(resultados["disjuntos"]["paths"]):
                color = COLORES_CAMINOS[indice % len(COLORES_CAMINOS)]
                for u, v in camino["path_edges"]:
                    destacados[(str(u), str(v))] = (color, f"Ruta disjunta {indice + 1}")
        elif vista == VISTA_CORTE:
            for u, v in resultados["corte"]["min_cut_edges"]:
                destacados[(str(u), str(v))] = (COLOR_CORTE, "Arco del corte mínimo")

    resaltando = bool(destacados)
    estilos = {}
    for arco in datos["arcos"]:
        u, v = arco["origen"], arco["destino"]
        clave = (u, v)
        activo = arco["activo"]
        estado = "Activo" if activo else "Bloqueado"
        titulo = f"{u} → {v}: {estado}"

        if not activo:
            # Tiene prioridad el estado real: los bloqueados son siempre rojos discontinuos.
            estilos[clave] = {
                "color": COLOR_BLOQUEADO,
                "width": 2,
                "dashes": True,
                "title": titulo,
            }
        elif clave in destacados:
            color, descripcion = destacados[clave]
            estilos[clave] = {
                "color": color,
                "width": 6,
                "dashes": False,
                "title": f"{titulo} | {descripcion}",
            }
        else:
            estilos[clave] = {
                "color": COLOR_ATENUADO if resaltando else COLOR_ACTIVO,
                "width": 2 if resaltando else 3,
                "dashes": False,
                "title": titulo,
            }
    return estilos


def generar_html(
    datos: dict,
    vista: str = VISTA_RED,
    resultados: dict | None = None,
) -> str:
    """Genera HTML autocontenido con la vista de resultados solicitada.

    La firma anterior generar_html(datos) permanece compatible.
    """
    red = Network(
        height="550px",
        width="100%",
        directed=True,
        bgcolor="#ffffff",
        font_color="#1f2937",
        cdn_resources="in_line",
    )

    red.set_options('''
    {
      "layout": {
        "hierarchical": {
          "enabled": true,
          "direction": "LR",
          "sortMethod": "directed",
          "levelSeparation": 160,
          "nodeSpacing": 140
        }
      },
      "physics": {"enabled": false},
      "interaction": {"hover": true},
      "edges": {
        "smooth": {
          "enabled": true,
          "type": "cubicBezier",
          "forceDirection": "horizontal",
          "roundness": 0.15
        }
      }
    }
    ''')

    for vertice in datos["vertices"]:
        if vertice == datos["s"]:
            color, descripcion = "#16a34a", "Entrada"
        elif vertice == datos["t"]:
            color, descripcion = "#dc2626", "Salida"
        else:
            color, descripcion = "#2563eb", "Intersección"

        red.add_node(
            vertice,
            label=vertice,
            title=f"{descripcion}: {vertice}",
            shape="circle",
            color=color,
            font={"color": "#ffffff", "size": 18},
            borderWidth=2,
        )

    estilos = estilos_arcos(datos, vista=vista, resultados=resultados)
    for arco in datos["arcos"]:
        u, v = arco["origen"], arco["destino"]
        red.add_edge(u, v, arrows="to", **estilos[(u, v)])

    return red.generate_html()
