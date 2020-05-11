#include <JIANE.h>

#ifndef _Included_jiane_signal
#define _Included_jiane_signal

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Definiert Funktionen, die den Signal-Handler für SIGINT und SIGTERM neu setzten, da
 * diese durch den Aufruf von Java nicht wie gewohnt funktionieren und TIANE sonst nicht
 * ordnungsgemäß beendet werden kann.
 */

// Gibt an, ob ein Signal gesendet wurde und TIANE beendet werden soll. Wird regelmäßig von TIANE überprüft.
jboolean PYTIANE_should_stop;

// Python-Funktion um die Signal-Handler zu setzen
PyObject *JIANE_signal_set_handlers(PyObject *, PyObject *);

// Python-Funktion um zu Erfahren, ob gestoppt werden sollte
PyObject *JIANE_signal_should_stop(PyObject *, PyObject *);

// Funktion die ein Signal verarbeitet. Kann verwendet werden um die Reaktion von JIANE auf ein Signal zu simulieren.
void JIANE_signal_handle(int);

#ifdef __cplusplus
}
#endif

#endif