#!/usr/bin/env python
"""waterworks.py
   Run a chip-seq pipeline, with output in the current directory.
   Place the raw reads at *.treat and *.control

"""

#  Current Version: 0.0
#  Last Modified: 2011-07-22 16:52

# --- imports ---
from ruffus import follows, files

from hts_waterworks.utils.ruffus_utils import (ruffus_main, ruffus_opt_parser,
                                               touch)
import hts_waterworks.preprocessing as preprocessing
import hts_waterworks.mapping as mapping
import hts_waterworks.call_peaks as call_peaks
import hts_waterworks.visualize as visualize
import hts_waterworks.annotation as annotation
import hts_waterworks.pas_seq as pas_seq
import hts_waterworks.motif_discovery as motif_discovery


# --- Current Pipeline dependencies ---
# Bowtie
# MEME (+ mpich2 if parallel desired)
# NestedMICA
# pygr (+ pyrex)
# scipy
# numpy
# motility
# ruffus
# bedtools
# matplotlib
# fastx toolkit (gnuplot)

@follows(preprocessing.final_output, preprocessing.read_length_histogram,
         preprocessing.quality_boxplot, preprocessing.quality_nuc_dist)
def preprocess():
    """preprocessing/filtering steps complete"""
    pass


@follows(*mapping.all_mappers_output)
def map_reads():
    """read mapping steps complete"""
    pass


@follows(*call_peaks.all_peak_caller_functions)
def peak_calling():
    """peak calling steps complete"""
    pass


# visualization
@follows(visualize.deploy_track_files)
def visualization():
    """visualization steps complete"""
    pass


@follows(annotation.gene_overlap, annotation.gene_ontology,
         annotation.find_nearby_genes, annotation.draw_expression_ks)
def expression():
    """expression/annotation steps complete"""
    pass


@follows(motif_discovery.motif_enrichment_genomic,
         motif_discovery.motif_enrichment_control,
         motif_discovery.consensus_enrichment,
         motif_discovery.motif_presence_sorted_peaks)
def motifs():
    """motif discovery complete"""
    pass


@follows(preprocess, map_reads, peak_calling, visualization, expression, motifs)
@files(None, 'all_complete.ready')
def all_complete(_, out_sentinel):
    """HTS workflow complete"""
    touch(out_sentinel)


# --- main ---
if __name__ == '__main__':
    parser = ruffus_opt_parser()
    opts, args = parser.parse_args()
    ruffus_main(opts, args)
