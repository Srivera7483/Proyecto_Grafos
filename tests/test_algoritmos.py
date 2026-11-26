"""Pruebas integradas: ejecutar dentro del repositorio real del equipo.

Se usa la implementación propia de algoritmos.py, sin NetworkX.
"""

from pathlib import Path
import unittest

from app import calcular_resultados, firma_grafo
from src.models.graph_model import DirectedGraph

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


class TestIssue8Integracion(unittest.TestCase):
    def _cargar(self, archivo):
        return DirectedGraph.from_json(str(DATA_DIR / archivo))

    def test_g0(self):
        resultados = calcular_resultados(self._cargar("config_inicial.json"))
        self.assertEqual(resultados["bfs"]["length"], 4)
        self.assertEqual(resultados["disjuntos"]["max_paths"], 2)
        self.assertEqual(resultados["corte"]["cut_size"], 2)

    def test_g1(self):
        resultados = calcular_resultados(self._cargar("mod_1.json"))
        self.assertEqual(resultados["bfs"]["length"], 5)
        self.assertEqual(resultados["disjuntos"]["max_paths"], 1)
        self.assertEqual(resultados["corte"]["cut_size"], 1)

    def test_g2(self):
        resultados = calcular_resultados(self._cargar("mod_2.json"))
        self.assertEqual(resultados["bfs"]["length"], 3)
        self.assertEqual(resultados["disjuntos"]["max_paths"], 3)
        self.assertEqual(resultados["corte"]["cut_size"], 3)

    def test_desconexion(self):
        grafo = self._cargar("config_inicial.json")
        grafo.block_edge("s", "2")
        grafo.block_edge("s", "5")
        r = calcular_resultados(grafo)
        self.assertFalse(r["bfs"]["exists"])
        self.assertIsNone(r["bfs"]["length"])
        self.assertEqual(r["disjuntos"]["max_paths"], 0)
        self.assertEqual(r["corte"]["cut_size"], 0)
        self.assertEqual(r["corte"]["min_cut_edges"], [])

    def test_firma_cambia_si_cambia_la_red(self):
        grafo = self._cargar("config_inicial.json")
        original = firma_grafo(grafo)
        grafo.block_edge("s", "2")
        self.assertNotEqual(original, firma_grafo(grafo))
        grafo.unblock_edge("s", "2")
        self.assertEqual(original, firma_grafo(grafo))
        grafo.set_terminals("2", "t")
        self.assertNotEqual(original, firma_grafo(grafo))

    def test_resultados_sin_mutar_red(self):
        grafo = self._cargar("config_inicial.json")
        original = firma_grafo(grafo)
        calcular_resultados(grafo)
        self.assertEqual(original, firma_grafo(grafo))


if __name__ == "__main__":
    unittest.main()
