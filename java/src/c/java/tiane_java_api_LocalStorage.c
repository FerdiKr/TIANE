#include <JIANE.h>

#include "tiane_java_api_LocalStorage.h"

#include <JIANE_DataConverters.h>

JNIEXPORT jobject JNICALL Java_tiane_java_api_LocalStorage_user(JNIEnv *env, jobject inst, jstring user) {
  if (user == NULL) {
    return NULL;
  } else {
    ENSURE_GIL;
    PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
    PyObject *dict = PyDict_GetItemString(obj, "users");
    PyObject *pyobj = PyDict_GetItemString(dict, (*env)->GetStringUTFChars(env, user, NULL));
    if (pyobj == NULL || pyobj == Py_None) {
      RELEASE_GIL;
      return NULL;
    } else {
      jobject ret = JIANEDC_createLazyPythonWrapper(env, (*env)->FindClass(env, "tiane/java/api/User"), pyobj, JNI_TRUE);
      RELEASE_GIL;
      return ret;
    }
  }
}

JNIEXPORT jobject JNICALL Java_tiane_java_api_LocalStorage_room(JNIEnv *env, jobject inst, jstring room) {
  if (room == NULL) {
    return NULL;
  } else {
    ENSURE_GIL;
    PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
    PyObject *dict = PyDict_GetItemString(obj, "rooms");
    PyObject *pyobj = PyDict_GetItemString(dict, (*env)->GetStringUTFChars(env, room, NULL));
    if (pyobj == NULL || pyobj == Py_None) {
      RELEASE_GIL;
      return NULL;
    } else {
      jobject ret = JIANEDC_createLazyPythonWrapper(env, (*env)->FindClass(env, "tiane/java/api/Room"), pyobj, JNI_TRUE);
      RELEASE_GIL;
      return ret;
    }
  }
}

JNIEXPORT jstring JNICALL Java_tiane_java_api_LocalStorage_pathRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jstring ret = JIANEDC_toJavaString(env, PyDict_GetItemString(obj, "TIANE_PATH"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jstring JNICALL Java_tiane_java_api_LocalStorage_serverNameRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jstring ret = JIANEDC_toJavaString(env, PyDict_GetItemString(obj, "server_name"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jstring JNICALL Java_tiane_java_api_LocalStorage_systemNameRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jstring ret = JIANEDC_toJavaString(env, PyDict_GetItemString(obj, "system_name"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jstring JNICALL Java_tiane_java_api_LocalStorage_homeLocationRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jstring ret = JIANEDC_toJavaString(env, PyDict_GetItemString(obj, "home_location"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jstring JNICALL Java_tiane_java_api_LocalStorage_activationPhraseRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jstring ret = JIANEDC_toJavaString(env, PyDict_GetItemString(obj, "activation_phrase"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jobjectArray JNICALL Java_tiane_java_api_LocalStorage_usersRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  PyObject *dict = PyDict_GetItemString(obj, "rooms");
  PyObject *list = PyDict_Keys(dict);
  int array_length = PyList_Size(list);
  jobjectArray array = (*env)->NewObjectArray(env, array_length, (*env)->FindClass(env, "java/lang/String"), NULL);
  for (int array_index = 0;array_index < array_length;array_index++) {
    (*env)->SetObjectArrayElement(env, array, array_index, JIANEDC_toJavaString(env, PyList_GetItem(list, array_index)));
  }
  RELEASE_GIL;
  return array;
}

JNIEXPORT jobjectArray JNICALL Java_tiane_java_api_LocalStorage_roomsRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  PyObject *dict = PyDict_GetItemString(obj, "users");
  PyObject *list = PyDict_Keys(dict);
  int array_length = PyList_Size(list);
  jobjectArray array = (*env)->NewObjectArray(env, array_length, (*env)->FindClass(env, "java/lang/String"), NULL);
  for (int array_index = 0;array_index < array_length;array_index++) {
    (*env)->SetObjectArrayElement(env, array, array_index, JIANEDC_toJavaString(env, PyList_GetItem(list, array_index)));
  }
  RELEASE_GIL;
  return array;
}