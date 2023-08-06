from apronpy.coeff import PyMPQScalarCoeff
from apronpy.environment import PyEnvironment
from apronpy.lincons0 import ConsTyp
from apronpy.lincons1 import PyLincons1
from apronpy.linexpr1 import PyLinexpr1
from apronpy.scalar import PyDoubleScalar
from apronpy.texpr1 import PyTexpr1
from apronpy.var import PyVar

e = PyEnvironment([PyVar('x'), PyVar('y')], [PyVar('z')])
x = PyLinexpr1(e)
x.set_coeff(PyVar('x'), PyMPQScalarCoeff(1))
x.set_cst(PyMPQScalarCoeff(3))
t = PyTexpr1(x)
# libapron.ap_texpr1_print.argtypes = [POINTER(Texpr1)]
# libapron.ap_texpr1_print(t.texpr1)
# print()
c = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x, PyDoubleScalar(3))
print("Done")
