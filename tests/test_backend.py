"""
Pruebas unitarias y de integración para el backend algorítmico.
Proyecto: Simulador interactivo de laberintos y rutas alternativas (INFO1158).
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.models.graph_model import DirectedGraph
from src.algorithms.algorithms import (
    bfs_shortest_path,
    max_edge_disjoint_paths,
    min_edge_cut,
)


class TestDirectedGraph(unittest.TestCase):
    """Pruebas para la clase DirectedGraph y sus restricciones."""

    def setUp(self):
        self.g = DirectedGraph(vertices=["s", "A", "B", "C", "t"], source="s", sink="t")

    def test_add_edge_success(self):
        """Verifica adición exitosa de un arco dirigido."""
        self.g.add_edge("s", "A")
        self.assertIn("A", self.g.active_edges["s"])
        self.assertNotIn(("s", "A"), self.g.blocked_edges)

    def test_add_edge_nonexistent_vertex(self):
        """Verifica que no se permita agregar arcos con vértices inexistentes."""
        with self.assertRaises(ValueError):
            self.g.add_edge("s", "Z")
        with self.assertRaises(ValueError):
            self.g.add_edge("X", "A")

    def test_add_edge_self_loop(self):
        """Verifica prohibición de lazos (u == v)."""
        with self.assertRaises(ValueError):
            self.g.add_edge("A", "A")

    def test_add_edge_repeated(self):
        """Verifica prohibición de arcos duplicados."""
        self.g.add_edge("s", "A")
        with self.assertRaises(ValueError):
            self.g.add_edge("s", "A")

    def test_add_edge_reciprocal(self):
        """Verifica prohibición de arcos recíprocos (u -> v y v -> u)."""
        self.g.add_edge("s", "A")
        with self.assertRaises(ValueError):
            self.g.add_edge("A", "s")

    def test_block_and_unblock_edge(self):
        """Verifica bloqueo y desbloqueo dinámico de pasillos."""
        self.g.add_edge("s", "A")
        self.g.block_edge("s", "A")
        self.assertNotIn("A", self.g.active_edges["s"])
        self.assertIn(("s", "A"), self.g.blocked_edges)

        with self.assertRaises(ValueError):
            self.g.block_edge("s", "A")

        self.g.unblock_edge("s", "A")
        self.assertIn("A", self.g.active_edges["s"])
        self.assertNotIn(("s", "A"), self.g.blocked_edges)

        with self.assertRaises(ValueError):
            self.g.unblock_edge("s", "A")

    def test_terminals_validation(self):
        """Verifica validación de los vértices terminales s y t."""
        with self.assertRaises(ValueError):
            self.g.set_terminals("s", "Z")
        with self.assertRaises(ValueError):
            self.g.set_terminals("s", "s")

    def test_validate_initial_constraints(self):
        """Verifica las reglas de la configuración inicial con exactamente 12 vértices."""
        json_path = os.path.join(os.path.dirname(__file__), "..", "data", "config_inicial.json")
        grafo_inicial = DirectedGraph.from_json(json_path)
        valido, errores = grafo_inicial.validate_initial_constraints()
        self.assertTrue(valido, f"La configuración inicial no fue válida: {errores}")
        self.assertEqual(len(grafo_inicial.vertices), 12)
        self.assertEqual(len(grafo_inicial.get_all_edges()), 16)


class TestAlgorithms(unittest.TestCase):
    """Pruebas para BFS, Caminos Disjuntos y Corte Mínimo."""

    def setUp(self):
        json_path = os.path.join(os.path.dirname(__file__), "..", "data", "config_inicial.json")
        self.g = DirectedGraph.from_json(json_path)

    def test_bfs_shortest_path_exists(self):
        """Verifica cálculo correcto del camino mínimo en config inicial de 12 vértices."""
        res = bfs_shortest_path(self.g)
        self.assertTrue(res["exists"])
        self.assertGreaterEqual(res["length"], 1)
        self.assertEqual(res["path_nodes"][0], "s")
        self.assertEqual(res["path_nodes"][-1], "t")

    def test_bfs_disconnection_critical_case(self):
        """Verifica que el caso sin camino devuelva exactamente la estructura requerida."""
        vecinos_s = list(self.g.active_edges.get("s", set()))
        for v in vecinos_s:
            self.g.block_edge("s", v)

        res = bfs_shortest_path(self.g)
        self.assertFalse(res["exists"])
        self.assertIsNone(res["length"])
        self.assertEqual(res["path_nodes"], [])
        self.assertEqual(res["path_edges"], [])

    def test_max_edge_disjoint_paths(self):
        """Verifica el cálculo de caminos disjuntos en arcos mediante Edmonds-Karp."""
        res = max_edge_disjoint_paths(self.g)
        self.assertEqual(res["max_paths"], 2)
        self.assertEqual(len(res["paths"]), 2)

        arcos_c1 = set(res["paths"][0]["path_edges"])
        arcos_c2 = set(res["paths"][1]["path_edges"])
        self.assertEqual(arcos_c1 & arcos_c2, set(), "Los caminos comparten arcos!")

        for p in res["paths"]:
            self.assertEqual(p["path_nodes"][0], "s")
            self.assertEqual(p["path_nodes"][-1], "t")

    def test_min_edge_cut(self):
        """Verifica el cálculo del corte mínimo y la dualidad con flujo máximo."""
        res_disj = max_edge_disjoint_paths(self.g)
        res_cut = min_edge_cut(self.g)

        self.assertEqual(res_cut["cut_size"], res_disj["max_paths"])
        self.assertEqual(res_cut["cut_size"], 2)

        for u, v in res_cut["min_cut_edges"]:
            self.g.block_edge(u, v)

        res_post = bfs_shortest_path(self.g)
        self.assertFalse(res_post["exists"])

    def test_algorithms_when_disconnected(self):
        """Verifica el comportamiento cuando no existe ningún camino hacia t."""
        for v in list(self.g.active_edges.get("s", set())):
            self.g.block_edge("s", v)

        res_disj = max_edge_disjoint_paths(self.g)
        self.assertEqual(res_disj["max_paths"], 0)
        self.assertEqual(res_disj["paths"], [])

        res_cut = min_edge_cut(self.g)
        self.assertEqual(res_cut["cut_size"], 0)
        self.assertEqual(res_cut["min_cut_edges"], [])


if __name__ == "__main__":
    unittest.main()
