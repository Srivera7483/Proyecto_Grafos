# Diapositivas de la Presentación Oficial (20 Minutos)
**Proyecto:** Simulador Interactivo de Laberintos y Rutas Alternativas  
**Asignatura:** Teoría de Grafos (INFO1158)  
**Alineación:** Estructurado en base al **Informe Técnico** (`docs/Borrador Informe Markdown.md`) y el **Guion de Grabación** (`docs/guion_video_presentacion.md`)  
**Equipo:** Diego Hernández · Antonio Lara · Sebastián Rivera  
**Fecha:** 26 de Noviembre de 2026  

---

## DIAPOSITIVA 1: Portada y Presentación
- **Título Principal:** Simulador Interactivo de Laberintos y Rutas Alternativas
- **Subtítulo:** Modelación formal de redes dirigidas, búsqueda de caminos mínimos y análisis de resiliencia mediante flujo máximo y corte mínimo
- **Asignatura:** Teoría de Grafos (INFO1158) - Universidad Católica de Temuco
- **Integrantes:**
  - Diego Hernández
  - Antonio Lara
  - Sebastián Rivera
- **Duración Estimada:** `00:00 - 00:45`
- **Notas del Orador (Diego Hernández):**
  > "Muy buenos días, profesor y compañeros. Presentamos la defensa técnica de nuestro proyecto para la asignatura Teoría de Grafos. En centros de distribución modernos, la automatización depende de robots de inspección que se desplazan por pasillos de un solo sentido. Hoy demostraremos cómo modelar, analizar y robustecer este sistema ante contingencias operativas."

---

## DIAPOSITIVA 2: Contexto Industrial y Planteamiento del Problema
- **Título:** Planteamiento del Problema: Circulación Unidireccional
- **Contenido Visual:**
  - **Entorno operativo:** Centro de almacenamiento inteligente con robots autónomos (AGV).
  - **Misión de inspección:** Desplazamiento obligatorio desde una estación de despacho/entrada ($s$) hasta una estación de salida ($t$).
  - **Vulnerabilidad operativa:** 
    - En pasillos de sentido único, la elección de trayectos influye en los pasillos recorridos.
    - El colapso de un pasillo puede inutilizar múltiples trayectos al mismo tiempo.
- **Interrogantes Fundamentales:**
  1. ¿Cuál es el camino de menor longitud en número de pasillos?
  2. ¿Cuántas rutas independientes pueden operar en simultáneo sin depender de los mismos pasillos?
  3. ¿Cuál es el conjunto mínimo de pasillos cuyo bloqueo aislaría por completo la salida?
- **Duración Estimada:** `00:45 - 01:30`
- **Notas del Orador (Diego Hernández):**
  > "Abstraemos la planta física como una red dirigida donde cada pasillo tiene un único sentido de circulación. La disponibilidad de rutas independientes es más exigente que la simple existencia de caminos alternativos: necesitamos saber qué bloqueos impiden el acceso a la salida y cómo cambia la resiliencia cuando modificamos la red."

---

## DIAPOSITIVA 3: Sección 1 - Modelación Matemática del Laberinto ($G_0$)
- **Título:** Modelación Matemática: Grafo Dirigido $G_0 = (V, E)$
- **Contenido Formal (Sección 1.1 del Informe):**
  - **Grafo Dirigido Simple:** $G_0 = (V, E)$
  - **Conjunto de Vértices $V$:** Representa posiciones físicas o intersecciones.
    $$V = \{s, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, t\} \quad \longrightarrow \quad |V| = 12$$
    - Cumple estrictamente con la cota requerida: $10 \le |V| \le 12$.
    - **Nodos terminales distinguidos:**
      - $s \in V$: Punto de entrada o estación de despacho inicial.
      - $t \in V$: Punto de salida o destino final de la inspección ($s \neq t$).
  - **Conjunto de Arcos Dirigidos $E$:** Pasillos de sentido único entre intersecciones $(u, v) \in V \times V$.
    $$E = \{(s,2), (s,5), (2,3), (2,6), (3,4), (3,7), (4,8), (5,6), (5,9), (6,7), (7,8), (7,t), (8,t), (9,10), (10,11), (11,7)\}$$
    - Total de arcos activos: $|E| = 16$. Cumple la cota $14 \le |E| \le 20$.
