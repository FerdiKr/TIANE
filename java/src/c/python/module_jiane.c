#include "module_jiane.h"

#define PY_SSIZE_T_CLEAN

#include <jni.h>
#include <Python.h>

#include <JIANE.h>

static PyMethodDef jiane_method_define[] = {
  {"javaPrint",  javaPrint, METH_VARARGS, ""},
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

PyObject *javaPrint(PyObject *self, PyObject *args) {
  char* string;
  if (!PyArg_ParseTuple(args, "s", &string))
    return NULL;

  JNIEnv *env;
  int mode = JIANE_get_env(&env);

  jclass clazz = (*env)->FindClass(env, "tiane/java/TIANEWrapper");
  jmethodID method = (*env)->GetStaticMethodID(env, clazz, "printSomething", "(Ljava/lang/String;)V");
  (*env)->CallStaticVoidMethod(env, clazz, method, (*env)->NewStringUTF(env, string));

  JIANE_end_env(mode);

  return Py_None;
}