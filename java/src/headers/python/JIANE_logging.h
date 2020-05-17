#include <JIANE.h>

#ifndef _Included_jiane_logging
#define _Included_jiane_logging

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Definiert Funktionen um den Singleton-Logger von TIANE in Java zu nutzen.
 */

PyObject *JLOG_PY_create(PyObject *, PyObject *);

#ifdef __cplusplus
}
#endif

#endif