- **Duración Estimada:** `01:30 - 02:45`
- **Notas del Orador (Diego Hernández):**
  > "Modelamos el centro de almacenamiento con un grafo dirigido simple $G_0$. Seleccionamos exactamente 12 vértices y 16 arcos dirigidos, respetando los intervalos fijados en la pauta. $s$ y $t$ definen los extremos fijos de la misión de inspección."

---

## DIAPOSITIVA 4: Sección 1.2 - Cumplimiento de Restricciones Estructurales
- **Título:** Verificación Rigurosa de Restricciones del Modelo
- **Puntos Clave (Sección 1.2 del Informe):**
  - **Ausencia de lazos:** $\forall v \in V, (v, v) \notin E$ (ningún pasillo conecta una intersección consigo misma).
  - **Ausencia de arcos repetidos:** $E$ es un conjunto simple sin multiplicidad de conexiones paralelas.
  - **Ausencia de arcos recíprocos:** $\forall (u, v) \in E \implies (v, u) \notin E$ (garantía de flujo exclusivamente unidireccional).
  - **Conectividad total (sin vértices aislados):**
    $$\forall v \in V, \quad \delta^-(v) + \delta^+(v) \ge 1$$
    Todo espacio físico participa de la circulación con al menos un pasillo incidente o saliente.
  - **Nodo de Cruce Central (Vértice 7):**
    - Permite que las rutas $P_1 = (s, 2, 3, 7, 8, t)$ y $P_2 = (s, 5, 6, 7, t)$ compartan una intersección física común sin compartir ningún pasillo dirigido.
    - Se verifica la existencia de **al menos 2 caminos dirigidos disjuntos en arcos**.
- **Duración Estimada:** `02:45 - 04:00`
- **Notas del Orador (Diego Hernández):**
  > "Demostramos en el informe que la red no contiene lazos, no tiene arcos recíprocos y ningún vértice está aislado. Un detalle crucial es el vértice 7: actúa como un cruce central donde dos trayectorias pueden compartir una intersección intermedia en momentos distintos, pero sin compartir ningún arco dirigido."

---

## DIAPOSITIVA 5: Sección 2.1 - Algoritmo de Camino Mínimo (BFS vs DFS)
- **Título:** Camino con Menor Número de Arcos: BFS vs DFS
- **Tabla Comparativa Formal (Sección 2.1 del Informe):**

| Criterio | Búsqueda en Anchura (BFS) | Búsqueda en Profundidad (DFS) |
| :--- | :--- | :--- |
| **Estructura de datos** | Cola FIFO (*First-In, First-Out*) | Pila LIFO (*Last-In, First-Out*) o recursión |
| **Orden de exploración** | Por niveles concéntricos de distancia creciente desde $s$ | Explora cada rama hasta su máxima profundidad antes de retroceder |
| **Optimalidad en no ponderados** | **Garantizada:** El primer arribo a $t$ es la ruta más corta | **No garantizada:** Puede encontrar rutas extensas antes de atajos |
| **Complejidad computacional** | $O(\|V\| + \|E\|)$ tiempo; $O(\|V\|)$ memoria | $O(\|V\| + \|E\|)$ tiempo; $O(\|V\|)$ memoria |

- **Fundamentación Teórica (Cormen et al., 2022):**
  - En grafos con costos uniformes (cantidad de pasillos), la distancia por capas de BFS garantiza hallar $d_G(s, t) = \min \{k\}$.
  - Reconstrucción determinista mediante arreglo de predecesores `parent[v]`.
  - **Manejo de desconexión:** Si $t$ no es alcanzado, reporta formalmente `exists: False, length: None`.
- **Duración Estimada:** `04:00 - 05:30`
- **Notas del Orador (Antonio Lara):**
  > "Para encontrar el camino más corto en cantidad de pasillos, comparamos BFS y DFS. Como nuestro grafo no es ponderado, BFS es la estrategia óptima: su exploración por capas concéntricas garantiza que el primer instante en que se alcanza $t$ corresponde al camino con el menor número de arcos, en tiempo lineal $O(|V|+|E|)$."

---

