#include <JIANE.h>

#include "tiane_java_api_Dictionary.h"

#include <JIANE_DataConverters.h>

JNIEXPORT jobject JNICALL Java_tiane_java_api_Dictionary_createDict(JNIEnv *env, jclass clazz) {
  PyObject *dict = PyDict_New();
  return JIANEDC_createLazyPythonWrapper(env, clazz, dict, JNI_FALSE);
}

JNIEXPORT jobject JNICALL Java_tiane_java_api_Dictionary_createList(JNIEnv *env, jclass clazz) {
  PyObject *list = PyList_New(0);
  return JIANEDC_createLazyPythonWrapper(env, clazz, list, JNI_FALSE);
}

// CAN BE NULL. PERFORM A NULL-CHECK AND AN EXCEPTION CHECK FIRST.
static PyObject *resolvePath(JNIEnv *env, PyObject *inst, jobjectArray path, const int idx) {
  if (inst == NULL || inst == Py_None) {
    return NULL;
  } else if (idx >= (*env)->GetArrayLength(env, path)) {
    return inst;
  } else if (PyDict_Check(inst)) {
    return resolvePath(env, PyDict_GetItemString(inst, (*env)->GetStringUTFChars(env, (*env)->GetObjectArrayElement(env, path, idx), NULL)), path, idx + 1);
  } else if (PyList_Check(inst)) {
    jclass intClass = (*env)->FindClass(env, "java/lang/Integer");
    jmethodID mid = (*env)->GetStaticMethodID(env, intClass, "parseInt", "(Ljava/lang/String;)I");
    jint listIndex = (*env)->CallStaticIntMethod(env, intClass, mid, (*env)->GetObjectArrayElement(env, path, idx));
    if ((*env)->ExceptionCheck(env) == JNI_TRUE) {
      return NULL;
    }
    if (listIndex < 0) {
      listIndex = PyList_Size(inst) + listIndex;
    }
    if (listIndex >= PyList_Size(inst) || listIndex < 0) {
      return NULL;
    } else {
      return resolvePath(env, PyList_GetItem(inst, listIndex), path, idx + 1);
    }
  } else {
    return NULL;
  }
}

static void setInPath(JNIEnv *env, PyObject *inst, jobjectArray path, const int idx, PyObject *value) {
  if (inst == NULL || inst == Py_None) {
    return;
  } else if (idx >= ((*env)->GetArrayLength(env, path) - 1)) {
    if (PyDict_Check(inst)) {
      PyDict_SetItemString(inst, (*env)->GetStringUTFChars(env, (*env)->GetObjectArrayElement(env, path, idx), NULL), value);
      return;
    } else if (PyList_Check(inst)) {
      jclass intClass = (*env)->FindClass(env, "java/lang/Integer");
      jmethodID mid = (*env)->GetStaticMethodID(env, intClass, "parseInt", "(Ljava/lang/String;)I");
      jint listIndex = (*env)->CallStaticIntMethod(env, intClass, mid, (*env)->GetObjectArrayElement(env, path, idx));
      if ((*env)->ExceptionCheck(env) == JNI_TRUE) {
        return;
      }
      if (listIndex < 0) {
        listIndex = PyList_Size(inst) + listIndex;
      }
      if (listIndex < 0) {
        return;
      }
      if (listIndex >= PyList_Size(inst)) {
        PyList_Append(inst, value);
      } else {
        PyList_SetItem(inst, listIndex, value);
      }
    }
  } else if (PyDict_Check(inst)) {
    setInPath(env, PyDict_GetItemString(inst, (*env)->GetStringUTFChars(env, (*env)->GetObjectArrayElement(env, path, idx), NULL)), path, idx + 1, value);
  } else if (PyList_Check(inst)) {
    jclass intClass = (*env)->FindClass(env, "java/lang/Integer");
    jmethodID mid = (*env)->GetStaticMethodID(env, intClass, "parseInt", "(Ljava/lang/String;)I");
    jint listIndex = (*env)->CallStaticIntMethod(env, intClass, mid, (*env)->GetObjectArrayElement(env, path, idx));
    if ((*env)->ExceptionCheck(env) == JNI_TRUE) {
      return;
    }
    if (listIndex < 0) {
      listIndex = PyList_Size(inst) + listIndex;
    }
    if (listIndex >= PyList_Size(inst) || listIndex < 0) {
      return;
    } else {
      setInPath(env, PyList_GET_ITEM(inst, listIndex), path, idx + 1, value);
    }
  } else {
    return;
  }
}

