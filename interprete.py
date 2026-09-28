import sys
import math

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[0] if text else None

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def number(self):
        result = ''
        has_dot = False
        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if has_dot:
                    raise Exception("Error lexico: Numero con formato decimal invalido")
                has_dot = True
            result += self.current_char
            self.advance()
        return ('num', float(result) if has_dot else int(result))

    def identifier(self):
        result = ''
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        keywords = {'abs': 'abs', 'Sin': 'Sin', 'Cos': 'Cos', 'Tan': 'Tan'}
        if result in keywords:
            return (keywords[result], result)
        return ('id', result)

    def get_next_token(self):
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char == '#':
                while self.current_char and self.current_char != '\n':
                    self.advance()
                continue
            if self.current_char.isdigit():
                return self.number()
            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()
            if self.current_char == '+':
                self.advance()
                return ('+', '+')
            if self.current_char == '-':
                self.advance()
                return ('-', '-')
            if self.current_char == '*':
                self.advance()
                return ('*', '*')
            if self.current_char == '/':
                self.advance()
                return ('/', '/')
            if self.current_char == '%':
                self.advance()
                return ('%', '%')
            if self.current_char == '=':
                self.advance()
                return ('=', '=')
            if self.current_char == '(':
                self.advance()
                return ('(', '(')
            if self.current_char == ')':
                self.advance()
                return (')', ')')
            if self.current_char == ';':
                self.advance()
                return (';', ';')
            char = self.current_char
            self.advance()
            raise Exception(f"Error lexico: Caracter no reconocido '{char}'")
        return ('$', '$')

class Parser:
    def __init__(self, lexer, symbol_table=None):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.symbol_table = symbol_table if symbol_table is not None else {}

    def match(self, token_type):
        if self.current_token[0] == token_type:
            val = self.current_token[1]
            self.current_token = self.lexer.get_next_token()
            return val
        raise Exception(f"Error sintactico: Se esperaba '{token_type}', se obtuvo '{self.current_token[0]}'")

    def programa(self):
        results = []
        while self.current_token[0] != '$':
            res = self.instruccion()
            if res is not None:
                results.append(res)
            if self.current_token[0] == ';':
                self.match(';')
        return results

    def instruccion(self):
        if self.current_token[0] == 'id':
            var_name = self.match('id')
            if self.current_token[0] == '=':
                self.match('=')
                val = self.E()
                self.symbol_table[var_name] = val
                return (var_name, val)
            else:
                if var_name not in self.symbol_table:
                    raise Exception(f"Error semantico: Variable '{var_name}' no ha sido inicializada")
                val = self.symbol_table[var_name]
                val = self.T_prime(val)
                val = self.E_prime(val)
                return val
        else:
            return self.E_noid()

    def E_noid(self):
        val = self.F_noid()
        val = self.T_prime(val)
        val = self.E_prime(val)
        return val

    def E(self):
        val = self.T()
        val = self.E_prime(val)
        return val

    def E_prime(self, left):
        if self.current_token[0] == '+':
            self.match('+')
            right = self.T()
            return self.E_prime(left + right)
        elif self.current_token[0] == '-':
            self.match('-')
            right = self.T()
            return self.E_prime(left - right)
        return left

    def T(self):
        val = self.F()
        val = self.T_prime(val)
        return val

    def T_prime(self, left):
        if self.current_token[0] == '*':
            self.match('*')
            right = self.F()
            return self.T_prime(left * right)
        elif self.current_token[0] == '/':
            self.match('/')
            right = self.F()
            if right == 0:
                raise Exception("Error semantico: Division por cero")
            return self.T_prime(left / right)
        elif self.current_token[0] == '%':
            self.match('%')
            right = self.F()
            if right == 0:
                raise Exception("Error semantico: Modulo por cero")
            return self.T_prime(left % right)
        return left

    def F(self):
        if self.current_token[0] == 'id':
            var_name = self.match('id')
            if var_name not in self.symbol_table:
                raise Exception(f"Error semantico: Variable '{var_name}' no ha sido inicializada")
            return self.symbol_table[var_name]
        return self.F_noid()

    def F_noid(self):
        if self.current_token[0] == 'num':
            return self.match('num')
        elif self.current_token[0] == '-':
            self.match('-')
            return -self.F()
        elif self.current_token[0] == '(':
            self.match('(')
            val = self.E()
            self.match(')')
            return val
        elif self.current_token[0] in ('abs', 'Sin', 'Cos', 'Tan'):
            fn = self.match(self.current_token[0])
            self.match('(')
            val = self.E()
            self.match(')')
            if fn == 'abs':
                return abs(val)
            elif fn == 'Sin':
                return math.sin(val)
            elif fn == 'Cos':
                return math.cos(val)
            elif fn == 'Tan':
                return math.tan(val)
        raise Exception(f"Error sintactico: Expresion no valida, token inesperado '{self.current_token[0]}'")

