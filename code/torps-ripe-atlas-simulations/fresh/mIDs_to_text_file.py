import sys
import ast



'''
Usage:
    python progname list_of_mID_files_as_CL_args_variable_number
    stdout: measurement IDs separated by newlines

Citation: http://stackoverflow.com/questions/988228/converting-a-string-to-dictionary
'''




def main():
    for fname in sys.argv[1:]:
        with open(fname, 'rb') as f:
            for line in f:
                if 'measurements' in line and 'error' not in line:
                    line_str = line.rstrip()
                    
                    # Convert to dictionary
                    the_d = ast.literal_eval(line_str)
                    for key in the_d:
                        as_list = the_d[key]
                        for asn in as_list:
                            print asn


if __name__ == '__main__':
    main()
