

# 1. Modelación matemática del laberinto
---
## 1.1. Definición formal de la red inicial
---
Para representar el centro de almacenamiento solicitado, se definió un grafo dirigido simple $G_0$ = $(V,E)$, donde:

- El **conjunto de vértices** ($V$) representa las posiciones físicas o intersecciones de los caminos recorridos por los robots de inspección, como en el modelo referencial del proyecto. El modelo cuenta con $|V|$ = 12 vértices, por lo que cumple coon la restricción $10 \le \vert{}V\vert{} \le 12$:
	$$V = \{s, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, t\}$$

	Dentro de ese conjunto se distingue los dos nodos terminales y diferenciados $s$ y $t$: 
	
	-  $s \in V$: Punto de entrada o estación de despacho desde donde inicia la inspección el robot.
	- $t \in V$: Punto de salida o estación de destino donde finaliza el recorrido.

- El **conjunto de arcos dirigidos** ($E$) representa los pasillos de un solo sentido que conectan pares ordenados de intersecciones ($(u, v) \in V \times V$)), indicando que un robot puede desplazarse desde $u$ hacia $v$. El modelo diseñado cuenta con $\vert{}E\vert{}$ = 16 arcos, lo que cumple con la resitricción solicitada $14 \le \vert{}E\vert{} \le 20$:
$$E = \{(s,2), (s,5), (2,3), (2,6), (3,4), (3,7), (4,8), (5,6), (5,9), (6,7), (7,8), (7,t), (8,t), (9,10), (10,11), (11,7)\}$$

## 1.2 Cumplimiento de restricciones adicionales
---
Además de la cardinalidad solicitada de vértices y arcos, esta configuración propuesta para el modelamiento del problema satisface el resto de las condiciones exigidas por el problema, las cuales son las siguientes:

- **Ausencia de lazos:** No existe ningún arco de la forma $(v, v) \in E$ para todo $v \in V$ (ningún pasillo conecta una intersección consigo misma).
    
- **Ausencia de arcos repetidos:** $E$ es un conjunto sin multiplicidad de arcos entre un mismo par ordenado $(u, v)$.
    
- **Ausencia de arcos recíprocos:** Para todo arco $(u, v) \in E$, se verifica que $(v, u) \notin E$, garantizando la circulación exclusivamente unidireccional en cada pasillo.
    
- **Conectividad total (sin vértices aislados):** Todo vértice $v \in V$ posee grado total $\delta^-(v) + \delta^+(v) \ge 1$. Es decir, cada vértice tiene al menos una conexión
    
- **Existencia de múltiples rutas disjuntas en arcos:** La red propuesta admite al menos dos caminos dirigidos de $s$ a $t$ sin pasillos en común. En particular, el vértice $7$ funciona como un nodo de cruce central que permite que las rutas $P_1 = (s, 2, 3, 7, 8, t)$ y $P_2 = (s, 5, 6, 7, t)$ compartan una intersección intermedia sin compartir ningún arco dirigido.


# 2. Algoritmos de análisis
---
## 2.1. Búsqueda del camino con menor número de arcos
---

Para determinar el algoritmo idóneo para obtener el menor número de arcos entre dos vértices y por qué el clásico BFS sirve para nuestro propósito, haremos una comparativa entre BFS y DFS.

| **Criterio**                            | **Búsqueda en Anchura (BFS)**                                                                                            | **Búsqueda en Profundidad (DFS)**                                                                           |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| **Estructura de datos**                 | Cola FIFO (_First-In, First-Out_).                                                                                       | Pila LIFO (_Last-In, First-Out_) o recursión.                                                               |
| **Orden de exploración**                | Por niveles o capas de distancia creciente desde $s$.                                                                    | Explora cada rama hasta su máxima profundidad antes de retroceder (_backtracking_).                         |
| **Optimalidad en grafos no ponderados** | **Garantizada:** El primer momento en que alcanza $t$ corresponde necesariamente al camino con el menor número de arcos. | **No garantizada:** Puede encontrar un camino largo hacia $t$ antes de explorar un atajo de menor longitud. |
| **Complejidad temporal y espacial**     | $O(\vert{}V\vert{} + \vert{}E\vert{})$ en tiempo; $O(\vert{}V\vert{})$ en memoria.                                       | $O(\vert{}V\vert{} + \vert{}E\vert{})$ en tiempo; $O(\vert{}V\vert{})$ en memoria.                          |

En realidad, desde la teoría se establece desde ya que el algoritmo BFS clásicamente sirve para hallar los recorridos más cortos entre vértices en grafos no ponderados.

La justificación de dicha afirmación se basa en que la exploración sucesiva de vecinos desde el nodo inicial, por niveles, da siempre la información de en qué nivel está el vértice (aumentando en 1 la distancia que tenía el vértice padre de ese vértice), y esos niveles siempre corresponden a la distancia de arcos del vértice analizado respecto al vértice inicial, y esa siempre será la distancia mínima, porque de lo contrario, por ejemplo, hacer avances y regresiones entre niveles siempre implicará un camino más extenso en vez de uno directo. 

Por el contrario, el algoritmo DFS baja inmediatamente por una ruta arbitraria que puede terminar justamente en esos avances de nivel y regresiones hasta llegar al vértice final. Sus usos serían otros, como poner un robot a recorrer toda el área (labores de limpieza) o para hallar errores estructurales (como bucles infinitos).



![[Pasted image 20261123150304.png|365]]![[Pasted image 20261123150430.png|235]]

