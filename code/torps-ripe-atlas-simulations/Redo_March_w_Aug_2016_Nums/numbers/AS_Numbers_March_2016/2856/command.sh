#!/bin/bash


# 8888 ##########
python ../../../../fresh/numbers/number_of_compromised_streams_per_sample.py \
    ../../../intersections/AS_Analysis_March_2016/8888/compromises_1guard_100K_2856.pickle \
    > 8888_comp_streams_2856.txt

python ../../../../fresh/numbers/time_to_first_compromise_per_sample_only_for_comp.py \
    ../../../intersections/AS_Analysis_March_2016/8888/compromises_1guard_100K_2856.pickle \
    > 8888_time_first_comp_2856.txt

python ../../../../fresh/numbers/popular_ASes_or_IXPs.py \
    ../../../intersections/AS_Analysis_March_2016/8888/compromises_1guard_100K_2856.pickle \
    > 8888_culprits_2856.txt


# ddptr ##########
python ../../../../fresh/numbers/number_of_compromised_streams_per_sample.py \
    ../../../intersections/AS_Analysis_March_2016/ddptr/compromises_1guard_100K_2856.pickle \
    > ddptr_comp_streams_2856.txt

python ../../../../fresh/numbers/time_to_first_compromise_per_sample_only_for_comp.py \
    ../../../intersections/AS_Analysis_March_2016/ddptr/compromises_1guard_100K_2856.pickle \
    > ddptr_time_first_comp_2856.txt

python ../../../../fresh/numbers/popular_ASes_or_IXPs.py \
    ../../../intersections/AS_Analysis_March_2016/ddptr/compromises_1guard_100K_2856.pickle \
    > ddptr_culprits_2856.txt

# isps ##########
python ../../../../fresh/numbers/number_of_compromised_streams_per_sample.py \
    ../../../intersections/AS_Analysis_March_2016/isps/compromises_1guard_100K_2856.pickle \
    > isps_comp_streams_2856.txt

python ../../../../fresh/numbers/time_to_first_compromise_per_sample_only_for_comp.py \
    ../../../intersections/AS_Analysis_March_2016/isps/compromises_1guard_100K_2856.pickle \
    > isps_time_first_comp_2856.txt

python ../../../../fresh/numbers/popular_ASes_or_IXPs.py \
    ../../../intersections/AS_Analysis_March_2016/isps/compromises_1guard_100K_2856.pickle \
    > isps_culprits_2856.txt


# status_quo ##########
python ../../../../fresh/numbers/number_of_compromised_streams_per_sample.py \
    ../../../intersections/AS_Analysis_March_2016/status_quo/compromises_1guard_100K_2856.pickle \
    > status_quo_comp_streams_2856.txt

python ../../../../fresh/numbers/time_to_first_compromise_per_sample_only_for_comp.py \
    ../../../intersections/AS_Analysis_March_2016/status_quo/compromises_1guard_100K_2856.pickle \
    > status_quo_time_first_comp_2856.txt

python ../../../../fresh/numbers/popular_ASes_or_IXPs.py \
    ../../../intersections/AS_Analysis_March_2016/status_quo/compromises_1guard_100K_2856.pickle \
    > status_quo_culprits_2856.txt
