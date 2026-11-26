# Guion Técnico de Grabación: Video Presentación (20 Minutos)
**Proyecto:** Simulador Interactivo de Laberintos y Rutas Alternativas  
**Asignatura:** Teoría de Grafos (INFO1158)  
**Alineación:** Estructurado rigurosamente en base al **Informe Técnico del Proyecto** (`docs/Borrador Informe Markdown.md`)  
**Equipo:** 
- **Integrante 1:** Diego Hernández
- **Integrante 2:** Antonio Lara
- **Integrante 3:** Sebastián Rivera  
**Duración Total Estimada:** 19:30 a 20:00 minutos  

---

## Tabla de Tiempos y Correspondencia con el Informe

| Segmento | Tiempo Estimado | Sección del Informe Técnico | Responsable |
| :--- | :--- | :--- | :--- |
| **Intro** | `00:00 - 00:45` (45 seg) | Introducción y Planteamiento del Centro de Almacenamiento | **Diego Hernández** |
| **Bloque 1** | `00:45 - 04:00` (3 min 15 seg) | **Sección 1:** Modelación matemática del laberinto ($G_0$, $V$, $E$ y restricciones) | **Diego Hernández** |
| **Bloque 2** | `04:00 - 08:30` (4 min 30 seg) | **Sección 2:** Algoritmos de análisis (BFS vs DFS, Greedy vs Edmonds-Karp, Menger y Min-Cut) | **Antonio Lara** |
| **Bloque 3** | `08:30 - 13:00` (4 min 30 seg) | **Implementación y Software:** Demostración interactiva en vivo sobre la Red Base $G_0$ | **Sebastián Rivera** |
| **Bloque 4** | `13:00 - 16:30` (3 min 30 seg) | **Simulación de Modificaciones:** Modificación 1 ($7 \to t$) y Modificación 2 ($s \to 6$, $11 \to t$) | **Diego Hernández y Antonio Lara** |
| **Bloque 5** | `16:30 - 18:45` (2 min 15 seg) | **Verificación de Resultados:** Caso de control manual independiente vs código | **Sebastián Rivera** |
| **Cierre** | `18:45 - 20:00` (1 min 15 seg) | Conclusiones finales y cierre formal | **Diego, Antonio y Sebastián** |

---

## GUION DETALLADO DE GRABACIÓN

### [00:00 - 00:45] Intro Audiovisual: El Problema de la Circulación Unidireccional
- **Recurso en pantalla:** 
  - *00:00 - 00:15:* Logo de la universidad / asignatura. Video de apoyo o animación de robots de inspección circulando por un centro de distribución. Título: *"Simulador interactivo de laberintos y rutas alternativas - INFO1158"*.
  - *00:15 - 00:35:* Tomas de los 3 expositores en cámara con sus nombres en un cintillo inferior (Diego Hernández, Antonio Lara y Sebastián Rivera).
  - *00:35 - 00:45:* Transición a la portada formal del informe técnico.
- **Locución (Diego Hernández):**
  > "Muy buenos días, profesor y compañeros. En los centros de almacenamiento logístico modernos, la inspección automatizada depende de robots que se desplazan por pasillos de sentido único, conectados mediante intersecciones y áreas de carga.  
  > En este esquema, cada misión exige trasladarse desde una entrada establecida hasta una salida obligatoria. Sin embargo, si un pasillo colapsa o se bloquea temporalmente, múltiples rutas pueden quedar inutilizadas al mismo tiempo.  
  > En base al informe técnico desarrollado para la asignatura Teoría de Grafos, presentaremos la modelación matemática, los fundamentos algorítmicos y la simulación interactiva de nuestro sistema. Somos el equipo integrado por Diego Hernández, Antonio Lara y Sebastián Rivera, y este es el análisis formal de nuestro proyecto."

---

