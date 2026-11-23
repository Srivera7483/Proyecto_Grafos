"""
Modelo de datos para la representación y gestión de grafos dirigidos.
Proyecto: Simulador interactivo de laberintos y rutas alternativas (INFO1158).
"""

import json
import os
from typing import Any


class DirectedGraph:
    """
    Representa un laberinto modelado como un grafo dirigido G = (V, E).
    
    Gestiona la estructura de adyacencia de los vértices, los pasillos (arcos) activos
    y los pasillos bloqueados temporalmente, así como los terminales de entrada (s) y salida (t).
    
    Atributos:
        vertices (set[str]): Conjunto de identificadores de los vértices V.
        active_edges (dict[str, set[str]]): Listas de adyacencia {origen: set(destinos)} para arcos activos.
        blocked_edges (set[tuple[str, str]]): Conjunto de arcos bloqueados {(u, v), ...}.
        source (str | None): Vértice terminal de entrada (s).
        sink (str | None): Vértice terminal de salida (t).
    """

    def __init__(
        self,
        vertices: list[str] | set[str] | None = None,
        source: str | None = None,
        sink: str | None = None,
    ) -> None:
        """
        Inicializa una nueva instancia de DirectedGraph.
        
        Parámetros:
            vertices: Lista o conjunto inicial de vértices (opcional).
            source: Vértice de entrada s (opcional).
            sink: Vértice de salida t (opcional).
        """
        self.vertices: set[str] = set()
        self.active_edges: dict[str, set[str]] = {}
        self.blocked_edges: set[tuple[str, str]] = set()
        self.source: str | None = None
        self.sink: str | None = None

        if vertices is not None:
            for v in vertices:
                self.add_vertex(str(v))

        if source is not None and sink is not None:
            self.set_terminals(str(source), str(sink))
        elif source is not None:
            self.source = str(source)
        elif sink is not None:
            self.sink = str(sink)

    def add_vertex(self, v: str) -> None:
        """
        Agrega un nuevo vértice al grafo e inicializa su lista de adyacencia si no existe.
        
        Parámetros:
            v (str): Identificador del vértice.
        """
        v_str = str(v)
        if v_str not in self.vertices:
            self.vertices.add(v_str)
            self.active_edges[v_str] = set()
        elif v_str not in self.active_edges:
            self.active_edges[v_str] = set()

    def add_edge(self, u: str, v: str, active: bool = True) -> None:
        """
        Agrega un nuevo pasillo dirigido u -> v al grafo.
        
        Lanza ValueError si se viola alguna de las siguientes restricciones:
        1. u o v no pertenecen al conjunto de vértices V.
        2. Es un lazo (u == v).
        3. Es un arco repetido (ya existe en active_edges o blocked_edges).
        4. Es un arco recíproco (ya existe el arco opuesto v -> u en active_edges o blocked_edges).
        
        Parámetros:
            u (str): Vértice origen.
            v (str): Vértice destino.
            active (bool): True si el arco debe iniciar como activo, False si inicia bloqueado.
        """
        u_str, v_str = str(u), str(v)

        if u_str not in self.vertices or v_str not in self.vertices:
            raise ValueError(
                f"Error al agregar arco ({u_str}, {v_str}): los vértices deben existir en V. "
                f"Vértices faltantes: {[nodo for nodo in (u_str, v_str) if nodo not in self.vertices]}."
            )

        if u_str == v_str:
            raise ValueError(
                f"Error al agregar arco ({u_str}, {v_str}): no se permiten lazos (el origen y destino son iguales)."
            )

        if v_str in self.active_edges.get(u_str, set()) or (u_str, v_str) in self.blocked_edges:
            raise ValueError(
                f"Error al agregar arco ({u_str}, {v_str}): el arco ya existe en el grafo "
                f"(activo: {v_str in self.active_edges.get(u_str, set())}, "
                f"bloqueado: {(u_str, v_str) in self.blocked_edges})."
            )

        if u_str in self.active_edges.get(v_str, set()) or (v_str, u_str) in self.blocked_edges:
            raise ValueError(
                f"Error al agregar arco ({u_str}, {v_str}): no se permiten arcos recíprocos; "
                f"ya existe el arco opuesto ({v_str}, {u_str})."
            )

        if active:
            self.active_edges[u_str].add(v_str)
        else:
            self.blocked_edges.add((u_str, v_str))

    def block_edge(self, u: str, v: str) -> None:
        """
        Mueve un arco actualmente activo (u, v) al conjunto de arcos bloqueados (blocked_edges).
        
        Parámetros:
            u (str): Vértice origen.
            v (str): Vértice destino.
            
        Lanza:
            ValueError: Si el arco no existe en el grafo o si ya se encuentra bloqueado.
        """
        u_str, v_str = str(u), str(v)

        if (u_str, v_str) in self.blocked_edges:
            raise ValueError(f"El arco ({u_str}, {v_str}) ya se encuentra bloqueado.")

        if u_str not in self.active_edges or v_str not in self.active_edges[u_str]:
            raise ValueError(f"El arco ({u_str}, {v_str}) no existe como arco activo en el grafo.")

        self.active_edges[u_str].remove(v_str)
        self.blocked_edges.add((u_str, v_str))

    def unblock_edge(self, u: str, v: str) -> None:
        """
        Restaura un arco bloqueado (u, v) al conjunto de arcos activos (active_edges).
        
        Parámetros:
            u (str): Vértice origen.
            v (str): Vértice destino.
            
        Lanza:
            ValueError: Si el arco no se encuentra en blocked_edges.
        """
        u_str, v_str = str(u), str(v)

        if (u_str, v_str) not in self.blocked_edges:
            raise ValueError(f"El arco ({u_str}, {v_str}) no se encuentra en la lista de arcos bloqueados.")

        self.blocked_edges.remove((u_str, v_str))
        if u_str not in self.active_edges:
            self.active_edges[u_str] = set()
        self.active_edges[u_str].add(v_str)

    def set_terminals(self, s: str, t: str) -> None:
        """
        Establece o cambia los vértices terminales de entrada (s) y salida (t).
        
        Parámetros:
            s (str): Vértice de entrada.
            t (str): Vértice de salida.
            
        Lanza:
            ValueError: Si s o t no pertenecen a V, o si s == t.
        """
        s_str, t_str = str(s), str(t)

        if s_str not in self.vertices:
            raise ValueError(f"El vértice de entrada s='{s_str}' no existe en el conjunto de vértices V.")
        if t_str not in self.vertices:
            raise ValueError(f"El vértice de salida t='{t_str}' no existe en el conjunto de vértices V.")
        if s_str == t_str:
            raise ValueError(f"Los vértices de entrada y salida deben ser distintos (s != t, recibido '{s_str}').")

        self.source = s_str
        self.sink = t_str

    def load_from_json(self, filepath: str) -> None:
        """
        Carga la configuración de vértices, arcos, s y t desde un archivo JSON,
        validando rigurosamente la integridad de los datos.
        
        Parámetros:
            filepath (str): Ruta al archivo JSON (absoluta o relativa).
            
        Lanza:
            FileNotFoundError: Si el archivo no existe.
            ValueError: Si el JSON no tiene el formato esperado o viola restricciones estructurales.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"No se encontró el archivo de configuración: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            try:
                data: dict[str, Any] = json.load(f)
            except json.JSONDecodeError as err:
                raise ValueError(f"El archivo '{filepath}' no contiene un JSON válido: {err}")

        if "vertices" not in data:
            raise ValueError("El archivo JSON debe contener la clave 'vertices'.")

        source_val = data.get("s", data.get("source"))
        sink_val = data.get("t", data.get("sink"))
        if source_val is None or sink_val is None:
            raise ValueError("El archivo JSON debe especificar los terminales 's' y 't' (o 'source' y 'sink').")

        raw_edges = data.get("arcos", data.get("edges", []))

        self.vertices.clear()
        self.active_edges.clear()
        self.blocked_edges.clear()
        self.source = None
        self.sink = None

        for v in data["vertices"]:
            self.add_vertex(str(v))

        self.set_terminals(str(source_val), str(sink_val))

        for edge_info in raw_edges:
            if isinstance(edge_info, dict):
                u = edge_info.get("origen", edge_info.get("from", edge_info.get("u")))
                v = edge_info.get("destino", edge_info.get("to", edge_info.get("v")))
                active = edge_info.get("activo", edge_info.get("active", True))
            elif isinstance(edge_info, (list, tuple)) and len(edge_info) >= 2:
                u, v = edge_info[0], edge_info[1]
                active = edge_info[2] if len(edge_info) > 2 else True
            else:
                raise ValueError(f"Formato de arco desconocido en el archivo JSON: {edge_info}")

            if u is None or v is None:
                raise ValueError(f"Definición de arco incompleta en JSON: {edge_info}")

            self.add_edge(str(u), str(v), active=bool(active))

    @classmethod
    def from_json(cls, filepath: str) -> "DirectedGraph":
        """
        Método de fábrica que instancia y retorna un DirectedGraph cargado desde JSON.
        
        Parámetros:
            filepath (str): Ruta al archivo JSON.
            
        Retorna:
            DirectedGraph: Instancia inicializada con los datos del archivo.
        """
        graph = cls()
        graph.load_from_json(filepath)
        return graph

    def get_all_edges(self) -> set[tuple[str, str]]:
        """
        Retorna el conjunto de todos los arcos del grafo (activos y bloqueados).
        
        Retorna:
            set[tuple[str, str]]: Conjunto de tuplas (u, v).
        """
        all_e = set(self.blocked_edges)
        for u, neighbors in self.active_edges.items():
            for v in neighbors:
                all_e.add((u, v))
        return all_e

    def validate_initial_constraints(self) -> tuple[bool, list[str]]:
        """
        Verifica el cumplimiento de las restricciones formales para la configuración inicial
        según la especificación de la guía del proyecto:
        - 10 <= |V| <= 12
        - 14 <= |E| <= 20 (contando arcos totales del modelo)
        - s, t pertenecientes a V y s != t
        - Ningún vértice aislado (grado total in-degree + out-degree > 0)
        - Sin lazos (u == v)
        - Sin arcos repetidos ni recíprocos (u -> v y v -> u)
        
        Retorna:
            tuple[bool, list[str]]: (es_valido, lista_de_mensajes_de_error).
        """
        errors: list[str] = []
        n_vertices = len(self.vertices)
        all_edges = self.get_all_edges()
        n_edges = len(all_edges)

        if not (10 <= n_vertices <= 12):
            errors.append(
                f"Cantidad de vértices inválida: |V| = {n_vertices}. Debe cumplir 10 <= |V| <= 12."
            )

        if not (14 <= n_edges <= 20):
            errors.append(
                f"Cantidad de arcos inválida: |E| = {n_edges}. Debe cumplir 14 <= |E| <= 20."
            )

        if self.source is None or self.source not in self.vertices:
            errors.append(f"Vértice de entrada s='{self.source}' no está definido o no pertenece a V.")
        if self.sink is None or self.sink not in self.vertices:
            errors.append(f"Vértice de salida t='{self.sink}' no está definido o no pertenece a V.")
        if self.source is not None and self.sink is not None and self.source == self.sink:
            errors.append("Los vértices de entrada y salida no pueden ser iguales (s != t).")

        in_degree: dict[str, int] = {v: 0 for v in self.vertices}
        out_degree: dict[str, int] = {v: 0 for v in self.vertices}
        for u, v in all_edges:
            if u in out_degree:
                out_degree[u] += 1
            if v in in_degree:
                in_degree[v] += 1

        for v in self.vertices:
            if in_degree[v] + out_degree[v] == 0:
                errors.append(f"Vértice aislado detectado: '{v}' no tiene arcos incidentes ni salientes.")

        for u, v in all_edges:
            if u == v:
                errors.append(f"Lazo detectado en el vértice '{u}'.")
            if (v, u) in all_edges:
                errors.append(f"Arco recíproco detectado entre '{u}' y '{v}'.")

        is_valid = len(errors) == 0
        return is_valid, errors

    def __repr__(self) -> str:
        """Representación concisa del grafo en formato texto."""
        n_act = sum(len(dest) for dest in self.active_edges.values())
        return (
            f"DirectedGraph(|V|={len(self.vertices)}, |E_activos|={n_act}, "
            f"|E_bloqueados|={len(self.blocked_edges)}, s={self.source}, t={self.sink})"
        )


if __name__ == "__main__":
    print("=== Prueba rápida de DirectedGraph ===")
    g = DirectedGraph()
    for nodo in ["s", "A", "B", "t"]:
        g.add_vertex(nodo)
    g.set_terminals("s", "t")

    g.add_edge("s", "A")
    g.add_edge("A", "B")
    g.add_edge("B", "t")
    print(f"Grafo inicial: {g}")

    print("Bloqueando arco ('A', 'B')...")
    g.block_edge("A", "B")
    print(f"Arcos bloqueados: {g.blocked_edges}")
    print("Desbloqueando arco ('A', 'B')...")
    g.unblock_edge("A", "B")
    print(f"Arcos bloqueados: {g.blocked_edges}")

    try:
        g.add_edge("A", "s")
    except ValueError as e:
        print(f"Capturado error esperado de arco recíproco: {e}")

    try:
        g.add_edge("A", "A")
    except ValueError as e:
        print(f"Capturado error esperado de lazo: {e}")
