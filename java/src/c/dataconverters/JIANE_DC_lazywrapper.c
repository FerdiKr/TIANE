#include <JIANE.h>

#include "JIANE_DataConverters.h"

jobject JIANEDC_createLazyPythonWrapper(JNIEnv *env, jclass clazz, PyObject *wrapped, jboolean incref) {
  if (wrapped == NULL || wrapped == Py_None) {
    return NULL;
  } else {
    jmethodID ctor = (*env)->GetMethodID(env, clazz, "<init>", "(J)V");
    if (incref == JNI_TRUE) {
      Py_XINCREF(wrapped);
    }
    jlong pointer = (jlong) wrapped;
    jobject wrapper = (*env)->NewObject(env, clazz, ctor, pointer);
    return (*env)->NewGlobalRef(env, wrapper);
  }
}

PyObject *JIANEDC_getLazyWrapped(JNIEnv *env, jobject wrapper) {

  jclass clazz = (*env)->FindClass(env, "tiane/java/api/LazyPythonObject");
  jfieldID fid = (*env)->GetFieldID(env, clazz, "pointer", "J");
  jlong pointer = (*env)->GetLongField(env, wrapper, fid);
  return (PyObject*) pointer;
}

void JIANEDC_decrefLazyWrapped(JNIEnv *env, jobject wrapper) {
  PyObject *wrapped = JIANEDC_getLazyWrapped(env, wrapper);
  Py_XDECREF(wrapped);
}