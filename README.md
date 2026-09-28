# Taller: Diseño e Implementación de una Gramática LL(1)

**Autora:** Yeimy Beltrán  
**Entorno:** Python 3 / Linux (Ubuntu)

---

## Qué se hizo

En este taller diseñé e implementé un analizador e intérprete basado en una gramática formal **LL(1)** para un lenguaje de programación aritmético. El lenguaje soporta operaciones binarias básicas ($+$, $-$, $*$, $/$, $\%$), funciones matemáticas ($\text{abs}$, $\text{Sin}$, $\text{Cos}$, $\text{Tan}$) y asignación de variables en memoria mediante una tabla de símbolos.

El sistema garantiza de manera estricta las tres fases fundamentales del procesamiento de lenguajes:

1. **Fase Léxica (Lexer):** Escanea el flujo de caracteres para producir tokens clasificados: identificadores ($\textbf{id}$), literales numéricos enteros y decimales ($\textbf{num}$), operadores aritméticos, asignación ($=$), agrupadores ($($ y $)$), delimitadores de instrucción ($;$) y palabras reservadas para las funciones ($\text{abs}$, $\text{Sin}$, $\text{Cos}$, $\text{Tan}$). Ignora espacios en blanco y comentarios con `#`, y reporta de inmediato cualquier carácter no admitido.
2. **Fase Sintáctica (Parser LL(1)):** Implementé un analizador descendente predictivo recursivo. Para admitir tanto asignaciones de variables ($\textbf{id} = E$) como expresiones sin ambigüedad en el token $\textbf{id}$, apliqué factorización por la izquierda. Esto asegura que la selección de cada producción sea determinista con exactamente 1 símbolo de preanálisis (*lookahead*).
3. **Fase Semántica (Evaluador y Tabla de Símbolos):** Valida la existencia y alcance de las variables antes de su uso (evitando variables no inicializadas), detecta en tiempo de ejecución divisiones y módulos por cero, y sintetiza el cálculo numérico respetando la precedencia formal y asociatividad de las operaciones.

---

### Especificación Formal de la Gramática LL(1)

#### Símbolos Terminales ($\Sigma$)
$$\Sigma = \{ \textbf{id}, \textbf{num}, =, +, -, *, /, \%, (, ), \textbf{abs}, \textbf{Sin}, \textbf{Cos}, \textbf{Tan}, ;, \$ \}$$

