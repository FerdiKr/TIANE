#include <JIANE.h>

#include "tiane_java_api_Room.h"

#include <JIANE_DataConverters.h>

JNIEXPORT jstring JNICALL Java_tiane_java_api_Room_nameRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jstring ret = JIANEDC_toJavaString(env, PyDict_GetItemString(obj, "name"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jobjectArray JNICALL Java_tiane_java_api_Room_usersRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  PyObject *list = PyDict_GetItemString(obj, "users");
  if (list == NULL || list == Py_None) {
    jobjectArray array = (*env)->NewObjectArray(env, 0, (*env)->FindClass(env, "java/lang/String"), NULL);
    RELEASE_GIL;
    return array;
  } else {
    int array_length = PyList_Size(list);
    jobjectArray array = (*env)->NewObjectArray(env, array_length, (*env)->FindClass(env, "java/lang/String"), NULL);
    for (int array_index = 0; array_index < array_length; array_index++) {
      (*env)->SetObjectArrayElement(env, array, array_index, JIANEDC_toJavaString(env, PyList_GetItem(list, array_index)));
    }
    RELEASE_GIL;
    return array;
  }
}