## DIAPOSITIVA 6: Sección 2.2 - Caminos Disjuntos: Fallo Voraz vs Flujo Máximo
- **Título:** Familia Máxima de Rutas Disjuntas en Arcos
- **Contenido Teórico (Sección 2.2 del Informe):**
  - **¿Por qué falla el enfoque voraz (_Greedy_)?**
    1. Se halla un camino con BFS.
    2. Se borran sus arcos de la red.
    3. Se repite hasta no encontrar conexión.
    - *Problema:* Si un camino inicial toma un arco transversal que cruza dos trayectorias independientes óptimas, su eliminación temprana bloquea ambas simultáneamente, reduciendo el total global encontrado.
  - **La Solución Formal: Formulación de Flujo Máximo Unitario**
    - Se modela cada pasillo activo con capacidad unitaria: $c(u, v) = 1$.
    - Por el **Teorema de Menger para arcos** (Diestel, 2017; Kleinberg & Tardos, 2006), el caudal máximo entre $s$ y $t$ equivale exactamente al cardinal máximo de caminos disjuntos en arcos.
- **Duración Estimada:** `05:30 - 07:00`
- **Notas del Orador (Antonio Lara):**
  > "Para hallar la máxima cantidad de caminos independientes no podemos usar una búsqueda voraz: un camino temprano mal elegido puede bloquear dos rutas mejores. La solución formal consiste en formular el problema como flujo máximo con capacidades unitarias mediante el algoritmo de Edmonds-Karp."

---

## DIAPOSITIVA 7: Fases del Algoritmo de Edmonds-Karp
- **Título:** Funcionamiento de Edmonds-Karp con Capacidad Unitaria
- **Las 4 Fases Operativas del Algoritmo:**
  1. **Búsqueda de trayectoria aumentante (BFS):** Desde $s$, identifica el camino hacia $t$ con menor cantidad de arcos en la red residual ($c_f > 0$).
  2. **Asignación de flujo y arco residual inverso:** Al saturar un pasillo $(u, v)$ ($c_f(u, v) = 0$), se habilita un arco residual inverso $(v, u)$ con capacidad unitaria ($c_f(v, u) = 1$).
  3. **Función de cancelación (*Augmenting Backtrack*):** Si una iteración posterior utiliza el arco inverso $(v, u)$, revierte la asignación previa en $(u, v)$ y desvía el flujo por otra ruta libre, superando óptimos locales.
  4. **Iteración hasta saturación:** Repite hasta que BFS no alcance $t$. Descompone el flujo positivo final en trayectorias completas consumiendo aristas.
- **Ventaja Matemática:** Complejidad fuertemente polinomial $O(|V| \cdot |E|)$ en redes unitarias.
- **Duración Estimada:** `07:00 - 07:45`
- **Notas del Orador (Antonio Lara):**
  > "El secreto de Edmonds-Karp radica en los arcos residuales inversos. Permiten al algoritmo 'cambiar de opinión': si detecta que redirigir un flujo previo permite habilitar dos rutas en lugar de una, reasigna el flujo y encuentra la familia globalmente máxima."

---

## DIAPOSITIVA 8: Sección 2.3 - Corte Mínimo y Teorema de Menger
- **Título:** Corte Mínimo de Pasillos y Dualidad Flujo-Corte
- **Contenido Teórico (Sección 2.3 del Informe):**
  - **Definición de Corte Mínimo:** Conjunto de pasillos $C \subseteq E$ de menor tamaño cuya supresión clausura todo desplazamiento desde $s$ hasta $t$ en $G - C$.
  - **Teorema de Menger (versión dirigida por arcos) & Teorema Max-Flow Min-Cut (Ford y Fulkerson, 1956):**
    $$\max |\mathcal{P}_{s,t}| = \min \{|C| : C \subseteq E,\; \text{no existe camino de } s \text{ a } t \text{ en } G - C\}$$
  - **Extracción Algorítmica del Corte:**
    - Se ejecuta BFS desde $s$ en la red residual final sobre aristas con $c_f > 0$.
    - Se define el subconjunto $S \subset V$ de vértices alcanzables ($t \notin S$).
    - El corte mínimo corresponde exactamente a los arcos originales activos que cruzan hacia el complemento $V \setminus S$:
      $$C = \{(u, v) \in E : u \in S \land v \in V \setminus S\}$$