JNIEXPORT jobject JNICALL Java_tiane_java_api_Dictionary_getDictRaw(JNIEnv *env, jobject inst, jobjectArray tokens) {
  ENSURE_GIL;
  PyObject *obj = resolvePath(env, JIANEDC_getLazyWrapped(env, inst), tokens, 0);
  if ((*env)->ExceptionCheck(env) == JNI_TRUE) {
    return NULL;
  }

  if (obj != NULL && (PyDict_Check(obj) || PyList_Check(obj))) {
    jobject ret = JIANEDC_createLazyPythonWrapper(env, (*env)->FindClass(env, "tiane/java/api/Dictionary"), obj, JNI_TRUE);
    RELEASE_GIL;
    return ret;
  } else {
    RELEASE_GIL;
    return NULL;
  }
}

JNIEXPORT jstring JNICALL Java_tiane_java_api_Dictionary_getStringRaw(JNIEnv *env, jobject inst, jobjectArray tokens) {
  ENSURE_GIL;
  PyObject *obj = resolvePath(env, JIANEDC_getLazyWrapped(env, inst), tokens, 0);
  if ((*env)->ExceptionCheck(env) == JNI_TRUE) {
    RELEASE_GIL;
    return NULL;
  }

  if (obj != NULL && PyUnicode_Check(obj)) {
    jstring ret = JIANEDC_toJavaString(env, obj);
    RELEASE_GIL;
    return ret;
  } else {
    RELEASE_GIL;
    return NULL;
  }
}

JNIEXPORT jint JNICALL Java_tiane_java_api_Dictionary_getIntRaw(JNIEnv *env, jobject inst, jobjectArray tokens) {
  ENSURE_GIL;
  PyObject *obj = resolvePath(env, JIANEDC_getLazyWrapped(env, inst), tokens, 0);
  if ((*env)->ExceptionCheck(env) == JNI_TRUE) {
    RELEASE_GIL;
    return 0;
  }

  if (obj != NULL && (PyLong_Check(obj) || PyFloat_Check(obj))) {
    jint ret = JIANEDC_toJavaInt(env, obj);
    RELEASE_GIL;
    return ret;
  } else {
    RELEASE_GIL;
    return 0;
  }
}

JNIEXPORT jlong JNICALL Java_tiane_java_api_Dictionary_getLongRaw(JNIEnv *env, jobject inst, jobjectArray tokens) {
  ENSURE_GIL;
  PyObject *obj = resolvePath(env, JIANEDC_getLazyWrapped(env, inst), tokens, 0);
  if ((*env)->ExceptionCheck(env) == JNI_TRUE) {
    RELEASE_GIL;
    return 0;
  }

  if (obj != NULL && (PyLong_Check(obj) || PyFloat_Check(obj))) {
    jlong ret = JIANEDC_toJavaLong(env, obj);
    RELEASE_GIL;
    return ret;
  } else {
    RELEASE_GIL;
    return 0;
  }
}

JNIEXPORT jdouble JNICALL Java_tiane_java_api_Dictionary_getDoubleRaw(JNIEnv *env, jobject inst, jobjectArray tokens) {
  ENSURE_GIL;
  PyObject *obj = resolvePath(env, JIANEDC_getLazyWrapped(env, inst), tokens, 0);
  if ((*env)->ExceptionCheck(env) == JNI_TRUE) {
    RELEASE_GIL;
    return 0;
  }

  if (obj != NULL && (PyLong_Check(obj) || PyFloat_Check(obj))) {
    jdouble ret = JIANEDC_toJavaDouble(env, obj);
    RELEASE_GIL;
    return ret;
  } else {
    RELEASE_GIL;
    return 0;
  }
}

