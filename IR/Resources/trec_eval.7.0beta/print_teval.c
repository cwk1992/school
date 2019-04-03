#ifdef RCSID
static char rcsid[] = "$Header: /home/smart/release/src/libprint/po_tr_eval.c,v 11.0 1992/07/21 18:23:29 chrisb Exp $";
#endif

/* Copyright (c) 1991, 1990, 1984 - Gerard Salton, Chris Buckley. 

   Permission is granted for use of this file in unmodified form for
   research purposes. Please contact the SMART project to obtain 
   permission for other uses.
*/

#include "common.h"
#include "sysfunc.h"
#include "buf.h"
#include "trec_eval.h"

static SM_BUF internal_output = {0, 0, (char *) 0};

static long cutoff[] = CUTOFF_VALUES;

int add_buf_string();

/* WARNING: Global variables! */
extern long query_flag;           /* If set, evaluation output will be
                                     printed for each query, in addition
                                     to summary at end. (not used currently
                                     in this procedure */
extern long all_flag;             /* If set, all evaluation measures will
                                     be printed instead of just the
                                     final TREC 2 measures. */
extern long doc_avg_flag;         /* If set, print avg_doc_prec in addition
                                     to final TREC 2 measures. */
extern long time_flag;             /* If set, print time based measures. */
extern double utility_a;       /* Default utility values */
extern double utility_b;       /* (see trec_eval.h) */
extern double utility_c;
extern double utility_d;
extern long num_docs_in_coll;

