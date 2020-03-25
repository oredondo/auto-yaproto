/*
 * Copyright 2004-2007 Daniel F. Savarese
 * Copyright 2009 Savarese Software Research Corporation
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

#include <stdio.h>
#include <errno.h>
#include <string.h>

#if defined(_WIN32)

#  include <winsock2.h>
#  include <ws2tcpip.h>

#  if !defined(close)
#    define close(fd) closesocket(fd)
#  endif

#else

#  include <netdb.h>
#  include <netinet/in.h>
#  include <sys/socket.h>
#  include <unistd.h>
#  include <sys/types.h>
#  include <sys/time.h>
/* netlink */
#  include <asm/types.h>
#  include <linux/netlink.h>
#  include <linux/rtnetlink.h>

#endif

#include "RawSocketNetlink.h"

/*
 * Utility functions.
 */

/* netlink*/
static struct sockaddr*
init_sockaddr_nl(JNIEnv *env, struct sockaddr_nl *snl, jbyteArray address) {
  jbyte *buf;

  /*int i;*/

  memset(snl, 0, sizeof(struct sockaddr_nl));
  snl->nl_family = AF_NETLINK;
  buf = (*env)->GetByteArrayElements(env, address, NULL);
  memcpy(snl, buf, sizeof(struct sockaddr_nl));
  printf("nl_family(antes)=%d, nl_pid=%d, nl_groups=%d\n", snl->nl_family,
         snl->nl_pid, snl->nl_groups);
  fflush(stdout);
  snl->nl_family = AF_NETLINK;
  printf("nl_family=%d, nl_pid=%d, nl_groups=%d\n", snl->nl_family,
         snl->nl_pid, snl->nl_groups);
  (*env)->ReleaseByteArrayElements(env, address, buf, JNI_ABORT);

  return (struct sockaddr *)snl;
}

/*
 * Class:     msti_util_RawSocketNetlink
 * Method:    __PF_NETLINK
 * Signature: ()I
 */
JNIEXPORT jint JNICALL
Java_msti_util_RawSocketNetlink__1_1PF_1NETLINK
(JNIEnv *env, jclass cls)
{
  return PF_NETLINK;
}

/*
 * Class:     msti_util_RawSocketNetlink
 * Method:    __bind
 * Signature: (II[B)I
 */
JNIEXPORT jint JNICALL
Java_msti_util_RawSocketNetlink__1_1bind
(JNIEnv *env, jclass cls, jint socket, jint family, jbyteArray address)
{
  struct sockaddr *saddr;
  socklen_t socklen;
  struct sockaddr_nl snl; /* netlink */

  if(family == AF_NETLINK) {
	 /* netlink */
    socklen = sizeof(snl);
    saddr = init_sockaddr_nl(env, &snl, address); /* address en realidad contiene la direcci�n completa como byte[] */
  }
  else
    return -1;

  /* printf("Intenta bind({fam=%d,pid=%d,groups=%d},len=%d)...\n", snl.nl_family, snl.nl_pid, snl.nl_groups, socklen); */
  return bind(socket, saddr, socklen);
}

/*
 * Class:     msti_util_RawSocketNetlink
 * Method:    __recvfrom
 * Signature: (I[BIII)I
 */
JNIEXPORT jint JNICALL
Java_msti_util_RawSocketNetlink__1_1recvfrom1
(JNIEnv *env, jclass cls, jint socket,
 jbyteArray data, jint offset, jint len, jint family)
{
  int result;
  jbyte *buf;

  if(family != PF_NETLINK) {
    errno = EINVAL;
    return errno;
  }

  buf = (*env)->GetByteArrayElements(env, data, NULL);

  result = recvfrom(socket, buf+offset, len, 0, NULL, NULL);

  (*env)->ReleaseByteArrayElements(env, data, buf, 0);

#if defined(_WIN32)
  if(result < 0)
    errno = WSAGetLastError();
#endif

  return result;
}

/*
 * Class:     msti_util_RawSocketNetlink
 * Method:    __recvfrom
 * Signature: (I[BIII[B)I
 */
JNIEXPORT jint JNICALL
Java_msti_util_RawSocketNetlink__1_1recvfrom2
(JNIEnv *env, jclass cls, jint socket,
 jbyteArray data, jint offset, jint len, jint family, jbyteArray address)
{
  int result;
  jbyte *buf;
  struct sockaddr_nl snl;
  struct sockaddr *saddr;
  socklen_t socklen;
  
  if(family == PF_NETLINK) {
    memset(&snl, 0, sizeof(struct sockaddr_nl));
    snl.nl_family = AF_NETLINK;
    saddr = (struct sockaddr *)&snl;
    socklen = sizeof(snl);
  } else {
    errno = EINVAL;
    return errno;
  }

  buf = (*env)->GetByteArrayElements(env, data, NULL);

  result = recvfrom(socket, buf+offset, len, 0, saddr, &socklen);

  (*env)->ReleaseByteArrayElements(env, data, buf, 0);

  buf = (*env)->GetByteArrayElements(env, address, NULL);
  memcpy(buf, saddr, socklen);
  (*env)->ReleaseByteArrayElements(env, address, buf, 0);

#if defined(_WIN32)
  if(result < 0)
    errno = WSAGetLastError();
#endif

  return result;
}

/*
 * Class:     msti_util_RawSocketNetlink
 * Method:    __sendto
 * Signature: (I[BIII[B)I
 */
JNIEXPORT jint JNICALL
Java_msti_util_RawSocketNetlink__1_1sendto
(JNIEnv *env, jclass cls, jint socket,
 jbyteArray data, jint offset, jint len, jint family, jbyteArray address)
{
  int result;
  jbyte *buf;
  struct sockaddr_nl snl;
  struct sockaddr *saddr;
  socklen_t socklen;

  if(family == AF_NETLINK) {
    socklen = sizeof(snl);
    saddr = init_sockaddr_nl(env, &snl, address);
  } else {
    errno = EINVAL;
    return errno;
  }

  buf = (*env)->GetByteArrayElements(env, data, NULL);

  result = sendto(socket, buf+offset, len, 0, saddr, socklen);

  (*env)->ReleaseByteArrayElements(env, data, buf, JNI_ABORT);

  return result;
}


/*
 * Class:     msti_util_RawSocketNetlink
 * Method:    __getSizeofType
 * Signature: (II)I
 */
JNIEXPORT jint JNICALL
Java_msti_util_RawSocketNetlink__1_1getSizeofType
(JNIEnv *env, jclass cls, jint tipo)
{
	switch (tipo)
	{
	case 1:
		return (int)sizeof(struct sockaddr_nl);
	case 2:
		return (int)sizeof(struct rtmsg);
	case 3:
		return (int)sizeof(struct rtattr);
	case 4:
		return (int)sizeof(struct rtnexthop);
	case 5:
		return (int)sizeof(struct ifinfomsg);
	case 6:
		return (int)sizeof(struct prefixmsg);
	default:
		return -1;
	}
}

/*
 * Class:    msti_util_RawSocketNetlink
 * Method:    __getAlignment
 * Signature: (II)I
 */
JNIEXPORT jint JNICALL
Java_msti_util_RawSocketNetlink__1_1getAlignment
(JNIEnv *env, jclass cls)
{
	return RTA_ALIGNTO;
}

/*
 * Class:    msti_util_RawSocketNetlink
 * Method:    __getPid
 * Signature: (II)I
 */
JNIEXPORT jlong JNICALL
Java_msti_util_RawSocketNetlink__1_1getPid
(JNIEnv *env, jclass cls)
{
	return (long)getpid();
}
