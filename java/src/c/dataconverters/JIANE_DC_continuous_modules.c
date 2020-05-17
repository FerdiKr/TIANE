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

static PyObject *JDC_PY_continuous_module_meth(PyObject *self, PyObject *args, char* mname) {
  PyObject *module;
  PyObject *tiane;
  PyObject *lstorage;
  if (!PyArg_ParseTuple(args, "OOO", &module, &tiane, &lstorage))
    return NULL;

  JNIEnv *env;
  int JNI_mode = JIANE_get_env(&env);

  jobject modObj = JIANEDC_get_java_instance(module);
  if (modObj != NULL) {
    jobject j_tiane = JIANEDC_createLazyPythonWrapper(env, (*env)->FindClass(env, "tiane/java/api/ModuleWrapperContinuous"), tiane, JNI_TRUE);
    jobject j_lstorage = JIANEDC_createLazyPythonWrapper(env, (*env)->FindClass(env, "tiane/java/api/LocalStorage"), lstorage, JNI_TRUE);
    jclass clazz = (*env)->FindClass(env, "tiane/java/api/ModuleContinuous");
    jmethodID mid_handle = (*env)->GetMethodID(env, clazz, mname, "(Ltiane/java/api/ModuleWrapperContinuous;Ltiane/java/api/LocalStorage;)V");
    (*env)->CallVoidMethod(env, modObj, mid_handle, j_tiane, j_lstorage);
  }

  JIANE_end_env(JNI_mode);
  Py_XINCREF(Py_None);
  return Py_None;
}

PyObject *JDC_PY_continuous_module_start(PyObject *self, PyObject *args) {
  return JDC_PY_continuous_module_meth(self, args, "start");
}

PyObject *JDC_PY_continuous_module_run(PyObject *self, PyObject *args) {
  return JDC_PY_continuous_module_meth(self, args, "run");
}

PyObject *JDC_PY_continuous_module_stop(PyObject *self, PyObject *args) {
  return JDC_PY_continuous_module_meth(self, args, "stop");
}

PyObject *JIANEDC_toContinuousModule(JNIEnv * env, jobject module) {
  jclass clazz = (*env)->FindClass(env, "tiane/java/api/ModuleContinuous");
  jobject glob = (*env)->NewGlobalRef(env, module);

  jmethodID mid_active = (*env)->GetMethodID(env, clazz, "active", "()Z");
  jboolean active = (*env)->CallBooleanMethod(env, glob, mid_active);

  if (active != JNI_TRUE) {
    Py_XINCREF(Py_None);
    return Py_None;
  }

  jmethodID mid_priority = (*env)->GetMethodID(env, clazz, "priority", "()I");
  int priority = (*env)->CallIntMethod(env, glob, mid_priority);

  jmethodID mid_interval = (*env)->GetMethodID(env, clazz, "interval", "()I");
  int interval = (*env)->CallIntMethod(env, glob, mid_interval);

  jmethodID mid_name = (*env)->GetMethodID(env, clazz, "name", "()Ljava/lang/String;");
  jstring jmodname = (jstring) (*env)->CallObjectMethod(env, glob, mid_name);

  char *modulename_generated = calloc((*env)->GetStringUTFLength(env, jmodname) + 11 + 4, sizeof(char));
  int moduleId = nextId;
  nextId += 1;
  sprintf(modulename_generated, "jiane.cmod%s_%d", (*env)->GetStringUTFChars(env, jmodname, NULL), moduleId);
  JIANEDC_push_modmap(moduleId, glob);

  PyObject *pymodule = PyModule_New(modulename_generated);
  PyModule_AddIntConstant(pymodule, "JAVA_MODULE_MAP_ID", moduleId);
  PyModule_AddObject(pymodule, "PRIORITY", PyLong_FromSize_t(priority));
  PyModule_AddObject(pymodule, "INTERVAL", PyLong_FromSize_t(interval));
  PyModule_AddObject(pymodule, "MODNAME", PyUnicode_FromString((*env)->GetStringUTFChars(env, jmodname, NULL)));

  PyDict_SetItemString(PySys_GetObject("modules"), modulename_generated, pymodule);
  PyObject *imported_module = PyImport_ImportModule(modulename_generated);
  Py_XINCREF(imported_module);
  return pymodule;
}