### [00:45 - 04:00] Bloque 1: Modelación Matemática del Laberinto (Sección 1 del Informe)
- **Recurso en pantalla:** 
  - Diapositiva con la formulación de la Sección 1.1 del informe: grafo $G_0 = (V, E)$, definición explícita de $V$ (12 vértices) y de $E$ (16 arcos).
  - Resaltado de las restricciones de la Sección 1.2: ausencia de lazos, no multiplicidad, unidireccionalidad estricta y fórmula de conectividad $\delta^-(v) + \delta^+(v) \ge 1$.
  - Esquema visual del vértice $7$ como nodo de cruce central.
- **Locución (Diego Hernández):**
  > "Tal como establecemos en la Sección 1 de nuestro informe técnico, modelamos el centro de almacenamiento mediante un grafo dirigido simple denominado $G_0 = (V, E)$.  
  > 
  > En primer lugar, definimos el **conjunto de vértices** $V$, que representa las posiciones físicas o intersecciones del laberinto. Nuestro modelo cuenta con exactamente $|V| = 12$ vértices, satisfaciendo la cota $10 \le |V| \le 12$:  
  > $$V = \{s, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, t\}$$  
  > Dentro de este conjunto, distinguimos formalmente los dos nodos terminales:  
  > - $s \in V$: Punto de entrada o estación de despacho donde el robot inicia la inspección.  
  > - $t \in V$: Punto de salida o estación de destino donde finaliza el trayecto, cumpliéndose que $s \neq t$.  
  > 
  > Por su parte, el **conjunto de arcos dirigidos** $E$ representa los pasillos de sentido único que conectan pares ordenados de intersecciones $(u, v) \in V \times V$, indicando que el desplazamiento está permitido únicamente desde $u$ hacia $v$. Nuestra configuración inicial consta de $|E| = 16$ arcos, cumpliendo con la restricción $14 \le |E| \le 20$:  
  > $$E = \{(s,2), (s,5), (2,3), (2,6), (3,4), (3,7), (4,8), (5,6), (5,9), (6,7), (7,8), (7,t), (8,t), (9,10), (10,11), (11,7)\}$$  
  > 
  > *(Transición a la Sección 1.2 del informe: Restricciones adicionales)*  
  > En la Sección 1.2 del informe demostramos que la red $G_0$ satisface todas las condiciones estructurales requeridas:  
  > 1. **Ausencia de lazos:** $\forall v \in V, (v, v) \notin E$. Ningún pasillo conecta una intersección consigo misma.  
  > 2. **Ausencia de arcos repetidos:** $E$ es un conjunto simple sin arcos paralelos entre el mismo par ordenado $(u, v)$.  
  > 3. **Ausencia de arcos recíprocos:** Para todo $(u, v) \in E$, se verifica que $(v, u) \notin E$, lo que garantiza que la circulación física sea estrictamente unidireccional.  
  > 4. **Conectividad total (sin vértices aislados):** Cada vértice $v \in V$ tiene un grado total $\delta^-(v) + \delta^+(v) \ge 1$, asegurando que toda intersección cuente con al menos un pasillo incidente o saliente.  
  > 5. **Existencia de múltiples rutas disjuntas en arcos:** La red admite al menos dos caminos dirigidos independientes desde $s$ hasta $t$. En particular, como analizamos en el informe, el vértice 7 actúa como un nodo de cruce central estratégico: permite que las rutas $P_1 = (s, 2, 3, 7, 8, t)$ y $P_2 = (s, 5, 6, 7, t)$ compartan la intersección intermedia 7, pero sin compartir ningún arco dirigido."

---

### [04:00 - 08:30] Bloque 2: Algoritmos de Análisis y Selección Teórica (Sección 2 del Informe)
- **Recurso en pantalla:** 
  - Tabla comparativa exacta de la Sección 2.1 del informe: BFS vs DFS (Estructura, Orden, Optimalidad, Complejidad).
  - Diagrama de exploración por capas de BFS vs avances/regresiones de DFS.
  - Sección 2.2: Esquema del fallo del algoritmo voraz (*Greedy*) y los 4 pasos del algoritmo de Edmonds-Karp.
  - Sección 2.3: Ecuación del Teorema de Menger y extracción del corte mínimo $C$ mediante el subconjunto residual $S$.
