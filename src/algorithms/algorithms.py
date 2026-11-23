"""
Módulo de algoritmos sobre grafos dirigidos para el laberinto.
Proyecto: Simulador interactivo de laberintos y rutas alternativas (INFO1158).

Implementación de algoritmos estándar sin dependencias de bibliotecas externas:
- Búsqueda en Anchura (BFS) para Camino Mínimo.
- Flujo Máximo unitario y descomposición en Caminos Disjuntos en Arcos (Edmonds-Karp).
- Corte Mínimo de Pasillos basado en el Teorema de Flujo Máximo - Corte Mínimo.
"""

from collections import deque
import os
import sys
from typing import Any

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
                    "length": int,
                    "path_nodes": list[str],
                    "path_edges": list[tuple]
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

    if source == sink:
        return {
            "exists": True,
            "length": 0,
            "path_nodes": [source],
            "path_edges": [],
        }

    queue: deque[str] = deque([source])
    visited: set[str] = {source}
    parent: dict[str, str] = {}

    found = False
    while queue:
        current = queue.popleft()

        if current == sink:
            found = True
            break

        neighbors = graph.active_edges.get(current, set())
        for neighbor in sorted(neighbors):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    if not found and sink not in parent:
        return {
            "exists": False,
            "length": None,
            "path_nodes": [],
            "path_edges": [],
        }

    path_nodes: list[str] = []
    curr: str | None = sink
    while curr is not None:
        path_nodes.append(curr)
        curr = parent.get(curr)

    path_nodes.reverse()

    path_edges: list[tuple[str, str]] = [
        (path_nodes[i], path_nodes[i + 1]) for i in range(len(path_nodes) - 1)
    ]

    return {
        "exists": True,
        "length": len(path_edges),
        "path_nodes": path_nodes,
        "path_edges": path_edges,
    }


def edmonds_karp_max_flow(
    graph: DirectedGraph,
) -> tuple[int, dict[str, dict[str, int]], dict[str, dict[str, int]]]:
    """
    Calcula el flujo máximo sobre los arcos activos del grafo con capacidades unitarias
    utilizando el algoritmo de Edmonds-Karp (BFS en la red residual).
    
    Parámetros:
        graph (DirectedGraph): Grafo con vértices, arcos activos y terminales s y t.
        
    Retorna:
        tuple[int, dict, dict]:
            - max_flow (int): Valor del flujo máximo alcanzado.
            - flow (dict[str, dict[str, int]]): Flujo neto en cada arco original u -> v.
            - residual (dict[str, dict[str, int]]): Capacidades residuales finales de la red.
    """
    s = graph.source
    t = graph.sink

    if s is None or t is None or s not in graph.vertices or t not in graph.vertices or s == t:
        return 0, {}, {}

    vertices = graph.vertices

    residual: dict[str, dict[str, int]] = {u: {} for u in vertices}
    flow: dict[str, dict[str, int]] = {u: {} for u in vertices}

    for u in vertices:
        for v in graph.active_edges.get(u, set()):
            residual[u][v] = 1
            if u not in residual[v]:
                residual[v][u] = 0
            flow[u][v] = 0

    max_flow = 0

    while True:
        parent: dict[str, str] = {}
        visited: set[str] = {s}
        queue: deque[str] = deque([s])
        found_t = False

        while queue:
            curr = queue.popleft()
            if curr == t:
                found_t = True
                break

            for neighbor in sorted(residual[curr].keys()):
                if neighbor not in visited and residual[curr][neighbor] > 0:
                    visited.add(neighbor)
                    parent[neighbor] = curr
                    queue.append(neighbor)

        if not found_t:
            break

        aug_path: list[tuple[str, str]] = []
        curr_node = t
        while curr_node != s:
            prev_node = parent[curr_node]
            aug_path.append((prev_node, curr_node))
            curr_node = prev_node

        aug_path.reverse()

        bottleneck = min(residual[u][v] for u, v in aug_path)

        for u, v in aug_path:
            residual[u][v] -= bottleneck
            residual[v][u] += bottleneck

            if v in graph.active_edges.get(u, set()):
                flow[u][v] += bottleneck
            else:
                flow[v][u] -= bottleneck

        max_flow += bottleneck

    return max_flow, flow, residual


