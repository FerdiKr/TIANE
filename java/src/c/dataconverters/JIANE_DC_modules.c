#include <JIANE.h>

#include "JIANE_DataConverters.h"

static int nextId = 0;

static int modmap_capacity = 0;
static jobject* modmap_objs;

static void JIANEDC_push_modmap(int id, jobject object) {
  while (id >= modmap_capacity) {
    if (modmap_capacity == 0) {
      modmap_capacity = 10;
      modmap_objs = malloc(modmap_capacity * sizeof(jobject));
    } else {
      modmap_capacity += 10;
      modmap_objs = realloc(modmap_objs, modmap_capacity * sizeof(jobject));
    }
  }
  modmap_objs[id] = object;
}

static jobject JIANEDC_get_modmap(int id) {
  if (id >= modmap_capacity) {
    return NULL;
  } else {
    return modmap_objs[id];
  }
}

static jobject JIANEDC_get_java_instance(PyObject *pythonModule) {
  PyObject *id_key = PyDict_GetItemString(PyModule_GetDict(pythonModule), "JAVA_MODULE_MAP_ID");
  if (id_key == NULL) {
    return NULL;
  } else {
    int moduleId = PyLong_AsSize_t(id_key);
    return JIANEDC_get_modmap(moduleId);
  }
}

static PyObject *JDC_PY_module_isValidGeneric(PyObject *self, PyObject *args, jboolean isTelegram) {
  PyObject *module;
  char* text;
  if (!PyArg_ParseTuple(args, "Os", &module, &text))
    return NULL;

  JNIEnv *env;
  int JNI_mode = JIANE_get_env(&env);

  jboolean isValid = JNI_FALSE;
  jobject modObj = JIANEDC_get_java_instance(module);
  if (modObj != NULL) {
    jclass clazz = (*env)->FindClass(env, "tiane/java/api/Module");
    jmethodID mid_isValid;
    if (isTelegram == JNI_TRUE) {
      mid_isValid = (*env)->GetMethodID(env, clazz, "isValidTelegram", "(Ljava/lang/String;)Z");
    } else {
      mid_isValid = (*env)->GetMethodID(env, clazz, "isValid", "(Ljava/lang/String;)Z");
    }
    isValid = (*env)->CallBooleanMethod(env, modObj, mid_isValid, (*env)->NewStringUTF(env, text));
  }

  JIANE_end_env(JNI_mode);

  if (isValid == JNI_TRUE) {
    Py_XINCREF(Py_True);
    return Py_True;
  } else {
    Py_XINCREF(Py_False);
    return Py_False;
  }
}

PyObject *JDC_PY_module_isValid(PyObject *self, PyObject *args) {
  return JDC_PY_module_isValidGeneric(self, args, JNI_FALSE);
}

PyObject *JDC_PY_module_isValidTelegram(PyObject *self, PyObject *args) {
  return JDC_PY_module_isValidGeneric(self, args, JNI_TRUE);
}

PyObject *JDC_PY_module_handle(PyObject *self, PyObject *args) {
  PyObject *module;
  char* text;
  PyObject *tiane;
  PyObject *lstorage;
  if (!PyArg_ParseTuple(args, "OsOO", &module, &text, &tiane, &lstorage))
    return NULL;

  JNIEnv *env;
  int JNI_mode = JIANE_get_env(&env);

  jobject modObj = JIANEDC_get_java_instance(module);
  if (modObj != NULL) {
    jobject j_tiane = JIANEDC_createLazyPythonWrapper(env, (*env)->FindClass(env, "tiane/java/api/ModuleWrapper"), tiane, JNI_TRUE);
    jobject j_lstorage = JIANEDC_createLazyPythonWrapper(env, (*env)->FindClass(env, "tiane/java/api/LocalStorage"), lstorage, JNI_TRUE);
    jclass clazz = (*env)->FindClass(env, "tiane/java/api/Module");
    jmethodID mid_handle = (*env)->GetMethodID(env, clazz, "handle", "(Ljava/lang/String;Ltiane/java/api/ModuleWrapper;Ltiane/java/api/LocalStorage;)V");
    (*env)->CallVoidMethod(env, modObj, mid_handle, (*env)->NewStringUTF(env, text), j_tiane, j_lstorage);
  }

  JIANE_end_env(JNI_mode);
  Py_XINCREF(Py_None);
  return Py_None;
}

PyObject *JIANEDC_toModule(JNIEnv *env, jobject module) {
  jclass clazz = (*env)->FindClass(env, "tiane/java/api/Module");
  jobject glob = (*env)->NewGlobalRef(env, module);

  jmethodID mid_active = (*env)->GetMethodID(env, clazz, "active", "()Z");
  jboolean active = (*env)->CallBooleanMethod(env, glob, mid_active);

  if (active != JNI_TRUE) {
    Py_XINCREF(Py_None);
    return Py_None;
  }

  jmethodID mid_priority = (*env)->GetMethodID(env, clazz, "priority", "()I");
  int priority = (*env)->CallIntMethod(env, glob, mid_priority);

  jmethodID mid_secure = (*env)->GetMethodID(env, clazz, "secure", "()Z");
  jboolean secure = (*env)->CallBooleanMethod(env, glob, mid_priority);

  jmethodID mid_words = (*env)->GetMethodID(env, clazz, "words", "()[Ljava/lang/String;");
  jobjectArray words = (jobjectArray)(*env)->CallObjectMethod(env, glob, mid_words);

  jmethodID mid_name = (*env)->GetMethodID(env, clazz, "name", "()Ljava/lang/String;");
  jstring jmodname = (jstring)(*env)->CallObjectMethod(env, glob, mid_name);

  int words_length = (*env)->GetArrayLength(env, words);
  PyObject *wordlist = PyList_New(words_length);
  for (int words_index = 0; words_index < words_length; words_index++) {
    jstring elem = (jstring)(*env)->GetObjectArrayElement(env, words, words_index);
    PyList_SetItem(wordlist, words_index, PyUnicode_FromString((*env)->GetStringUTFChars(env, elem, NULL)));
  }

  char *modulename_generated = calloc((*env)->GetStringUTFLength(env, jmodname) + 10 + 4, sizeof(char));
  int moduleId = nextId;
  nextId += 1;
  sprintf(modulename_generated, "jiane.mod%s_%d", (*env)->GetStringUTFChars(env, jmodname, NULL), moduleId);
  JIANEDC_push_modmap(moduleId, glob);

  PyObject *pymodule = PyModule_New(modulename_generated);
  PyModule_AddIntConstant(pymodule, "JAVA_MODULE_MAP_ID", moduleId);
  PyModule_AddObject(pymodule, "PRIORITY", PyLong_FromSize_t(priority));
  if (secure == JNI_TRUE) {
    Py_XINCREF(Py_True);
    PyModule_AddObject(pymodule, "SECURE", Py_True);
  } else {
    Py_XINCREF(Py_False);
    PyModule_AddObject(pymodule, "SECURE", Py_False);
  }
  PyModule_AddObject(pymodule, "WORDS", wordlist);
  PyModule_AddObject(pymodule, "MODNAME", PyUnicode_FromString((*env)->GetStringUTFChars(env, jmodname, NULL)));

  PyDict_SetItemString(PySys_GetObject("modules"), modulename_generated, pymodule);
  PyObject *imported_module = PyImport_ImportModule(modulename_generated);
  Py_XINCREF(imported_module);
  return pymodule;
}