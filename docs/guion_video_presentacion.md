# Guion Técnico de Grabación: Video Presentación (20 Minutos)
**Proyecto:** Simulador Interactivo de Laberintos y Rutas Alternativas  
**Asignatura:** Teoría de Grafos (INFO1158)  
**Equipo:** 3 Integrantes (Estudiante 1, Estudiante 2, Estudiante 3)  
**Duración Total Estimada:** ~19:30 a 20:00 minutos  

---

## Estructura General y Asignación de Tiempos

| Bloque | Contenido | Tiempo Estimado | Responsable Sugerido |
| :--- | :--- | :--- | :--- |
| **Intro** | Gancho audiovisual, presentación del equipo y contexto real | `00:00 - 00:45` (45 seg) | Integrante 1 |
| **Bloque 1** | Modelación matemática del laberinto, restricciones y formalización | `00:45 - 04:00` (3 min 15 s) | Integrante 1 |
| **Bloque 2** | Fundamentación teórica y selección de algoritmos (BFS, Edmonds-Karp, Min-Cut) | `04:00 - 08:30` (4 min 30 s) | Integrante 2 |
| **Bloque 3** | Arquitectura de software y demostración funcional en vivo (Red Base $G_0$) | `08:30 - 13:00` (4 min 30 s) | Integrante 3 |
| **Bloque 4** | Simulación y análisis comparativo de modificaciones (Mod 1 y Mod 2) | `13:00 - 16:30` (3 min 30 s) | Integrante 1 y 2 |
| **Bloque 5** | Verificación manual (caso de control 5 vértices) vs código | `16:30 - 18:45` (2 min 15 s) | Integrante 3 |
| **Cierre** | Conclusiones, aportes de la teoría de grafos y despedida | `18:45 - 20:00` (1 min 15 s) | Todo el equipo |

---

## GUION DETALLADO PASO A PASO

### [00:00 - 00:45] Intro Audiovisual: El Desafío de la Navegación Autónoma
- **Plano en pantalla:** 
  - *Seg 00:00 - 00:10:* Video animado o imágenes B-roll de un almacén logístico inteligente con robots AGV transitando por pasillos estrechos. Título de impacto: *"Simulador de Laberintos y Rutas Alternativas - INFO1158"*.
  - *Seg 00:10 - 00:30:* Cámara web con los 3 integrantes o pantalla dividida presentando nombres y roles.
  - *Seg 00:30 - 00:45:* Transición a una diapositiva con la red de pasillos y la pregunta motriz.
- **Locución (Integrante 1):**
  > "En la industria logística moderna, centros de almacenamiento de alta densidad dependen de robots autónomos que navegan por redes de pasillos de sentido único. Pero en un entorno operativo real, un pasillo bloqueado por mantenimiento o una colisión no solo anula un trayecto: puede aislar completamente la salida de la instalación.  
  > ¿Cómo garantizamos que un robot siempre cuente con la ruta más eficiente, cuántas alternativas verdaderamente independientes existen y cuál es el conjunto crítico de pasillos que paralizaría toda la planta?  
  > Bienvenidos a la presentación de nuestro proyecto final de Teoría de Grafos. Somos [Nombre 1], [Nombre 2] y [Nombre 3], y hoy demostraremos cómo modelar, optimizar y blindar la conectividad de un laberinto logístico utilizando teoría formal de grafos y algoritmos implementados desde cero."

---

### [00:45 - 04:00] Bloque 1: Modelación Matemática del Laberinto
- **Plano en pantalla:** 
  - Diapositiva con la formulación formal: $G = (V, E)$, definición de vértices como intersecciones y arcos dirigidos como pasillos de sentido único.
  - Tabla de restricciones impuestas por la pauta del proyecto.
  - Diagrama visual de la red inicial resaltando $s$ (verde) y $t$ (rojo).
