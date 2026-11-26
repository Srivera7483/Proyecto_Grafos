"""
Punto de entrada principal del simulador interactivo de laberintos.

Modos de ejecución:
- python app.py: pruebas de backend en consola.
- python -m streamlit run app.py: simulación interactiva web con PyVis.
"""

import importlib
import os
from pathlib import Path
from typing import Any

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
    """Conserva el flujo de pruebas del backend en consola (Issue #6)."""
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

    print("\n[+] 1. Búsqueda de Camino Mínimo (BFS):")
    resultado = bfs_shortest_path(grafo)
    if resultado["exists"]:
        print("    - Estado: Camino encontrado")
        print(f"    - Longitud d_G(s, t): {resultado['length']} arcos")
        print(f"    - Secuencia de nodos: {' -> '.join(resultado['path_nodes'])}")
        print(f"    - Secuencia de arcos: {resultado['path_edges']}")
    else:
        print("    - Estado: No existe camino entre s y t.")

    print("\n[+] 2. Familia Máxima de Caminos Disjuntos en Arcos (Edmonds-Karp):")
    res_disj = max_edge_disjoint_paths(grafo)
    print(f"    - Total caminos disjuntos: {res_disj['max_paths']}")
    for i, p in enumerate(res_disj["paths"], 1):
        print(f"      * Camino {i} (longitud {p['length']}): {' -> '.join(p['path_nodes'])}")
        print(f"        Arcos: {p['path_edges']}")

    print("\n[+] 3. Corte Mínimo de Pasillos (Min-Cut):")
    res_cut = min_edge_cut(grafo)
    print(f"    - Cardinalidad mínima |C|: {res_cut['cut_size']}")
    print(f"    - Pasillos a eliminar C: {res_cut['min_cut_edges']}")
    print(f"    - Vértices alcanzables R: {res_cut['reachable_nodes']}")
    print(f"    - Vértices no alcanzables V \\ R: {res_cut['non_reachable_nodes']}")
    print(f"    - Coincidencia (|C| == max_caminos): {res_cut['cut_size'] == res_disj['max_paths']}")

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


def firma_grafo(grafo: DirectedGraph) -> tuple:
    """Identifica inequívocamente el estado sobre el cual se calculan resultados."""
    activos = {
        (u, v)
        for u, destinos in grafo.active_edges.items()
        for v in destinos
    }
    return (
        tuple(sorted(grafo.vertices)),
        tuple(sorted(activos)),
        tuple(sorted(grafo.blocked_edges)),
        grafo.source,
        grafo.sink,
    )


def calcular_resultados(grafo: DirectedGraph) -> dict[str, dict]:
    """Calcula las tres soluciones sobre un mismo estado del grafo."""
    return {
        "bfs": bfs_shortest_path(grafo),
        "disjuntos": max_edge_disjoint_paths(grafo),
        "corte": min_edge_cut(grafo),
    }