JNIEXPORT jboolean JNICALL Java_tiane_java_api_Dictionary_getBoolRaw(JNIEnv *env, jobject inst, jobjectArray tokens) {
  ENSURE_GIL;
  PyObject *obj = resolvePath(env, JIANEDC_getLazyWrapped(env, inst), tokens, 0);
  if ((*env)->ExceptionCheck(env) == JNI_TRUE) {
    RELEASE_GIL;
    return 0;
  }

  jboolean ret = JIANEDC_toJavaBoolean(env, obj);
  RELEASE_GIL;
  return ret;
}

JNIEXPORT jobjectArray JNICALL Java_tiane_java_api_Dictionary_keysRaw(JNIEnv *env, jobject inst) {
  ENSURE_GIL;
  PyObject *obj = JIANEDC_getLazyWrapped(env, inst);
  if (PyDict_Check(obj)) {
    PyObject *list = PyDict_Keys(obj);
    int array_length = PyList_Size(list);
    jobjectArray array = (*env)->NewObjectArray(env, array_length, (*env)->FindClass(env, "java/lang/String"), NULL);
    for (int array_index = 0;array_index < array_length;array_index++) {
      (*env)->SetObjectArrayElement(env, array, array_index, JIANEDC_toJavaString(env, PyObject_Str(PyList_GetItem(list, array_index))));
    }
    RELEASE_GIL;
    return array;
  } else if (PyList_Check(obj)) {
    int array_length = PyList_Size(obj);
    jobjectArray array = (*env)->NewObjectArray(env, array_length, (*env)->FindClass(env, "java/lang/String"), NULL);
    for (int array_index = 0;array_index < array_length;array_index++) {
      int buffer_size = 2 + (array_index / 10);
      char str[buffer_size];
      sprintf(str, "%d", array_index);
      (*env)->SetObjectArrayElement(env, array, array_index, (*env)->NewStringUTF(env, str));
    }
    RELEASE_GIL;
    return array;
  } else {
    jobjectArray ret = (*env)->NewObjectArray(env, 0, (*env)->FindClass(env, "java/lang/String"), NULL);
    RELEASE_GIL;
    return ret;
  }
}

JNIEXPORT void JNICALL Java_tiane_java_api_Dictionary_setDictRaw(JNIEnv *env, jobject inst, jobjectArray tokens, jobject value) {
  ENSURE_GIL;
  setInPath(env, JIANEDC_getLazyWrapped(env, inst), tokens, 0, JIANEDC_getLazyWrapped(env, value));
  RELEASE_GIL;
}

JNIEXPORT void JNICALL Java_tiane_java_api_Dictionary_setStringRaw(JNIEnv *env, jobject inst, jobjectArray tokens, jstring value) {
  ENSURE_GIL;
  setInPath(env, JIANEDC_getLazyWrapped(env, inst), tokens, 0, JIANEDC_toPythonString(env, value));
  RELEASE_GIL;
}

JNIEXPORT void JNICALL Java_tiane_java_api_Dictionary_setIntRaw(JNIEnv *env, jobject inst, jobjectArray tokens, jint value) {
  ENSURE_GIL;
  setInPath(env, JIANEDC_getLazyWrapped(env, inst), tokens, 0, JIANEDC_toPythonInt(env, value));
  RELEASE_GIL;
}

JNIEXPORT void JNICALL Java_tiane_java_api_Dictionary_setLongRaw(JNIEnv *env, jobject inst, jobjectArray tokens, jlong value) {
  ENSURE_GIL;
  setInPath(env, JIANEDC_getLazyWrapped(env, inst), tokens, 0, JIANEDC_toPythonLong(env, value));
  RELEASE_GIL;
}

JNIEXPORT void JNICALL Java_tiane_java_api_Dictionary_setDoubleRaw(JNIEnv *env, jobject inst, jobjectArray tokens, jdouble value) {
  ENSURE_GIL;
  setInPath(env, JIANEDC_getLazyWrapped(env, inst), tokens, 0, JIANEDC_toPythonDouble(env, value));
  RELEASE_GIL;
}

JNIEXPORT void JNICALL Java_tiane_java_api_Dictionary_setBoolRaw(JNIEnv *env, jobject inst, jobjectArray tokens, jboolean value) {
  ENSURE_GIL;
  setInPath(env, JIANEDC_getLazyWrapped(env, inst), tokens, 0, JIANEDC_toPythonBoolean(env, value));
  RELEASE_GIL;
}