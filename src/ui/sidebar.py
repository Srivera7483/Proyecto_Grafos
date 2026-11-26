"""Panel lateral para modificar un DirectedGraph en memoria (Issue #7).

Mantiene separados los datos del grafo y el estado de los widgets de Streamlit.
En particular, los selectores de pasillos se reinician de forma controlada
cuando cambia la lista de arcos activos/bloqueados.
"""

from pathlib import Path

import streamlit as st

from src.models.graph_model import DirectedGraph


CONFIGURACIONES = {
    "Inicial (G0)": "config_inicial.json",
    "Alternativa (12 vértices)": "config_12v.json",
    "Modificación 1 (G1)": "mod_1.json",
    "Modificación 2 (G2)": "mod_2.json",
    "Ejercicio manual (provisional)": "ejercicio_manual.json",
}


def _cargar_desde_json(data_dir: Path, nombre_archivo: str) -> DirectedGraph:
    """Devuelve un grafo nuevo sin modificar el archivo original."""
    return DirectedGraph.from_json(str(data_dir / nombre_archivo))


def _mostrar_error_nuevo_arco(grafo: DirectedGraph, u: str, v: str, error: ValueError) -> None:
    """Explica de forma comprensible el rechazo de add_edge()."""
    arcos = grafo.get_all_edges()
    if u == v:
        st.sidebar.error("No se permiten lazos: origen y destino deben ser distintos.")
    elif (u, v) in arcos:
        st.sidebar.error(f"El pasillo {u} → {v} ya existe (activo o bloqueado).")
    elif (v, u) in arcos:
        st.sidebar.error(f"No se permiten arcos recíprocos: ya existe {v} → {u}.")
    else:
        st.sidebar.error(f"No fue posible agregar el pasillo: {error}")


def _confirmar_cambio(mensaje: str, seccion: str) -> None:
    """Reinicia selectores y muestra el éxito en su sección tras el rerun."""
    st.session_state["issue7_revision"] += 1
    st.session_state["issue7_notificacion"] = (seccion, mensaje)
    st.rerun()


def _mostrar_aviso(seccion: str) -> None:
    """Muestra una sola vez el aviso pendiente junto al control responsable."""
    notificacion = st.session_state.get("issue7_notificacion")
    if notificacion is not None and notificacion[0] == seccion:
        st.sidebar.success(notificacion[1])
        st.session_state.pop("issue7_notificacion", None)