def max_edge_disjoint_paths(graph: DirectedGraph) -> dict[str, Any]:
    """
    Calcula el número máximo de caminos dirigidos desde s hasta t que no comparten arcos
    (pueden compartir vértices intermedios), mediante la formulación de flujo máximo unitario
    con el algoritmo de Edmonds-Karp.
    
    Reconstruye cada camino completo descomponiendo el flujo positivo y consumiendo las aristas
    usadas para garantizar que ningún arco se repita entre los caminos.
    
    Parámetros:
        graph (DirectedGraph): Grafo con terminales s y t definidos.
        
    Retorna:
        dict[str, Any]:
            {
                "max_paths": int,
                "paths": list[dict],
                "paths_nodes": list[list[str]],
                "paths_edges": list[list[tuple]]
            }
            Si no existe camino, retorna 0 caminos y listas vacías [].
    """
    s = graph.source
    t = graph.sink

    if s is None or t is None or s not in graph.vertices or t not in graph.vertices or s == t:
        return {
            "max_paths": 0,
            "paths": [],
            "paths_nodes": [],
            "paths_edges": [],
        }

    max_flow, flow, _ = edmonds_karp_max_flow(graph)

    if max_flow == 0:
        return {
            "max_paths": 0,
            "paths": [],
            "paths_nodes": [],
            "paths_edges": [],
        }

    flow_edges: dict[str, set[str]] = {u: set() for u in graph.vertices}
    for u in graph.vertices:
        for v, f_val in flow.get(u, {}).items():
            if f_val > 0:
                flow_edges[u].add(v)

    disjoint_paths: list[dict[str, Any]] = []

    while True:
        queue: deque[str] = deque([s])
        visited: set[str] = {s}
        parent: dict[str, str] = {}
        found = False

        while queue:
            curr = queue.popleft()
            if curr == t:
                found = True
                break

            for nxt in sorted(flow_edges[curr]):
                if nxt not in visited:
                    visited.add(nxt)
                    parent[nxt] = curr
                    queue.append(nxt)

        if not found:
            break

        path_nodes: list[str] = []
        curr_node: str | None = t
        while curr_node is not None:
            path_nodes.append(curr_node)
            curr_node = parent.get(curr_node)

        path_nodes.reverse()

        path_edges = [
            (path_nodes[i], path_nodes[i + 1]) for i in range(len(path_nodes) - 1)
        ]

        for u_edge, v_edge in path_edges:
            flow_edges[u_edge].remove(v_edge)

        disjoint_paths.append({
            "path_nodes": path_nodes,
            "path_edges": path_edges,
            "length": len(path_edges),
        })

    return {
        "max_paths": len(disjoint_paths),
        "paths": disjoint_paths,
        "paths_nodes": [p["path_nodes"] for p in disjoint_paths],
        "paths_edges": [p["path_edges"] for p in disjoint_paths],
    }


def min_edge_cut(graph: DirectedGraph) -> dict[str, Any]:
    r"""
    Determina un conjunto mínimo de pasillos C subseteq E cuya eliminación
    interrumpe toda conexión dirigida desde s hasta t en G - C = (V, E \ C).
    
    Aplica el Teorema de Flujo Máximo - Corte Mínimo sobre la red residual final
    de Edmonds-Karp, identificando el conjunto R de vértices alcanzables desde s
    mediante aristas residuales > 0, y seleccionando todos los arcos originales
    activos u -> v tales que u in R y v not in R.
    
    Parámetros:
        graph (DirectedGraph): Grafo con terminales s y t.
        
    Retorna:
        dict[str, Any]:
            {
                "min_cut_edges": list[tuple[str, str]],
                "cut_size": int,
                "reachable_nodes": list[str],
                "non_reachable_nodes": list[str]
            }
            Si no existe camino de s a t, retorna conjunto vacío [] y cut_size 0.
    """
    s = graph.source
    t = graph.sink

    if s is None or t is None or s not in graph.vertices or t not in graph.vertices or s == t:
        return {
            "min_cut_edges": [],
            "cut_size": 0,
            "reachable_nodes": [],
            "non_reachable_nodes": [],
        }

    max_flow, _, residual = edmonds_karp_max_flow(graph)

    if max_flow == 0:
        return {
            "min_cut_edges": [],
            "cut_size": 0,
            "reachable_nodes": [s],
            "non_reachable_nodes": sorted(list(graph.vertices - {s})),
        }

    reachable: set[str] = {s}
    queue: deque[str] = deque([s])

    while queue:
        curr = queue.popleft()
        for neighbor, cap in residual.get(curr, {}).items():
            if cap > 0 and neighbor not in reachable:
                reachable.add(neighbor)
                queue.append(neighbor)

    cut_edges: list[tuple[str, str]] = []
    for u in sorted(reachable):
        for v in sorted(graph.active_edges.get(u, set())):
            if v not in reachable:
                cut_edges.append((u, v))

    if len(cut_edges) != max_flow:
        raise RuntimeError(
            f"Violación del Teorema Flujo-Corte: |C| = {len(cut_edges)} no coincide "
            f"con max_flow = {max_flow}."
        )

    return {
        "min_cut_edges": cut_edges,
        "cut_size": len(cut_edges),
        "reachable_nodes": sorted(list(reachable)),
        "non_reachable_nodes": sorted(list(graph.vertices - reachable)),
    }


