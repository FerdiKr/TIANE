#include "module_jiane.h"

#define PY_SSIZE_T_CLEAN

#include <jni.h>
#include <Python.h>

#include <JIANE.h>
#include <JIANE_DataConverters.h>

#include <stdio.h>

PyObject *JPY_loadModules(PyObject *self, PyObject *args) {
  char* string;
  if (!PyArg_ParseTuple(args, "s", &string))
    return NULL;

  JNIEnv *env;
  int mode = JIANE_get_env(&env);

  jclass clazz = (*env)->FindClass(env, "tiane/java/TIANEWrapper");
  jmethodID method = (*env)->GetStaticMethodID(env, clazz, "loadModules", "(Ljava/lang/String;)[Ltiane/java/api/Module;");
  jobjectArray ret = (jobjectArray) (*env)->CallStaticObjectMethod(env, clazz, method, (*env)->NewStringUTF(env, string));

  int ret_length = (*env)->GetArrayLength(env, ret);
  PyObject *modlist = PyList_New(ret_length);
  for (int ret_index = 0;ret_index < ret_length;ret_index++) {
    jobject elem = (*env)->GetObjectArrayElement(env, ret, ret_index);
    PyList_SET_ITEM(modlist, ret_index, JIANEDC_toModule(env, &elem));
  }

  JIANE_end_env(mode);

  return modlist;
}

PyObject *JPY_loadModulesContinuous(PyObject *self, PyObject *args) {
  return PyList_New(0);
}