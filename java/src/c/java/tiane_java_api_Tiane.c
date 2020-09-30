#include <JIANE.h>

#include "tiane_java_api_Tiane.h"

#include <JIANE_DataConverters.h>

JNIEXPORT jboolean JNICALL Java_tiane_java_api_Tiane_openMode__(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jboolean ret = JIANEDC_toJavaBoolean(env, PyObject_GetAttrString(obj, "open_mode"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT void JNICALL Java_tiane_java_api_Tiane_openMode__Z(JNIEnv *env, jobject inst, jboolean open) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  PyObject_SetAttrString(obj, "open_mode", JIANEDC_toPythonBoolean(env, open));
  RELEASE_GIL;
}

JNIEXPORT jboolean JNICALL Java_tiane_java_api_Tiane_presentationMode__(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jboolean ret = JIANEDC_toJavaBoolean(env, PyObject_GetAttrString(obj, "presentation_mode"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT void JNICALL Java_tiane_java_api_Tiane_presentationMode__Z(JNIEnv *env, jobject inst, jboolean presentation) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  PyObject_SetAttrString(obj, "presentation_mode", JIANEDC_toPythonBoolean(env, presentation));
  RELEASE_GIL;
}

JNIEXPORT jobject JNICALL Java_tiane_java_api_Tiane_analyze(JNIEnv *env, jobject inst, jstring text) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  PyObject *analyzer = PyObject_GetAttrString(obj, "Analyzer");
  PyObject *result = JDC_call(analyzer, "analyze", 1, JIANEDC_toPythonString(env, text));
  jobject ret = JIANEDC_createLazyPythonWrapper(env, (*env)->FindClass(env, "tiane/java/api/Analysis"), result , JNI_FALSE);
  RELEASE_GIL;
  return ret;
}

JNIEXPORT void JNICALL Java_tiane_java_api_Tiane_sendWebSocketEvent(JNIEnv *env, jobject inst, jstring event, jobject data) {
    ENSURE_GIL;
    PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
    JDC_call(obj, "sendWebSocketEvent", 2, JIANEDC_toPythonString(env, event), JIANEDC_getLazyWrapped(env, data));
    RELEASE_GIL;
}

JNIEXPORT jobject JNICALL Java_tiane_java_api_Tiane_userListRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jobject ret = JIANEDC_createLazyPythonWrapper(env, (*env)->FindClass(env, "tiane/java/api/Dictionary"), PyObject_GetAttrString(obj, "userlist"), JNI_FALSE);
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jobject JNICALL Java_tiane_java_api_Tiane_userDictRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  PyObject *usersInst = PyObject_GetAttrString(obj, "Users");
  jobject toReturn =  JIANEDC_createLazyPythonWrapper(env, (*env)->FindClass(env, "tiane/java/api/Dictionary"), PyObject_GetAttrString(usersInst, "userdict"), JNI_FALSE);
  Py_XDECREF(usersInst);
  RELEASE_GIL;
  return toReturn;
}

JNIEXPORT jobject JNICALL Java_tiane_java_api_Tiane_activeModulesRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jobject ret = JIANEDC_createLazyPythonWrapper(env, (*env)->FindClass(env, "tiane/java/api/Dictionary"), PyObject_GetAttrString(obj, "active_modules"), JNI_FALSE);
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jobject JNICALL Java_tiane_java_api_Tiane_continuousModulesRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jobject ret = JIANEDC_createLazyPythonWrapper(env, (*env)->FindClass(env, "tiane/java/api/Dictionary"), PyObject_GetAttrString(obj, "continuous_modules"), JNI_FALSE);
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jobject JNICALL Java_tiane_java_api_Tiane_roomDictRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jobject ret = JIANEDC_createLazyPythonWrapper(env, (*env)->FindClass(env, "tiane/java/api/Dictionary"), PyObject_GetAttrString(obj, "rooms"), JNI_FALSE);
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jobject JNICALL Java_tiane_java_api_Tiane_otherDevicesRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jobject ret = JIANEDC_createLazyPythonWrapper(env, (*env)->FindClass(env, "tiane/java/api/Dictionary"), PyObject_GetAttrString(obj, "other_devices"), JNI_FALSE);
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jobject JNICALL Java_tiane_java_api_Tiane_devicesConnectingRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jobject ret = JIANEDC_createLazyPythonWrapper(env, (*env)->FindClass(env, "tiane/java/api/Dictionary"), PyObject_GetAttrString(obj, "devices_connecting"), JNI_FALSE);
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jobject JNICALL Java_tiane_java_api_Tiane_telegramQueuedUsersRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jobject ret = JIANEDC_createLazyPythonWrapper(env, (*env)->FindClass(env, "tiane/java/api/Dictionary"), PyObject_GetAttrString(obj, "telegram_queued_users"), JNI_FALSE);
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jobject JNICALL Java_tiane_java_api_Tiane_lstorageRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jobject ret = JIANEDC_createLazyPythonWrapper(env, (*env)->FindClass(env, "tiane/java/api/LocalStorage"), PyObject_GetAttrString(obj, "local_storage"), JNI_FALSE);
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jobject JNICALL Java_tiane_java_api_Tiane_roomListRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jobject ret = JIANEDC_createLazyPythonWrapper(env, (*env)->FindClass(env, "tiane/java/api/Dictionary"), PyObject_GetAttrString(obj, "room_list"), JNI_FALSE);
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jstring JNICALL Java_tiane_java_api_Tiane_pathRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jstring ret = JIANEDC_toJavaString(env, PyObject_GetAttrString(obj, "path"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jstring JNICALL Java_tiane_java_api_Tiane_serverNameRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jstring ret = JIANEDC_toJavaString(env, PyObject_GetAttrString(obj, "server_name"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jstring JNICALL Java_tiane_java_api_Tiane_systemNameRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jstring ret = JIANEDC_toJavaString(env, PyObject_GetAttrString(obj, "system_name"));
  RELEASE_GIL;
  return ret;
}