En síntesis, la exploración por capas garantiza matemáticamente que el árbol de búsqueda generado desde $s$ contiene los caminos más cortos en número de arcos hacia todo vértice alcanzable (Cormen et al., 2022). Mediante un arreglo de predecesores `parent[v]`, el algoritmo reconstruye la secuencia óptima desde $t$ hasta $s$. Si al finalizar la cola el vértice $t$ no fue visitado, el procedimiento informa explícitamente la inexistencia de ruta sin asignar valores numéricos artificiales.

Esta selección, por lo demás, es solo valida en este modelo ya que los arcos no presentan diferencias de *pesos* o *costes*, al ser nuestro grafo no ponderado. De lo contrario, una selección de camino mínimo solo en base a los niveles o escalas no serviría y habría que considerar el factor de ponderación adicionalmente.

## 2.2 Cálculo del máximo número de caminos disjuntos en arcos
---
Con el objetivo de determinar un algoritmo que permita hallar la familia máxima de caminos dirigidos entre $s$ y $t$ que no compartan arcos se analizaron dos enfoques:

### Búsqueda voraz (_Greedy_) iterativa mediante BFS/DFS:
---
Un algoritmo *greedy* es un algoritmo que opera tomando decisiones de conveniencia inmediata sin tomar en cuenta el largo plazo del resto del análisis de un grafo (seleccionar un arco con menos peso, selecionar el vértice con mayor grado, etc.) y no cuentan con operaciones de reversión. 

En este caso, implementar un algoritmo basado BFS sucesivos para hallar la familia máxima de caminos independientes consistiría en lo siguiente: 

1. Se halla un camino de $s$ a $t$ con BFS.
2. Una vez delimitado ese camino BFS, se eliminan sus arcos del grafo.
3. Se repite el proceso buscando otro camino de $s$ a $t$ hasta que no exista conexión.

El algoritmo parece tener lógica, se borran los arcos usados, de modo que queden reservadas solo para ese primer camino independiente. Sin embargo, un problema surge si existe una ruta transversal que utiliza simultáneamente un arco perteneciente a una primera trayectoria óptima y otro arco de una segunda trayectoria óptima, su selección temprana y eliminación bloqueará ambas rutas a la vez, reduciendo el total de caminos encontrados. 

Véase el ejemplo:

![[Pasted image 20261123145849.png|492]]



### Formulación de Flujo Máximo con capacidad unitaria (Algoritmo de Edmonds-Karp):
---

El algoritmo exacto de flujo en redes que determina el caudal máximo transportable desde un nodo fuente $s$ hacia un sumidero $t$ a través de arcos dirigidos acotados por restricciones de capacidad. Al modelar los pasillos del almacén con capacidad unitaria ($c(u,v) = 1$), el cálculo del flujo máximo se reduce directamente a hallar la familia máxima de trayectorias independientes (disjuntas en arcos) entre $s$ y $t$. (Cormen et al., 2022; Kleinberg & Tardos, 2006):

#### Funcionamiento del algoritmo de Edmonds-Karp
---
1. **Búsqueda de camino libre (BFS):** Desde $s$, identifica la trayectoria hacia $t$ con la menor cantidad de arcos disponibles (capacidad residual $c_f > 0$).

2. **Asignación de flujo y arco residual inverso:** Al enviar una unidad de flujo ($1$ robot) por cada arco $(u, v)$ del camino, este queda bloqueado ($c_f(u, v) = 0$) y se habilita un arco residual inverso $(v, u)$ con capacidad $1$.

3. **Función de cancelación:** Si una iteración posterior utiliza el arco inverso $(v, u)$, anula la asignación previa en $(u, v)$ y obliga al primer flujo a desviarse por otra ruta libre, evitando quedar atrapado en óptimos locales y asegurando que ambos robots alcancen $t$ sin compartir pasillos.

4. **Iteración hasta saturación:** Repite la búsqueda en el grafo residual (combinando arcos directos disponibles e inversos) hasta que BFS no logre alcanzar $t$, contabilizando el total de trayectorias disjuntas en arcos obtenidas.

### Conclusión y selección de algoritmo
---

Se seleccionó el **algoritmo de Edmonds-Karp** (especialización del método de Ford-Fulkerson que utiliza BFS para hallar caminos de aumento más cortos en el grafo residual $G_f$). La inclusión de arcos residuales inversos con capacidad de retorno permite al algoritmo reasignar flujo previamente asignado cuando detecta una mejor combinación de rutas, evitando quedar atrapado en máximos locales.


## 2.3 Corte mínimo
---
En el contexto de nuestro modelo, el «corte mínimo» es el conjunto mínimo de arcos que deja aislado el vértice del inicio del vértice final.

Este valor se puede relacionar con la cantidad máxima de caminos dirigidos disjunto en arcos mediante el **Teorema de Menger**, el cual en su versión dirigida por arcos, el número máximo de caminos dirigidos disjuntos en arcos entre $s$ y $t$ es estrictamente igual a la cardinalidad mínima de un corte $C \subseteq E$ que interrumpe toda trayectoria dirigida de $s$ a $t$ (Diestel, 2017):

$$\max \vert{}\mathcal{P}_{s,t}\vert{} = \min \{\vert{}C\vert{} : C \subseteq E,\; \text{no existe camino de } s \text{ a } t \text{ en } G - C\}$$

Cabe señalar que este teorema fue generalizado mediante el **Teorema de Flujo Máximo–Corte Mínimo** de Ford y Fulkerson (1956), al incorporar capacidades o ponderaciones.

De forma práctica, al finalizar Edmonds-Karp, el conjunto de vértices alcanzables $S \subseteq V$ desde $s$ en el último grafo residual $G_f$ define directamente un corte mínimo mediante los arcos originales que cruzan hacia el complemento $V \setminus S$:

$$C = \{(u, v) \in E : u \in S \;\land\; v \in V \setminus S\}$$