- **Locución (Antonio Lara):**
  > "En la Sección 2 de nuestro informe analizamos teóricamente las estrategias algorítmicas, justificando la selección de los métodos idóneos.  
  > 
  > *(Sub-bloque 2.1: Camino con menor número de arcos - BFS vs DFS)*  
  > En nuestro modelo, la métrica es no ponderada: cada pasillo representa una unidad de longitud. Al comparar la Búsqueda en Anchura (BFS) frente a la Búsqueda en Profundidad (DFS):  
  > - BFS utiliza una cola FIFO y explora el grafo por capas concéntricas de distancia creciente desde $s$.  
  > - Como explicamos en el informe, cada nivel sucesivo incrementa en 1 la distancia del vértice padre, garantizando que el instante en que alcanzamos $t$ corresponde matemáticamente al camino con la menor cantidad de arcos, con complejidad temporal óptima $O(|V| + |E|)$ y espacial $O(|V|)$ (Cormen et al., 2022).  
  > - Por el contrario, DFS utiliza una pila LIFO o recursión y desciende por ramas arbitrarias. Puede encontrar una ruta muy larga hacia $t$ antes de explorar un atajo directo. Por tanto, DFS no garantiza optimalidad y sus usos serían otros, como labores de patrullaje total o detección de ciclos.  
  > Reconstruimos la secuencia óptima mediante el arreglo `parent[v]`. Si $t$ no es alcanzado, nuestro algoritmo reporta explícitamente `exists: False` sin asignar valores numéricos ficticios.  
  > 
  > *(Sub-bloque 2.2: Máximo número de caminos disjuntos en arcos)*  
  > En la Sección 2.2 comparamos dos enfoques para calcular cuántas rutas independientes pueden coexistir:  
  > 1. **Búsqueda voraz (_Greedy_) iterativa:** Consiste en hallar un camino con BFS, eliminar sus arcos y repetir. Demostramos en el informe por qué esto **falla**: si un camino transversal temprano consume un arco de una primera ruta óptima y otro arco de una segunda ruta óptima, bloquea ambas a la vez, reduciendo el total global encontrado.  
  > 2. **Formulación de Flujo Máximo Unitario (Edmonds-Karp):**  
  > Modelamos cada pasillo con capacidad unitaria $c(u, v) = 1$. Por los fundamentos de Cormen et al. (2022) y Kleinberg & Tardos (2006), el caudal máximo equivale exactamente al cardinal máximo de caminos dirigidos disjuntos en arcos.  
  > El algoritmo de Edmonds-Karp opera en 4 fases rigurosas:  
  >    - **Búsqueda libre por BFS:** Halla la trayectoria aumentante más corta en la red residual con capacidad $c_f > 0$.  
  >    - **Asignación de flujo y arco residual inverso:** Al saturar un pasillo ($c_f(u, v) = 0$), habilita un arco inverso $(v, u)$ con capacidad 1.  
  >    - **Función de cancelación:** Si una iteración posterior utiliza $(v, u)$, anula la asignación previa en $(u, v)$ y desvía el flujo por otra ruta libre, evitando óptimos locales.  
  >    - **Iteración hasta saturación:** Repite hasta que no existan caminos aumentantes hacia $t$.  
  > 
  > *(Sub-bloque 2.3: Corte Mínimo y Teorema de Menger)*  
  > En la Sección 2.3 del informe formalizamos el corte mínimo como el conjunto de pasillos cuya eliminación desconecta a $s$ de $t$.  
  > Por el **Teorema de Menger** en su versión dirigida por arcos (Diestel, 2017), y su generalización en el **Teorema de Flujo Máximo–Corte Mínimo** de Ford y Fulkerson (1956):  
  > $$\max |\mathcal{P}_{s,t}| = \min \{|C| : C \subseteq E,\; \text{no existe camino de } s \text{ a } t \text{ en } G - C\}$$  
  > Para extraer $C$ en el código, ejecutamos un BFS en la red residual final desde $s$, determinando el conjunto de vértices alcanzables $S \subseteq V$. Los pasillos del corte son aquellos arcos originales que van desde $S$ hacia su complemento $V \setminus S$:  
  > $$C = \{(u, v) \in E : u \in S \land v \in V \setminus S\}$$  
  > Su cardinalidad $|C|$ coincide exactamente con el valor del flujo máximo."

