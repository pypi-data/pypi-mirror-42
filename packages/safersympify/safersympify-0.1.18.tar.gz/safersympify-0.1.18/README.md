# Safer Sympify

Convert unsanitized user input into SymPy expression.

This does not prevent all possible attacks. However, this is much safer than using `eval()`, which SymPy still does.

See SymPy PR12524 for more details: https://github.com/sympy/sympy/pull/12524



## Examples

```
    Create a SymPy expression from user input. 
    This uses pure Python syntax. 
    Whitelisted operators and functions only are allowed.
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

```
