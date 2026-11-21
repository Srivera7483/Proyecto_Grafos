"""
Punto de entrada principal para la verificación y ejecución del backend del proyecto.
Simulador interactivo de laberintos y rutas alternativas (INFO1158).
"""

import os
from src.models.graph_model import DirectedGraph
from src.algorithms.algorithms import bfs_shortest_path


def main() -> None:
    print("=" * 65)
    print("  SIMULADOR INTERACTIVO DE LABERINTOS Y RUTAS ALTERNATIVAS")
    print("                 Teoría de Grafos - INFO1158               ")
    print("=" * 65)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "data", "config_inicial.json")

    print(f"\n[+] Cargando configuración inicial desde: {json_path}")
    grafo = DirectedGraph.from_json(json_path)
    print(f"    {grafo}")

    valido, errores = grafo.validate_initial_constraints()
    print(f"\n[+] Validación de restricciones iniciales:")
    if valido:
        print("    -> ¡Configuración VÁLIDA según las reglas de la pauta!")
        print(f"       - Vértices |V|: {len(grafo.vertices)} (10 <= |V| <= 12)")
        print(f"       - Arcos |E|: {len(grafo.get_all_edges())} (14 <= |E| <= 20)")
        print(f"       - Terminales: s='{grafo.source}', t='{grafo.sink}' (s != t)")
    else:
        print("    -> Configuración INVÁLIDA:")
        for err in errores:
            print(f"       * {err}")

    print("\n[+] Búsqueda de Camino Mínimo (BFS):")
    resultado = bfs_shortest_path(grafo)
    if resultado["exists"]:
        print(f"    - Estado: Camino encontrado")
        print(f"    - Longitud d_G(s, t): {resultado['length']} arcos")
        print(f"    - Secuencia de nodos: {' -> '.join(resultado['path_nodes'])}")
        print(f"    - Secuencia de arcos: {resultado['path_edges']}")
    else:
        print("    - Estado: No existe camino entre s y t.")

    # Simulación de bloqueo en vivo
    if resultado["exists"] and resultado["path_edges"]:
        arco_a_bloquear = resultado["path_edges"][0]
        print(f"\n[+] Simulando bloqueo de pasillo crítico: {arco_a_bloquear}")
        grafo.block_edge(arco_a_bloquear[0], arco_a_bloquear[1])
        print(f"    - Arcos activos restantes: {sum(len(d) for d in grafo.active_edges.values())}")
        print(f"    - Arcos bloqueados: {list(grafo.blocked_edges)}")

        nuevo_res = bfs_shortest_path(grafo)
        print("\n[+] Recalculando ruta mínima alternativa tras el bloqueo:")
        if nuevo_res["exists"]:
            print(f"    - Nueva ruta encontrada: {' -> '.join(nuevo_res['path_nodes'])}")
            print(f"    - Nueva longitud: {nuevo_res['length']} arcos")
        else:
            print("    - No hay ruta alternativa disponible.")

        print(f"\n[+] Restaurando (desbloqueando) pasillo: {arco_a_bloquear}")
        grafo.unblock_edge(arco_a_bloquear[0], arco_a_bloquear[1])
        res_restaurado = bfs_shortest_path(grafo)
        print(f"    - Ruta restaurada con longitud: {res_restaurado['length']}")

    print("\n" + "=" * 65)
    print("  Ejecución finalizada con éxito.")
    print("=" * 65)


if __name__ == "__main__":
    main()