- **Duración Estimada:** `07:45 - 08:30`
- **Notas del Orador (Antonio Lara):**
  > "Por el teorema de flujo máximo y corte mínimo, la capacidad del corte más pequeño que separa la entrada de la salida coincide con el número máximo de caminos independientes. Identificamos el conjunto $S$ de nodos alcanzables en la red residual y extraemos los pasillos que cruzan la frontera."

---

## DIAPOSITIVA 9: Arquitectura de Software e Implementación Propia
- **Título:** Arquitectura del Sistema (Python Puro)
- **Componentes del Repositorio:**
  - **`src/models/graph_model.py`:** Clase `DirectedGraph` con listas de adyacencia `{u: set(v)}`, conjunto `blocked_edges`, terminales $s, t$ y validación de restricciones en cada inserción.
  - **`src/algorithms/algorithms.py`:** Funciones de cálculo algorítmico sin bibliotecas de grafos externas:
    - `bfs_shortest_path`
    - `edmonds_karp_max_flow`
    - `max_edge_disjoint_paths`
    - `min_edge_cut`
  - **`src/ui/visualizer.py` & `app.py`:** Interfaz interactiva desacoplada basada en Streamlit y PyVis.
  - **`tests/test_backend.py`:** Suite automatizada de 13 pruebas unitarias (`0.007s` de ejecución).
- **Duración Estimada:** `08:30 - 09:45`
- **Notas del Orador (Sebastián Rivera):**
  > "Diseñamos la solución bajo una arquitectura modular y limpia en Python puro. Ningún cálculo recurre a librerías de grafos. En consola ejecutamos 13 pruebas unitarias automatizadas que certifican el correcto manejo de excepciones, bloqueos y casos borde."

---

## DIAPOSITIVA 10: Demostración Interactiva en Vivo: Red Base $G_0$
- **Título:** Resultados Computacionales en la Configuración Inicial ($G_0$)
- **Datos de la Red:** $|V| = 12$, $|E| = 16$, $s = \text{'s'}$, $t = \text{'t'}$
- **Resultados del Simulador:**
  - **1. Camino Mínimo (BFS):**
    - Longitud mínima: **4 arcos**.
    - Secuencia: $s \to 2 \to 3 \to 7 \to t$.
  - **2. Familia Máxima de Caminos Disjuntos (Edmonds-Karp):**
    - Total de caminos: **2 rutas independientes**.
    - *Ruta 1 (longitud 4):* $s \to 2 \to 3 \to 7 \to t$
    - *Ruta 2 (longitud 5):* $s \to 5 \to 6 \to 7 \to 8 \to t$
    - *(Coincidencia con el informe: comparten nodo 7, pero 0 arcos).*
  - **3. Corte Mínimo de Pasillos:**
    - Pasillos del corte: $C = \{(s, 2), (s, 5)\}$.
    - Cardinalidad: $|C| = 2$.
    - **Comprobación:** $|C| = \text{max\_caminos} = 2$. Al suprimirlos, la red colapsa a 0 caminos.
- **Duración Estimada:** `09:45 - 13:00`
- **Notas del Orador (Sebastián Rivera):**
  > "Vemos en pantalla la interfaz interactiva. Para la red base $G_0$, el camino mínimo tiene longitud 4. El algoritmo de Edmonds-Karp extrae dos rutas independientes que se cruzan en la intersección 7 sin tocar ningún pasillo en común. Y el corte mínimo de tamaño 2 aísla completamente a la entrada de la salida."

---

## DIAPOSITIVA 11: Modificación 1 - Bloqueo de Pasillo Directo (`mod_1.json`)
- **Título:** Modificación 1: Bloqueo de Pasillo Directo $7 \to t$
- **Descripción de la Contingencia:**
  - Se deshabilita el arco directo a la salida: $(7, t)$ queda bloqueado (línea roja discontinua).
  - Simula una obstrucción en el pasillo principal de evacuación o despacho.
