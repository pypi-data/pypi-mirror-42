from _ctypes import byref, POINTER
from ctypes import c_size_t, c_char_p

from apronpy.abstract1 import Abstract1
from apronpy.box import PyBoxD
from apronpy.cdll import cstdout, libapron, libboxD
from apronpy.coeff import PyDoubleScalarCoeff, PyMPQScalarCoeff
from apronpy.environment import PyEnvironment, Environment
from apronpy.interval import PyInterval, PyDoubleInterval
from apronpy.lincons0 import ConsTyp
from apronpy.lincons1 import PyLincons1
from apronpy.linexpr0 import Linexpr0
from apronpy.linexpr1 import PyLinexpr1
from apronpy.manager import Manager
from apronpy.scalar import PyDoubleScalar
from apronpy.var import PyVar

e = PyEnvironment([PyVar('x'), PyVar('y')], [PyVar('z')])

l = PyLinexpr1(e)
# libapron.ap_linexpr1_fprint(cstdout, byref(l.linexpr1))

# l.minimize()
print(l)
l0 = PyLinexpr1(e, 0)

print(l0)
#
#
l.set_coeff(PyVar('x'), PyDoubleScalarCoeff(3))
# l.set_coeff(PyVar('y'), PyDoubleScalarCoeff(0))
l.set_coeff(PyVar('z'), PyDoubleScalarCoeff(-9))
l.set_cst(PyDoubleScalarCoeff(8))
#

print(l)
# # l.minimize()
# # print(l)
#
# libapron.ap_linexpr0_type.argtypes = [POINTER(Linexpr0)]
# # print(libapron.ap_linexpr0_type(l.linexpr1.linexpr0))
#
# print(l.is_integer())
# print(l.is_real())
# print(l.is_linear())
# print(l.is_quasilinear())
# c = l.get_coeff(PyVar('x'))
# # print(c)
# cst = l.get_cst()
# print(cst)

c = PyLincons1(ConsTyp.AP_CONS_SUPEQ, l, PyDoubleScalar(3))
print(c)

c = PyLincons1.unsat(e)
print(c)






print("Done")