- **Locución (Integrante 1):**
  > "Para abordar este problema, abstraemos la infraestructura física del centro de almacenamiento en un grafo dirigido $G = (V, E)$.  
  > En nuestro modelo:
  > - Cada vértice $v \in V$ representa una ubicación, bifurcación o intersección dentro del laberinto.
  > - Cada arco dirigido $e = (u, v) \in E$ representa un pasillo que solo puede recorrerse en el sentido estricto de la flecha, desde el espacio $u$ hacia el espacio $v$.
  > - Definimos dos vértices terminales distinguidos: la entrada del centro de distribución, denominada fuente o source $s$, y la salida de despacho, denominada sumidero o sink $t$, donde $s, t \in V$ y $s \neq t$."
  > 
  > *(Cambio a diapositiva con restricciones formales)*  
  > "La pauta técnica nos exige modelar una configuración inicial que cumpla rigurosamente con parámetros estructurales de diseño:
  > 1. El cardinal de vértices debe estar acotado entre 10 y 12: $10 \le |V| \le 12$. Nuestra red base contiene exactamente $|V| = 12$ nodos.
  > 2. El cardinal de arcos activos debe estar entre 14 y 20: $14 \le |E| \le 20$. Nuestra red base posee $|E| = 16$ pasillos dirigidos.
  > 3. Ausencia estricta de lazos ($u \to u$), de arcos duplicados y de arcos recíprocos entre el mismo par de nodos (es decir, no permitimos $u \to v$ y $v \to u$ simultáneos, lo que asegura sentidos únicos estrictos).
  > 4. Ningún vértice puede ser aislado: todo nodo debe participar activamente en la circulación, verificándose que $d^+(v) + d^-(v) > 0$.
  > 5. Finalmente, la red inicial debe admitir de forma garantizada **al menos dos caminos dirigidos desde $s$ hasta $t$ que no compartan ningún arco**."
  > 
  > *(Énfasis en la distinción arcos vs nodos)*  
  > "Un detalle teórico crucial: la independencia de rutas se mide en **arcos disjuntos**, no en vértices disjuntos. Dos robots pueden pasar por una misma intersección intermedia en momentos distintos, pero nunca pueden depender del mismo pasillo físico; si ese pasillo colapsa, no debe arrastrar consigo ambas trayectorias."

---

### [04:00 - 08:30] Bloque 2: Selección y Fundamentación Algorítmica
- **Plano en pantalla:** 
  - Cuadro comparativo: BFS vs DFS vs Dijkstra.
  - Esquema conceptual de la Red Residual y Algoritmo de Edmonds-Karp.
  - Esquema del Teorema de Flujo Máximo - Corte Mínimo de Ford-Fulkerson.
- **Locución (Integrante 2):**
  > "Para dar vida al simulador, investigamos, seleccionamos y justificamos tres procedimientos algorítmicos fundamentales, implementados bajo una restricción estricta: **cero uso de bibliotecas de grafos externas**. Todo el motor matemático está programado en Python estándar puro."
  > 
  > *(Sub-bloque 2.1: Camino Mínimo con BFS)*  
  > "¿Cómo encontramos la ruta más corta en cantidad de pasillos?  
  > En nuestro modelo, la métrica de costo es unitaria: cada arco suma una unidad de longitud, $d_G(s, t) = \min \{k : (s = v_0, v_1, \dots, v_k = t)\}$.  
  > Mientras que una Búsqueda en Profundidad (DFS) explora ramas arbitrarias y puede devolver un camino innecesariamente largo de orden $O(\|V\|)$, y algoritmos como Dijkstra introducen la sobrecarga de una cola de prioridad $O(\|E\| \log \|V\|)$, la **Búsqueda en Anchura (BFS)** es óptima. BFS explora el espacio por niveles concéntricos de distancia y garantiza matemáticamente hallar el camino con la menor cantidad de arcos en tiempo lineal $O(\|V\| + \|E\|)$ y memoria $O(\|V\|)$.  
  > Además, en caso de desconexión, nuestro algoritmo no devuelve infinitos engañosos, sino que reporta explícitamente `exists: False` y longitud nula."
  > 
  > *(Sub-bloque 2.2: Familia Máxima de Caminos Disjuntos en Arcos)*  
  > "El segundo desafío es calcular la máxima cantidad de rutas independientes en arcos.  
  > Un error común sería aplicar una estrategia voraz (Greedy): hallar un camino con BFS, borrar sus arcos y buscar otro. Eso falla catastróficamente porque un primer camino subóptimo puede 'bloquear' dos caminos mejores.  
  > La solución formal proviene del **Teorema de Menger para arcos** y su equivalencia con la **Formulación de Flujo Máximo**. Asignamos a cada pasillo activo una capacidad unitaria $c(u, v) = 1$. El número máximo de caminos disjuntos en arcos equivale exactamente al valor del flujo máximo entero que puede transportarse desde $s$ hasta $t$.  
  > Para resolverlo, seleccionamos el algoritmo de **Edmonds-Karp**, que implementa la búsqueda de caminos aumentantes en la red residual mediante BFS. En redes con capacidades unitarias, su complejidad es fuertemente polinomial y muy eficiente, $O(\|V\| \cdot \|E\|)$.  
  > Posteriormente, descomponemos el flujo positivo resultante extrayendo caminos dirigidos completos desde $s$ hasta $t$ y consumiendo las aristas usadas, lo que asegura que ninguna ruta resultante comparta pasillos."
  > 
  > *(Sub-bloque 2.3: Corte Mínimo de Pasillos)*  
  > "Finalmente, ¿cuál es el número mínimo de pasillos que deben bloquearse para aislar completamente a $s$ de $t$?  
  > Por el célebre **Teorema de Flujo Máximo - Corte Mínimo** (Ford y Fulkerson), la capacidad de un corte mínimo coincide exactamente con el valor del flujo máximo.  
  > Para extraer el conjunto de pasillos $C \subseteq E$, analizamos la red residual final generada por Edmonds-Karp. Ejecutamos un recorrido desde $s$ siguiendo únicamente aristas con capacidad residual positiva, determinando el subconjunto $R \subset V$ de vértices alcanzables. Como no hay camino aumentante, $t \notin R$.  
  > El corte mínimo de pasillos está conformado exactamente por todos los arcos originales activos $(u, v)$ tales que $u \in R$ y $v \notin R$. La eliminación de estos pasillos en $G - C$ interrumpe toda conectividad hacia la salida."