- **Impacto y Resultados del Recálculo:**
  - **Camino Mínimo:** Obligado a desviarse por el nodo 8: $s \to 2 \to 3 \to 4 \to 8 \to t$. Aumenta a **5 arcos**.
  - **Caminos Disjuntos:** Colapso de 2 a **1 solo camino independiente**.
  - **Cuello de Botella:** El vértice 8 se convierte en el único acceso físico hacia $t$.
  - **Corte Mínimo:** $|C| = 1$, conformado exclusivamente por $\{(8, t)\}$.
  - *Conclusión:* La red se torna altamente frágil; una falla adicional paraliza la planta por completo.
- **Duración Estimada:** `13:00 - 14:45`
- **Notas del Orador (Diego Hernández):**
  > "En la primera modificación inhabilitamos el pasillo directo 7 a t. Observen cómo la red pierde toda su redundancia: el camino mínimo se alarga a 5 arcos, los caminos independientes se reducen a uno solo y el nodo 8 pasa a ser un cuello de botella absoluto."

---

## DIAPOSITIVA 12: Modificación 2 - Expansión de Capacidad (`mod_2.json`)
- **Título:** Modificación 2: Expansión de Capacidad de Tránsito
- **Descripción de la Mejora:**
  - Se incorporan dos nuevos pasillos estratégicos:
    1. Atajo inicial: $(s, 6)$ desde la estación de despacho.
    2. Salida directa: $(11, t)$ desde el sector inferior de la nave.
  - La red pasa a tener 18 arcos en total.
- **Impacto y Resultados del Recálculo:**
  - **Caminos Disjuntos:** Se incrementa a **3 caminos independientes simultáneos**:
    - *Ruta 1:* $s \to 2 \to 3 \to 4 \to 8 \to t$
    - *Ruta 2:* $s \to 6 \to 7 \to t$
    - *Ruta 3:* $s \to 5 \to 9 \to 10 \to 11 \to t$
  - **Corte Mínimo:** Se eleva correspondientemente a $|C| = 3$.
  - *Conclusión:* La tolerancia a fallos se triplica. Se requeriría la caída simultánea de tres pasillos para aislar la salida.
- **Duración Estimada:** `14:45 - 16:30`
- **Notas del Orador (Antonio Lara):**
  > "En la segunda modificación añadimos dos pasillos estratégicos: s a 6 y 11 a t. El resultado es notable: triplicamos la capacidad de rutas simultáneas a 3 caminos disjuntos y el corte mínimo sube a 3 pasillos. Esto justifica inversiones en infraestructura basadas en resiliencia comprobada."

---

## DIAPOSITIVA 13: Cuadro Comparativo de Configuraciones
- **Título:** Análisis Comparativo de Conectividad y Resiliencia
- **Tabla Síntesis de Resultados:**

| Parámetro de Evaluación | Configuración Inicial ($G_0$) | Modificación 1 (Falla $7 \to t$) | Modificación 2 (Expansión) |
| :--- | :---: | :---: | :---: |
| **Total Vértices ($|V|$)** | 12 | 12 | 12 |
| **Total Arcos Activos** | 16 | 15 (1 bloqueado) | 18 |
| **Longitud Camino Mínimo** | **4 arcos** | **5 arcos** | **4 arcos** |
| **Máx. Caminos Disjuntos** | **2 rutas** | **1 ruta** | **3 rutas** |
| **Tamaño Corte Mínimo ($|C|$)** | **2 pasillos** | **1 pasillo** | **3 pasillos** |
| **Pasillos del Corte Mínimo** | $\{(s,2), (s,5)\}$ | $\{(8,t)\}$ | $\{(s,2), (s,5), (s,6)\}$ |
| **Nivel de Resiliencia** | Moderado (balanceado) | Crítico (vulnerable) | Alto (alta redundancia) |

- **Duración Estimada:** `16:00 - 16:30`
- **Notas del Orador (Antonio Lara):**
  > "Este cuadro resumen ilustra con claridad el valor de la modelación: pasamos de una red base balanceada a una configuración crítica al perder un solo pasillo, y a una red de alta tolerancia tras agregar solo dos conexiones estratégicas."

---

## DIAPOSITIVA 14: Verificación Manual Independiente (Caso de 5 Vértices)
- **Título:** Verificación Matemática: Caso de Control Manual
- **Definición del Grafo de Control (Sección 5 de la Pauta):**
  $$V = \{s, A, B, C, t\}, \quad E = \{(s, A), (s, B), (A, C), (B, C), (B, t), (C, t)\}$$
