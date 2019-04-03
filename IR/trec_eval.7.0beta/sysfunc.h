#ifndef SYSFUNCH
#define SYSFUNCH
/*        $Header: /home/smart/release/./src/h/sysfunc.h,v 10.1 91/11/05 23:47:33 smart Exp Locker: smart $ */
/* Declarations of major functions within standard C libraries */
/* Once all of the major systems get their act together (and I follow
   suit!), this file should just include system header files from 
   /usr/include.  Until then... */

#ifdef NeXT
#include <libc.h>
#include <stdlib.h>
#include <math.h>
#else

int open(), close(), write(), read(), link(), stat(), unlink();
long lseek();

void exit();

#ifdef AIX
#include <malloc.h>
#else
char *malloc(), *realloc(), *calloc(), *valloc();
#endif /* AIX */
int bcopy(), bzero();
int free();
#ifndef AIX
int qsort();
#endif AIX
#include <stdio.h>

int atoi(), printf(), puts(), fseek();
long atol();
int scanf(), fscanf(), sscanf();
double atof();

double sqrt(), log(), floor(), exp(), pow();

int strncmp(), strlen(), strcmp();
char *strcpy(), *strncpy(), *strcat(), *strncat();
#endif /* NeXT */

#endif /* SYSFUNCH */
