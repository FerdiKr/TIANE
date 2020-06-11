#include <JIANE.h>

#include "module_jiane.h"

#include <JIANE_DataConverters.h>
#include <JIANE_logging.h>
#include <JIANE_signal.h>

static PyMethodDef jiane_method_define[] = {
  {"loadModules", JPY_loadModules, METH_VARARGS, ""},
  {"loadModulesContinuous", JPY_loadModulesContinuous, METH_VARARGS, ""},
  {"javaModuleIsValid", JDC_PY_module_isValid, METH_VARARGS, ""},
  {"javaModuleIsValidTelegram", JDC_PY_module_isValidTelegram, METH_VARARGS, ""},
  {"javaModuleHandle", JDC_PY_module_handle, METH_VARARGS, ""},
  {"javaContinuousModuleStart", JDC_PY_continuous_module_start, METH_VARARGS, ""},
  {"javaContinuousModuleRun", JDC_PY_continuous_module_run, METH_VARARGS, ""},
  {"javaContinuousModuleStop", JDC_PY_continuous_module_stop, METH_VARARGS, ""},
  {"createLogger", JLOG_PY_create, METH_VARARGS, ""},
  {"setSignalHandlers", JIANE_signal_set_handlers, METH_VARARGS, ""},
  {"shouldStop", JIANE_signal_should_stop, METH_VARARGS, ""},
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