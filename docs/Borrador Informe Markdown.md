
# 1. Introducción
---
La planeación eficiente e inteligente de centros de almacenamiento automatizados con robots de inspección requiere un análisis cuidado de los espacios de circulación de estos, más aún si dicho centro opera con pasillos de circulación unidireccional y no admiten regresiones por parte de las máquinas.

El presente proyecto busca abordar este problema mediante la aplicación de la teoría de grafos en el modelamiento de la red de pasillos por los cuales se desplazan los robots: esta estructura entonces se representa como un grafo dirigido simple $G=(V,E)$ entre una estación inicial $s$ y un punto final $t$. Dicho modelamiento y análisis de la red viene acompañado de un simulador interactivo con interfaz web implementado en Python para efectuar el modelamiento estructural del grafo y permitir la aplicación de motores algorítmicos basados en Búsqueda en Anchura (BFS o *Breadth-first search*) y Flujo máximo unitario (*Edmonds-Karp*) para determinar rutas mínimas, trayectorias disjuntas en arcos y cortes mínimos.

Las tecnologías usadas y el acceso al proyecto se encuentran en la sección de *Anexos*.

# 2. Modelación matemática del laberinto
---
## 2.1. Definición formal de la red inicial
---
Para representar el centro de almacenamiento solicitado, se definió un grafo dirigido simple $G_0$ = $(V,E)$, donde:

- El **conjunto de vértices** ($V$) representa las posiciones físicas o intersecciones de los caminos recorridos por los robots de inspección, como en el modelo referencial del proyecto. El modelo cuenta con $|V|$ = 12 vértices, por lo que cumple coon la restricción $10 \le \vert{}V\vert{} \le 12$:
	$$V = \{s, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, t\}$$

	Dentro de ese conjunto se distingue los dos nodos terminales y diferenciados $s$ y $t$: 
	
	-  $s \in V$: Punto de entrada o estación de despacho desde donde inicia la inspección el robot.
	- $t \in V$: Punto de salida o estación de destino donde finaliza el recorrido.

- El **conjunto de arcos dirigidos** ($E$) representa los pasillos de un solo sentido que conectan pares ordenados de intersecciones ($(u, v) \in V \times V$)), indicando que un robot puede desplazarse desde $u$ hacia $v$. El modelo diseñado cuenta con $\vert{}E\vert{}$ = 16 arcos, lo que cumple con la resitricción solicitada $14 \le \vert{}E\vert{} \le 20$:
$$E = \{(s,2), (s,5), (2,3), (2,6), (3,4), (3,7), (4,8), (5,6), (5,9), (6,7), (7,8), (7,t), (8,t), (9,10), (10,11), (11,7)\}$$

## 2.2 Cumplimiento de restricciones adicionales
---
Además de la cardinalidad solicitada de vértices y arcos, esta configuración propuesta para el modelamiento del problema satisface el resto de las condiciones exigidas por el problema, las cuales son las siguientes:

- **Ausencia de lazos:** No existe ningún arco de la forma $(v, v) \in E$ para todo $v \in V$ (ningún pasillo conecta una intersección consigo misma).
    
- **Ausencia de arcos repetidos:** $E$ es un conjunto sin multiplicidad de arcos entre un mismo par ordenado $(u, v)$.
    
- **Ausencia de arcos recíprocos:** Para todo arco $(u, v) \in E$, se verifica que $(v, u) \notin E$, garantizando la circulación exclusivamente unidireccional en cada pasillo.
    
- **Conectividad total (sin vértices aislados):** Todo vértice $v \in V$ posee grado total $\delta^-(v) + \delta^+(v) \ge 1$. Es decir, cada vértice tiene al menos una conexión
    
- **Existencia de múltiples rutas disjuntas en arcos:** La red propuesta admite al menos dos caminos dirigidos de $s$ a $t$ sin pasillos en común. En particular, el vértice $7$ funciona como un nodo de cruce central que permite que las rutas $P_1 = (s, 2, 3, 7, 8, t)$ y $P_2 = (s, 5, 6, 7, t)$ compartan una intersección intermedia sin compartir ningún arco dirigido.


# 3. Algoritmos de análisis
---
## 3.1. Búsqueda del camino con menor número de arcos
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

![[Pasted image 20261125124404.png]]



En síntesis, la exploración por capas garantiza matemáticamente que el árbol de búsqueda generado desde $s$ contiene los caminos más cortos en número de arcos hacia todo vértice alcanzable (Cormen et al., 2022). Mediante un arreglo de predecesores `parent[v]`, el algoritmo reconstruye la secuencia óptima desde $t$ hasta $s$. Si al finalizar la cola el vértice $t$ no fue visitado, el procedimiento informa explícitamente la inexistencia de ruta sin asignar valores numéricos artificiales.

