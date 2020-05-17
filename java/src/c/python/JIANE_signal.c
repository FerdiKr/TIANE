#include <JIANE.h>

#include "JIANE_signal.h"

#include <signal.h>

PyObject *JIANE_signal_set_handlers(PyObject *self, PyObject *args) {

  PYTIANE_should_stop = JNI_FALSE;

  if (signal(SIGINT, JIANE_signal_handle) == SIG_ERR) {
    Py_XINCREF(Py_False);
    return Py_False;
  }
  if (signal(SIGTERM, JIANE_signal_handle) == SIG_ERR) {
    Py_XINCREF(Py_False);
    return Py_False;
  }
  Py_XINCREF(Py_True);
  return Py_True;
}

PyObject *JIANE_signal_should_stop(PyObject *self, PyObject *args) {
  if (PYTIANE_should_stop == JNI_TRUE) {
    Py_XINCREF(Py_True);
    return Py_True;
  } else {
    Py_XINCREF(Py_False);
    return Py_False;
  }
}

void JIANE_signal_handle(int signal) {
  if (signal == SIGINT || signal == SIGTERM) {
    PYTIANE_should_stop = JNI_TRUE;
  }
}