---

### [08:30 - 13:00] Bloque 3: Demostración Interactiva en Vivo (Red Base $G_0$)
- **Recurso en pantalla:** 
  - Terminal ejecutando la suite de pruebas: `python -m unittest tests/test_backend.py`.
  - Navegador web con la aplicación en Streamlit (`python -m streamlit run app.py`).
  - Grafo interactivo en PyVis: mostrando los 12 nodos, 16 arcos activos, terminales en verde ($s$) y rojo ($t$).
  - Despliegue de los expansores con los resultados calculados.
- **Locución (Sebastián Rivera):**
  > "Pasamos ahora a contrastar la teoría del informe con el funcionamiento en tiempo real de nuestra aplicación.  
  > 
  > *(Terminal en pantalla)*  
  > En la terminal observamos la ejecución de nuestras pruebas unitarias automatizadas (`test_backend.py`). 13 pruebas pasan exitosamente, certificando que el modelo rechaza lazos, arcos recíprocos y duplicados, y que maneja correctamente los casos borde de desconexión.  
  > 
  > *(Navegador web en pantalla con Streamlit)*  
  > En pantalla tenemos el simulador interactivo montado sobre Streamlit y PyVis, cargando automáticamente `config_inicial.json` ($G_0$).  
  > El panel de métricas confirma: 12 vértices, 16 arcos activos, entrada en verde en el nodo $s$ y salida en rojo en el nodo $t$.  
  > 
  > *(Consultando Camino Mínimo BFS)*  
  > Al consultar el **Camino Mínimo**, el algoritmo BFS arroja:  
  > - Longitud mínima: **4 arcos**.  
  > - Secuencia de nodos: $s \to 2 \to 3 \to 7 \to t$.  
  > - Arcos recorridos: $(s, 2), (2, 3), (3, 7), (7, t)$.  
  > 
  > *(Consultando Caminos Disjuntos)*  
  > Al abrir la sección de **Caminos Disjuntos por Edmonds-Karp**:  
  > - Se confirma un flujo máximo de **2**, extrayendo 2 trayectorias disjuntas en arcos:  
  >   - **Ruta 1:** $s \to 2 \to 3 \to 7 \to t$ (longitud 4).  
  >   - **Ruta 2:** $s \to 5 \to 6 \to 7 \to 8 \to t$ (longitud 5).  
  > Coincide de manera exacta con lo predicho en la Sección 1.2 del informe: ambas rutas pasan por el nodo 7, pero ninguna comparte arcos.  
  > 
  > *(Consultando Corte Mínimo)*  
  > Al consultar el **Corte Mínimo de Pasillos**:  
  > - Se obtiene el conjunto $C = \{(s, 2), (s, 5)\}$, con cardinalidad $|C| = 2$.  
  > - El conjunto de vértices alcanzables en la red residual es $S = \{s\}$.  
  > - Se comprueba que $|C| = 2$ es idéntico a la cantidad de caminos disjuntos ($2$).  
  > Si en la simulación bloqueamos ambos pasillos, la red queda totalmente desconectada, confirmando la validez del teorema."

---

