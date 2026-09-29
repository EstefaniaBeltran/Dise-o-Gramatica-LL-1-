# Taller: Diseño e Implementación de una Gramática LL(1)

**Estudiante:** Yeimy Beltrán  
**Materia:** Compiladores / Lenguajes Formales  
**Lenguaje:** Python 3 (entorno Linux/Ubuntu)

---

## Qué se hizo

En este taller construí un pequeño lenguaje de programación que funciona como una calculadora avanzada con memoria. El programa es capaz de:
- Realizar operaciones aritméticas básicas: suma (`+`), resta (`-`), multiplicación (`*`), división (`/`) y residuo o módulo (`%`).
- Evaluar funciones matemáticas: valor absoluto (`abs`) y trigonometría (`Sin`, `Cos`, `Tan`).
- Guardar valores en variables mediante asignación (por ejemplo: `x = 10;`, `y = Sin(x) + 5;`).
- Manejar expresiones libres y combinadas respetando los paréntesis y la jerarquía de operaciones.

Para que el computador entienda este código, el proyecto está dividido en las tres fases clásicas de un compilador:

1. **Fase Léxica (Analizador Léxico o Lexer):**  
   Lee el texto que escribe el usuario caracter por caracter y lo agrupa en fichas llamadas *tokens* (números, nombres de variables, signos de suma, palabras reservadas como `Sin`, etc.). Si el usuario escribe algo inválido (como un signo `@`), aquí se detecta de inmediato y se avisa el error. También ignora espacios y comentarios iniciados con `#`.

2. **Fase Sintáctica (Analizador Sintáctico o Parser LL(1)):**  
   Verifica que los tokens estén en el orden correcto de acuerdo con las reglas de la gramática. Si el usuario olvida cerrar un paréntesis o pone dos operadores seguidos (`5 + * 3`), el parser detecta el error de sintaxis. Está programado mediante la técnica de *descenso recursivo*, lo que significa que cada regla de la gramática se convierte en una función de Python.

3. **Fase Semántica (Evaluador y Tabla de Símbolos):**  
   Aquí se revisa el significado de las cosas y se calculan los resultados:
   - Administra la **tabla de símbolos** (un diccionario en memoria donde se guardan los nombres de las variables y sus valores).
   - Comprueba que no usemos una variable que no ha sido creada o inicializada antes.
   - Previene errores matemáticos en tiempo de ejecución, como dividir entre cero o sacar el módulo entre cero.

---

## Explicación Sencilla de la Gramática

Para que el analizador funcione sin equivocarse y con solo mirar un símbolo hacia adelante (técnica **LL(1)**), la gramática se organiza por niveles de importancia (jerarquía matemática):

1. **Nivel del Programa y Sentencias ($P, L, S$):**  
   Un programa es una lista de instrucciones separadas por punto y coma (`;`). Cada instrucción puede ser una asignación a una variable (`x = ...`) o una operación directa.

