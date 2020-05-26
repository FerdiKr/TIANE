#include <JIANE.h>

#include "tiane_java_api_User.h"

#include <JIANE_DataConverters.h>

JNIEXPORT jstring JNICALL Java_tiane_java_api_User_room(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jstring ret = JIANEDC_toJavaString(env, PyDict_GetItemString(obj, "room"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jstring JNICALL Java_tiane_java_api_User_nameRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jstring ret = JIANEDC_toJavaString(env, PyDict_GetItemString(obj, "name"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jstring JNICALL Java_tiane_java_api_User_firstNameRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jstring ret = JIANEDC_toJavaString(env, PyDict_GetItemString(obj, "first_name"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jstring JNICALL Java_tiane_java_api_User_lastNameRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jstring ret = JIANEDC_toJavaString(env, PyDict_GetItemString(obj, "last_name"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jstring JNICALL Java_tiane_java_api_User_roleRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jstring ret = JIANEDC_toJavaString(env, PyDict_GetItemString(obj, "role"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jint JNICALL Java_tiane_java_api_User_uidRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jint ret = JIANEDC_toJavaInt(env, PyDict_GetItemString(obj, "uid"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jlong JNICALL Java_tiane_java_api_User_telegramIdRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jlong ret = JIANEDC_toJavaLong(env, PyDict_GetItemString(obj, "telegram_id"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jstring JNICALL Java_tiane_java_api_User_pathRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jstring ret = JIANEDC_toJavaString(env, PyDict_GetItemString(obj, "path"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jintArray JNICALL Java_tiane_java_api_User_birthdayRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  PyObject *dict = PyDict_GetItemString(obj, "date_of_birth");
  if (dict == NULL || dict == Py_None) {
    RELEASE_GIL;
    return NULL;
  } else {
    jint values[5];

    PyObject *py_year = PyDict_GetItemString(dict, "year");
    if (py_year == NULL || py_year == Py_None) {
      values[0] = -1;
    } else {
      values[0] = JIANEDC_toJavaInt(env, py_year);
    }

    PyObject *py_month = PyDict_GetItemString(dict, "month");
    if (py_month == NULL || py_month == Py_None) {
      values[1] = -1;
    } else {
      values[1] = JIANEDC_toJavaInt(env, py_month);
    }

    PyObject *py_day = PyDict_GetItemString(dict, "day");
    jint day;
    if (py_day == NULL || py_day == Py_None) {
      values[2] = -1;
    } else {
      values[2] = JIANEDC_toJavaInt(env, py_day);
    }

    jintArray data = (*env)->NewIntArray(env, 3);
    (*env)->SetIntArrayRegion(env, data, 0, 3, values);

    RELEASE_GIL;
    return data;
  }
}