#include <JIANE.h>

#ifndef _Included_jiane_module
#define _Included_jiane_module

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Header des JIANE Python-Moduls.
 */

// Die Initialisierungs-Funktion für das Python-Modul
PyMODINIT_FUNC PyInit_jiane(void);

// Lädt normale Module von Java
PyObject *JPY_loadModules(PyObject *, PyObject *);

// Lädt fortlaufende Module von Java
PyObject *JPY_loadModulesContinuous(PyObject *, PyObject *);

#ifdef __cplusplus
}
#endif

#endif