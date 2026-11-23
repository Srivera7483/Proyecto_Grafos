"""
Punto de entrada principal del simulador interactivo de laberintos.

Modos de ejecución:
- python app.py: pruebas originales de backend en consola.
- python -m streamlit run app.py: visualización web con PyVis.
"""

import importlib
import os
from typing import Any

# Importación dinámica segura para evitar diagnósticos de missing-import en el linter
st: Any = None
try:
    st = importlib.import_module("streamlit")
    _st_runtime = importlib.import_module("streamlit.runtime")
    streamlit_runtime_exists = getattr(_st_runtime, "exists", lambda: False)
    HAS_STREAMLIT = True
except (ImportError, ModuleNotFoundError):
    HAS_STREAMLIT = False
    def streamlit_runtime_exists() -> bool:
        return False

from src.models.graph_model import DirectedGraph
from src.algorithms.algorithms import (
    bfs_shortest_path,
    max_edge_disjoint_paths,
    min_edge_cut,
)
try:
    from src.ui.visualizer import (
        grafo_a_datos_visualizacion,
        generar_html,
    )
except ImportError:
    grafo_a_datos_visualizacion = None
    generar_html = None


def ruta_configuracion() -> str:
    """Devuelve la ruta absoluta del JSON original del proyecto."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "data", "config_inicial.json")


def main() -> None:
    """Conserva el flujo de pruebas del backend en consola."""
    print("=" * 65)
    print("  SIMULADOR INTERACTIVO DE LABERINTOS Y RUTAS ALTERNATIVAS")
    print("                 Teoría de Grafos - INFO1158               ")
    print("=" * 65)

    json_path = ruta_configuracion()

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

    # 1. BFS Shortest Path
    print("\n[+] 1. Búsqueda de Camino Mínimo (BFS):")
    resultado = bfs_shortest_path(grafo)
    if resultado["exists"]:
        print(f"    - Estado: Camino encontrado")
        print(f"    - Longitud d_G(s, t): {resultado['length']} arcos")
        print(f"    - Secuencia de nodos: {' -> '.join(resultado['path_nodes'])}")
        print(f"    - Secuencia de arcos: {resultado['path_edges']}")
    else:
        print("    - Estado: No existe camino entre s y t.")

    # 2. Max Edge-Disjoint Paths (Edmonds-Karp)
    print("\n[+] 2. Familia Máxima de Caminos Disjuntos en Arcos (Edmonds-Karp):")
    res_disj = max_edge_disjoint_paths(grafo)
    print(f"    - Total caminos disjuntos: {res_disj['max_paths']}")
    for i, p in enumerate(res_disj["paths"], 1):
        print(f"      * Camino {i} (longitud {p['length']}): {' -> '.join(p['path_nodes'])}")
        print(f"        Arcos: {p['path_edges']}")

    # 3. Min-Cut
    print("\n[+] 3. Corte Mínimo de Pasillos (Min-Cut):")
    res_cut = min_edge_cut(grafo)
    print(f"    - Cardinalidad mínima |C|: {res_cut['cut_size']}")
    print(f"    - Pasillos a eliminar C: {res_cut['min_cut_edges']}")
    print(f"    - Vértices alcanzables R: {res_cut['reachable_nodes']}")
    print(f"    - Vértices no alcanzables V \\ R: {res_cut['non_reachable_nodes']}")
    print(f"    - Coincidencia (|C| == max_caminos): {res_cut['cut_size'] == res_disj['max_paths']}")

    # 4. Simulación de bloqueo en vivo
    if resultado["exists"] and resultado["path_edges"]:
        arco_a_bloquear = resultado["path_edges"][0]
        print(f"\n[+] 4. Simulando bloqueo de pasillo crítico: {arco_a_bloquear}")
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


def main_streamlit() -> None:
    """Muestra el grafo real del proyecto usando Streamlit y PyVis."""
    if not HAS_STREAMLIT or st is None:
        print("Streamlit no está disponible en este entorno.")
        return

    st.set_page_config(
        page_title="Simulador de Laberintos | INFO1158",
        page_icon="🧭",
        layout="wide",
    )

    st.title("Simulador de Laberintos y Rutas Alternativas")
    st.write("Grafo dirigido del centro de almacenamiento (INFO1158).")

    if grafo_a_datos_visualizacion is None or generar_html is None:
        st.error("No se pudo cargar el módulo de visualización. Asegúrate de tener PyVis instalado.")
        return

    json_path = ruta_configuracion()
    try:
        grafo = DirectedGraph.from_json(json_path)
        datos = grafo_a_datos_visualizacion(grafo)
    except (FileNotFoundError, ValueError, TypeError, KeyError, AttributeError) as error:
        st.error(f"No se pudo cargar el grafo inicial: {error}")
        st.stop()

    valido, errores = grafo.validate_initial_constraints()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Vértices", len(datos["vertices"]))
    col2.metric("Arcos", len(datos["arcos"]))
    col3.metric("Arcos activos", sum(a["activo"] for a in datos["arcos"]))
    col4.metric("Arcos bloqueados", sum(not a["activo"] for a in datos["arcos"]))

    st.write(f"**Entrada:** `{datos['s']}`  ·  **Salida:** `{datos['t']}`")
    if valido:
        st.success("Configuración inicial válida según las restricciones implementadas en DirectedGraph.")
    else:
        st.warning("La configuración inicial no cumple todas las restricciones del proyecto.")
        for error in errores:
            st.write(f"- {error}")

    st.subheader("Visualización del grafo dirigido")
    st.iframe(
        generar_html(datos),
        height=580,
        alt="Grafo dirigido: entrada, salida y arcos activos o bloqueados",
    )
    st.caption(
        "Verde: entrada · Rojo: salida · Azul: intersección · "
        "Gris continuo: arco activo · Rojo discontinuo: arco bloqueado"
    )

    # Expander 1: BFS
    with st.expander("Resultado de Camino Mínimo (BFS)"):
        resultado = bfs_shortest_path(grafo)
        if resultado["exists"]:
            st.success("Existe un camino de entrada a salida.")
            st.write(f"**Longitud mínima:** {resultado['length']} arcos")
            st.write("**Camino:** " + " → ".join(map(str, resultado["path_nodes"])))
            st.write(f"**Arcos:** `{resultado['path_edges']}`")
        else:
            st.info("No existe camino dirigido entre la entrada y la salida.")

    # Expander 2: Caminos Disjuntos
    with st.expander("Familia Máxima de Caminos Disjuntos en Arcos (Edmonds-Karp)"):
        res_disj = max_edge_disjoint_paths(grafo)
        st.write(f"**Máximo número de caminos independientes en arcos:** {res_disj['max_paths']}")
        for i, p in enumerate(res_disj["paths"], 1):
            st.write(f"- **Ruta {i}** (longitud {p['length']}): " + " → ".join(p["path_nodes"]))

    # Expander 3: Corte Mínimo
    with st.expander("Corte Mínimo de Pasillos (Min-Cut)"):
        res_cut = min_edge_cut(grafo)
        st.write(f"**Cantidad mínima de pasillos a bloquear (|C|):** {res_cut['cut_size']}")
        st.write(f"**Pasillos del corte C:** `{res_cut['min_cut_edges']}`")
        st.write(f"**Vértices alcanzables R:** `{res_cut['reachable_nodes']}`")
        st.write(f"**Vértices no alcanzables V \\ R:** `{res_cut['non_reachable_nodes']}`")
        if res_cut["cut_size"] == res_disj["max_paths"]:
            st.success("✓ Se comprueba que |C| coincide exactamente con la cantidad máxima de caminos disjuntos.")

    with st.expander("Lista de pasillos y estados"):
        filas = [
            {
                "Origen": arco["origen"],
                "Destino": arco["destino"],
                "Estado": "Activo" if arco["activo"] else "Bloqueado",
            }
            for arco in datos["arcos"]
        ]
        st.table(filas)


if __name__ == "__main__":
    if streamlit_runtime_exists():
        main_streamlit()
    else:
        main()
