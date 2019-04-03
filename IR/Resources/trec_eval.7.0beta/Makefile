BIN = /home/smart/src/bin
H   = .

# Static libraries with gcc
CC       = gcc
CFLAGS   = -I$H -O4 -Wall

# Static libraries with cc
###CC       = cc
###CFLAGS   = -I$H -O4
###cc CFLAGS   = -I$H -g -Bstatic

# Other macros used in some or all makefiles
INSTALL = /bin/mv


OBJS = trec_eval.o error_msgs.o print_teval.o textline.o \
       tr_teval.o trvec_teval.o buf_util.o

SRCS = trec_eval.c error_msgs.c print_teval.c textline.c \
       tr_teval.c trvec_teval.c buf_util.c

SRCH = common.h trec_eval.h smart_error.h sysfunc.h textline.h tr_vec.h buf.h

SRCOTHER = README Makefile

trec_eval: $(OBJS)
	$(CC) $(CFLAGS) -o trec_eval $(OBJS)

install: $(BIN)/trec_eval

$(BIN)/trec_eval: trec_eval
	if [ -f $@ ]; then $(INSTALL) $@ $@.old; fi;
	$(INSTALL) trec_eval $@

##4##########################################################################
##5##########################################################################
#  All code below this line (except for automatically created dependencies)
#  is independent of this particular makefile, and should not be changed!
#############################################################################

#########################################################################
# Odds and ends                                                         #
#########################################################################
clean semiclean:
	/bin/rm -f *.o *.BAK *~ trec_eval shar.out

shar:
	shar -v -c -pX $(SRCOTHER) $(SRCS) $(SRCH) > shar.out


lint:
	lint $(SRCS)

#########################################################################
# Determining program dependencies                                      #
#########################################################################
depend:
	grep '^#[ ]*include' *.c \
		| sed -e 's?:[^"]*"\([^"]*\)".*?: \$H/\1?' \
			-e '/</d' \
			-e '/functions.h/d' \
		        -e 's/\.c/.o/' \
		        -e 's/\.y/.o/' \
		        -e 's/\.l/.o/' \
		> makedep
	echo '/^# DO NOT DELETE THIS LINE/+2,$$d' >eddep
	echo '$$r makedep' >>eddep
	echo 'w' >>eddep
	cp Makefile Makefile.bak
	ed - Makefile < eddep
	/bin/rm eddep makedep
	echo '# DEPENDENCIES MUST END AT END OF FILE' >> Makefile
	echo '# IF YOU PUT STUFF HERE IT WILL GO AWAY' >> Makefile
	echo '# see make depend above' >> Makefile

# DO NOT DELETE THIS LINE -- make depend uses it

buf_util.o: ./common.h
buf_util.o: ./sysfunc.h
buf_util.o: ./buf.h
error_msgs.o: ./smart_error.h
error_msgs.o: ./sysfunc.h
print_teval.o: ./common.h
print_teval.o: ./sysfunc.h
print_teval.o: ./buf.h
print_teval.o: ./trec_eval.h
textline.o: ./common.h
textline.o: ./textline.h
tr_teval.o: ./common.h
tr_teval.o: ./sysfunc.h
tr_teval.o: ./smart_error.h
tr_teval.o: ./tr_vec.h
tr_teval.o: ./trec_eval.h
tr_teval.o: ./buf.h
trec_eval.o: ./common.h
trec_eval.o: ./sysfunc.h
trec_eval.o: ./smart_error.h
trec_eval.o: ./tr_vec.h
trec_eval.o: ./textline.h
trec_eval.o: ./trec_eval.h
trec_eval.o: ./buf.h
trvec_teval.o: ./common.h
trvec_teval.o: ./sysfunc.h
trvec_teval.o: ./smart_error.h
trvec_teval.o: ./tr_vec.h
trvec_teval.o: ./trec_eval.h
# DEPENDENCIES MUST END AT END OF FILE
# IF YOU PUT STUFF HERE IT WILL GO AWAY
# see make depend above
