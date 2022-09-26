import sys
import os
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib.pyplot as plt
from man_bit_plot import gun_bezier
import sympy


plot = True
dam_prof = [(100, 1), (300, 0.3)]
curve = gun_bezier(dam_prof)
# print(curve.locate(np.array([[150], [1]])))
# print(curve.locate(1))

funct = curve.implicitize()
x1 = 150
solution1, = sympy.solveset(funct.evalf(subs={'x': x1}), 'y', domain=sympy.S.Reals)
print(solution1)

# simp_exp = sympy.simplify(funct.subs('x', x1))
# print(simp_exp)
# solution1 = sympy.solveset(simp_exp, domain=sympy.S.Reals)
# print(solution1.evalf())

x2 = 240
# print(simp_exp)
solution2, = sympy.solveset(funct.evalf(subs={'x': x2}), 'y', domain=sympy.S.Reals)
print(solution2)

if plot:
    curve.plot(100)
    plt.show()