#### Símbolos No Terminales ($V_N$)
$$V_N = \{ P, L, S, S', E_{noid}, E, E', T, T', F, F_{noid}, Fn \}$$

**Símbolo inicial:** $P$

#### Producciones de la Gramática
1. $P \to L$
2. $L \to S \; ; \; L$
3. $L \to \epsilon$
4. $S \to \textbf{id} \; S'$
5. $S \to E_{noid}$
6. $S' \to = \; E$
7. $S' \to T' \; E'$
8. $E_{noid} \to F_{noid} \; T' \; E'$
9. $E \to T \; E'$
10. $E' \to + \; T \; E'$
11. $E' \to - \; T \; E'$
12. $E' \to \epsilon$
13. $T \to F \; T'$
14. $T' \to * \; F \; T'$
15. $T' \to / \; F \; T'$
16. $T' \to \% \; F \; T'$
17. $T' \to \epsilon$
18. $F \to \textbf{id}$
19. $F \to F_{noid}$
20. $F_{noid} \to \textbf{num}$
21. $F_{noid} \to - \; F$
22. $F_{noid} \to ( \; E \; )$
23. $F_{noid} \to Fn \; ( \; E \; )$
24. $Fn \to \textbf{abs}$
25. $Fn \to \textbf{Sin}$
26. $Fn \to \textbf{Cos}$
27. $Fn \to \textbf{Tan}$

---

### Conjuntos Matemáticos: Primeros ($FIRST$) y Siguientes ($FOLLOW$)

A continuación presento el cálculo formal de los conjuntos de primeros y siguientes para cada no terminal:

| No Terminal ($A$) | $FIRST(A)$ | $FOLLOW(A)$ |
| :--- | :--- | :--- |
| $P$ | $\{ (, -, \textbf{Cos}, \textbf{Sin}, \textbf{Tan}, \textbf{abs}, \textbf{id}, \textbf{num}, \epsilon \}$ | $\{ \$ \}$ |
| $L$ | $\{ (, -, \textbf{Cos}, \textbf{Sin}, \textbf{Tan}, \textbf{abs}, \textbf{id}, \textbf{num}, \epsilon \}$ | $\{ \$ \}$ |
| $S$ | $\{ (, -, \textbf{Cos}, \textbf{Sin}, \textbf{Tan}, \textbf{abs}, \textbf{id}, \textbf{num} \}$ | $\{ ; \}$ |
| $S'$ | $\{ \%, *, +, -, /, =, \epsilon \}$ | $\{ ; \}$ |
| $E_{noid}$ | $\{ (, -, \textbf{Cos}, \textbf{Sin}, \textbf{Tan}, \textbf{abs}, \textbf{num} \}$ | $\{ ; \}$ |
| $E$ | $\{ (, -, \textbf{Cos}, \textbf{Sin}, \textbf{Tan}, \textbf{abs}, \textbf{id}, \textbf{num} \}$ | $\{ ), ; \}$ |
| $E'$ | $\{ +, -, \epsilon \}$ | $\{ ), ; \}$ |
| $T$ | $\{ (, -, \textbf{Cos}, \textbf{Sin}, \textbf{Tan}, \textbf{abs}, \textbf{id}, \textbf{num} \}$ | $\{ ), +, -, ; \}$ |
| $T'$ | $\{ \%, *, /, \epsilon \}$ | $\{ ), +, -, ; \}$ |
| $F$ | $\{ (, -, \textbf{Cos}, \textbf{Sin}, \textbf{Tan}, \textbf{abs}, \textbf{id}, \textbf{num} \}$ | $\{ \%, ), *, +, -, /, ; \}$ |
| $F_{noid}$ | $\{ (, -, \textbf{Cos}, \textbf{Sin}, \textbf{Tan}, \textbf{abs}, \textbf{num} \}$ | $\{ \%, ), *, +, -, /, ; \}$ |
| $Fn$ | $\{ \textbf{Cos}, \textbf{Sin}, \textbf{Tan}, \textbf{abs} \}$ | $\{ ( \}$ |

---

### Conjuntos de Predicción / Selección ($PRED$)

El conjunto de predicción para cada regla $A \to \alpha$ se define como:

$$PRED(A \to \alpha) = \begin{cases} FIRST(\alpha) & \text{si } \epsilon \notin FIRST(\alpha) \\ (FIRST(\alpha) \setminus \{ \epsilon \}) \cup FOLLOW(A) & \text{si } \epsilon \in FIRST(\alpha) \end{cases}$$

| Regla | Producción | $PRED$ (Conjunto de Predicción) |
| :---: | :--- | :--- |
| **1** | $P \to L$ | $\{ \$, (, -, \textbf{Cos}, \textbf{Sin}, \textbf{Tan}, \textbf{abs}, \textbf{id}, \textbf{num} \}$ |
| **2** | $L \to S \; ; \; L$ | $\{ (, -, \textbf{Cos}, \textbf{Sin}, \textbf{Tan}, \textbf{abs}, \textbf{id}, \textbf{num} \}$ |
| **3** | $L \to \epsilon$ | $\{ \$ \}$ |
| **4** | $S \to \textbf{id} \; S'$ | $\{ \textbf{id} \}$ |
| **5** | $S \to E_{noid}$ | $\{ (, -, \textbf{Cos}, \textbf{Sin}, \textbf{Tan}, \textbf{abs}, \textbf{num} \}$ |
| **6** | $S' \to = \; E$ | $\{ = \}$ |
| **7** | $S' \to T' \; E'$ | $\{ \%, *, +, -, /, ; \}$ |
| **8** | $E_{noid} \to F_{noid} \; T' \; E'$ | $\{ (, -, \textbf{Cos}, \textbf{Sin}, \textbf{Tan}, \textbf{abs}, \textbf{num} \}$ |
| **9** | $E \to T \; E'$ | $\{ (, -, \textbf{Cos}, \textbf{Sin}, \textbf{Tan}, \textbf{abs}, \textbf{id}, \textbf{num} \}$ |
| **10** | $E' \to + \; T \; E'$ | $\{ + \}$ |
| **11** | $E' \to - \; T \; E'$ | $\{ - \}$ |
| **12** | $E' \to \epsilon$ | $\{ ), ; \}$ |
| **13** | $T \to F \; T'$ | $\{ (, -, \textbf{Cos}, \textbf{Sin}, \textbf{Tan}, \textbf{abs}, \textbf{id}, \textbf{num} \}$ |
| **14** | $T' \to * \; F \; T'$ | $\{ * \}$ |
| **15** | $T' \to / \; F \; T'$ | $\{ / \}$ |
| **16** | $T' \to \% \; F \; T'$ | $\{ \% \}$ |
| **17** | $T' \to \epsilon$ | $\{ ), +, -, ; \}$ |
| **18** | $F \to \textbf{id}$ | $\{ \textbf{id} \}$ |
| **19** | $F \to F_{noid}$ | $\{ (, -, \textbf{Cos}, \textbf{Sin}, \textbf{Tan}, \textbf{abs}, \textbf{num} \}$ |
| **20** | $F_{noid} \to \textbf{num}$ | $\{ \textbf{num} \}$ |
| **21** | $F_{noid} \to - \; F$ | $\{ - \}$ |
| **22** | $F_{noid} \to ( \; E \; )$ | $\{ ( \}$ |
| **23** | $F_{noid} \to Fn \; ( \; E \; )$ | $\{ \textbf{Cos}, \textbf{Sin}, \textbf{Tan}, \textbf{abs} \}$ |
| **24** | $Fn \to \textbf{abs}$ | $\{ \textbf{abs} \}$ |
| **25** | $Fn \to \textbf{Sin}$ | $\{ \textbf{Sin} \}$ |
| **26** | $Fn \to \textbf{Cos}$ | $\{ \textbf{Cos} \}$ |
| **27** | $Fn \to \textbf{Tan}$ | $\{ \textbf{Tan} \}$ |

#### Verificación de la Condición LL(1)
Para cada no terminal con producciones alternativas $A \to \alpha_1 \mid \alpha_2 \mid \dots \mid \alpha_n$, se cumple rigurosamente que:

$$PRED(A \to \alpha_i) \cap PRED(A \to \alpha_j) = \emptyset \quad \forall \; i \neq j$$

Por lo tanto, la gramática es estrictamente determinista y pertenece a la clase **LL(1)**.

---

## Cómo se ejecuta

### Requisitos
- Linux (probado en Ubuntu 20.04 / 22.04 LTS).
- Python 3.8 o superior.
- No requiere dependencias externas ni librerías de terceros (utiliza únicamente la librería estándar de Python).

### Estructura del proyecto
```text
taller_gramatica_ll1/
├── interprete.py    # Analizador Léxico, Sintáctico LL(1) y Semántico
├── ejemplo.txt       # Script de demostración con operaciones y asignaciones
└── README.md         # Documentación académica del taller
```

### Instrucciones paso a paso en terminal

1. **Abrir la terminal e ingresar al directorio del taller:**
   ```bash
   cd taller_gramatica_ll1
   ```

2. **Verificar la versión instalada de Python:**
   ```bash
   python3 --version
   ```

3. **Ejecutar el script de prueba integrado:**
   Para ejecutar el archivo de ejemplo `ejemplo.txt` y observar la evaluación de las instrucciones junto a la tabla de símbolos final:
   ```bash
   python3 interprete.py ejemplo.txt
   ```

4. **Ejecutar la suite automatizada de pruebas:**
   Para comprobar todos los casos válidos y los escenarios de error controlado (léxico, sintáctico y semántico):
   ```bash
   python3 interprete.py --test
   ```

5. **Modo interactivo (REPL):**
   Si se desea ingresar instrucciones interactivamente línea por línea:
   ```bash
   python3 interprete.py
   ```
   *Ejemplo de uso en el prompt:*
   ```text
   >> x = 10;
   x = 10
   >> y = Sin(0) + 5;
   y = 5.0
   >> res = (x * 2) - y;
   res = 15.0
   >> salir
   ```

---

## Pruebas y Resultados

Para certificar el correcto funcionamiento de las fases léxica, sintáctica y semántica, diseñé un conjunto completo de pruebas unitarias y de integración.

### Prueba 1: Asignaciones de variables y aritmética básica ($+$, $-$, $*$, $/$, $\%$)
Esta prueba comprueba la correcta tokenización de identificadores y números, el análisis sintáctico de operaciones binarias y la actualización en la tabla de símbolos.
- **Entrada:**
  ```text
  a = 15; b = 4; suma = a + b; resta = a - b; mult = a * b; div = a / b; mod = a % b;
  ```
- **Resultado:**
  Se asigna $a = 15$, $b = 4$, $\text{suma} = 19$, $\text{resta} = 11$, $\text{mult} = 60$, $\text{div} = 3.75$ y $\text{mod} = 3$.

[Insertar pantallazo de la prueba 1 aquí]

---

### Prueba 2: Funciones matemáticas ($\text{abs}$, $\text{Sin}$, $\text{Cos}$, $\text{Tan}$)
Se verifica el reconocimiento de palabras reservadas, la resolución de argumentos entre paréntesis y la invocación de las funciones matemáticas estándar.
- **Entrada:**
  ```text
  ang = 0; s = Sin(ang); c = Cos(ang); t = Tan(ang); val = abs(-42.5);
  ```
- **Resultado:**
  $\text{ang} = 0$, $s = 0.0$, $c = 1.0$, $t = 0.0$ y $\text{val} = 42.5$.

[Insertar pantallazo de la prueba 2 aquí]

---

### Prueba 3: Jerarquía de operadores y expresiones compuestas con paréntesis
Se evalúa la correcta precedencia gramatical (multiplicación, división y módulo preceden a la suma y resta), la asociatividad por izquierda y la anidación de paréntesis.
- **Entrada:**
  ```text
  x = 10; y = 5; res = ((x + y) * 2) - abs(-8) / 2;
  ```
- **Resultado:**
  El analizador evalúa primero $(x + y) = 15$, luego multiplica por $2$ ($30$), calcula $\text{abs}(-8) / 2 = 4.0$ y finalmente resta para obtener $\text{res} = 26.0$.

[Insertar pantallazo de la prueba 3 aquí]

---

### Prueba 4: Reutilización acumulativa de variables en la tabla de símbolos
Demuestra que la memoria de variables persiste durante la ejecución del programa y que los valores previamente computados pueden ser utilizados en nuevas fórmulas.
- **Entrada:**
  ```text
  radio = 3; area_aprox = 3.14159 * radio * radio;
  ```
- **Resultado:**
  $\text{radio} = 3$ y $\text{area\_aprox} = 28.27431$.

[Insertar pantallazo de la prueba 4 aquí]

---

### Prueba 5: Detección y captura de errores léxicos
Se verifica que el analizador léxico identifique caracteres ajenos al alfabeto del lenguaje y reporte el error sin generar un fallo abrupto en el intérprete.
- **Entrada:**
  ```text
  x = 10 @ 2;
  ```
- **Resultado obtenido:**
  `Error lexico: Caracter no reconocido '@'`

[Insertar pantallazo de la prueba 5 aquí]

---

### Prueba 6: Detección y captura de errores sintácticos
Se valida que el parser descendente reporte discrepancias con la gramática, tales como paréntesis sin cerrar o tokens inesperados que violen los conjuntos de selección.
- **Caso A (Paréntesis sin cerrar):**
  - **Entrada:** `y = (5 + 3 * 2;`
  - **Resultado:** `Error sintactico: Se esperaba ')', se obtuvo ';'`
- **Caso B (Operador sin operando):**
  - **Entrada:** `z = 5 + * 2;`
  - **Resultado:** `Error sintactico: Expresion no valida, token inesperado '*'`

[Insertar pantallazo de la prueba 6 aquí]

---

### Prueba 7: Detección y captura de errores semánticos
Se asegura la consistencia de las reglas semánticas en tiempo de ejecución: uso de variables declaradas y prohibición de operaciones aritméticas matemáticamente indefinidas.
- **Caso A (Variable no inicializada):**
  - **Entrada:** `total = precio + 10;`
  - **Resultado:** `Error semantico: Variable 'precio' no ha sido inicializada`
- **Caso B (División por cero):**
  - **Entrada:** `n = 20 / 0;`
  - **Resultado:** `Error semantico: Division por cero`
- **Caso C (Módulo por cero):**
  - **Entrada:** `m = 20 % 0;`
  - **Resultado:** `Error semantico: Modulo por cero`

[Insertar pantallazo de la prueba 7 aquí]
