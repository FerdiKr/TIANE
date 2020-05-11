#include <JIANE.h>

#include "tiane_java_api_Analysis.h"

#include <JIANE_DataConverters.h>

JNIEXPORT jstring JNICALL Java_tiane_java_api_Analysis_roomRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jstring ret = JIANEDC_toJavaString(env, PyDict_GetItemString(obj, "room"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jstring JNICALL Java_tiane_java_api_Analysis_townRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  jstring ret = JIANEDC_toJavaString(env, PyDict_GetItemString(obj, "town"));
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jobject JNICALL Java_tiane_java_api_Analysis_timeRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  PyObject *dict = PyDict_GetItemString(obj, "time");
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

    PyObject *py_hour = PyDict_GetItemString(dict, "hour");
    jint hour;
    if (py_hour == NULL || py_hour == Py_None) {
      values[3] = -1;
    } else {
      values[3] = JIANEDC_toJavaInt(env, py_hour);
    }

    PyObject *py_minute = PyDict_GetItemString(dict, "minute");
    jint minute;
    if (py_minute == NULL || py_minute == Py_None) {
      values[4] = -1;
    } else {
      values[4] = JIANEDC_toJavaInt(env, py_minute);
    }

    jintArray data = (*env)->NewIntArray(env, 5);
    (*env)->SetIntArrayRegion(env, data, 0, 5, values);

    RELEASE_GIL;
    return data;
  }
}