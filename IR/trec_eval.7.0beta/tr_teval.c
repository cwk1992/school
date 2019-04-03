#ifdef RCSID
static char rcsid[] = "$Header: /home/smart/release/src/libevaluate/tr_eval.c,v 11.0 1992/07/21 18:20:33 chrisb Exp chrisb $";
#endif

/* Copyright (c) 1991, 1990, 1984 - Gerard Salton, Chris Buckley. 

   Permission is granted for use of this file in unmodified form for
   research purposes. Please contact the SMART project to obtain 
   permission for other uses.
*/

/********************   PROCEDURE DESCRIPTION   ************************
 *0 Given a tr file, evaluate it using trec, returning the evaluation in eval
 *2 tr_trec_eval (tr_file, eval, inst)
 *3   char *tr_file;
 *3   TREC_EVAL *eval;
 *3   int inst;
 *4 init_tr_trec_eval (spec, unused)
 *5   "eval.tr_file"
 *5   "eval.tr_file.rmode"
 *5   "eval.trace"
 *4 close_tr_trec_eval (inst)
 *7 Evaluate the given tr_file, returning the average over all queries of
 *7 each query's evaluation.  Eval->qid will contain the number of queries
 *7 evaluated. Tr_file is taken from the argument tr_file if
 *7 that is valid, else from the spec parameter eval.tr_file.
 *7 Return 1 if successful, 0 if no queries were evaluated, and UNDEF otherwise
 *8 Call trvec_smeval for each query in tr_file, and simply average results.
 *9 Note: Only the max iteration over all queries is averaged.  Thus, if query
 *9 1 had one iteration of feedback, and query 2 had two iterations of
 *9 feedback, query 1 will not be included in the final average (or counted
 *9 in eval->qid).
***********************************************************************/

#include "common.h"
#include "sysfunc.h"
#include "smart_error.h"
#include "tr_vec.h"
#include "trec_eval.h"
#include "buf.h"

int trvec_trec_eval();
void print_trec_eval_list();

static int max_iter;

/* WARNING: Global variables! */
extern long query_flag;           /* If set, evaluation output will be
                                     printed for each query, in addition
                                     to summary at end. */
extern long all_flag;             /* If set, all evaluation measures will
                                     be printed instead of just the
                                     final TREC 2 measures. */
extern long doc_avg_flag;         /* If set, print avg_doc_prec in addition
                                     to final TREC 2 measures. */
extern long time_flag;             /* If set, calculate time based measures. */


int
init_tr_trec_eval (eval)
TREC_EVAL *eval;
{
    (void) bzero ((char *) eval, sizeof (TREC_EVAL));
    max_iter = 0;

    return (0);
}

int
tr_trec_eval (tr_vec, eval, num_rel)
TR_VEC *tr_vec;
TREC_EVAL *eval;
long num_rel;
{
    long i;
    int max_iter_achieved;
    TREC_EVAL query_eval;

    /* Check that max_iter has not been exceeded.  If it has, then have
       to throw away all previous results.
       Also check to see that max_iter has been achieved.  If not, then
       no docs were retrieved for this query on this iteration */
    max_iter_achieved = 0;
    for (i = 0; i < tr_vec->num_tr; i++) {
        if (tr_vec->tr[i].iter > max_iter) {
            (void) bzero ((char *) eval, sizeof (TREC_EVAL));
            max_iter = tr_vec->tr[i].iter;
        }
        if (tr_vec->tr[i].iter == max_iter) {
            max_iter_achieved++;
        }
    }
    if (max_iter_achieved == 0)
        return (0);

    /* Evaluate this query, then add into totals so far */
    if (1 == trvec_trec_eval (tr_vec, &query_eval, num_rel)) {
        if (query_eval.num_ret > 0) {
            eval->qid++;
            eval->num_rel       += query_eval.num_rel;
            eval->num_ret       += query_eval.num_ret;
            eval->num_rel_ret   += query_eval.num_rel_ret;
            eval->avg_doc_prec  += query_eval.avg_doc_prec;
            eval->exact_recall  += query_eval.exact_recall;
            eval->exact_precis  += query_eval.exact_precis;
            eval->exact_rel_precis += query_eval.exact_rel_precis;
            eval->exact_uap += query_eval.exact_uap;
            eval->exact_rel_uap += query_eval.exact_rel_uap;
            eval->exact_utility += query_eval.exact_utility;
	    eval->av_rel_precis += query_eval.av_rel_precis;
	    eval->av_rel_uap += query_eval.av_rel_uap;
            eval->av_recall_precis += query_eval.av_recall_precis;
            eval->int_av_recall_precis += query_eval.int_av_recall_precis;
            eval->int_av3_recall_precis += query_eval.int_av3_recall_precis;
            eval->int_av11_recall_precis += query_eval.int_av11_recall_precis;
            eval->av_fall_recall += query_eval.av_fall_recall;
            eval->R_recall_precis += query_eval.R_recall_precis;
            eval->av_R_precis += query_eval.av_R_precis;
            eval->int_R_recall_precis += query_eval.int_R_recall_precis;
            eval->int_av_R_precis += query_eval.int_av_R_precis;
            for (i = 0; i < NUM_CUTOFF; i++) {
                eval->recall_cut[i] += query_eval.recall_cut[i];
                eval->precis_cut[i] += query_eval.precis_cut[i];
                eval->rel_precis_cut[i] += query_eval.rel_precis_cut[i];
                eval->uap_cut[i] += query_eval.uap_cut[i];
                eval->rel_uap_cut[i] += query_eval.rel_uap_cut[i];
            }
            for (i = 0; i < NUM_RP_PTS; i++)
                eval->int_recall_precis[i] += query_eval.int_recall_precis[i];
            for (i = 0; i < NUM_FR_PTS; i++)
                eval->fall_recall[i] += query_eval.fall_recall[i];
            for (i = 0; i < NUM_PREC_PTS; i++) {
                eval->R_prec_cut[i] += query_eval.R_prec_cut[i];
                eval->int_R_prec_cut[i] += query_eval.int_R_prec_cut[i];
            }
	    if (time_flag) {
		eval->av_time_precis += query_eval.av_time_precis;
		eval->av_time_relprecis += query_eval.av_time_relprecis;
		eval->av_time_uap +=query_eval.av_time_uap;
		eval->av_time_reluap +=query_eval.av_time_reluap;
		eval->av_time_utility += query_eval.av_time_utility;
		eval->av_time_cum_rel += query_eval.av_time_cum_rel;
		for (i = 0; i < NUM_TIME_PTS; i++) {
		    eval->time_num_rel[i] += query_eval.time_num_rel[i];
		    eval->time_num_nrel[i] += query_eval.time_num_nrel[i];
		    eval->time_cum_rel[i] += query_eval.time_cum_rel[i];
		    eval->time_precis[i] += query_eval.time_precis[i];
		    eval->time_relprecis[i] += query_eval.time_relprecis[i];
		    eval->time_uap[i] += query_eval.time_uap[i];
		    eval->time_reluap[i] += query_eval.time_reluap[i];
		    eval->time_utility[i] += query_eval.time_utility[i];
		}
	    }
        }
        if (query_flag) {
            print_trec_eval_list (&query_eval, 1, (SM_BUF *) NULL);
        }
    }

        
    return (0);
}

