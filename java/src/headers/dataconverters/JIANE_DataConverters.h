#include <jni.h>
#include <Python.h>

PyObject *JIANEDC_toModule(JNIEnv * env, jobject *);
PyObject *JIANEDC_toContinuousModule(JNIEnv * env, jobject *);

jobject *JIANEDC_toLocalStorage(JNIEnv * env, PyObject *);
jobject *JIANEDC_toModuleWrapper(JNIEnv * env, PyObject *);
jobject *JIANEDC_toModuleWrapperC(JNIEnv * env, PyObject *);