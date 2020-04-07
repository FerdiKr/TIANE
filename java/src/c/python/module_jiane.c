#include "module_jiane.h"

#define PY_SSIZE_T_CLEAN

#include <jni.h>
#include <Python.h>

#include <JIANE.h>

static PyMethodDef jiane_method_define[] = {
  {"loadModules",  JPY_loadModules, METH_VARARGS, ""},
  {"loadModulesContinuous",  JPY_loadModulesContinuous, METH_VARARGS, ""},
  {NULL, NULL, 0, NULL} //Must be the last entry, do not delete
};

static struct PyModuleDef jiane_module_define = {
  PyModuleDef_HEAD_INIT,
  "jiane",
  NULL,
  -1,
  jiane_method_define
};

PyMODINIT_FUNC PyInit_jiane(void) {
  return PyModule_Create(&jiane_module_define);
}