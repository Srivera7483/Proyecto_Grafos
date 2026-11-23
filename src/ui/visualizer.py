"""Adaptación del modelo de grafos a una visualización dirigida con PyVis."""

from pyvis.network import Network


def grafo_a_datos_visualizacion(grafo) -> dict:
    """
    Convierte DirectedGraph al contrato visual utilizado por PyVis.

    Asume que grafo.active_edges es un diccionario de adyacencia,
    cuyos valores se pueden recorrer para obtener los destinos, y que
    grafo.blocked_edges es una colección de pares (origen, destino).
    """
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
            {"origen": origen, "destino": destino, "activo": (origen, destino) not in bloqueados}
            for origen, destino in sorted(todos)
        ],
        "s": str(grafo.source),
        "t": str(grafo.sink),
    }


def generar_html(datos: dict) -> str:
    """Genera un HTML autocontenido con vértices, flechas y estados."""
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

    for arco in datos["arcos"]:
        activo = arco["activo"]
        origen, destino = arco["origen"], arco["destino"]
        red.add_edge(
            origen,
            destino,
            arrows="to",
            color="#64748b" if activo else "#dc2626",
            width=3 if activo else 2,
            dashes=not activo,
            title=f"{origen} → {destino}: {'Activo' if activo else 'Bloqueado'}",
        )

    return red.generate_html()