---

### [08:30 - 13:00] Bloque 3: Arquitectura y Demostración Funcional en Vivo
- **Plano en pantalla:** 
  - Captura de pantalla de la arquitectura de carpetas: `src/models/`, `src/algorithms/`, `src/ui/`, `data/`.
  - Terminal ejecutando las pruebas unitarias: `python -m unittest tests/test_backend.py`.
  - Navegador web abriendo la aplicación interactiva Streamlit (`python -m streamlit run app.py`).
- **Locución (Integrante 3):**
  > "Pasemos a la demostración en vivo de nuestra aplicación y su arquitectura de software.  
  > Estructuramos el proyecto siguiendo el principio de responsabilidad única:
  > - En `src/models/graph_model.py`, la clase `DirectedGraph` encapsula las listas de adyacencia activa, el conjunto de arcos bloqueados y valida en cada inserción que no se violen las reglas de lazos o arcos recíprocos.
  > - En `src/algorithms/algorithms.py`, residen las funciones puras `bfs_shortest_path`, `max_edge_disjoint_paths` y `min_edge_cut`.
  > - Y en `app.py` junto con `src/ui/visualizer.py`, integramos **Streamlit** y **PyVis** para renderizar un grafo interactivo dinámico, permitiendo arrastrar nodos, ver estados de pasillos y consultar resultados."
  > 
  > *(En pantalla: Ejecución de las 13 pruebas unitarias en consola)*  
  > "Antes de ver la interfaz, observemos la terminal: ejecutamos nuestras pruebas unitarias automatizadas. 13 tests pasan en menos de 10 milisegundos, validando la captura de excepciones, el bloqueo de arcos, la consistencia de los caminos disjuntos y la verificación de desconexión."
  > 
  > *(En pantalla: Interfaz Web Streamlit con la Configuración Inicial $G_0$)*  
  > "Ahora vemos en pantalla la interfaz interactiva con la **Configuración Inicial ($G_0$)**.  
  > En las métricas superiores confirmamos:
  > - 12 vértices totales.
  > - 16 arcos activos, 0 bloqueados.
  > - Entrada en verde ($s$), salida en rojo ($t$), intersecciones en azul.
  > 
  > Al desplegar la sección de **Camino Mínimo (BFS)**, el sistema nos indica:
  > - Longitud mínima: **4 arcos**.
  > - Ruta exacta: $s \to 2 \to 3 \to 7 \to t$.
  > 
  > Al abrir la sección de **Caminos Disjuntos en Arcos (Edmonds-Karp)**:
  > - El flujo máximo unitario es **2**, lo que confirma la existencia de 2 rutas independientes:
  >   1. Ruta 1: $s \to 2 \to 3 \to 7 \to t$ (longitud 4).
  >   2. Ruta 2: $s \to 5 \to 6 \to 7 \to 8 \to t$ (longitud 5).  
  > Noten un detalle fascinante: ¡ambas rutas pasan por el nodo 7! Sin embargo, la Ruta 1 utiliza los arcos $(3, 7)$ y $(7, t)$, mientras que la Ruta 2 utiliza $(6, 7)$ y $(7, 8)$. Comparten una intersección, pero **ningún pasillo**. Son 100% disjuntas en arcos.
  > 
  > Finalmente, en la sección de **Corte Mínimo**:
  > - El conjunto crítico identificado es $C = \{(s, 2), (s, 5)\}$, con cardinalidad $|C| = 2$.
  > - El sistema comprueba automáticamente la igualdad: el tamaño del corte (2) coincide con el número de caminos disjuntos (2)."

