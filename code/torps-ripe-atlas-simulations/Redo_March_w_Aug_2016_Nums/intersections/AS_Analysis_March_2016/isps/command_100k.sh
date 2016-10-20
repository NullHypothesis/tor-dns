#!/bin/bash

python intersect_isps.py ../../../traceroutes/clients_to_all_guards_forward/results/clients_to_all_guards_forward_dict.pickle compromises_1guard_100K_7922 7922 \
    ../../../../fresh/forPyASN/ipasn_20160729.dat < ../../torps_typical_my_final_model_1_guard_100000_samples.txt > output_dict_1guard_100K_7922.txt

python intersect_isps.py ../../../traceroutes/clients_to_all_guards_forward/results/clients_to_all_guards_forward_dict.pickle compromises_1guard_100K_42610 42610 \
    ../../../../fresh/forPyASN/ipasn_20160729.dat < ../../torps_typical_my_final_model_1_guard_100000_samples.txt > output_dict_1guard_100K_42610.txt

python intersect_isps.py ../../../traceroutes/clients_to_all_guards_forward/results/clients_to_all_guards_forward_dict.pickle compromises_1guard_100K_3320 3320 \
    ../../../../fresh/forPyASN/ipasn_20160729.dat < ../../torps_typical_my_final_model_1_guard_100000_samples.txt > output_dict_1guard_100K_3320.txt

python intersect_isps.py ../../../traceroutes/clients_to_all_guards_forward/results/clients_to_all_guards_forward_dict.pickle compromises_1guard_100K_3215 3215 \
    ../../../../fresh/forPyASN/ipasn_20160729.dat < ../../torps_typical_my_final_model_1_guard_100000_samples.txt > output_dict_1guard_100K_3215.txt

python intersect_isps.py ../../../traceroutes/clients_to_all_guards_forward/results/clients_to_all_guards_forward_dict.pickle compromises_1guard_100K_2856 2856 \
    ../../../../fresh/forPyASN/ipasn_20160729.dat < ../../torps_typical_my_final_model_1_guard_100000_samples.txt > output_dict_1guard_100K_2856.txt
