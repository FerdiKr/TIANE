#include <JIANE.h>

#include "tiane_java_api_LazyPythonObject.h"

#include <JIANE_DataConverters.h>

JNIEXPORT void JNICALL Java_tiane_java_api_LazyPythonObject_finalize(JNIEnv *env, jobject obj) {
  ENSURE_GIL;
  JIANEDC_decrefLazyWrapped(env, obj);
  RELEASE_GIL;
}