---

### [13:00 - 16:30] Bloque 4: Simulación y Análisis de Modificaciones en la Red
- **Plano en pantalla:** 
  - Demostración de interacción: bloqueo en caliente de pasillos.
  - Carga de `mod_1.json` en la interfaz.
  - Carga de `mod_2.json` en la interfaz.
  - Gráfico comparativo de resiliencia entre las 3 configuraciones.
- **Locución (Integrante 1 y 2):**
  > *(Integrante 1)*  
  > "Una de las mayores fortalezas del simulador es la capacidad de analizar modificaciones dinámicas sin alterar el código fuente. Analizaremos las dos variantes solicitadas en la pauta manteniendo siempre los mismos terminales $s$ y $t$."
  > 
  > *(Carga de Modificación 1: Bloqueo de Pasillo Directo $7 \to t$)*  
  > "En la **Modificación 1**, simulamos una contingencia operativa: el pasillo directo de salida $7 \to t$ queda inhabilitado (línea roja discontinua en el visualizador).  
  > ¿Qué ocurre con la red?
  > - El camino mínimo ahora se ve forzado a desviarse: pasa a ser $s \to 2 \to 3 \to 4 \to 8 \to t$, aumentando su longitud a **5 arcos**.
  > - Más crítico aún: la familia máxima de caminos independientes colapsa de 2 a **1 solo camino disjunto**. El nodo 8 se convierte en un cuello de botella absoluto porque es el único que puede acceder a $t$.
  > - El corte mínimo se reduce a $|C| = 1$, conformado únicamente por el pasillo $\{(8, t)\}$. La red se ha vuelto extremadamente frágil: basta que falle una sola conexión para aislar la salida por completo."
  > 
  > *(Integrante 2 - Carga de Modificación 2: Expansión de Capacidad)*  
  > "En la **Modificación 2**, evaluamos una propuesta de mejora en la infraestructura: añadimos dos nuevos pasillos estratégicos: un atajo desde la entrada $s \to 6$ y un acceso directo desde el fondo $11 \to t$, alcanzando 18 arcos en total.  
  > Los resultados demuestran un salto sustancial en resiliencia:
  > - La red ahora admite **3 caminos disjuntos en arcos simultáneos**:
  >   1. $s \to 2 \to 3 \to 4 \to 8 \to t$
  >   2. $s \to 6 \to 7 \to t$
  >   3. $s \to 5 \to 9 \to 10 \to 11 \to t$
  > - El corte mínimo aumenta correspondientemente a $|C| = 3$. Se necesitaría bloquear al menos tres pasillos simultáneos para interrumpir el flujo.  
  > Esto demuestra cuantitativamente cómo la teoría de grafos permite a los ingenieros de operaciones justificar inversiones en infraestructura basándose en redundancia y tolerancia a fallos."

---

### [16:30 - 18:45] Bloque 5: Verificación Matemática y Caso Manual
- **Plano en pantalla:** 
  - Diapositiva con el grafo de control reducido de 5 vértices: $V = \{s, A, B, C, t\}$.
  - Demostración de resolución analítica a mano paso a paso.
  - Salida de la consola del script ejecutando el caso manual comprobando que los resultados coinciden.