int
close_tr_trec_eval(eval)
TREC_EVAL *eval;
{
    long i;

    /* Calculate averages (for those eval fields returning averages) */
    if (eval->qid > 0) {
        if (eval->num_rel > 0)
            eval->avg_doc_prec /= (float) eval->num_rel;
        eval->exact_recall /= (float) eval->qid;
        eval->exact_precis /= (float) eval->qid;
        eval->exact_rel_precis /= (float) eval->qid;
	eval->exact_uap /= (float) eval->qid;
	eval->exact_rel_uap /= (float) eval->qid;
	eval->exact_utility /= (float) eval->qid;
	eval->av_rel_precis /= (float) eval->qid;
	eval->av_rel_uap /= (float) eval->qid;
        eval->av_recall_precis /= (float) eval->qid;
        eval->int_av_recall_precis /= (float) eval->qid;
        eval->int_av3_recall_precis /= (float) eval->qid;
        eval->int_av11_recall_precis /= (float) eval->qid;
        eval->av_fall_recall /= (float) eval->qid;
        eval->R_recall_precis /= (float) eval->qid;
        eval->av_R_precis /= (float) eval->qid;
        eval->int_R_recall_precis /= (float) eval->qid;
        eval->int_av_R_precis /= (float) eval->qid;
        for (i = 0; i < NUM_CUTOFF; i++) {
            eval->recall_cut[i] /= (float) eval->qid;
            eval->precis_cut[i] /= (float) eval->qid;
            eval->rel_precis_cut[i] /= (float) eval->qid;
	    eval->uap_cut[i] /= (float) eval->qid;
	    eval->rel_uap_cut[i] /= (float) eval->qid;
        }
        for (i = 0; i < NUM_RP_PTS; i++)
            eval->int_recall_precis[i] /= (float) eval->qid;
        for (i = 0; i < NUM_FR_PTS; i++)
            eval->fall_recall[i] /= (float) eval->qid;
        for (i = 0; i < NUM_PREC_PTS; i++) {
            eval->R_prec_cut[i] /= (float) eval->qid;
            eval->int_R_prec_cut[i] /= (float) eval->qid;
        }
	if (time_flag) {
	    eval->av_time_precis /= (float) eval->qid;
	    eval->av_time_relprecis /= (float) eval->qid;
	    eval->av_time_uap /= (float) eval->qid;
	    eval->av_time_reluap /= (float) eval->qid;
	    eval->av_time_utility /= (float) eval->qid;
	    eval->av_time_cum_rel /= (float) eval->qid;
	    for (i = 0; i < NUM_TIME_PTS; i++) {
		eval->time_num_rel[i] /= (float) eval->qid;
		eval->time_num_nrel[i] /= (float) eval->qid;
		eval->time_cum_rel[i] /= (float) eval->qid;
		eval->time_precis[i] /= (float) eval->qid;
		eval->time_relprecis[i] /= (float) eval->qid;
		eval->time_uap[i] /= (float) eval->qid;
		eval->time_reluap[i] /= (float) eval->qid;
		eval->time_utility[i] /= (float) eval->qid;
	    }
	}
    }

    return (0);
}