void
print_trec_eval_list (eval, num_runs, output)
TREC_EVAL *eval;
int num_runs;
SM_BUF *output;
{
    long i,j;
    char temp_buf[1024];
    SM_BUF *out_p;

    if (output == NULL) {
        out_p = &internal_output;
        out_p->end = 0;
    }
    else
        out_p = output;

    /* Print total numbers retrieved/rel for all runs */
    if (UNDEF == add_buf_string("\nQueryid (Num):", out_p))
        return;
    for (i = 0; i < num_runs; i++) {
        (void) sprintf (temp_buf, "    %5ld", eval[i].qid);
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
    }
    if (UNDEF == add_buf_string("\nTotal number of documents over all queries",
                                out_p))
        return;
    if (UNDEF == add_buf_string("\n    Retrieved:", out_p))
        return;
    for (i = 0; i < num_runs; i++) {
        (void) sprintf (temp_buf, "    %5ld", eval[i].num_ret);
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
    }
    if (UNDEF == add_buf_string("\n    Relevant: ", out_p))
        return;
    for (i = 0; i < num_runs; i++) {
        (void) sprintf (temp_buf, "    %5ld", eval[i].num_rel);
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
    }
    if (UNDEF == add_buf_string("\n    Rel_ret:  ", out_p))
        return;
    for (i = 0; i < num_runs; i++) {
        (void) sprintf (temp_buf, "    %5ld", eval[i].num_rel_ret);
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
    }

    /* Print recall precision figures at NUM_RP_PTS recall levels */
    if (UNDEF == add_buf_string
        ("\nInterpolated Recall - Precision Averages:", out_p))
        return;
    for (j = 0; j < NUM_RP_PTS; j++) {
        (void) sprintf (temp_buf, "\n    at %4.2f     ",
                        (float) j / (NUM_RP_PTS - 1));
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
        for (i = 0; i < num_runs; i++) {
            (void) sprintf (temp_buf, "  %6.4f ",eval[i].int_recall_precis[j]);
            if (UNDEF == add_buf_string (temp_buf, out_p))
                return;
        }
    }

    /* Print average recall precision and percentage improvement */
    (void) sprintf (temp_buf,
                   "\nAverage precision (non-interpolated) for all rel docs(averaged over queries)\n                ");
    if (UNDEF == add_buf_string (temp_buf, out_p))
        return;
    for (i = 0; i < num_runs; i++) {
        (void) sprintf (temp_buf, "  %6.4f ", eval[i].av_recall_precis);
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
    }
    if (num_runs > 1) {
        (void) sprintf (temp_buf, "\n    %% Change:           ");
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
        for (i = 1; i < num_runs; i++) {
            (void) sprintf (temp_buf, "  %6.1f ",
                            ((eval[i].av_recall_precis /
                              eval[0].av_recall_precis)
                             - 1.0) * 100.0);
            if (UNDEF == add_buf_string (temp_buf, out_p))
                return;
        }
    }
    /* Print average document precision, if requested */
    if (doc_avg_flag) {
        (void) sprintf (temp_buf,
                        "\nAverage document precision for all rel docs(averaged over rel docs)\n                ");
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
        for (i = 0; i < num_runs; i++) {
            (void) sprintf (temp_buf, "  %6.4f ", eval[i].avg_doc_prec);
            if (UNDEF == add_buf_string (temp_buf, out_p))
                return;
        }
    }

    (void) sprintf (temp_buf, "\nPrecision:");
    if (UNDEF == add_buf_string (temp_buf, out_p))
        return;
    for (j = 0; j < NUM_CUTOFF; j++) {
        (void) sprintf (temp_buf, "\n  At %4ld docs:", cutoff[j]);
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
        for (i = 0; i < num_runs; i++) {
            (void) sprintf (temp_buf, "   %6.4f", eval[i].precis_cut[j]);
            if (UNDEF == add_buf_string (temp_buf, out_p))
                return;
        }
    }

    (void) sprintf (temp_buf, "\nR-Precision (precision after R (= num_rel for a query) docs retrieved):\n    Exact:     ");
    if (UNDEF == add_buf_string (temp_buf, out_p))
        return;
    for (i = 0; i < num_runs; i++) {
        (void) sprintf (temp_buf, "   %6.4f", eval[i].R_recall_precis);
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
    }

    if (! all_flag) {
        if (UNDEF == add_buf_string ("\n", out_p))
            return;
        
        if (output == NULL) {
            (void) fwrite (out_p->buf, 1, out_p->end, stdout);
            out_p->end = 0;
        }
        return;
    }



    (void) sprintf (temp_buf, "\n\n----------------------------------------------------------------\nThe following measures included for TREC 1 compatability\n");
    if (UNDEF == add_buf_string (temp_buf, out_p))
        return;

    (void) sprintf (temp_buf, "\nPrecision:\n   Exact:      ");
    if (UNDEF == add_buf_string (temp_buf, out_p))
        return;
    for (i = 0; i < num_runs; i++) {
        (void) sprintf (temp_buf, "   %6.4f", eval[i].exact_precis);
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
    }
    (void) sprintf (temp_buf, "\nRecall:\n   Exact:      ");
    if (UNDEF == add_buf_string (temp_buf, out_p))
        return;
    for (i = 0; i < num_runs; i++) {
        (void) sprintf (temp_buf, "   %6.4f", eval[i].exact_recall);
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
    }
    for (j = 0; j < NUM_CUTOFF; j++) {
        (void) sprintf (temp_buf, "\n   at %3ld docs:", cutoff[j]);
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
        for (i = 0; i < num_runs; i++) {
            (void) sprintf (temp_buf, "   %6.4f", eval[i].recall_cut[j]);
            if (UNDEF == add_buf_string (temp_buf, out_p))
                return;
        }
    }

    /* Print average recall precision and percentage improvement */
    (void) sprintf (temp_buf,
                    "\nAverage interpolated precision for all %d recall points\n   %2d-pt Avg:   ",
                    NUM_RP_PTS, NUM_RP_PTS);
    if (UNDEF == add_buf_string (temp_buf, out_p))
        return;
    for (i = 0; i < num_runs; i++) {
        (void) sprintf (temp_buf, "  %6.4f ", eval[i].int_av11_recall_precis);
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
    }
    if (num_runs > 1) {
        (void) sprintf (temp_buf, "\n    %% Change:           ");
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
        for (i = 1; i < num_runs; i++) {
            (void) sprintf (temp_buf, "  %6.1f ",
                            ((eval[i].int_av11_recall_precis /
                              eval[0].int_av11_recall_precis)
                             - 1.0) * 100.0);
            if (UNDEF == add_buf_string (temp_buf, out_p))
                return;
        }
    }

    /* Print 3 point average recall precision and percentage improvement */
    if (UNDEF == add_buf_string
        ("\nAverage interpolated precision for 3 intermediate points (0.20, 0.50, 0.80)\n    3-pt Avg:   ",
         out_p))
        return;
    for (i = 0; i < num_runs; i++) {
        (void) sprintf (temp_buf, "  %6.4f ", eval[i].int_av3_recall_precis);
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
    }
    if (num_runs > 1) {
        (void) sprintf (temp_buf, "\n    %% Change:           ");
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
        for (i = 1; i < num_runs; i++) {
            (void) sprintf (temp_buf, "  %6.1f ",
                            ((eval[i].int_av3_recall_precis /
                              eval[0].int_av3_recall_precis)
                             - 1.0) * 100.0);
            if (UNDEF == add_buf_string (temp_buf, out_p))
                return;
        }
    }


    (void) sprintf (temp_buf, "\n\n----------------------------------------------------------------\nThe following measures are possible for future TRECs\n");
    if (UNDEF == add_buf_string (temp_buf, out_p))
        return;

    (void) sprintf (temp_buf, "\nR-based-Precision (precision after given multiple of R docs retrieved):\n    Exact:     ");
    if (UNDEF == add_buf_string (temp_buf, out_p))
        return;
    for (i = 0; i < num_runs; i++) {
        (void) sprintf (temp_buf, "   %6.4f", eval[i].R_recall_precis);
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
    }
    for (j = 1; j < NUM_PREC_PTS; j++) {
        (void) sprintf (temp_buf, "\n    At %4.2f  R:",
                        (float) MAX_RPREC * j / (float) (NUM_PREC_PTS - 1));
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
        for (i = 0; i < num_runs; i++) {
            (void) sprintf (temp_buf, "   %6.4f", eval[i].R_prec_cut[j]);
            if (UNDEF == add_buf_string (temp_buf, out_p))
                return;
        }
    }


    (void) sprintf (temp_buf, "\nRelative Precision:\n   Exact:      ");
    if (UNDEF == add_buf_string (temp_buf, out_p))
        return;
    for (i = 0; i < num_runs; i++) {
        (void) sprintf (temp_buf, "   %6.4f", eval[i].exact_rel_precis);
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
    }
    (void) sprintf (temp_buf, "\n   Average:    ");
    if (UNDEF == add_buf_string (temp_buf, out_p))
        return;
    for (i = 0; i < num_runs; i++) {
        (void) sprintf (temp_buf, "   %6.4f", eval[i].av_rel_precis);
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
    }
    for (j = 0; j < NUM_CUTOFF; j++) {
        (void) sprintf (temp_buf, "\n   At %3ld docs:", cutoff[j]);
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
        for (i = 0; i < num_runs; i++) {
            (void) sprintf (temp_buf, "   %6.4f", eval[i].rel_precis_cut[j]);
            if (UNDEF == add_buf_string (temp_buf, out_p))
                return;
        }
    }

    (void) sprintf (temp_buf, "\nUnranked Average Precision:\n   Exact:      ");
    if (UNDEF == add_buf_string (temp_buf, out_p))
        return;
    for (i = 0; i < num_runs; i++) {
        (void) sprintf (temp_buf, "   %6.4f", eval[i].exact_uap);
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
    }
    for (j = 0; j < NUM_CUTOFF; j++) {
        (void) sprintf (temp_buf, "\n   At %3ld docs:", cutoff[j]);
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
        for (i = 0; i < num_runs; i++) {
            (void) sprintf (temp_buf, "   %6.4f", eval[i].uap_cut[j]);
            if (UNDEF == add_buf_string (temp_buf, out_p))
                return;
        }
    }

    (void) sprintf (temp_buf, "\nRelative Unranked Average Precision:\n   Exact:      ");
    if (UNDEF == add_buf_string (temp_buf, out_p))
        return;
    for (i = 0; i < num_runs; i++) {
        (void) sprintf (temp_buf, "   %6.4f", eval[i].exact_rel_uap);
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
    }
    (void) sprintf (temp_buf, "\n   Average:    ");
    if (UNDEF == add_buf_string (temp_buf, out_p))
        return;
    for (i = 0; i < num_runs; i++) {
        (void) sprintf (temp_buf, "   %6.4f", eval[i].av_rel_uap);
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
    }
    for (j = 0; j < NUM_CUTOFF; j++) {
        (void) sprintf (temp_buf, "\n   At %3ld docs:", cutoff[j]);
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
        for (i = 0; i < num_runs; i++) {
            (void) sprintf (temp_buf, "   %6.4f", eval[i].rel_uap_cut[j]);
            if (UNDEF == add_buf_string (temp_buf, out_p))
                return;
        }
    }

    (void) sprintf (temp_buf,
		    "\nUtility (%3.1f,%3.1f,%3.1f,%3.1f):\n   Exact:      ",
		    utility_a, utility_b, utility_c, utility_d);
    if (UNDEF == add_buf_string (temp_buf, out_p))
        return;
    for (i = 0; i < num_runs; i++) {
        (void) sprintf (temp_buf, "   %6.4f", eval[i].exact_utility);
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
    }

    (void) sprintf (temp_buf, "\nAverage precision for first R docs retrieved:\n               ");
    if (UNDEF == add_buf_string (temp_buf, out_p))
        return;
    for (i = 0; i < num_runs; i++) {
        (void) sprintf (temp_buf, "   %6.4f", eval[i].av_R_precis);
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
    }

    (void) sprintf (temp_buf, "\nFallout - Recall Averages (recall after X nonrel docs retrieved):");
    if (UNDEF == add_buf_string (temp_buf, out_p))
        return;
    for (j = 0; j < NUM_FR_PTS; j++) {
        (void) sprintf (temp_buf, "\n    At %3ld docs:",
                        (long) (MAX_FALL_RET * j) / (NUM_FR_PTS - 1));
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
        for (i = 0; i < num_runs; i++) {
            (void) sprintf (temp_buf, "   %6.4f", eval[i].fall_recall[j]);
            if (UNDEF == add_buf_string (temp_buf, out_p))
                return;
        }
    }
    (void) sprintf (temp_buf, "\nAverage recall for first %d nonrel docs retrieved:\n                ", MAX_FALL_RET);
    if (UNDEF == add_buf_string (temp_buf, out_p))
        return;
    for (i = 0; i < num_runs; i++) {
        (void) sprintf (temp_buf, "   %6.4f", eval[i].av_fall_recall);
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
    }

    (void) sprintf (temp_buf, "\n\n----------------------------------------------------------------\nThe following measures are interpolated versions of measures above.\nFor the following, interpolated_prec(X) == MAX (prec(Y)) for all Y >= X\nAll these measures are experimental\n");
    if (UNDEF == add_buf_string (temp_buf, out_p))
        return;

    /* Print average recall precision and percentage improvement */
    (void) sprintf (temp_buf,
                   "\nAverage interpolated precision over all rel docs\n                ");
    if (UNDEF == add_buf_string (temp_buf, out_p))
        return;
    for (i = 0; i < num_runs; i++) {
        (void) sprintf (temp_buf, "  %6.4f ", eval[i].int_av_recall_precis);
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
    }
    if (num_runs > 1) {
        (void) sprintf (temp_buf, "\n    %% Change:           ");
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
        for (i = 1; i < num_runs; i++) {
            (void) sprintf (temp_buf, "  %6.1f ",
                            ((eval[i].int_av_recall_precis /
                              eval[0].int_av_recall_precis)
                             - 1.0) * 100.0);
            if (UNDEF == add_buf_string (temp_buf, out_p))
                return;
        }
    }

    (void) sprintf (temp_buf, "\nR-based-interpolated-Precision:\n    Exact:     ");
    if (UNDEF == add_buf_string (temp_buf, out_p))
        return;
    for (i = 0; i < num_runs; i++) {
        (void) sprintf (temp_buf, "   %6.4f", eval[i].int_R_recall_precis);
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
    }
    for (j = 1; j < NUM_PREC_PTS; j++) {
        (void) sprintf (temp_buf, "\n    At %4.2f  R:",
                        (float) MAX_RPREC * j / (float) (NUM_PREC_PTS - 1));
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
        for (i = 0; i < num_runs; i++) {
            (void) sprintf (temp_buf, "   %6.4f", eval[i].int_R_prec_cut[j]);
            if (UNDEF == add_buf_string (temp_buf, out_p))
                return;
        }
    }

    (void) sprintf (temp_buf, "\nAverage interpolated precision for first R docs retrieved:\n               ");
    if (UNDEF == add_buf_string (temp_buf, out_p))
        return;
    for (i = 0; i < num_runs; i++) {
        (void) sprintf (temp_buf, "   %6.4f", eval[i].int_av_R_precis);
        if (UNDEF == add_buf_string (temp_buf, out_p))
            return;
    }

    if (time_flag) {
	(void) sprintf (temp_buf, "\n\n----------------------------------------------------------------\nThe following measures are time-based, and are experimental\n");
	if (UNDEF == add_buf_string (temp_buf, out_p))
	    return;
	

	(void) sprintf (temp_buf, "\nAverage (integral) Precision:                 ");
	if (UNDEF == add_buf_string (temp_buf, out_p))
	    return;
	for (i = 0; i < num_runs; i++) {
	    (void) sprintf (temp_buf, "   %6.4f", eval[i].av_time_precis);
	    if (UNDEF == add_buf_string (temp_buf, out_p))
		return;
	}
	
	(void) sprintf (temp_buf, "\nAverage (integral) Relative Precision:        ");
	if (UNDEF == add_buf_string (temp_buf, out_p))
	    return;
	for (i = 0; i < num_runs; i++) {
	    (void) sprintf (temp_buf, "   %6.4f", eval[i].av_time_relprecis);
	    if (UNDEF == add_buf_string (temp_buf, out_p))
		return;
	}
	
	(void) sprintf (temp_buf,
			"\nAverage (integral) UAP:                       ");
	if (UNDEF == add_buf_string (temp_buf, out_p))
	    return;
	for (i = 0; i < num_runs; i++) {
	    (void) sprintf (temp_buf, "   %6.4f", eval[i].av_time_uap);
	    if (UNDEF == add_buf_string (temp_buf, out_p))
	        return;
	}
	    
	(void) sprintf (temp_buf,
			"\nAverage (integral) Relative UAP:              ");
	if (UNDEF == add_buf_string (temp_buf, out_p))
	    return;
	for (i = 0; i < num_runs; i++) {
	    (void) sprintf (temp_buf, "   %6.4f", eval[i].av_time_reluap);
	    if (UNDEF == add_buf_string (temp_buf, out_p))
	        return;
	}
	    
	(void) sprintf (temp_buf,
		     "\nAverage (integral) utility (%3.1f,%3.1f,%3.1f,%3.1f):",
			utility_a, utility_b, utility_c, utility_d);
	if (UNDEF == add_buf_string (temp_buf, out_p))
	    return;
	for (i = 0; i < num_runs; i++) {
	    (void) sprintf (temp_buf, "   %6.4f", eval[i].av_time_utility);
	    if (UNDEF == add_buf_string (temp_buf, out_p))
		return;
	}
		
	(void) sprintf (temp_buf,
			"\nAverage (integral) cumulative rel:            ");
	if (UNDEF == add_buf_string (temp_buf, out_p))
	    return;
	for (i = 0; i < num_runs; i++) {
	    (void) sprintf (temp_buf, "   %6.4f", eval[i].av_time_cum_rel);
	    if (UNDEF == add_buf_string (temp_buf, out_p))
		return;
	}
		
	for (i = 0; i < num_runs; i++) {
	    /* WARNING Prints out one run at a time rather than in parallel */
	    (void) sprintf (temp_buf, "\nEvaluation measures at %ld time cutoffs over %6.4f seconds:\ncutoff num_rel num_nrel cum_rel   prec  relprec  uap  reluap utility\n", (long) NUM_TIME_PTS, (float) MAX_TIME);
	    if (UNDEF == add_buf_string (temp_buf, out_p))
		return;
	    for (j=0; j < NUM_TIME_PTS; j++) {
		(void) sprintf (temp_buf,
				"  %-4ld %6.4f  %6.4f  %6.4f  %6.4f  %6.4f  %6.4f  %6.4f  %6.4f\n",
				(long) (j * MAX_TIME / NUM_TIME_PTS),
				eval[i].time_num_rel[j],
				eval[i].time_num_nrel[j],
				eval[i].time_cum_rel[j],
				eval[i].time_precis[j],
				eval[i].time_relprecis[j],
				eval[i].time_uap[j],
				eval[i].time_reluap[j],
				eval[i].time_utility[j]);
		if (UNDEF == add_buf_string (temp_buf, out_p))
		    return;
	    }
	}
    }
    
    if (UNDEF == add_buf_string ("\n", out_p))
	return;

    if (output == NULL) {
        (void) fwrite (out_p->buf, 1, out_p->end, stdout);
        out_p->end = 0;
    }
}
