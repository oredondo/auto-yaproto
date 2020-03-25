/*
 * Copyright 2012 Javier Ramirez
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.savarese.com/software/ApacheLicense-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#ifndef __ROCKSAW_RAW_SOCKET_NETLINK_H
#define __ROCKSAW_RAW_SOCKET_NETLINK_H

#include <jni.h>

#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT jint JNICALL
Java_msti_util_RawSocketNetlink__1_1PF_1NETLINK
(JNIEnv *, jclass);

JNIEXPORT jint JNICALL
Java_msti_util_RawSocketNetlink__1_1bind
(JNIEnv *, jclass, jint, jint, jbyteArray);

JNIEXPORT jint JNICALL
Java_msti_util_RawSocketNetlink__1_1sendto
(JNIEnv *env, jclass cls, jint socket,
 jbyteArray data, jint offset, jint len, jint family, jbyteArray address);

JNIEXPORT jint JNICALL
Java_msti_util_RawSocketNetlink__1_1recvfrom1
(JNIEnv *env, jclass cls, jint socket,
 jbyteArray data, jint offset, jint len, jint family);

JNIEXPORT jint JNICALL
Java_msti_util_RawSocketNetlink__1_1recvfrom2
(JNIEnv *env, jclass cls, jint socket,
 jbyteArray data, jint offset, jint len, jint family, jbyteArray address);

/* sizeof estructuras */
JNIEXPORT jint JNICALL
Java_msti_util_RawSocketNetlink__1_1getSizeofType
(JNIEnv *, jclass, jint);

/* alineamiento */
JNIEXPORT jint JNICALL
Java_msti_util_RawSocketNetlink__1_1getAlignment
(JNIEnv *, jclass);

/* pid */
JNIEXPORT jlong JNICALL
Java_msti_util_RawSocketNetlink__1_1getPid
(JNIEnv *, jclass);

#ifdef __cplusplus
}
#endif

#endif
