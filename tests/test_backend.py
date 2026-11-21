"""
Pruebas unitarias y de integración para el backend algorítmico.
Proyecto: Simulador interactivo de laberintos y rutas alternativas (INFO1158).
"""

import os
import sys
import unittest

# Asegurar importación de los módulos del proyecto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.models.graph_model import DirectedGraph
from src.algorithms.algorithms import bfs_shortest_path


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
        # Bloquear
        self.g.block_edge("s", "A")
        self.assertNotIn("A", self.g.active_edges["s"])
        self.assertIn(("s", "A"), self.g.blocked_edges)

        # Bloquear de nuevo debe fallar
        with self.assertRaises(ValueError):
            self.g.block_edge("s", "A")

        # Desbloquear
        self.g.unblock_edge("s", "A")
        self.assertIn("A", self.g.active_edges["s"])
        self.assertNotIn(("s", "A"), self.g.blocked_edges)

        # Desbloquear cuando ya está activo debe fallar
        with self.assertRaises(ValueError):
            self.g.unblock_edge("s", "A")

    def test_terminals_validation(self):
        """Verifica validación de los vértices terminales s y t."""
        with self.assertRaises(ValueError):
            self.g.set_terminals("s", "Z")  # Z no existe
        with self.assertRaises(ValueError):
            self.g.set_terminals("s", "s")  # s == t no permitido

    def test_validate_initial_constraints(self):
        """Verifica las reglas de la configuración inicial."""
        # Grafo con 5 vértices: debe fallar por tener menos de 10
        valido, errores = self.g.validate_initial_constraints()
        self.assertFalse(valido)
        self.assertTrue(any("vértices" in e for e in errores))

        # Cargar configuración válida desde JSON
        json_path = os.path.join(os.path.dirname(__file__), "..", "data", "config_inicial.json")
        grafo_inicial = DirectedGraph.from_json(json_path)
        valido, errores = grafo_inicial.validate_initial_constraints()
        self.assertTrue(valido, f"La configuración inicial no fue válida: {errores}")
        self.assertEqual(len(errores), 0)


class TestBFSShortestPath(unittest.TestCase):
    """Pruebas para el algoritmo de camino mínimo por BFS."""

    def setUp(self):
        json_path = os.path.join(os.path.dirname(__file__), "..", "data", "config_inicial.json")
        self.g = DirectedGraph.from_json(json_path)

    def test_shortest_path_exists(self):
        """Verifica cálculo correcto del camino mínimo en config inicial."""
        res = bfs_shortest_path(self.g)
        self.assertTrue(res["exists"])
        self.assertEqual(res["length"], 3)
        self.assertEqual(res["path_nodes"], ["s", "8", "9", "t"])
        self.assertEqual(res["path_edges"], [("s", "8"), ("8", "9"), ("9", "t")])

    def test_dynamic_rerouting_after_blocking(self):
        """Verifica que BFS recalcule una ruta alternativa cuando se bloquea un arco."""
        # Bloquear el primer arco del camino mínimo (s -> 8)
        self.g.block_edge("s", "8")
        res = bfs_shortest_path(self.g)
        self.assertTrue(res["exists"])
        self.assertEqual(res["length"], 4)
        # Camino alternativo
        self.assertEqual(res["path_nodes"][0], "s")
        self.assertEqual(res["path_nodes"][-1], "t")

    def test_disconnection_critical_case(self):
        """Verifica que el caso sin camino devuelva exactamente la estructura requerida."""
        # Bloquear todos los arcos que salen de s
        vecinos_s = list(self.g.active_edges.get("s", set()))
        for v in vecinos_s:
            self.g.block_edge("s", v)

        res = bfs_shortest_path(self.g)
        self.assertFalse(res["exists"])
        self.assertIsNone(res["length"])
        self.assertEqual(res["path_nodes"], [])
        self.assertEqual(res["path_edges"], [])


if __name__ == "__main__":
    unittest.main()