def renderizar_panel_lateral(data_dir: Path) -> tuple[DirectedGraph, str]:
    """Renderiza controles y devuelve el grafo modificado y el archivo elegido.

    El grafo vive en session_state. Los JSON originales nunca se sobrescriben.
    """
    st.sidebar.header("Modificar red")

    nombre = st.sidebar.selectbox(
        "Configuración predefinida",
        options=list(CONFIGURACIONES),
        key="issue7_preset",
    )
    archivo = CONFIGURACIONES[nombre]

    if (
        "issue7_grafo" not in st.session_state
        or st.session_state.get("issue7_archivo") != archivo
    ):
        try:
            nuevo = _cargar_desde_json(data_dir, archivo)
        except (OSError, ValueError, TypeError, KeyError) as exc:
            st.sidebar.error(f"No se pudo cargar '{archivo}': {exc}")
            st.stop()
        st.session_state["issue7_grafo"] = nuevo
        st.session_state["issue7_archivo"] = archivo
        st.session_state["issue7_revision"] = st.session_state.get("issue7_revision", 0) + 1
        st.session_state.pop("issue7_notificacion", None)

    if st.sidebar.button("Restablecer configuración", key="issue7_reset"):
        try:
            nuevo = _cargar_desde_json(data_dir, archivo)
        except (OSError, ValueError, TypeError, KeyError) as exc:
            st.sidebar.error(f"No fue posible restablecer el grafo: {exc}")
        else:
            st.session_state["issue7_grafo"] = nuevo
            _confirmar_cambio("Configuración restaurada desde el JSON original.", "configuracion")

    grafo: DirectedGraph = st.session_state["issue7_grafo"]
    revision = st.session_state["issue7_revision"]
    vertices = sorted(grafo.vertices)

    st.sidebar.caption(
        "Los cambios se guardan solo en esta sesión; los archivos JSON no se sobrescriben. "
        "Cambiar de configuración o restablecer descarta los cambios actuales."
    )

    _mostrar_aviso("configuracion")

    st.sidebar.divider()
    st.sidebar.subheader("Entrada y salida")
    with st.sidebar.form("issue7_terminales_form"):
        fuente = st.selectbox(
            "Vértice de entrada (s)",
            vertices,
            index=vertices.index(grafo.source),
            key=f"issue7_s_{revision}",
        )
        sumidero = st.selectbox(
            "Vértice de salida (t)",
            vertices,
            index=vertices.index(grafo.sink),
            key=f"issue7_t_{revision}",
        )
        aplicar_terminales = st.form_submit_button("Aplicar entrada y salida")

    if aplicar_terminales:
        try:
            grafo.set_terminals(fuente, sumidero)
        except ValueError as exc:
            st.sidebar.error(f"No se pudieron cambiar los extremos: {exc}")
        else:
            _confirmar_cambio(f"Entrada: {fuente} · Salida: {sumidero}", "terminales")

    _mostrar_aviso("terminales")

    st.sidebar.divider()
    st.sidebar.subheader("Bloquear un pasillo")
    activos = sorted((u, v) for u, destinos in grafo.active_edges.items() for v in destinos)
    if activos:
        with st.sidebar.form("issue7_bloquear_form"):
            a_bloquear = st.selectbox(
                "Pasillo activo",
                options=activos,
                index=None,
                placeholder="Selecciona el pasillo a bloquear",
                format_func=lambda e: f"{e[0]} → {e[1]}",
                key=f"issue7_pasillo_activo_{revision}",
            )
            bloquear = st.form_submit_button("Bloquear pasillo")

        if bloquear:
            if a_bloquear is None:
                st.sidebar.warning("Selecciona primero un pasillo activo.")
            elif a_bloquear not in activos:
                st.sidebar.warning("La selección ya no está disponible. Vuelve a escoger el pasillo.")
            else:
                try:
                    grafo.block_edge(*a_bloquear)
                except ValueError as exc:
                    st.sidebar.error(f"No se pudo bloquear el pasillo: {exc}")
                else:
                    _confirmar_cambio(
                        f"Pasillo {a_bloquear[0]} → {a_bloquear[1]} bloqueado.",
                        "bloqueo",
                    )
    else:
        st.sidebar.info("No quedan pasillos activos para bloquear.")

    _mostrar_aviso("bloqueo")

    st.sidebar.subheader("Restablecer un pasillo")
    bloqueados = sorted(grafo.blocked_edges)
    if bloqueados:
        with st.sidebar.form("issue7_restaurar_form"):
            a_restaurar = st.selectbox(
                "Pasillo bloqueado",
                options=bloqueados,
                index=None,
                placeholder="Selecciona el pasillo a restablecer",
                format_func=lambda e: f"{e[0]} → {e[1]}",
                key=f"issue7_pasillo_bloqueado_{revision}",
            )
            restaurar = st.form_submit_button("Restablecer pasillo")

        if restaurar:
            if a_restaurar is None:
                st.sidebar.warning("Selecciona primero un pasillo bloqueado.")
            elif a_restaurar not in bloqueados:
                st.sidebar.warning("La selección ya no está disponible. Vuelve a escoger el pasillo.")
            else:
                try:
                    grafo.unblock_edge(*a_restaurar)
                except ValueError as exc:
                    st.sidebar.error(f"No se pudo restablecer el pasillo: {exc}")
                else:
                    _confirmar_cambio(
                        f"Pasillo {a_restaurar[0]} → {a_restaurar[1]} restablecido.",
                        "restauracion",
                    )
    else:
        st.sidebar.caption("No hay pasillos bloqueados.")

    _mostrar_aviso("restauracion")

    st.sidebar.divider()
    st.sidebar.subheader("Agregar pasillo dirigido")
    with st.sidebar.form("issue7_agregar_form"):
        origen = st.selectbox("Origen", vertices, key=f"issue7_origen_{revision}")
        destino = st.selectbox("Destino", vertices, key=f"issue7_destino_{revision}")
        agregar = st.form_submit_button("Agregar pasillo")

    if agregar:
        try:
            grafo.add_edge(origen, destino)
        except ValueError as exc:
            _mostrar_error_nuevo_arco(grafo, origen, destino, exc)
        else:
            _confirmar_cambio(f"Pasillo {origen} → {destino} agregado correctamente.", "agregar")

    _mostrar_aviso("agregar")

    return grafo, archivo