Esta selección, por lo demás, es solo valida en este modelo ya que los arcos no presentan diferencias de *pesos* o *costes*, al ser nuestro grafo no ponderado. De lo contrario, una selección de camino mínimo solo en base a los niveles o escalas no serviría y habría que considerar el factor de ponderación adicionalmente.

## 3.2 Cálculo del máximo número de caminos disjuntos en arcos
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

![[Pasted image 20261125124353.png]]



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


## 3.3 Corte mínimo
---
En el contexto de nuestro modelo, el «corte mínimo» es el conjunto mínimo de arcos que deja aislado el vértice del inicio del vértice final.

Este valor se puede relacionar con la cantidad máxima de caminos dirigidos disjunto en arcos mediante el **Teorema de Menger**, el cual en su versión dirigida por arcos, el número máximo de caminos dirigidos disjuntos en arcos entre $s$ y $t$ es estrictamente igual a la cardinalidad mínima de un corte $C \subseteq E$ que interrumpe toda trayectoria dirigida de $s$ a $t$ (Diestel, 2017):

$$\max \vert{}\mathcal{P}_{s,t}\vert{} = \min \{\vert{}C\vert{} : C \subseteq E,\; \text{no existe camino de } s \text{ a } t \text{ en } G - C\}$$

Cabe señalar que este teorema fue generalizado mediante el **Teorema de Flujo Máximo–Corte Mínimo** de Ford y Fulkerson (1956), al incorporar capacidades o ponderaciones.

De forma práctica, al finalizar Edmonds-Karp, el conjunto de vértices alcanzables $S \subseteq V$ desde $s$ en el último grafo residual $G_f$ define directamente un corte mínimo mediante los arcos originales que cruzan hacia el complemento $V \setminus S$:

$$C = \{(u, v) \in E : u \in S \;\land\; v \in V \setminus S\}$$

# 4. Simulación y análisis de modificaciones
---
## 4.1. Análisis de la configuración inicial
---
La red original descrita anteriormente cuenta con 12 vértices y 16 pasillos (arcos) dirigidos activos. Esto se representa mediante el archivo `config_inicial.json`:

```json
{
  "nombre": "Configuración Inicial (G0)",
  "descripcion": "Grafo inicial de 12 vértices y 16 pasillos dirigidos con al menos dos caminos disjuntos en arcos de s a t",
  "s": "s",
  "t": "t",
  "vertices": ["s", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "t"],
  "arcos": [
    {"origen": "s", "destino": "2", "activo": true},
    {"origen": "s", "destino": "5", "activo": true},
    {"origen": "2", "destino": "3", "activo": true},
    {"origen": "2", "destino": "6", "activo": true},
    {"origen": "3", "destino": "4", "activo": true},
    {"origen": "3", "destino": "7", "activo": true},
    {"origen": "4", "destino": "8", "activo": true},
    {"origen": "5", "destino": "6", "activo": true},
    {"origen": "5", "destino": "9", "activo": true},
    {"origen": "6", "destino": "7", "activo": true},
    {"origen": "7", "destino": "8", "activo": true},
    {"origen": "7", "destino": "t", "activo": true},
    {"origen": "8", "destino": "t", "activo": true},
    {"origen": "9", "destino": "10", "activo": true},
    {"origen": "10", "destino": "11", "activo": true},
    {"origen": "11", "destino": "7", "activo": true}
  ]
}
```

El simulador procesa el modelo y obtiene los siguientes valores de análisis:

- **Camino mínimo (BFS):** Se identifica una ruta óptima de longitud $d_{G}(s, t) = 4$ arcos correspondiente a la secuencia $s \to 2 \to 3 \to 7 \to t$. 
	- *También existe la trayectoria $s \to 5 \to 6 \to 7 \to t$, la cual presenta la misma longitud, pero el algoritmo selecciona la primera por criterio alfabético*.
	
- **Caminos disjuntos en arcos (Edmonds-Karp):** El flujo máximo unitario alcanza un valor de $2$, descomponiéndose en las trayectorias independientes $P_1 = (s, 2, 3, 7, t)$ y $P_2 = (s, 5, 6, 7, 8, t)$. Aunque ambas rutas comparten la intersección intermedia $7$, no reutilizan ningún pasillo dirigido.
    
