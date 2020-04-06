#include <jni.h>

JavaVM * JIANE_jvm;
jint JIANE_jni_version;

int JIANE_get_env(JNIEnv **);
void JIANE_end_env(int);