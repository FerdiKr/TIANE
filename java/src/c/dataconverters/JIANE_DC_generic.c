#include <JIANE.h>

#include "JIANE_DataConverters.h"

jstring JIANEDC_toJavaString(JNIEnv *env, PyObject *string) {
  if (string == NULL || string == Py_None) {
    return NULL;
  } else {
    (*env)->NewStringUTF(env, PyUnicode_AsUTF8(string));
  }
}

PyObject *JIANEDC_toPythonString(JNIEnv  *env, jstring string) {
  if (string == NULL) {
    return Py_None;
  } else {
    return PyUnicode_FromString((*env)->GetStringUTFChars(env, string, NULL));
  }
}

jint JIANEDC_toJavaInt(JNIEnv  *env, PyObject *number) {
  if (PyFloat_Check(number)) {
    return (long) PyFloat_AsDouble(number);
  } else {
    return PyLong_AsLong(number);
  }
}

PyObject *JIANEDC_toPythonInt(JNIEnv  *env, jint number) {
  return PyLong_FromLong(number);
}

jlong JIANEDC_toJavaLong(JNIEnv  *env, PyObject *number) {
  if (PyFloat_Check(number)) {
    return (long long) PyFloat_AsDouble(number);
  } else {
    return PyLong_AsLongLong(number);
  }
}

PyObject *JIANEDC_toPythonLong(JNIEnv  *env, jlong number) {
  return PyLong_FromLongLong(number);
}

jdouble JIANEDC_toJavaDouble(JNIEnv  *env, PyObject *number) {
  if (PyLong_Check(number)) {
    return (jdouble) PyLong_AsLongLong(number);
  } else {
    return PyFloat_AsDouble(number);
  }
}

PyObject *JIANEDC_toPythonDouble(JNIEnv  *env, jdouble number) {
  return PyFloat_FromDouble(number);
}

jboolean JIANEDC_toJavaBoolean(JNIEnv  *env, PyObject *boolean) {
  if (boolean == Py_True) {
    return JNI_TRUE;
  } else {
    return JNI_FALSE;
  }
}

PyObject *JIANEDC_toPythonBoolean(JNIEnv  *env, jboolean boolean) {
  if (boolean == JNI_TRUE) {
    Py_XINCREF(Py_True);
    return Py_True;
  } else {
    Py_XINCREF(Py_False);
    return Py_False;
  }
}