def main_streamlit() -> None:
    """Mantiene el panel Issue #7 e integra vistas y recálculo del Issue #8."""
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
        st.error("No se pudo cargar el módulo de visualización. Comprueba que PyVis esté instalado.")
        st.stop()

    # Se preserva el sidebar corregido del Issue #7 sin ninguna modificación.
    from src.ui.sidebar import renderizar_panel_lateral
    from src.ui.visualizer import (
        VISTA_RED, VISTA_BFS, VISTA_DISJUNTOS, VISTA_CORTE,
        COLOR_BFS, COLOR_CORTE, COLORES_CAMINOS,
    )

    grafo, archivo_actual = renderizar_panel_lateral(
        Path(__file__).resolve().parent / "data"
    )
    datos = grafo_a_datos_visualizacion(grafo)
    firma_actual = firma_grafo(grafo)
    # La revisión cambia al modificar el grafo, incluso si se vuelve al mismo estado.
    revision_actual = st.session_state.get("issue7_revision", 0)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Vértices", len(datos["vertices"]))
    col2.metric("Arcos", len(datos["arcos"]))
    col3.metric("Arcos activos", sum(a["activo"] for a in datos["arcos"]))
    col4.metric("Arcos bloqueados", sum(not a["activo"] for a in datos["arcos"]))

    st.write(f"**Configuración:** `{archivo_actual}`")
    st.write(f"**Entrada:** `{datos['s']}`  ·  **Salida:** `{datos['t']}`")

    # No se calculan algoritmos en cada rerun. Solo mediante el botón.
    st.subheader("Resultados algorítmicos")
    if st.button("Recalcular resultados", type="primary", key="issue8_recalcular"):
        try:
            nuevos_resultados = calcular_resultados(grafo)
        except (ValueError, RuntimeError) as exc:
            st.session_state.pop("issue8_resultados", None)
            st.error(f"No fue posible recalcular las soluciones: {exc}")
        else:
            st.session_state["issue8_resultados"] = nuevos_resultados
            st.session_state["issue8_firma"] = firma_actual
            st.session_state["issue8_revision"] = revision_actual
            st.success("Resultados actualizados para el estado actual de la red.")

    vigente = (
        st.session_state.get("issue8_firma") == firma_actual
        and st.session_state.get("issue8_revision") == revision_actual
        and "issue8_resultados" in st.session_state
    )
    resultados = st.session_state["issue8_resultados"] if vigente else None

    if resultados is None:
        st.info(
            "Todavía no hay resultados calculados para esta versión de la red. "
            "Pulsa «Recalcular resultados» para obtener las métricas y los resaltados."
        )
        if "issue8_resultados" in st.session_state:
            st.warning("La red cambió. Los resultados anteriores están desactualizados y no se muestran.")

    metr1, metr2, metr3 = st.columns(3)
    if resultados is None:
        metr1.metric("dG(s,t) · arcos", "—")
        metr2.metric("Caminos disjuntos", "—")
        metr3.metric("|C| · corte mínimo", "—")
    else:
        bfs = resultados["bfs"]
        disjuntos = resultados["disjuntos"]
        corte = resultados["corte"]
        metr1.metric("dG(s,t) · arcos", str(bfs["length"]) if bfs["exists"] else "Sin ruta")
        metr2.metric("Caminos disjuntos", disjuntos["max_paths"])
        metr3.metric("|C| · corte mínimo", corte["cut_size"])
        if not bfs["exists"]:
            st.warning("Desconexión: no existe un camino dirigido entre la entrada y la salida.")
            st.caption("No hay caminos disponibles; el corte mínimo es el conjunto vacío (|C| = 0).")
        if disjuntos["max_paths"] != corte["cut_size"]:
            st.error("Los resultados de flujo máximo y corte mínimo no coinciden. Revisar los algoritmos.")

    # La comprobación de la pauta sobre G0 no debe usar resultados anteriores.
    if archivo_actual == "config_inicial.json":
        valido, errores = grafo.validate_initial_constraints()
        if not valido:
            st.warning(
                "La red actual no cumple todas las restricciones estructurales iniciales de G0. "
                "Las modificaciones interactivas siguen permitidas."
            )
            for error in errores:
                st.write(f"- {error}")
        elif resultados is not None and resultados["disjuntos"]["max_paths"] < 2:
            st.warning("Hay menos de dos caminos independientes en arcos para los terminales elegidos.")
        elif resultados is not None:
            st.success("G0 cumple las restricciones iniciales y admite al menos dos rutas independientes.")
        else:
            st.caption("Restricciones estructurales de G0 correctas. La condición de rutas independientes se verificará al recalcular.")
    else:
        st.caption("Configuración alternativa o de prueba: no se exigen aquí los límites iniciales de G0.")

    st.subheader("Visualización del grafo dirigido")
    vista = st.radio(
        "Seleccionar vista",
        [VISTA_RED, VISTA_BFS, VISTA_DISJUNTOS, VISTA_CORTE],
        horizontal=True,
        key="issue8_vista",
    )

    if vista != VISTA_RED and resultados is None:
        st.caption("Se muestra la red sin resaltados hasta que recalcules los resultados.")
    st.iframe(
        generar_html(datos, vista=vista, resultados=resultados),
        height=580,
        alt=f"Grafo dirigido en la vista {vista}",
    )

    # Leyenda textual compatible con el modo seleccionado.
    st.caption(
        "Verde: entrada · Rojo: salida · Azul: intersección · "
        "Gris: arco activo normal · Rojo discontinuo: arco bloqueado"
    )
    if resultados is not None:
        if vista == VISTA_BFS:
            st.caption(f"🟠 Camino mínimo resaltado en naranja ({COLOR_BFS}).")
        elif vista == VISTA_CORTE:
            st.caption(f"🟣 Arcos del corte mínimo resaltados en violeta ({COLOR_CORTE}).")
        elif vista == VISTA_DISJUNTOS:
            rutas = resultados["disjuntos"]["paths"]
            if rutas:
                for i, ruta in enumerate(rutas):
                    st.markdown(
                        f"**Ruta {i + 1}** · Color `{COLORES_CAMINOS[i % len(COLORES_CAMINOS)]}`: "
                        + " → ".join(ruta["path_nodes"])
                    )
            else:
                st.caption("No hay rutas disjuntas que resaltar.")

    # Se preservan las secciones de detalle de Issue #7, pero nunca se muestran
    # con datos desactualizados.
    if resultados is not None:
        with st.expander("Resultado de Camino Mínimo (BFS)"):
            bfs = resultados["bfs"]
            if bfs["exists"]:
                st.success("Existe un camino de entrada a salida.")
                st.write(f"**Longitud mínima:** {bfs['length']} arcos")
                st.write("**Camino:** " + " → ".join(map(str, bfs["path_nodes"])))
                st.write(f"**Arcos:** `{bfs['path_edges']}`")
            else:
                st.info("No existe camino dirigido entre la entrada y la salida.")

        with st.expander("Familia Máxima de Caminos Disjuntos en Arcos (Edmonds-Karp)"):
            disjuntos = resultados["disjuntos"]
            st.write(f"**Máximo número de caminos:** {disjuntos['max_paths']}")
            for i, ruta in enumerate(disjuntos["paths"], 1):
                st.write(f"- **Ruta {i}** (longitud {ruta['length']}): " + " → ".join(ruta["path_nodes"]))
            if not disjuntos["paths"]:
                st.info("No hay caminos dirigidos disponibles.")

        with st.expander("Corte Mínimo de Pasillos (Min-Cut)"):
            corte = resultados["corte"]
            st.write(f"**Cardinalidad del corte mínimo |C|:** {corte['cut_size']}")
            st.write(f"**Pasillos del corte C:** `{corte['min_cut_edges']}`")
            st.write(f"**Vértices alcanzables R:** `{corte['reachable_nodes']}`")
            st.write(f"**Vértices no alcanzables V \\ R:** `{corte['non_reachable_nodes']}`")
            if corte["cut_size"] == resultados["disjuntos"]["max_paths"]:
                st.success("✓ |C| coincide con el número máximo de caminos disjuntos.")

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
