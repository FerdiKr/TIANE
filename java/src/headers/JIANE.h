#define PY_SSIZE_T_CLEAN

#include <jni.h>
#include <Python.h>

#ifndef _Included_jiane
#define _Included_jiane

#ifdef __cplusplus
extern "C" {
#endif

/*
 * JIANES Haupt-Header. Alle anderen `c` oder `h` Dateien von JIANE (mit Ausnahme der automatisch generierten
 * Header der JNI) müssen mit `#include <JIANE.h>` beginnen.
 */

// Die Java Virtual Machine. Wird dazu benötigt, zu einem späteren Zeitpunkt Threads zur JVM zu attchen.
JavaVM * JIANE_jvm;

// Die Version der JNI.
jint JIANE_jni_version;

/**
 * Gibt das `JNIEnv` des aktuellen Threads zurück. Ist der Thread noch nicht zu JVM hinzugefügt, fügt diese Funktion
 * den Thread hinzu. Der Rückgabewert ist ein int, der Anzaigt, ob der Thread vorher schon zur JVM hinzugefügt wurde.
 * Wenn ein Fehler auftritt wird 0 zurückgegeben.
 */
int JIANE_get_env(JNIEnv **);

/**
 * Diese Funktion sollte mit dem Rückgabewert von `JIANE_get_env` aufgerufen werden, wenn Java nicht mehr benötigt
 * wird. Fals der Thread vorher nicht zu JVM hinzugefügt war, wird er jetzt wieder abgelöst.
 */
void JIANE_end_env(int);

// Sichert dem aktuellen Thread den Python GLOBAL_INTERPRETER_LOCK. Die Variable py_gil_mode wird dazu definiert.
#define ENSURE_GIL const PyGILState_STATE py_gil_mode = PyGILState_Ensure()

// Stellt den Zustand vor der Beschlagnahmung des GIL wieder her. Vorher muss `ENSURE_GIL` aufgerufen worden sein.
#define RELEASE_GIL PyGILState_Release(py_gil_mode)

#ifdef __cplusplus
}
#endif

#endif