2. **Nivel de Sumas y Restas ($E, E'$):**  
   Representa las expresiones generales. Tienen menor prioridad, por lo que se resuelven al final.

3. **Nivel de Multiplicaciones, Divisiones y Módulos ($T, T'$):**  
   Los términos tienen mayor prioridad que las sumas y restas.

4. **Nivel de Factores y Funciones ($F, F_{noid}, Fn$):**  
   Es lo más básico y con máxima prioridad: números directos, signos negativos, expresiones entre paréntesis `( ... )`, y llamadas a funciones como `Sin(...)` o `abs(...)`.

> **¿Por qué aparecen "primas" como $E'$ o $T'$ y el símbolo $\epsilon$?**  
> Si una regla dijera $E \to E + T$, el computador se llamaría a sí mismo infinitamente intentando resolver $E$ antes de avanzar. Para evitar ese bucle infinito (llamado *recursión izquierda*), dividimos la regla usando primas ($E'$). El símbolo $\epsilon$ (épsilon) simplemente le dice al código: *"si ya no hay más sumas ni restas, termina aquí y continúa"*.

---

### Producciones Formales de la Gramática

A continuación se listan las 27 reglas ordenadas por su función dentro del lenguaje:

#### 1. Estructura general de instrucciones
- **Regla 1:** $P \to L$ *(Un programa inicia con una lista de instrucciones)*
- **Regla 2:** $L \to S \; ; \; L$ *(Una instrucción terminada en punto y coma seguida de más instrucciones)*
- **Regla 3:** $L \to \epsilon$ *(Fin de la lista de instrucciones)*

#### 2. Instrucciones: Asignaciones y expresiones
- **Regla 4:** $S \to \textbf{id} \; S'$ *(Instrucción que empieza con una variable)*
- **Regla 5:** $S \to E_{noid}$ *(Instrucción que empieza directamente con un número, paréntesis o función)*
- **Regla 6:** $S' \to = \; E$ *(Si después de la variable viene un `=`, es una asignación)*
- **Regla 7:** $S' \to T' \; E'$ *(Si no hay `=`, la variable hace parte de una operación aritmética normal)*
- **Regla 8:** $E_{noid} \to F_{noid} \; T' \; E'$ *(Operación que no inicia con identificador)*

#### 3. Sumas y restas (Menor prioridad)
- **Regla 9:** $E \to T \; E'$ *(Una expresión comienza con un término)*
- **Regla 10:** $E' \to + \; T \; E'$ *(Operación suma)*
- **Regla 11:** $E' \to - \; T \; E'$ *(Operación resta)*
- **Regla 12:** $E' \to \epsilon$ *(No hay más sumas ni restas)*

#### 4. Multiplicaciones, divisiones y residuos (Media prioridad)
- **Regla 13:** $T \to F \; T'$ *(Un término comienza con un factor)*
- **Regla 14:** $T' \to * \; F \; T'$ *(Operación multiplicación)*
- **Regla 15:** $T' \to / \; F \; T'$ *(Operación división)*
- **Regla 16:** $T' \to \text{mod} \; F \; T'$ *(Operación módulo o residuo `%`)*
- **Regla 17:** $T' \to \epsilon$ *(No hay más multiplicaciones ni divisiones)*

#### 5. Factores, números y funciones matemáticas (Máxima prioridad)
- **Regla 18:** $F \to \textbf{id}$ *(Uso del valor de una variable guardada)*
- **Regla 19:** $F \to F_{noid}$ *(Otro tipo de factor)*
- **Regla 20:** $F_{noid} \to \textbf{num}$ *(Un número entero o decimal)*
- **Regla 21:** $F_{noid} \to - \; F$ *(Signo negativo unario, por ejemplo `-5`)*
- **Regla 22:** $F_{noid} \to ( \; E \; )$ *(Expresión agrupada entre paréntesis)*
- **Regla 23:** $F_{noid} \to Fn \; ( \; E \; )$ *(Llamada a una función con su argumento entre paréntesis)*
- **Regla 24:** $Fn \to \textbf{abs}$ *(Función valor absoluto)*
- **Regla 25:** $Fn \to \textbf{Sin}$ *(Función trigonométrica seno)*
- **Regla 26:** $Fn \to \textbf{Cos}$ *(Función trigonométrica coseno)*
- **Regla 27:** $Fn \to \textbf{Tan}$ *(Función trigonométrica tangente)*

---

## Conjuntos Matemáticos (Primeros, Siguientes y Predicción)

Para que el programa sea **LL(1)**, el analizador sintáctico necesita una "guía" para saber qué regla aplicar en cada momento con solo ver el siguiente token que tiene al frente (*lookahead*):

- **Primeros ($FIRST$):** Indica con qué fichas o símbolos válidos puede empezar una regla determinada.
- **Siguientes ($FOLLOW$):** Indica qué fichas pueden aparecer legalmente justo después de que se termina de procesar esa regla.
- **Predicción ($PRED$):** Es la regla de decisión que usa el código. Cuando el analizador lee el siguiente token, compara con este conjunto y elige el camino correcto sin dudar y sin tener que devolverse.

### Definición Matemática en $\LaTeX$

$$
\begin{aligned}
FIRST(P) &= \{ (, -, \text{Cos}, \text{Sin}, \text{Tan}, \text{abs}, \textbf{id}, \textbf{num}, \epsilon \} \\
FOLLOW(P) &= \{ \text{EOF} \} \\
FIRST(L) &= \{ (, -, \text{Cos}, \text{Sin}, \text{Tan}, \text{abs}, \textbf{id}, \textbf{num}, \epsilon \} \\
FOLLOW(L) &= \{ \text{EOF} \} \\
FIRST(S) &= \{ (, -, \text{Cos}, \text{Sin}, \text{Tan}, \text{abs}, \textbf{id}, \textbf{num} \} \\
FOLLOW(S) &= \{ ; \} \\
FIRST(S') &= \{ \text{mod}, *, +, -, /, =, \epsilon \} \\
FOLLOW(S') &= \{ ; \} \\
FIRST(E_{noid}) &= \{ (, -, \text{Cos}, \text{Sin}, \text{Tan}, \text{abs}, \textbf{num} \} \\
FOLLOW(E_{noid}) &= \{ ; \} \\
FIRST(E) &= \{ (, -, \text{Cos}, \text{Sin}, \text{Tan}, \text{abs}, \textbf{id}, \textbf{num} \} \\
FOLLOW(E) &= \{ ), ; \} \\
FIRST(E') &= \{ +, -, \epsilon \} \\
FOLLOW(E') &= \{ ), ; \} \\
FIRST(T) &= \{ (, -, \text{Cos}, \text{Sin}, \text{Tan}, \text{abs}, \textbf{id}, \textbf{num} \} \\
FOLLOW(T) &= \{ ), +, -, ; \} \\
FIRST(T') &= \{ \text{mod}, *, /, \epsilon \} \\
FOLLOW(T') &= \{ ), +, -, ; \} \\
FIRST(F) &= \{ (, -, \text{Cos}, \text{Sin}, \text{Tan}, \text{abs}, \textbf{id}, \textbf{num} \} \\
FOLLOW(F) &= \{ \text{mod}, ), *, +, -, /, ; \} \\
FIRST(F_{noid}) &= \{ (, -, \text{Cos}, \text{Sin}, \text{Tan}, \text{abs}, \textbf{num} \} \\
FOLLOW(F_{noid}) &= \{ \text{mod}, ), *, +, -, /, ; \} \\
FIRST(Fn) &= \{ \text{Cos}, \text{Sin}, \text{Tan}, \text{abs} \} \\
FOLLOW(Fn) &= \{ ( \}
\end{aligned}
$$

### Tabla Resumen de Primeros y Siguientes

| No Terminal ($A$) | ¿Con qué puede empezar? ($FIRST$) | ¿Qué puede venir después? ($FOLLOW$) |
| :--- | :--- | :--- |
| **$P$ (Programa)** | `(`, `-`, `Cos`, `Sin`, `Tan`, `abs`, `id`, `num`, `ε` | `EOF` (fin de archivo) |
| **$L$ (Lista de sentencias)** | `(`, `-`, `Cos`, `Sin`, `Tan`, `abs`, `id`, `num`, `ε` | `EOF` |
| **$S$ (Sentencia)** | `(`, `-`, `Cos`, `Sin`, `Tan`, `abs`, `id`, `num` | `;` |
| **$S'$ (Cola de sentencia)** | `%`, `*`, `+`, `-`, `/`, `=`, `ε` | `;` |
| **$E_{noid}$ (Expresión sin ID inicial)** | `(`, `-`, `Cos`, `Sin`, `Tan`, `abs`, `num` | `;` |
| **$E$ (Expresión)** | `(`, `-`, `Cos`, `Sin`, `Tan`, `abs`, `id`, `num` | `)`, `;` |
| **$E'$ (Cola de suma/resta)** | `+`, `-`, `ε` | `)`, `;` |
| **$T$ (Término)** | `(`, `-`, `Cos`, `Sin`, `Tan`, `abs`, `id`, `num` | `)`, `+`, `-`, `;` |
| **$T'$ (Cola de mult/div/mod)** | `%`, `*`, `/`, `ε` | `)`, `+`, `-`, `;` |
| **$F$ (Factor)** | `(`, `-`, `Cos`, `Sin`, `Tan`, `abs`, `id`, `num` | `%`, `)`, `*`, `+`, `-`, `/`, `;` |
| **$F_{noid}$ (Factor numérico/función)** | `(`, `-`, `Cos`, `Sin`, `Tan`, `abs`, `num` | `%`, `)`, `*`, `+`, `-`, `/`, `;` |
| **$Fn$ (Nombre de función)** | `Cos`, `Sin`, `Tan`, `abs` | `(` |

---

### Conjuntos de Predicción (La toma de decisiones del Parser)

Para cada producción posible $A \to \alpha$, el conjunto de predicción le indica al analizador exactamente qué token debe ver para elegir esa regla:

$$
PRED(A \to \alpha) = \begin{cases} 
FIRST(\alpha) & \text{si la regla no produce } \epsilon \\ 
(FIRST(\alpha) \setminus \{ \epsilon \}) \cup FOLLOW(A) & \text{si la regla produce } \epsilon 
\end{cases}
$$

$$
\begin{aligned}
PRED(P \to L) &= \{ \text{EOF}, (, -, \text{Cos}, \text{Sin}, \text{Tan}, \text{abs}, \textbf{id}, \textbf{num} \} \\
PRED(L \to S \; ; \; L) &= \{ (, -, \text{Cos}, \text{Sin}, \text{Tan}, \text{abs}, \textbf{id}, \textbf{num} \} \\
PRED(L \to \epsilon) &= \{ \text{EOF} \} \\
PRED(S \to \textbf{id} \; S') &= \{ \textbf{id} \} \\
PRED(S \to E_{noid}) &= \{ (, -, \text{Cos}, \text{Sin}, \text{Tan}, \text{abs}, \textbf{num} \} \\
PRED(S' \to = \; E) &= \{ = \} \\
PRED(S' \to T' \; E') &= \{ \text{mod}, *, +, -, /, ; \} \\
PRED(E_{noid} \to F_{noid} \; T' \; E') &= \{ (, -, \text{Cos}, \text{Sin}, \text{Tan}, \text{abs}, \textbf{num} \} \\
PRED(E \to T \; E') &= \{ (, -, \text{Cos}, \text{Sin}, \text{Tan}, \text{abs}, \textbf{id}, \textbf{num} \} \\
PRED(E' \to + \; T \; E') &= \{ + \} \\
PRED(E' \to - \; T \; E') &= \{ - \} \\
PRED(E' \to \epsilon) &= \{ ), ; \} \\
PRED(T \to F \; T') &= \{ (, -, \text{Cos}, \text{Sin}, \text{Tan}, \text{abs}, \textbf{id}, \textbf{num} \} \\
PRED(T' \to * \; F \; T') &= \{ * \} \\
PRED(T' \to / \; F \; T') &= \{ / \} \\
PRED(T' \to \text{mod} \; F \; T') &= \{ \text{mod} \} \\
PRED(T' \to \epsilon) &= \{ ), +, -, ; \} \\
PRED(F \to \textbf{id}) &= \{ \textbf{id} \} \\
PRED(F \to F_{noid}) &= \{ (, -, \text{Cos}, \text{Sin}, \text{Tan}, \text{abs}, \textbf{num} \} \\
PRED(F_{noid} \to \textbf{num}) &= \{ \textbf{num} \} \\
PRED(F_{noid} \to - \; F) &= \{ - \} \\
PRED(F_{noid} \to ( \; E \; )) &= \{ ( \} \\
PRED(F_{noid} \to Fn \; ( \; E \; )) &= \{ \text{Cos}, \text{Sin}, \text{Tan}, \text{abs} \} \\
PRED(Fn \to \textbf{abs}) &= \{ \textbf{abs} \} \\
PRED(Fn \to \textbf{Sin}) &= \{ \textbf{Sin} \} \\
PRED(Fn \to \textbf{Cos}) &= \{ \textbf{Cos} \} \\
PRED(Fn \to \textbf{Tan}) &= \{ \textbf{Tan} \}
\end{aligned}
$$

#### Tabla Resumen de Predicción

| Regla | Producción | Tokens que activan esta regla ($PRED$) |
| :---: | :--- | :--- |
| **1** | $P \to L$ | `EOF`, `(`, `-`, `Cos`, `Sin`, `Tan`, `abs`, `id`, `num` |
| **2** | $L \to S \; ; \; L$ | `(`, `-`, `Cos`, `Sin`, `Tan`, `abs`, `id`, `num` |
| **3** | $L \to \epsilon$ | `EOF` |
| **4** | $S \to \textbf{id} \; S'$ | `id` |
| **5** | $S \to E_{noid}$ | `(`, `-`, `Cos`, `Sin`, `Tan`, `abs`, `num` |
| **6** | $S' \to = \; E$ | `=` |
| **7** | $S' \to T' \; E'$ | `%`, `*`, `+`, `-`, `/`, `;` |
| **8** | $E_{noid} \to F_{noid} \; T' \; E'$ | `(`, `-`, `Cos`, `Sin`, `Tan`, `abs`, `num` |
| **9** | $E \to T \; E'$ | `(`, `-`, `Cos`, `Sin`, `Tan`, `abs`, `id`, `num` |
| **10** | $E' \to + \; T \; E'$ | `+` |
| **11** | $E' \to - \; T \; E'$ | `-` |
| **12** | $E' \to \epsilon$ | `)`, `;` |
| **13** | $T \to F \; T'$ | `(`, `-`, `Cos`, `Sin`, `Tan`, `abs`, `id`, `num` |
| **14** | $T' \to * \; F \; T'$ | `*` |
| **15** | $T' \to / \; F \; T'$ | `/` |
| **16** | $T' \to \text{mod} \; F \; T'$ | `%` |
| **17** | $T' \to \epsilon$ | `)`, `+`, `-`, `;` |
| **18** | $F \to \textbf{id}$ | `id` |
| **19** | $F \to F_{noid}$ | `(`, `-`, `Cos`, `Sin`, `Tan`, `abs`, `num` |
| **20** | $F_{noid} \to \textbf{num}$ | `num` |
| **21** | $F_{noid} \to - \; F$ | `-` |
| **22** | $F_{noid} \to ( \; E \; )$ | `(` |
| **23** | $F_{noid} \to Fn \; ( \; E \; )$ | `Cos`, `Sin`, `Tan`, `abs` |
| **24** | $Fn \to \textbf{abs}$ | `abs` |
| **25** | $Fn \to \textbf{Sin}$ | `Sin` |
| **26** | $Fn \to \textbf{Cos}$ | `Cos` |
| **27** | $Fn \to \textbf{Tan}$ | `Tan` |

#### ¿Por qué esto demuestra que es LL(1)?
Si revisamos las opciones de cualquier decisión (por ejemplo, para $E'$ si sumamos con `+`, restamos con `-`, o terminamos con `)` o `;`), **ningún conjunto comparte tokens**:

$$
PRED(A \to \alpha_i) \cap PRED(A \to \alpha_j) = \emptyset \quad \forall \; i \neq j
$$

Al ser conjuntos completamente disjuntos, el código en Python nunca tiene dudas de qué función llamar ni necesita retroceder (*backtracking*).

---

## Cómo se ejecuta

### Requisitos
- Linux (Ubuntu 20.04 / 22.04 LTS o similar).
- Python 3.8 o superior.
- No se necesitan librerías externas (solo la librería estándar de Python).

### Estructura de la carpeta
```text
taller_gramatica_ll1/
├── interprete.py    # Código en Python con el Lexer, Parser y Evaluador
├── ejemplo.txt       # Archivo de texto con instrucciones de prueba
└── README.md         # Este documento con las explicaciones del taller
```

### Comandos en la terminal

1. **Entrar a la carpeta del proyecto en Documentos:**
   ```bash
   cd ~/Documentos/taller_gramatica_ll1
   ```

2. **Revisar que Python esté disponible:**
   ```bash
   python3 --version
   ```

3. **Ejecutar el archivo de prueba (`ejemplo.txt`):**
   Lee el archivo, ejecuta todas las asignaciones y operaciones, y muestra la tabla de variables al final:
   ```bash
   python3 interprete.py ejemplo.txt
   ```

4. **Correr las pruebas automáticas:**
   Prueba todas las operaciones y comprueba que los errores se capturen con mensajes claros:
   ```bash
   python3 interprete.py --test
   ```

5. **Modo interactivo (escribir operaciones directamente):**
   ```bash
   python3 interprete.py
   ```
   *Ejemplo en la consola:*
   ```text
   >> x = 10;
   x = 10
   >> y = Sin(0) + 5;
   y = 5.0
   >> total = x * y;
   total = 50.0
   >> salir
   ```

---

## Pruebas y Resultados

Diseñé estas pruebas para comprobar que cada parte del código funciona correctamente y que ningún error inesperado hace caer el programa.

### Prueba 1: Asignaciones de variables y aritmética básica (+, -, *, /, %)
Se prueba que se reconozcan los nombres de las variables y los números, que se calculen las 5 operaciones y que queden guardadas en memoria.
- **Entrada:**
  ```text
  a = 15; b = 4; suma = a + b; resta = a - b; mult = a * b; div = a / b; mod = a % b;
  ```
- **Resultado esperado:**
  $a = 15$, $b = 4$, $\text{suma} = 19$, $\text{resta} = 11$, $\text{mult} = 60$, $\text{div} = 3.75$ y $\text{mod} = 3$.

[Insertar pantallazo de la prueba 1 aquí]

---

### Prueba 2: Funciones matemáticas (abs, Sin, Cos, Tan)
Se evalúa que el programa reconozca las funciones especiales y calcule su valor numérico real.
- **Entrada:**
  ```text
  ang = 0; s = Sin(ang); c = Cos(ang); t = Tan(ang); val = abs(-42.5);
  ```
- **Resultado esperado:**
  $\text{ang} = 0$, $s = 0.0$, $c = 1.0$, $t = 0.0$ y $\text{val} = 42.5$.

[Insertar pantallazo de la prueba 2 aquí]

---

### Prueba 3: Jerarquía de operaciones y paréntesis
Se comprueba que se respeten las reglas matemáticas: resolver primero lo de adentro de los paréntesis y hacer las multiplicaciones/divisiones antes de las sumas.
- **Entrada:**
  ```text
  x = 10; y = 5; res = ((x + y) * 2) - abs(-8) / 2;
  ```
- **Resultado esperado:**
  Primero suma $(10 + 5) = 15$, luego multiplica por 2 ($30$), calcula $\text{abs}(-8)/2 = 4.0$ y resta para obtener $\text{res} = 26.0$.

[Insertar pantallazo de la prueba 3 aquí]

---

### Prueba 4: Reutilización de variables en memoria
Verifica que las variables guardadas se puedan usar en cálculos posteriores.
- **Entrada:**
  ```text
  radio = 3; area_aprox = 3.14159 * radio * radio;
  ```
- **Resultado esperado:**
  $\text{radio} = 3$ y $\text{area\_aprox} = 28.27431$.

[Insertar pantallazo de la prueba 4 aquí]

---

### Prueba 5: Detección de errores léxicos
Si el usuario escribe caracteres raros que no existen en el lenguaje, el programa debe avisar en qué caracter falló.
- **Entrada:**
  ```text
  x = 10 @ 2;
  ```
- **Resultado:**
  `Error lexico: Caracter no reconocido '@'`

[Insertar pantallazo de la prueba 5 aquí]

---

### Prueba 6: Detección de errores sintácticos
Si la estructura de la oración está rota (por ejemplo, faltan paréntesis o sobran signos).
- **Caso A (Paréntesis sin cerrar):**
  - **Entrada:** `y = (5 + 3 * 2;`
  - **Resultado:** `Error sintactico: Se esperaba ')', se obtuvo ';'`
- **Caso B (Operador sin número al lado):**
  - **Entrada:** `z = 5 + * 2;`
  - **Resultado:** `Error sintactico: Expresion no valida, token inesperado '*'`

[Insertar pantallazo de la prueba 6 aquí]

---

### Prueba 7: Detección de errores semánticos
Errores de lógica que violan las reglas del lenguaje o de las matemáticas:
- **Caso A (Usar una variable que no existe todavía):**
  - **Entrada:** `total = precio + 10;`
  - **Resultado:** `Error semantico: Variable 'precio' no ha sido inicializada`
- **Caso B (División entre cero):**
  - **Entrada:** `n = 20 / 0;`
  - **Resultado:** `Error semantico: Division por cero`
- **Caso C (Módulo entre cero):**
  - **Entrada:** `m = 20 % 0;`
  - **Resultado:** `Error semantico: Modulo por cero`

[Insertar pantallazo de la prueba 7 aquí]