edmonds_karp_disjoint_paths = max_edge_disjoint_paths
find_min_cut = min_edge_cut


if __name__ == "__main__":
    print("=" * 65)
    print("  PRUEBA DE ALGORITMOS: BFS, CAMINOS DISJUNTOS Y CORTE MÍNIMO")
    print("=" * 65)

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    json_path = os.path.join(base_dir, "data", "config_inicial.json")

    print(f"\n1. Cargando grafo desde '{json_path}'...")
    grafo = DirectedGraph.from_json(json_path)
    print(f"   {grafo}")

    valido, errores = grafo.validate_initial_constraints()
    print(f"   ¿Cumple restricciones iniciales?: {valido}")
    if not valido:
        print(f"   Errores: {errores}")

    res_bfs = bfs_shortest_path(grafo)
    print(f"\n2. Camino Mínimo (BFS):")
    print(f"   - Existe: {res_bfs['exists']}")
    print(f"   - Longitud d_G(s, t): {res_bfs['length']}")
    print(f"   - Ruta: {' -> '.join(res_bfs['path_nodes'])}")
    print(f"   - Arcos: {res_bfs['path_edges']}")

    res_disj = max_edge_disjoint_paths(grafo)
    print(f"\n3. Caminos Disjuntos en Arcos (Edmonds-Karp unitario):")
    print(f"   - Máximo número de caminos: {res_disj['max_paths']}")
    for i, p in enumerate(res_disj["paths"], 1):
        print(f"     Camino {i} (longitud {p['length']}): {' -> '.join(p['path_nodes'])}")
        print(f"       Arcos: {p['path_edges']}")

    res_cut = min_edge_cut(grafo)
    print(f"\n4. Corte Mínimo de Pasillos (Min-Cut):")
    print(f"   - Cardinalidad mínima |C|: {res_cut['cut_size']}")
    print(f"   - Pasillos a eliminar C: {res_cut['min_cut_edges']}")
    print(f"   - Vértices alcanzables R: {res_cut['reachable_nodes']}")
    print(f"   - Vértices no alcanzables V \\ R: {res_cut['non_reachable_nodes']}")

    print(f"\n5. Verificación de igualdad (Dualidad Min-Cut / Max-Flow):")
    print(f"   - Max caminos disjuntos: {res_disj['max_paths']}")
    print(f"   - Min corte de pasillos: {res_cut['cut_size']}")
    assert res_disj["max_paths"] == res_cut["cut_size"], "¡Error: no coinciden!"
    print("   -> ¡TEOREMA CONFIRMADO: La cardinalidad coincide exactamente!")

    print(f"\n6. Verificando que eliminando C se desconecta s de t...")
    for u, v in res_cut["min_cut_edges"]:
        grafo.block_edge(u, v)

    res_post_corte = bfs_shortest_path(grafo)
    print(f"   - Camino BFS tras bloquear C: {res_post_corte}")
    assert res_post_corte["exists"] is False, "¡Error: todavía hay camino!"
    print("   -> ¡CONFIRMADO: El corte C interrumpe totalmente el acceso a t!")
