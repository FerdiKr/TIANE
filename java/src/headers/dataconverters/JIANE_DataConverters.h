#include <JIANE.h>

#ifndef _Included_jiane_dc
#define _Included_jiane_dc

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Definiert einige Funktionen zum Umwandeln zwischen Java und Python - Objekten.
 */

// Methoden zur Nutzung von `LazyWrapped` Python Objekten.
jobject JIANEDC_createLazyPythonWrapper(JNIEnv *, jclass, PyObject *, jboolean);
PyObject *JIANEDC_getLazyWrapped(JNIEnv *, jobject);
void JIANEDC_decrefLazyWrapped(JNIEnv *, jobject);

// Javas primitive Datentypen und String Konversationen
jstring JIANEDC_toJavaString(JNIEnv *, PyObject *);  // Diese Funktionen berücksichtigen nicht, dass Java Modified-UTF8 nutzt
PyObject *JIANEDC_toPythonString(JNIEnv *, jstring); // un Python nicht. Ich habe keine gute Methode zum Umwandeln gefunden.
jint JIANEDC_toJavaInt(JNIEnv *, PyObject *);
PyObject *JIANEDC_toPythonInt(JNIEnv *, jint);
jlong JIANEDC_toJavaLong(JNIEnv *, PyObject *);
PyObject *JIANEDC_toPythonLong(JNIEnv *, jlong);
jdouble JIANEDC_toJavaDouble(JNIEnv *, PyObject *);
PyObject *JIANEDC_toPythonDouble(JNIEnv *, jdouble);
jboolean JIANEDC_toJavaBoolean(JNIEnv *, PyObject *);
PyObject *JIANEDC_toPythonBoolean(JNIEnv *, jboolean);

// TIANE-Module
PyObject *JIANEDC_toModule(JNIEnv *, jobject);
PyObject *JIANEDC_toContinuousModule(JNIEnv * env, jobject);

// Funktionen von normalen Modulen
PyObject *JDC_PY_module_handle(PyObject *, PyObject *);
PyObject *JDC_PY_module_isValid(PyObject *, PyObject *);
PyObject *JDC_PY_module_isValidTelegram(PyObject *, PyObject *);

// Funktionen von fortlaufenden Modulen
PyObject *JDC_PY_continuous_module_start(PyObject *, PyObject *);
PyObject *JDC_PY_continuous_module_run(PyObject *, PyObject *);
PyObject *JDC_PY_continuous_module_stop(PyObject *, PyObject *);

// Ruft die Funktion mit dem namen `name` des Objekts `obj` auf und gibt das Ergebnis zurück. `numArgs` ist die Parameteranzahl und `...` sind die Funktionparameter.
#define JDC_call(obj, name, numArgs, ...) PyObject_Call(PyObject_GetAttrString(obj, name), PyTuple_Pack(numArgs, ##__VA_ARGS__), NULL)

// Wie `JDC_call`, aber zusätzlich gibt es den Parameter `kwargs`, der Benannte Argumente angiebt.
#define JDC_kwcall(obj, name, kwargs, numArgs, ...) PyObject_Call(PyObject_GetAttrString(obj, name), PyTuple_Pack(numArgs, ##__VA_ARGS__), kwargs)

#ifdef __cplusplus
}
#endif

#endif