### [13:00 - 16:30] Bloque 4: Simulación y Análisis de Modificaciones (Mod 1 y Mod 2)
- **Recurso en pantalla:** 
  - Interfaz web cargando `mod_1.json` (bloqueo de pasillo directo $7 \to t$).
  - Recálculo en vivo de BFS, caminos disjuntos y corte mínimo.
  - Interfaz web cargando `mod_2.json` (adición de pasillos $s \to 6$ y $11 \to t$).
  - Cuadro comparativo entre las tres configuraciones ($G_0$, Mod 1, Mod 2).
- **Locución (Diego Hernández y Antonio Lara):**
  > *(Diego Hernández - Modificación 1)*  
  > "Siguiendo los requerimientos del proyecto, comparamos la red base contra dos modificaciones conservando los mismos terminales $s$ y $t$.  
  > 
  > En la **Modificación 1** (`mod_1.json`), simulamos la inhabilitación del pasillo directo a la salida $(7, t)$, representado con línea roja discontinua en el visualizador.  
  > Al presionar recalcular:  
  > - El camino mínimo se ve obligado a desviarse hacia el nodo 8: $s \to 2 \to 3 \to 4 \to 8 \to t$, aumentando su longitud a **5 arcos**.  
  > - La disponibilidad de rutas independientes colapsa de 2 a **1 solo camino disjunto**.  
  > - El corte mínimo se reduce a $|C| = 1$, conformado únicamente por el pasillo $\{(8, t)\}$.  
  > Esto demuestra que el bloqueo de un pasillo clave crea un cuello de botella absoluto en el nodo 8, volviendo la red sumamente vulnerable ante cualquier falla adicional."  
  > 
  > *(Antonio Lara - Modificación 2)*  
  > "En la **Modificación 2** (`mod_2.json`), evaluamos una expansión de capacidad: agregamos un nuevo pasillo desde la entrada $(s, 6)$ y una salida directa desde el cuadrante inferior $(11, t)$, alcanzando 18 arcos en total.  
  > Al recalcular:  
  > - La red ahora admite **3 caminos disjuntos en arcos simultáneos**:  
  >   1. $s \to 2 \to 3 \to 4 \to 8 \to t$  
  >   2. $s \to 6 \to 7 \to t$  
  >   3. $s \to 5 \to 9 \to 10 \to 11 \to t$  
  > - La cardinalidad del corte mínimo se eleva a $|C| = 3$.  
  > Esta modificación no solo agiliza el tránsito de los robots, sino que triplica la tolerancia a fallos del almacén: se requeriría el colapso simultáneo de tres pasillos distintos para interrumpir las operaciones de despacho."

---

### [16:30 - 18:45] Bloque 5: Verificación de Resultados y Caso Manual (Sección 5 de la Rúbrica)
- **Recurso en pantalla:** 
  - Diapositiva con el grafo de control reducido de 5 vértices: $V = \{s, A, B, C, t\}$ y 6 arcos.
  - Tabla de resolución manual analítica (inspección de caminos, arcos disjuntos y corte mínimo).
  - Terminal ejecutando el algoritmo sobre el caso manual y verificando que la salida coincide 100%.
