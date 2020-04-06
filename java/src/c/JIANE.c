#include "JIANE.h"

#include <jni.h>

int JIANE_get_env(JNIEnv **env) {
  int stat = (*JIANE_jvm)->GetEnv(JIANE_jvm, (void **)env, JIANE_jni_version);
  if (stat == JNI_EDETACHED) {
    JavaVMAttachArgs args;
    args.version = JIANE_jni_version;
    args.name = NULL;
    args.group = NULL;
    stat = (*JIANE_jvm)->AttachCurrentThread(JIANE_jvm, (void **)&env, &args);
    if (stat = JNI_OK) {
      return 2;
    } else {
      return 0;
    }
  } else if (stat == JNI_OK) {
    return 1;
  } else {
    return 0;
  }
}

void JIANE_end_env(int envMode) {
  if (envMode == 2) { // Was attached before, we ned to detach it now
    (*JIANE_jvm)->DetachCurrentThread(JIANE_jvm);
  }
}