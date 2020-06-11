#include <JIANE.h>

#include "tiane_java_api_ModuleWrapperContinuous.h"

#include <JIANE_DataConverters.h>

static void genericStartRaw(JNIEnv *env, jobject inst, jstring name, jstring text, jstring user, jstring room, char *function) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  PyObject *kwargs = PyDict_New();

  if (name == NULL) {
    Py_XINCREF(Py_None);
    PyDict_SetItemString(kwargs, "name", Py_None);
  } else {
    PyDict_SetItemString(kwargs, "name", JIANEDC_toPythonString(env, name));
  }

  if (text == NULL) {
    Py_XINCREF(Py_None);
    PyDict_SetItemString(kwargs, "text", Py_None);
  } else {
    PyDict_SetItemString(kwargs, "text", JIANEDC_toPythonString(env, text));
  }

  if (user == NULL) {
    Py_XINCREF(Py_None);
    PyDict_SetItemString(kwargs, "user", Py_None);
  } else {
    PyDict_SetItemString(kwargs, "user", JIANEDC_toPythonString(env, user));
  }

  if (room == NULL) {
    Py_XINCREF(Py_None);
    PyDict_SetItemString(kwargs, "room", Py_None);
  } else {
    PyDict_SetItemString(kwargs, "room", JIANEDC_toPythonString(env, room));
  }

  JDC_kwcall(obj, function, kwargs, 0);
  RELEASE_GIL;
}

JNIEXPORT jboolean JNICALL Java_tiane_java_api_ModuleWrapperContinuous_startModule(JNIEnv *env, jobject inst, jstring name, jstring text, jstring user, jstring room) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  PyObject *kwargs = PyDict_New();

  if (name == NULL) {
    Py_XINCREF(Py_None);
    PyDict_SetItemString(kwargs, "name", Py_None);
  } else {
    PyDict_SetItemString(kwargs, "name", JIANEDC_toPythonString(env, name));
  }

  if (text == NULL) {
    Py_XINCREF(Py_None);
    PyDict_SetItemString(kwargs, "text", Py_None);
  } else {
    PyDict_SetItemString(kwargs, "text", JIANEDC_toPythonString(env, text));
  }

  if (user == NULL) {
    Py_XINCREF(Py_None);
    PyDict_SetItemString(kwargs, "user", Py_None);
  } else {
    PyDict_SetItemString(kwargs, "user", JIANEDC_toPythonString(env, user));
  }

  if (room == NULL) {
    Py_XINCREF(Py_None);
    PyDict_SetItemString(kwargs, "room", Py_None);
  } else {
    PyDict_SetItemString(kwargs, "room", JIANEDC_toPythonString(env, room));
  }

  jboolean ret = JIANEDC_toJavaBoolean(env, JDC_kwcall(obj, "start_module_and_confirm", kwargs, 0));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jobject JNICALL Java_tiane_java_api_ModuleWrapperContinuous_lstorageRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jobject ret = JIANEDC_createLazyPythonWrapper(env, (*env)->FindClass(env, "tiane/java/api/LocalStorage"), PyObject_GetAttrString(obj, "local_storage") , JNI_FALSE);
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jstring JNICALL Java_tiane_java_api_ModuleWrapperContinuous_pathRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jstring ret = JIANEDC_toJavaString(env, PyObject_GetAttrString(obj, "path"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jstring JNICALL Java_tiane_java_api_ModuleWrapperContinuous_serverNameRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jstring ret = JIANEDC_toJavaString(env, PyObject_GetAttrString(obj, "server_name"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jstring JNICALL Java_tiane_java_api_ModuleWrapperContinuous_systemNameRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jstring ret = JIANEDC_toJavaString(env, PyObject_GetAttrString(obj, "system_name"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jobjectArray JNICALL Java_tiane_java_api_ModuleWrapperContinuous_roomsRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  PyObject *list = PyObject_GetAttrString(obj, "room_list");
  int array_length = PyList_Size(list);
  jobjectArray array = (*env)->NewObjectArray(env, array_length, (*env)->FindClass(env, "java/lang/String"), NULL);
  for (int array_index = 0;array_index < array_length;array_index++) {
    (*env)->SetObjectArrayElement(env, array, array_index, JIANEDC_toJavaString(env, PyList_GetItem(list, array_index)));
  }
  RELEASE_GIL;
  return array;
}

JNIEXPORT jobjectArray JNICALL Java_tiane_java_api_ModuleWrapperContinuous_usersRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  PyObject *list = PyObject_GetAttrString(obj, "userlist");
  int array_length = PyList_Size(list);
  jobjectArray array = (*env)->NewObjectArray(env, array_length, (*env)->FindClass(env, "java/lang/String"), NULL);
  for (int array_index = 0;array_index < array_length;array_index++) {
    (*env)->SetObjectArrayElement(env, array, array_index, JIANEDC_toJavaString(env, PyList_GetItem(list, array_index)));
  }
  RELEASE_GIL;
  return array;
}

JNIEXPORT jobject JNICALL Java_tiane_java_api_ModuleWrapperContinuous_coreRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jobject ret = JIANEDC_createLazyPythonWrapper(env, (*env)->FindClass(env, "tiane/java/api/Tiane"), PyObject_GetAttrString(obj, "core") , JNI_FALSE);
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jint JNICALL Java_tiane_java_api_ModuleWrapperContinuous_intervalTimeRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jint ret = JIANEDC_toJavaInt(env, PyObject_GetAttrString(obj, "intervall_time"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jint JNICALL Java_tiane_java_api_ModuleWrapperContinuous_counterRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jint ret = JIANEDC_toJavaInt(env, PyObject_GetAttrString(obj, "counter"));
  RELEASE_GIL;
  return ret;
}