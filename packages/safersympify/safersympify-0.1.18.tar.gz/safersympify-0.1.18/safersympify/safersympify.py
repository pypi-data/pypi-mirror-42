r"""
    Convert user input into SymPy expressions.


    RECIPES:

    Create a SymPy expression from user input (pure Python syntax with whitelisted oprators and functions only):
    >>> expr = SaferSympify().str2sympy('-sqrt(1 + a**b*b)/((a**b)*b+1)')
    >>> expr
    -1/sqrt(a**b*b + 1)

    Get free symbols:
    >>> sorted(expr.free_symbols, key=lambda x: str(x))
    [a, b]

    Evaluate expression:
    >>> expr.evalf(subs={'a': 1, 'b': 3, 'c': 5})  # Note extra values can be passed too
    -0.500000000000000

    Simplify expression:
    >>> expr.simplify()
    -1/sqrt(a**b*b + 1)

    Pretty-print expression as Latex (could be displayed in browser with MathJax)
    >>> sympy.latex(expr)
    '- \\frac{1}{\\sqrt{a^{b} b + 1}}'

    Pretty-print in terminal
    >>> sympy.pprint(expr, use_unicode_sqrt_char=True)
         -1      
    ─────────────
       __________
      ╱  b       
    ╲╱  a ⋅b + 1 

"""
import ast
import operator
import sympy


class SaferSympify:
    """ Handles unsanitized user input instead of SymPy, which does not do that yet.
    See SymPy PR12524 for details: https://github.com/sympy/sympy/pull/12524

    """
    def __init__(self):
        self.node_types_allowed = self._get_node_types_allowed()
        self.binary_operator_types_allowed = self._get_binary_operator_types_allowed()
        self.unary_operator_types_allowed =  self._get_unary_operator_types_allowed()
        self.functions_allowed =  self._get_functions_allowed()

    def str2sympy(self, string):
        ast_expr = ast.parse(string, mode='eval')
        root_node = ast_expr.body
        sympy_expr = self.safer_eval(root_node)
        return sympy_expr

    def safer_eval(self, node):
        node_type = type(node)
        try:
            node_handler = self.node_types_allowed[node_type]
        except KeyError:
            raise ValueError("Node type %s is not allowed." % node_type)
        return node_handler(node)

    def _get_node_types_allowed(self):
        return {
            ast.Name: self._symbol,
            ast.Num: self._number,
            ast.UnaryOp: self._unary_op,
            ast.BinOp: self._binary_op,
            ast.Call: self._function
        }

    def _get_unary_operator_types_allowed(self):
        return {
            ast.USub: operator.neg,
        }

    def _get_binary_operator_types_allowed(self):
        return {
            ast.Add: sympy.Add,
            ast.Sub: operator.sub,
            ast.Mult: sympy.Mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.BitXor: operator.xor,
        }

    def _get_functions_allowed(self):
        return {
            'sin': sympy.sin,
            'cos': sympy.cos,
            'sqrt': sympy.sqrt
        }

    def _symbol(self, node):
        return sympy.Symbol(node.id)

    def _number(self, node):
        return sympy.Number(node.n)

    def _unary_op(self, node):
        operator_type = type(node.op)
        o = self.unary_operator_types_allowed[operator_type]
        operand = self.safer_eval(node.operand)
        return o(operand)

    def _binary_op(self, node):
        operator_type = type(node.op)
        o = self.binary_operator_types_allowed[operator_type]
        left = self.safer_eval(node.left)
        right = self.safer_eval(node.right)
        return o(left, right)

    def _function(self, node):
        function_name = node.func.id
        arg_list = []
        for node_arg in node.args:
            arg_list.append(self.safer_eval(node_arg))
        try:
            f = self.functions_allowed[function_name]
        except KeyError:
            raise ValueError("Function %s is not allowed" % function_name)
        return f(*arg_list)


