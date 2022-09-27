import sys
import os
import sympy
import matplotlib.pyplot as plt
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import gun_obj


plot = True
gun = gun_obj.Hk419()
curve = gun.gen_bez_curve()
# print(curve.locate(np.array([[150], [1]])))
# print(curve.locate(1))

funct = curve.implicitize()
x1 = 150
solution1, = sympy.solveset(funct.evalf(subs={'x': x1}), 'y',
                            domain=sympy.S.Reals)
print(solution1)

# simp_exp = sympy.simplify(funct.subs('x', x1))
# print(simp_exp)
# solution1 = sympy.solveset(simp_exp, domain=sympy.S.Reals)
# print(solution1.evalf())

x2 = 240
# print(simp_exp)
solution2, = sympy.solveset(funct.evalf(subs={'x': x2}), 'y',
                            domain=sympy.S.Reals)
print(solution2)

if plot:
    curve.plot(100)
    plt.show()