- **Locución (Sebastián Rivera):**
  > "Para cumplir con la verificación matemática exigida por la pauta, construimos un caso de control independiente de 5 vértices que puede resolverse rigurosamente a mano:  
  > $$V = \{s, A, B, C, t\}, \quad E = \{(s, A), (s, B), (A, C), (B, C), (B, t), (C, t)\}$$  
  > 
  > *(Resolución manual analítica)*  
  > 1. **Camino Mínimo:**  
  >    Enumerando las rutas dirigidas posibles:  
  >    - Ruta 1: $s \to B \to t$ (longitud 2).  
  >    - Ruta 2: $s \to A \to C \to t$ (longitud 3).  
  >    - Ruta 3: $s \to B \to C \to t$ (longitud 3).  
  >    Por simple inspección, el camino de longitud mínima es $s \to B \to t$ con $d_G(s, t) = 2$.  
  > 
  > 2. **Familia de Caminos Disjuntos:**  
  >    Tomamos las rutas $P_1 = (s, B, t)$ y $P_2 = (s, A, C, t)$.  
  >    Sus conjuntos de arcos son $E(P_1) = \{(s, B), (B, t)\}$ y $E(P_2) = \{(s, A), (A, C), (C, t)\}$.  
  >    Como $E(P_1) \cap E(P_2) = \emptyset$, son completamente disjuntos en arcos. Dado que el grado de salida de la fuente es $\delta^+(s) = 2$ y el de entrada al sumidero es $\delta^-(t) = 2$, es matemáticamente imposible que existan 3 caminos. Por tanto, la familia máxima es de cardinalidad 2.  
  > 
  > 3. **Corte Mínimo:**  
  >    El conjunto de arcos $C = \{(B, t), (C, t)\}$ clausura todo arribo a $t$. Su cardinalidad es $|C| = 2$.  
  >    La coincidencia entre el número máximo de caminos disjuntos (2) y el corte mínimo (2) verifica analíticamente la cota óptima por el Teorema de Menger.  
  > 
  > *(Contraste con el código)*  
  > Al ejecutar nuestras funciones `bfs_shortest_path`, `max_edge_disjoint_paths` y `min_edge_cut` sobre esta red de control, el software arrojó exactamente longitud 2, las dos mismas rutas disjuntas y el corte de tamaño 2. El contraste entre la solución manual y la computacional es de un 100% de coincidencia."

---

### [18:45 - 20:00] Cierre y Conclusiones
- **Recurso en pantalla:** 
  - Diapositiva final con conclusiones sintetizadas y bibliografía citada en el informe (Cormen et al., Kleinberg & Tardos, Diestel, Ford & Fulkerson).
  - Cámara de los 3 integrantes (Diego Hernández, Antonio Lara y Sebastián Rivera).
- **Locución (Diego Hernández, Antonio Lara y Sebastián Rivera):**
  > *(Diego Hernández)*  
  > "A través de este proyecto hemos comprobado cómo la modelación formal mediante grafos dirigidos permite transformar un problema de logística física en un modelo computacional robusto y predecible."  
  > 
  > *(Antonio Lara)*  
  > "La selección e implementación desde cero de algoritmos como BFS y Edmonds-Karp demostró que la optimalidad y la capacidad de reversión mediante redes residuales son indispensables para evitar las trampas de los enfoques voraces."  
  > 
  > *(Sebastián Rivera)*  
  > "El simulador desarrollado no solo responde a las interrogantes operativas de ruta mínima y redundancia, sino que proporciona una plataforma interactiva visual para evaluar la resiliencia de la red ante contingencias o expansiones.  
  > Muchas gracias por su atención, y quedamos a disposición del docente para sus preguntas."  
  > 
  > *(Placa final con créditos: Diego Hernández, Antonio Lara, Sebastián Rivera - Noviembre 2026)*

---

## Recomendaciones para la Grabación del Video

1. **Uso de Apoyos Visuales:** Mantener en pantalla las mismas ecuaciones y tablas del informe (`docs/Borrador Informe Markdown.md`), ya que la coherencia entre el texto entregado y la presentación oral es uno de los puntos mejor evaluados en la rúbrica.
2. **Ritmo de Voz:** Con un ritmo pausado de ~130 palabras por minuto, este guion se ajusta de manera natural entre los 19 y 20 minutos de grabación.
3. **Coordinación de Escenas:** En OBS Studio, configurar 3 escenas:
   - *Escena 1:* Diapositivas + Cámara web en esquina.
   - *Escena 2:* Pantalla completa de la aplicación web Streamlit con el grafo PyVis interactivo.
   - *Escena 3:* Terminal con la ejecución de tests y demostraciones por consola.
