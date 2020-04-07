#include "JIANE_DataConverters.h"

#define PY_SSIZE_T_CLEAN

#include <jni.h>
#include <Python.h>

#include <JIANE.h>

#include <stdio.h>

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
    printf("JAVA-KEY: %d\n", moduleId);
    return JIANEDC_get_modmap(moduleId);
  }
}

static PyObject *JDC_PY_isValid(PyObject *self, PyObject *args) {
  char* text;
  if (!PyArg_ParseTuple(args, "s", &text))
    return NULL;

  JNIEnv * env;
  int JNI_mode = JIANE_get_env(&env);

  jboolean isValid = JNI_FALSE;
  jobject modObj = JIANEDC_get_java_instance(self);
  if (modObj != NULL) {
    jclass clazz = (*env)->FindClass(env, "tiane/java/api/Module");
    jmethodID mid_isValid = (*env)->GetMethodID(env, clazz, "isValid", "(Ljava/lang/String;)Z");
    isValid = (*env)->CallBooleanMethod(env, modObj, mid_isValid, (*env)->NewStringUTF(env, text));
  }

  JIANE_end_env(JNI_mode);

  if (isValid == JNI_TRUE) {
    printf("TRUE\n");
    return Py_True;
  } else {
    printf("FALSE\n");
    return Py_False;
  }
}

static PyObject *JDC_PY_handle(PyObject *self, PyObject *args) {
  /*JNIEnv * env;
  int JNI_mode = JIANE_get_env(&env);

  jobject modObj = JIANEDC_get_java_instance(self);

  JIANE_end_env(JNI_mode);*/
  return Py_None;
}

PyObject *JIANEDC_toModule(JNIEnv *env, jobject *module) {
  jclass clazz = (*env)->FindClass(env, "tiane/java/api/Module");
  jobject glob = (*env)->NewGlobalRef(env, *module);

  jmethodID mid_priority = (*env)->GetMethodID(env, clazz, "priority", "()I");
  int priority = (*env)->CallIntMethod(env, glob, mid_priority);

  jmethodID mid_words = (*env)->GetMethodID(env, clazz, "words", "()[Ljava/lang/String;");
  jobjectArray words = (jobjectArray) (*env)->CallObjectMethod(env, glob, mid_words);

  jmethodID mid_name = (*env)->GetMethodID(env, clazz, "name", "()Ljava/lang/String;");
  jstring jmodname = (jstring) (*env)->CallObjectMethod(env, glob, mid_name);

  int words_length = (*env)->GetArrayLength(env, words);
  PyObject *wordlist = PyList_New(words_length);
  for (int words_index = 0;words_index < words_length;words_index++) {
    jstring elem = (jstring)(*env)->GetObjectArrayElement(env, words, words_index);
    PyList_SetItem(wordlist, words_index, PyUnicode_FromString((*env)->GetStringUTFChars(env, elem, NULL)));
  }

  char *modulename_generated = malloc((*env)->GetStringUTFLength(env, jmodname) + 6 + 4);
  int moduleId = nextId;
  nextId += 1;
  sprintf(modulename_generated, "jiane.%s_%d", (*env)->GetStringUTFChars(env, jmodname, NULL), moduleId);
  JIANEDC_push_modmap(moduleId, glob);

  PyObject *pymodule = PyImport_AddModule(modulename_generated);
  PyModule_AddIntConstant(pymodule, "JAVA_MODULE_MAP_ID", moduleId);
  PyModule_AddObject(pymodule, "PRIORITY", PyLong_FromSize_t(priority));
  PyModule_AddObject(pymodule, "WORDS", wordlist);
  PyMethodDef method_define[] = {
      {"isValid",  JDC_PY_isValid, METH_VARARGS, ""},
      {"handle",  JDC_PY_handle, METH_VARARGS, ""},
      {NULL, NULL, 0, NULL} //Must be the last entry, do not delete
  };
  PyModule_AddFunctions(pymodule, method_define);
  printf("%d\n", (PyCFunction_GET_FLAGS(PyDict_GetItemString(PyModule_GetDict(pymodule), "isValid"))) & ~(METH_CLASS | METH_STATIC | METH_COEXIST));
  if (
      PyCFunction_Call(
          PyDict_GetItemString(
              PyModule_GetDict(pymodule),
              "isValid"),
          PyTuple_Pack(1, PyUnicode_FromString("HaLLo WelT dfsihbdisfvdaisbvpinguindhiwbcqwibcdqlibvqa")),
          NULL) == Py_True) { printf("YES\n"); } else { printf("NO\n"); }
  return pymodule;
}

PyObject *JIANEDC_toContinuousModule(JNIEnv * env, jobject *module) {
}