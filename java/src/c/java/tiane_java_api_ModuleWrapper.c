#include <JIANE.h>

#include "tiane_java_api_ModuleWrapper.h"

#include <JIANE_DataConverters.h>

JNIEXPORT jobject JNICALL Java_tiane_java_api_ModuleWrapper_analyze(JNIEnv *env, jobject inst, jstring text) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  PyObject *analyzer = PyObject_GetAttrString(obj, "Analyzer");
  PyObject *result = JDC_call(analyzer, "analyze", 1, JIANEDC_toPythonString(env, text));
  jobject ret = JIANEDC_createLazyPythonWrapper(env, (*env)->FindClass(env, "tiane/java/api/Analysis"), result , JNI_FALSE);
  RELEASE_GIL;
  return ret;
}

JNIEXPORT void JNICALL Java_tiane_java_api_ModuleWrapper_endConversation(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  JDC_call(obj, "end_Conversation", 0);
  RELEASE_GIL;
}

static void genericSayRaw(JNIEnv *env, jobject inst, jstring text, jstring room, jstring user, jstring type, char *function) {
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  PyObject *kwargs = PyDict_New();

  if (room == NULL) {
    Py_XINCREF(Py_None);
    PyDict_SetItemString(kwargs, "room", Py_None);
  } else {
    PyDict_SetItemString(kwargs, "room", JIANEDC_toPythonString(env, room));
  }

  if (user == NULL) {
    Py_XINCREF(Py_None);
    PyDict_SetItemString(kwargs, "user", Py_None);
  } else {
    PyDict_SetItemString(kwargs, "user", JIANEDC_toPythonString(env, user));
  }

  if (type == NULL) {
    PyDict_SetItemString(kwargs, "output", PyUnicode_FromString("auto"));
  } else {
    PyDict_SetItemString(kwargs, "output", JIANEDC_toPythonString(env, type));
  }

  JDC_kwcall(obj, function, kwargs, 1, JIANEDC_toPythonString(env, text));
}

JNIEXPORT void JNICALL Java_tiane_java_api_ModuleWrapper_sayRaw(JNIEnv *env, jobject inst, jstring text, jstring room, jstring user, jstring type) {
  ENSURE_GIL;
  genericSayRaw(env, inst, text, room, user, type, "say");
  RELEASE_GIL;
}

JNIEXPORT void JNICALL Java_tiane_java_api_ModuleWrapper_asyncSayRaw(JNIEnv *env, jobject inst, jstring text, jstring room, jstring user, jstring type) {
  ENSURE_GIL;
  genericSayRaw(env, inst, text, room, user, type, "asynchronous_say");
  RELEASE_GIL;
}

JNIEXPORT jstring JNICALL Java_tiane_java_api_ModuleWrapper_listenRaw(JNIEnv *env, jobject inst, jstring user, jstring type) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  PyObject *kwargs = PyDict_New();

  if (user == NULL) {
    Py_XINCREF(Py_None);
    PyDict_SetItemString(kwargs, "user", Py_None);
  } else {
    PyDict_SetItemString(kwargs, "user", JIANEDC_toPythonString(env, user));
  }

  if (type == NULL) {
    PyDict_SetItemString(kwargs, "input", PyUnicode_FromString("auto"));
  } else {
    PyDict_SetItemString(kwargs, "input", JIANEDC_toPythonString(env, type));
  }

  jstring ret = JIANEDC_toJavaString(env, JDC_kwcall(obj, "listen", kwargs, 0));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jboolean JNICALL Java_tiane_java_api_ModuleWrapper_startModule(JNIEnv *env, jobject inst, jstring name, jstring text, jstring user, jstring room) {
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

JNIEXPORT jobject JNICALL Java_tiane_java_api_ModuleWrapper_analysisRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jobject ret = JIANEDC_createLazyPythonWrapper(env, (*env)->FindClass(env, "tiane/java/api/Analysis"), PyObject_GetAttrString(obj, "analysis") , JNI_FALSE);
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jstring JNICALL Java_tiane_java_api_ModuleWrapper_textRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  PyObject *text = PyObject_GetAttrString(obj, "text");
  if (PyUnicode_Check(text)) {
    jstring ret = JIANEDC_toJavaString(env, text);
    RELEASE_GIL;
    return ret;
  } else {
    RELEASE_GIL;
    return NULL;
  }
}

JNIEXPORT jobject JNICALL Java_tiane_java_api_ModuleWrapper_lstorageRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jobject ret = JIANEDC_createLazyPythonWrapper(env, (*env)->FindClass(env, "tiane/java/api/LocalStorage"), PyObject_GetAttrString(obj, "local_storage") , JNI_FALSE);
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jstring JNICALL Java_tiane_java_api_ModuleWrapper_userRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jstring ret = JIANEDC_toJavaString(env, PyObject_GetAttrString(obj, "user"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jstring JNICALL Java_tiane_java_api_ModuleWrapper_pathRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jstring ret = JIANEDC_toJavaString(env, PyObject_GetAttrString(obj, "path"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jstring JNICALL Java_tiane_java_api_ModuleWrapper_serverNameRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jstring ret = JIANEDC_toJavaString(env, PyObject_GetAttrString(obj, "server_name"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jstring JNICALL Java_tiane_java_api_ModuleWrapper_systemNameRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jstring ret = JIANEDC_toJavaString(env, PyObject_GetAttrString(obj, "system_name"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jobjectArray JNICALL Java_tiane_java_api_ModuleWrapper_roomsRaw(JNIEnv *env, jobject inst) {
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

JNIEXPORT jobjectArray JNICALL Java_tiane_java_api_ModuleWrapper_usersRaw(JNIEnv *env, jobject inst) {
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

JNIEXPORT jboolean JNICALL Java_tiane_java_api_ModuleWrapper_telegramRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jboolean ret = JIANEDC_toJavaBoolean(env, PyObject_GetAttrString(obj, "telegram_call"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jobject JNICALL Java_tiane_java_api_ModuleWrapper_telegramDataRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jobject ret = JIANEDC_createLazyPythonWrapper(env, (*env)->FindClass(env, "tiane/java/api/Dictionary"), PyObject_GetAttrString(obj, "telegram_data") , JNI_FALSE);
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jobject JNICALL Java_tiane_java_api_ModuleWrapper_coreRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jobject ret = JIANEDC_createLazyPythonWrapper(env, (*env)->FindClass(env, "tiane/java/api/Tiane"), PyObject_GetAttrString(obj, "core") , JNI_FALSE);
  RELEASE_GIL;
  return ret;
}