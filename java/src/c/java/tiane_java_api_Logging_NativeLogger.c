#include <JIANE.h>

#include "JIANE_logging.h"
#include "tiane_java_api_Logging_NativeLogger.h"

#include <JIANE_DataConverters.h>

PyObject *JLOG_PY_create(PyObject *self, PyObject *args) {
  PyObject *logger;
  if (!PyArg_ParseTuple(args, "O", &logger))
    return NULL;

  JNIEnv *env;
  int JNI_mode = JIANE_get_env(&env);

  jclass clazz = (*env)->FindClass(env, "tiane/java/api/Logging");
  jmethodID ctor = (*env)->GetMethodID(env, clazz, "<init>", "(J)V");
  Py_XINCREF(logger);
  jlong pointer = (jlong) logger;
  (*env)->NewGlobalRef(env, (*env)->NewObject(env, clazz, ctor, pointer));
  // It gets inserted int o the static field automatically in the constructor.

  JIANE_end_env(JNI_mode);

  Py_XINCREF(Py_None);
  return Py_None;
}

JNIEXPORT void JNICALL Java_tiane_java_api_Logging_00024NativeLogger_writeRaw(JNIEnv *env, jobject inst, jstring type, jstring message, jboolean show) {
  ENSURE_GIL;
  PyObject *wrapped = JIANEDC_getLazyWrapped(env, inst);
  PyObject *dict = PyDict_New();
  if (show == JNI_TRUE) {
    Py_XINCREF(Py_True);
    PyDict_SetItemString(dict, "show", Py_True);
  } else {
    Py_XINCREF(Py_False);
    PyDict_SetItemString(dict, "show", Py_False);
  }
  JDC_kwcall(wrapped, "write", dict, 2, JIANEDC_toPythonString(env, type), JIANEDC_toPythonString(env, message));
  RELEASE_GIL;
}