- **Corte mínimo ($C_0$):** Una vez saturadas las rutas anteriores en la red residual final, desde la estación $s$ sigue siendo posible alcanzar todos los vértices internos del almacén, pero no ingresar al destino $t$ ($R = V \setminus \{t\}$). Al identificar los pasillos originales que cruzan desde la zona alcanzable hacia el destino aislado, el corte mínimo queda determinado por $C_0 = \{(7, t), (8, t)\}$, con tamaño $\vert{}C_0\vert{} = 2$. Esta igualdad entre el tamaño del corte mínimo y los $2$ caminos disjuntos en arcos verifica directamente el **Teorema de Menger**, demostrando que esos dos pasillos finales constituyen el cuello de botella estructural que limita la capacidad simultánea de toda la red base.****


## 4.2. Análisis de modificaciones
---
Dentro de las modificaciones que la aplicación permite están:

- Bloquear un pasillo y restablecerlo posteriormente.
- Agregar un nuevo pasillo dirigido entre dos espacios.
- Cambiar los vértices seleccionados como entrada y salida.

Para visualizar cómo cambian los análisis implementados en el motor algorítmico del problema se configuraron dos modificaciones predeterminadas en los archivos `mod_1.json` y `mod_2.json`.

- **Modificación 1:** Resulta interesante, por un lado, analizar qué sucede si se bloquea un pasillo que según el análisis de la configuración inicial forma parte del camino mínimo, de uno de los caminos disjuntos en arcos, y que es uno de los cortes mínimos.

Se provee también una tabla comparativa para facilitar la visualización de cómo cambian los factores de análisis según las modificaciones predeterminadas que se eligieron.

### 4.2.1. Modificación 1
---
En este escenario (`mod1.json`), se simula lo que en la realidad del contexto podría ser un mantenimiento programado de un pasillo mediante el bloqueo del pasillo $(7, t)$ (`activo: false`), reduciendo los arcos operativos a $\vert{}E_{\text{act}}\vert{} = 15$:

- **Camino mínimo (BFS):** Al perder el acceso directo desde la intersección $7$ hacia $t$, el robot debe desviarse obligatoriamente a través del nodo $8$, incrementando la distancia mínima a $d_{G_1}(s, t) = 5$ arcos mediante la ruta $s \to 2 \to 3 \to 7 \to 8 \to t$.
    
- **Caminos disjuntos en arcos (Edmonds-Karp):** La capacidad simultánea de la red cae de $2$ a $1$ trayectoria independiente ($P_1 = (s, 2, 3, 7, 8, t)$), ya que todo el flujo disponible converge hacia el único arco de ingreso restante a la salida.
    
- **Corte mínimo ($C_1$):** El corte mínimo se reduce a un único pasillo crítico: $C_1 = \{(8, t)\}$, con $\vert{}C_1\vert{} = 1$. Operativamente, esto convierte al arco $(8, t)$ en un punto único de falla (_single point of failure_), dejando al sistema sin redundancia ante un segundo bloqueo.

### 4.2.2. Modificación 2
---
En el segundo escenario (`mod2.json`), se evalúa una mejora de infraestructura incorporando dos nuevos pasillos dirigidos sin violar las restricciones de grafo simple: un acceso rápido $(s, 6)$ desde el despacho hacia la zona media y una salida directa $(11, t)$ desde el circuito inferior, elevando la red a $\vert{}E\vert{} = 18$ arcos activos:

- **Camino mínimo (BFS):** El nuevo pasillo $(s, 6)$ habilita un atajo directo hacia el eje central, generando un camino con una nueva distancia mínima, la que correspondería a 3 arcos a través de $s \to 6 \to 7 \to t$.
    
- **Caminos disjuntos en arcos (Edmonds-Karp):** La red aumenta su capacidad máxima a $3$ trayectorias completamente disjuntas en arcos, agregando uno que no tiene convergencia $7$, por lo que sería este nuevo camino también disjunto en vértices respecto a los dos anteriores:
    
    1. $P_1 = (s, 6, 7, t)$ (longitud $3$)
        
    2. $P_2 = (s, 2, 3, 7, 8, t)$ (longitud $5$)
        
    3. $P_3 = (s, 5, 9, 10, 11, t)$ (longitud $5$)
        
- **Corte mínimo ($C_2$):** El corte mínimo pasa a ser $C_2 = \{(7, t), (8, t), (11, t)\}$ con cardinalidad $\vert{}C_2\vert{} = 3$. Al desacoplar el subcircuito inferior ($5 \to 9 \to 10 \to 11$) del cuello de botella del nodo $7$, el centro de almacenamiento tolera hasta dos bloqueos simultáneos sin interrumpir el flujo hacia $t$.

### 4.2.3. Tabla comparativa: Configuración inicial vs. Modificaciones
---
![[Pasted image 20261125120827.png]]



# 5. Código vs. Resolución manual
---
Para validar que los algoritmos funcionan correctamente, se diseñó un grafo dirigido de prueba con tamaño reducido, el cual está compuesto por $|V| = 5$ vértices y $|E|$ = 7 arcos.


