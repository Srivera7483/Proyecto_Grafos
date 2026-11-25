"""Pruebas unitarias de resaltados de la vista del Issue #8.

Ejecutar desde la raíz del proyecto:
    python -m unittest discover -s tests -p 'test_issue8_*.py' -v
"""

import unittest
from unittest.mock import patch

from src.ui.visualizer import (
    COLOR_ACTIVO,
    COLOR_BFS,
    COLOR_BLOQUEADO,
    COLOR_CORTE,
    COLORES_CAMINOS,
    VISTA_BFS,
    VISTA_CORTE,
    VISTA_DISJUNTOS,
    VISTA_RED,
    estilos_arcos,
    generar_html,
)


DATOS = {
    "vertices": ["s", "2", "3", "4", "t"],
    "s": "s",
    "t": "t",
    "arcos": [
        {"origen": "s", "destino": "2", "activo": True},
        {"origen": "2", "destino": "3", "activo": True},
        {"origen": "3", "destino": "t", "activo": True},
        {"origen": "s", "destino": "4", "activo": True},
        {"origen": "4", "destino": "t", "activo": True},
        {"origen": "2", "destino": "4", "activo": False},
    ],
}

RESULTADOS = {
    "bfs": {
        "exists": True, "length": 3,
        "path_nodes": ["s", "2", "3", "t"],
        "path_edges": [("s", "2"), ("2", "3"), ("3", "t")],
    },
    "disjuntos": {
        "max_paths": 2,
        "paths": [
            {"path_edges": [("s", "2"), ("2", "3"), ("3", "t")], "path_nodes": ["s", "2", "3", "t"], "length": 3},
            {"path_edges": [("s", "4"), ("4", "t")], "path_nodes": ["s", "4", "t"], "length": 2},
        ],
    },
    "corte": {
        "cut_size": 2,
        "min_cut_edges": [("s", "2"), ("s", "4")],
        "reachable_nodes": ["s"], "non_reachable_nodes": ["2", "3", "4", "t"],
    },
}


class TestIssue8Estilos(unittest.TestCase):
    def test_red_base_preserva_colores_del_issue6(self):
        estilos = estilos_arcos(DATOS, VISTA_RED, RESULTADOS)
        self.assertEqual(estilos[("s", "2")]["color"], COLOR_ACTIVO)
        self.assertEqual(estilos[("2", "4")]["color"], COLOR_BLOQUEADO)
        self.assertTrue(estilos[("2", "4")]["dashes"])

    def test_camino_minimo_solo_destaca_arcos_bfs(self):
        estilos = estilos_arcos(DATOS, VISTA_BFS, RESULTADOS)
        for arco in RESULTADOS["bfs"]["path_edges"]:
            self.assertEqual(estilos[arco]["color"], COLOR_BFS)
            self.assertEqual(estilos[arco]["width"], 6)
        self.assertNotEqual(estilos[("s", "4")]["color"], COLOR_BFS)

    def test_cada_camino_disjunto_tiene_color_propio(self):
        estilos = estilos_arcos(DATOS, VISTA_DISJUNTOS, RESULTADOS)
        self.assertEqual(estilos[("s", "2")]["color"], COLORES_CAMINOS[0])
        self.assertEqual(estilos[("s", "4")]["color"], COLORES_CAMINOS[1])
        self.assertNotEqual(estilos[("s", "2")]["color"], estilos[("s", "4")]["color"])

    def test_corte_minimo_destaca_solo_arcos_del_corte(self):
        estilos = estilos_arcos(DATOS, VISTA_CORTE, RESULTADOS)
        self.assertEqual(estilos[("s", "2")]["color"], COLOR_CORTE)
        self.assertEqual(estilos[("s", "4")]["color"], COLOR_CORTE)
        self.assertNotEqual(estilos[("3", "t")]["color"], COLOR_CORTE)

    def test_bloqueados_nunca_se_muestran_como_soluciones(self):
        adulterados = {
            **RESULTADOS,
            "bfs": {**RESULTADOS["bfs"], "path_edges": [("2", "4")]},
        }
        estilos = estilos_arcos(DATOS, VISTA_BFS, adulterados)
        self.assertEqual(estilos[("2", "4")]["color"], COLOR_BLOQUEADO)
        self.assertTrue(estilos[("2", "4")]["dashes"])

    def test_sin_resultados_se_muestra_red_neutral(self):
        estilos = estilos_arcos(DATOS, VISTA_BFS, None)
        self.assertEqual(estilos[("s", "2")]["color"], COLOR_ACTIVO)

    def test_sin_camino_ni_corte_no_inventa_resaltados(self):
        vacios = {
            "bfs": {"exists": False, "length": None, "path_edges": []},
            "disjuntos": {"max_paths": 0, "paths": []},
            "corte": {"cut_size": 0, "min_cut_edges": []},
        }
        for vista in (VISTA_BFS, VISTA_DISJUNTOS, VISTA_CORTE):
            estilos = estilos_arcos(DATOS, vista, vacios)
            self.assertEqual(estilos[("s", "2")]["color"], COLOR_ACTIVO)

    def test_vista_desconocida_se_rechaza(self):
        with self.assertRaises(ValueError):
            estilos_arcos(DATOS, "Vista incorrecta", RESULTADOS)

    def test_generar_html_compatibilidad_antigua(self):
        class RedFalsa:
            ultima = None

            def __init__(self, **kwargs):
                self.arcos = []
                RedFalsa.ultima = self

            def set_options(self, options):
                self.options = options

            def add_node(self, *args, **kwargs):
                pass

            def add_edge(self, u, v, **kwargs):
                self.arcos.append((u, v, kwargs))

            def generate_html(self):
                return "<html>OK</html>"

        with patch("src.ui.visualizer.Network", RedFalsa):
            self.assertEqual(generar_html(DATOS), "<html>OK</html>")
            self.assertEqual(len(RedFalsa.ultima.arcos), len(DATOS["arcos"]))
            for _, _, opciones in RedFalsa.ultima.arcos:
                self.assertEqual(opciones["arrows"], "to")


if __name__ == "__main__":
    unittest.main()