def ejecutar_codigo(codigo, tabla=None):
    if tabla is None:
        tabla = {}
    lexer = Lexer(codigo)
    parser = Parser(lexer, tabla)
    return parser.programa(), tabla

def modo_pruebas():
    casos = [
        ("Asignaciones y Aritmetica basica", "a = 15; b = 4; suma = a + b; resta = a - b; mult = a * b; div = a / b; mod = a % b;"),
        ("Funciones Trigonometricas y Absoluto", "ang = 0; s = Sin(ang); c = Cos(ang); t = Tan(ang); val = abs(-42.5);"),
        ("Expresiones combinadas con parentesis", "x = 10; y = 5; res = ((x + y) * 2) - abs(-8) / 2;"),
        ("Reutilizacion de variables en expresiones", "radio = 3; area_aprox = 3.14159 * radio * radio;"),
        ("Error lexico (caracter no valido)", "x = 10 @ 2;"),
        ("Error sintactico (parentesis sin cerrar)", "y = (5 + 3 * 2;"),
        ("Error sintactico (operador sin operando)", "z = 5 + * 2;"),
        ("Error semantico (variable no inicializada)", "total = precio + 10;"),
        ("Error semantico (division por cero)", "n = 20 / 0;"),
        ("Error semantico (modulo por cero)", "m = 20 % 0;")
    ]

    print("=" * 60)
    print("EJECUTANDO BATERIA DE PRUEBAS DEL INTERPRETE LL(1)")
    print("=" * 60)
    
    tabla_compartida = {}
    for titulo, codigo in casos:
        print(f"\n[PRUEBA] {titulo}")
        print(f"Codigo entrada: {codigo}")
        try:
            resultados, _ = ejecutar_codigo(codigo, {} if "Error" in titulo else tabla_compartida)
            print("Resultado:")
            for r in resultados:
                if isinstance(r, tuple):
                    print(f"  {r[0]} = {r[1]}")
                else:
                    print(f"  Salida: {r}")
        except Exception as e:
            print(f"  Captura controlada: {e}")

    print("\n" + "=" * 60)
    print("Pruebas completadas.")
    print("=" * 60)

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            modo_pruebas()
            return
        
        with open(sys.argv[1], 'r') as f:
            codigo = f.read()
        try:
            resultados, tabla = ejecutar_codigo(codigo)
            print("Ejecucion finalizada con exito:")
            for r in resultados:
                if isinstance(r, tuple):
                    print(f"{r[0]} = {r[1]}")
                else:
                    print(f"Salida: {r}")
            print("\nTabla de simbolos final:")
            for k, v in tabla.items():
                print(f"  {k} : {v}")
        except Exception as e:
            print(f"Error durante la ejecucion: {e}")
        return

    print("Interprete Gramatica LL(1) - Yeimy Beltran")
    print("Escriba 'salir' para terminar o ingrese sentencias terminadas en ';' (ej: x = Sin(0) + 5;)\n")
    tabla = {}
    while True:
        try:
            linea = input(">> ")
            if linea.strip() == "salir":
                break
            if not linea.strip():
                continue
            if not linea.strip().endswith(';'):
                linea += ';'
            res, tabla = ejecutar_codigo(linea, tabla)
            for r in res:
                if isinstance(r, tuple):
                    print(f"{r[0]} = {r[1]}")
                else:
                    print(r)
        except Exception as e:
            print(f"{e}")

if __name__ == "__main__":
    main()
