"""
Módulo de algoritmos sobre grafos dirigidos para el laberinto.
Proyecto: Simulador interactivo de laberintos y rutas alternativas (INFO1158).

Implementación de algoritmos estándar sin dependencias de bibliotecas externas.
"""

from collections import deque
import os
import sys
from typing import Any

# Asegurar importación de DirectedGraph tanto como paquete como ejecutado directamente
try:
    from src.models.graph_model import DirectedGraph
except ModuleNotFoundError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    from src.models.graph_model import DirectedGraph


def bfs_shortest_path(graph: DirectedGraph) -> dict[str, Any]:
    """
    Encuentra un camino dirigido de longitud mínima (en cantidad de arcos)
    desde el vértice fuente 'source' (s) hasta el sumidero 'sink' (t)
    utilizando el algoritmo de Búsqueda en Anchura (Breadth-First Search - BFS).
    
    Opera exclusivamente sobre los pasillos actualmente activos (graph.active_edges),
    garantizando la complejidad temporal O(|V| + |E|) y espacial O(|V|).
    
    Parámetros:
        graph (DirectedGraph): Instancia del modelo de grafo que contiene la
            configuración de vértices, arcos activos y terminales s y t.
            
    Retorna:
        dict[str, Any]: Diccionario con el resultado de la búsqueda:
            - Si existe camino:
                {
                    "exists": True,
                    "length": int,                # Cantidad de arcos del camino
                    "path_nodes": list[str],       # Vértices ordenados [s, ..., t]
                    "path_edges": list[tuple]      # Arcos dirigidos [(s, v1), ..., (vk, t)]
                }
            - Si no existe camino (desconexión o ausencia de ruta dirigida):
                {
                    "exists": False,
                    "length": None,
                    "path_nodes": [],
                    "path_edges": []
                }
    """
    source = graph.source
    sink = graph.sink

    # Validación de existencia de terminales
    if source is None or sink is None:
        return {
            "exists": False,
            "length": None,
            "path_nodes": [],
            "path_edges": [],
        }

    if source not in graph.vertices or sink not in graph.vertices:
        return {
            "exists": False,
            "length": None,
            "path_nodes": [],
            "path_edges": [],
        }

    # Caso borde: si el origen y destino fueran el mismo vértice
    if source == sink:
        return {
            "exists": True,
            "length": 0,
            "path_nodes": [source],
            "path_edges": [],
        }

    # Estructuras para BFS
    queue: deque[str] = deque([source])
    visited: set[str] = {source}
    # parent registra el predecesor de cada vértice para reconstruir el camino
    parent: dict[str, str] = {}

    found = False
    while queue:
        current = queue.popleft()

        if current == sink:
            found = True
            break

        # Exploramos los vecinos a través de los arcos activos
        # Ordenamos los vecinos para garantizar un recorrido determinista
        neighbors = graph.active_edges.get(current, set())
        for neighbor in sorted(neighbors):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    # Si el sumidero no fue alcanzado
    if not found and sink not in parent:
        return {
            "exists": False,
            "length": None,
            "path_nodes": [],
            "path_edges": [],
        }

    # Reconstrucción del camino desde el sumidero hacia la fuente
    path_nodes: list[str] = []
    curr: str | None = sink
    while curr is not None:
        path_nodes.append(curr)
        curr = parent.get(curr)

    path_nodes.reverse()

    # Construcción de la lista de arcos dirigidos recorridos
    path_edges: list[tuple[str, str]] = [
        (path_nodes[i], path_nodes[i + 1]) for i in range(len(path_nodes) - 1)
    ]

    return {
        "exists": True,
        "length": len(path_edges),
        "path_nodes": path_nodes,
        "path_edges": path_edges,
    }


if __name__ == "__main__":
    print("=== Demostración y pruebas de BFS Shortest Path ===")

    # Construir ruta al archivo data/config_inicial.json
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    json_path = os.path.join(base_dir, "data", "config_inicial.json")

    if os.path.exists(json_path):
        print(f"\n1. Cargando grafo desde '{json_path}'...")
        grafo = DirectedGraph.from_json(json_path)
        print(f"Grafo cargado: {grafo}")

        valido, errores = grafo.validate_initial_constraints()
        print(f"¿Cumple restricciones iniciales?: {valido}")
        if not valido:
            print("Errores encontrados:")
            for err in errores:
                print(f"  - {err}")

        # Calcular camino más corto inicial
        resultado = bfs_shortest_path(grafo)
        print("\n2. Resultado BFS en configuración inicial activa:")
        print(f"   Existe camino: {resultado['exists']}")
        print(f"   Longitud d_G(s, t): {resultado['length']}")
        print(f"   Vértices: {' -> '.join(resultado['path_nodes'])}")
        print(f"   Arcos: {resultado['path_edges']}")

        # Probar bloqueo de un arco del camino mínimo
        if resultado["exists"] and resultado["path_edges"]:
            primer_arco = resultado["path_edges"][0]
            print(f"\n3. Bloqueando arco crítico {primer_arco}...")
            grafo.block_edge(primer_arco[0], primer_arco[1])
            nuevo_resultado = bfs_shortest_path(grafo)
            print("   Resultado BFS tras el bloqueo:")
            print(f"   Existe camino: {nuevo_resultado['exists']}")
            print(f"   Nueva longitud: {nuevo_resultado['length']}")
            print(f"   Nueva ruta: {' -> '.join(nuevo_resultado['path_nodes'])}")

            # Desbloquear para restaurar
            print(f"\n4. Desbloqueando arco {primer_arco}...")
            grafo.unblock_edge(primer_arco[0], primer_arco[1])
            restaurado = bfs_shortest_path(grafo)
            print(f"   Longitud tras restaurar: {restaurado['length']}")

        # Probar caso de desconexión total hacia t
        print("\n5. Simulando desconexión forzada hacia t...")
        # Bloquear todos los arcos que entran a t
        arcos_a_t = [
            (u, v) for u, vecinos in list(grafo.active_edges.items()) for v in vecinos if v == grafo.sink
        ]
        for u, v in arcos_a_t:
            grafo.block_edge(u, v)

        res_desconectado = bfs_shortest_path(grafo)
        print(f"   Resultado en grafo desconectado: {res_desconectado}")
        assert res_desconectado["exists"] is False
        assert res_desconectado["length"] is None
        assert res_desconectado["path_nodes"] == []
        assert res_desconectado["path_edges"] == []
        print("   ¡Caso de desconexión validado correctamente!")
    else:
        print(f"No se encontró el archivo {json_path} para la prueba.")