- **Resolución Analítica Manual:**
  1. **Camino Mínimo:**
     - Rutas posibles: $s \to B \to t$ (2 arcos), $s \to A \to C \to t$ (3 arcos), $s \to B \to C \to t$ (3 arcos).
     - Camino mínimo: $s \to B \to t$ con longitud $d_G(s, t) = 2$.
  2. **Caminos Disjuntos en Arcos:**
     - $P_1 = (s, B, t)$ con arcos $\{(s, B), (B, t)\}$.
     - $P_2 = (s, A, C, t)$ con arcos $\{(s, A), (A, C), (C, t)\}$.
     - Intersección: $E(P_1) \cap E(P_2) = \emptyset$.
     - Como $\delta^+(s) = 2$, el máximo teórico es 2.
  3. **Corte Mínimo:**
     - $C = \{(B, t), (C, t)\}$ clausura todo arribo a $t$. Cardinalidad $|C| = 2$.
- **Contraste con el Software:** El algoritmo arrojó idénticos valores ($d_G=2$, 2 caminos, $|C|=2$). Coincidencia al 100%.
- **Duración Estimada:** `16:30 - 18:45`
- **Notas del Orador (Sebastián Rivera):**
  > "Para cumplir con la verificación matemática independiente, resolvimos a mano este grafo de 5 nodos. El camino más corto es s-B-t de longitud 2, existen dos caminos disjuntos y un corte mínimo de tamaño 2. Al ingresar la red al backend, la salida computacional coincidió con exactitud matemática."

---

## DIAPOSITIVA 15: Conclusiones y Aportes del Proyecto
- **Título:** Conclusiones y Lecciones Aprendidas
- **Síntesis del Trabajo:**
  1. **Modelación formal sólida:** Abstraer el espacio físico mediante grafos dirigidos simples permite predecir y controlar flujos de tráfico en almacenes automatizados.
  2. **Rigor algorítmico frente a heurísticas:** Demostramos que los algoritmos voraces fallan en problemas globales de independencia; Edmonds-Karp con capacidad unitaria garantiza la cota óptima de rutas disjuntas.
  3. **Impacto práctico del Teorema de Menger:** El cálculo del corte mínimo permite identificar los cuellos de botella exactos y planificar mantenimientos preventivos sin interrumpir la operación.
  4. **Software robusto y accesible:** Interfaz gráfica interactiva desarrollada sin librerías de cálculo externas, cumpliendo todas las directrices de la asignatura.
- **Referencias Bibliográficas Citadas en el Informe:**
  - Cormen, T. H., et al. (2022). *Introduction to Algorithms* (4th ed.). MIT Press.
  - Diestel, R. (2017). *Graph Theory* (5th ed.). Springer.
  - Ford, L. R., & Fulkerson, D. R. (1956). *Maximal Flow Through a Network*.
  - Kleinberg, J., & Tardos, É. (2006). *Algorithm Design*. Pearson.
- **Duración Estimada:** `18:45 - 19:40`
- **Notas del Orador (Diego Hernández, Antonio Lara y Sebastián Rivera):**
  > "A través de este proyecto comprobamos que la Teoría de Grafos es una herramienta decisiva para la ingeniería aplicada. Implementar algoritmos desde cero nos permitió comprender a fondo la red residual, la dualidad flujo-corte y la importancia de la redundancia operativa."

---

## DIAPOSITIVA 16: Preguntas y Agradecimientos
- **Título:** ¡Muchas Gracias por su Atención!
- **Subtítulo:** Preguntas del Docente y Mesa Redonda
- **Créditos:**
  - **Diego Hernández** (Modelación matemática y análisis de Modificación 1)
  - **Antonio Lara** (Fundamentación teórica de algoritmos y Modificación 2)
  - **Sebastián Rivera** (Desarrollo de software, interfaz PyVis y verificación analítica)
- **Repositorio de Código Fuente:** `Proyecto_Grafos` (INFO1158 - Noviembre 2026)
- **Duración Estimada:** `19:40 - 20:00`
- **Notas del Orador (Todo el equipo):**
  > "Quedamos a total disposición del docente para responder las preguntas sobre el código, la modelación y los fundamentos matemáticos. ¡Muchas gracias!"