- **Locución (Integrante 3):**
  > "La sección 5 de la rúbrica exige construir y resolver manualmente un caso independiente de entre 4 y 6 vértices para contrastar los fundamentos analíticos contra el código del backend.  
  > Diseñamos una red de control con 5 vértices: $V = \{s, A, B, C, t\}$ y 6 arcos:
  > $E = \{(s, A), (s, B), (A, C), (B, C), (B, t), (C, t)\}$.
  > 
  > *(Resolución analítica en pantalla)*  
  > 1. **Camino Mínimo:**  
  >    Inspeccionando los caminos posibles:
  >    - Camino 1: $s \to B \to t$ (longitud 2).
  >    - Camino 2: $s \to A \to C \to t$ (longitud 3).
  >    - Camino 3: $s \to B \to C \to t$ (longitud 3).  
  >    El camino de longitud mínima es unívocamente $s \to B \to t$ con $d_G(s, t) = 2$.
  > 
  > 2. **Caminos Disjuntos en Arcos:**  
  >    Los caminos $P_1 = (s, B, t)$ y $P_2 = (s, A, C, t)$ utilizan los conjuntos de arcos $E(P_1) = \{(s, B), (B, t)\}$ y $E(P_2) = \{(s, A), (A, C), (C, t)\}$.  
  >    Su intersección es vacía: $E(P_1) \cap E(P_2) = \emptyset$.  
  >    Por lo tanto, existen al menos 2 caminos disjuntos. Como el grado de salida de la fuente es $d^+(s) = 2$ y el de entrada al sumidero es $d^-(t) = 2$, es imposible que existan 3. La familia es estrictamente máxima con cardinalidad 2.
  > 
  > 3. **Corte Mínimo:**  
  >    Si eliminamos el conjunto de pasillos $C = \{(B, t), (C, t)\}$, todo acceso a $t$ queda clausurado. Su cardinalidad es $|C| = 2$.  
  >    Dado que el número de caminos disjuntos es 2 y encontramos un corte de tamaño 2, por el teorema de dualidad garantizamos que 2 es la cota óptima absoluta.
  > 
  > *(Contraste con el algoritmo)*  
  > Al ingresar esta matriz a nuestro backend, `bfs_shortest_path` arrojó exactamente longitud 2 y `max_edge_disjoint_paths` retornó exactamente las dos rutas manuales, validando formalmente la exactitud de nuestra implementación."

---

### [18:45 - 20:00] Cierre y Conclusiones
- **Plano en pantalla:** 
  - Diapositiva con conclusiones finales y resumen de aportes.
  - Cámara web con los 3 integrantes despidiéndose.
- **Locución (Integrantes 1, 2 y 3 alternados):**
  > *(Integrante 1)*  
  > "En conclusión, este proyecto demuestra que la Teoría de Grafos no es solo un marco abstracto, sino una herramienta computacional poderosa para resolver problemas críticos en robótica y logística."  
  > 
  > *(Integrante 2)*  
  > "Comprobamos que implementar algoritmos desde cero nos otorga un entendimiento profundo sobre la estructura interna de la red residual, la búsqueda en anchura determinista y el balance entre eficiencia de ruta y redundancia ante fallos."  
  > 
  > *(Integrante 3)*  
  > "El simulador entrega una respuesta visual e interactiva clara: permite predecir cuellos de botella, planificar expansiones de pasillos y asegurar que, ante cualquier imprevisto, la operación continúe sin interrupciones.  
  > Muchas gracias por su atención, y quedamos atentos a sus preguntas."
  > 
  > *(Placa final con repositorio de GitHub y créditos de los integrantes)*

---

## Consejos Técnicos para la Grabación del Video

1. **Software recomendado:** OBS Studio para alternar escenas entre presentación (PowerPoint/Canva), navegador (Streamlit en `localhost:8501`) y terminal (pruebas unitarias).
2. **Audio:** Usar micrófonos de solapa o auriculares con cancelación de ruido. Hablar a ritmo constante (aproximadamente 130 a 140 palabras por minuto).
3. **Pausas y transiciones:** No apresurarse entre secciones; respetar los silencios breves de 1-2 segundos al cambiar de diapositiva o de orador para facilitar la edición.
4. **Verificación previa:** Comprobar que Streamlit esté corriendo (`python -m streamlit run app.py`) antes de presionar grabar para evitar demoras de inicio en pantalla.