## 5.1. Grafo base
---
**Grafo base**

Su modelamiento para el código está inserto en el archivo `caso_manual.json` de la siguiente forma:

```json
{
  "nombre": "Caso Manual de Verificación (5 vértices, 7 arcos)",
  "descripcion": "Grafo de prueba",
  "s": "s",
  "t": "t",
  "vertices": ["s", "A", "B", "C", "t"],
  "arcos": [
    {"origen": "s", "destino": "A", "activo": true},
    {"origen": "s", "destino": "B", "activo": true},
    {"origen": "A", "destino": "B", "activo": true},
    {"origen": "A", "destino": "C", "activo": true},
    {"origen": "B", "destino": "C", "activo": true},
    {"origen": "B", "destino": "t", "activo": true},
    {"origen": "C", "destino": "t", "activo": true}
  ]
}
```
![[Pasted image 20261125124234.png|377]]

## 5.2. Aplicación de algoritmos
---
**Camino mínimo mediante Búsqueda en Anchura (BFS):**

- **Capa $N_0$ (distancia $0$):** $\{s\}$.
- **Capa $N_1$ (distancia $1$):** Al expandir $s$, se descubren sus vecinos directos $\{A, B\}$ con predecesor $s$.
- **Capa $N_2$ (distancia $2$):** Al expandir $A$ se descubre $C$, y al expandir $B$ se alcanza el sumidero $t$ (deteniendo la exploración).
- **Resultado analítico:** Existe ruta mínima de longitud $d_G(s, t) = 2$ arcos dada por $s \to B \to t$.


![[Pasted image 20261125123541.png]]

**Caminos disjuntos en arcos mediante Edmonds-Karp unitario ($c(e) = 1$):**

- **Iteración 1:** BFS sobre la red residual inicial encuentra el camino de aumento más corto $P_1: s \to B \to t$ (longitud $2$). Se envía $1$ unidad de flujo, saturando $(s, B)$ y $(B, t)$ y habilitando sus arcos residuales inversos $(B, s)$ y $(t, B)$.
    
- **Iteración 2:** En la red residual resultante, el arco $(s, B)$ tiene capacidad $0$, por lo que BFS explora desde $(s, A)$ y encuentra el camino de aumento $P_2: s \to A \to C \to t$ (longitud $3$). Se envía $1$ unidad adicional de flujo (flujo acumulado $= 2$).
    
- **Iteración 3 (terminación):** Los únicos arcos salientes de $s$, $(s, A)$ y $(s, B)$, presentan capacidad residual nula. No existen más caminos de aumento desde $s$ hacia $t$, concluyendo con $\max \vert{}\mathcal{P}_{s,t}\vert{} = 2$.

![[Pasted image 20261125123938.png]]

**Corte mínimo ($C$) mediante el Teorema Flujo Máximo - Corte Mínimo:**

- En la red residual final, ningún arco saliente de $s$ conserva capacidad positiva, por lo que el conjunto de vértices alcanzables desde la fuente es $R = \{s\}$ y su complemento es $V \setminus R = \{A, B, C, t\}$.
    
- Los arcos dirigidos originales que cruzan desde $R$ hacia $V \setminus R$ son $C = \{(s, A), (s, B)\}$, con cardinalidad $\vert{}C\vert{} = 2$. Su eliminación desconecta por completo el origen $s$ del resto de la red, verificando $\max \vert{}\mathcal{P}_{s,t}\vert{} = \min \vert{}C\vert{} = 2$.

## 5.3. Tabla comparativa de resultados
---

| Métrica evaluada | Resolución Manual | Ejecución en Simulador (`algorithms.py`) | Coincidencia |
| :--- | :---: | :---: | :---: |
| **Longitud camino mínimo $d_G(s, t)$** | $2$ arcos | $2$ arcos | $100\%$ |
| **Ruta mínima (BFS)** | $s \to B \to t$ | $s \to B \to t$ | $100\%$ |
| **Máx. caminos disjuntos ($\max \vert \mathcal{P}_{s,t} \vert$)** | $2$ caminos | $2$ caminos | $100\%$ |
| **Trayectorias disjuntas obtenidas** | $s \to B \to t$<br>$s \to A \to C \to t$ | $s \to B \to t$<br>$s \to A \to C \to t$ | $100\%$ |
| **Corte mínimo ($C$)** | $\{(s, A), (s, B)\}$ | $\{(s, A), (s, B)\}$ | $100\%$ |
| **Cardinalidad del corte ($\vert C \vert$)** | $2$ arcos | $2$ arcos | $100\%$ |


# 6. Conclusión
---



# 7. Anexos
---



# 8. Bibliografía
---
