#!/usr/bin/env python3
# script to help friend convert Juniper routes to Fortigate commands

import textwrap
import argparse
import sys
import re

def strip_cidr(cidr):
    '''
    regex to return CIDR's from juniper routes
    '''
    #return re.findall('(?:\d{1,3}\.){3}\d{1,3}(?:/\d\d?)?', cidr)
    return re.findall('[0-9]{1,3}(?:\.[0-9]{1,3}){0,3}/[0-9]+', cidr)

def get_cidrs_from_file(cidrfile):
    with open(cidrfile) as cidr_file:
        return strip_cidr(cidr_file.read())

def set_dst(cidrlist, variable):
    '''
    iterates the CIDR's stripped out from the Juniper file
    and creates the Fortigate commands for each new device
    including the variable declared via command line
    returns commands that should be written to the outfile
    '''
    cidr_list = cidrlist
    cidr_out = ''

    for cidr in cidr_list:
        cidr_out += textwrap.dedent('''
                Edit 0
                Set dst {0}
                Set device {1}
                Next
                ''').format(cidr, variable)
        
    return cidr_out

def write_dst_to_file(outfile, juniper_syntax):
    with open(outfile, 'w') as dst_file:
        dst_file.write(juniper_syntax)

def main(infile, outfile, variable):
    cidr_list = get_cidrs_from_file(infile)
    juniper_syntax = set_dst(cidr_list, variable)
    write_dst_to_file(outfile, juniper_syntax)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This script will parse CIDR\'s from a file and convert to juniper syntax.')
    parser.add_argument('-i', '--input', help='Input file to parse out cidrs', required=True)
    parser.add_argument('-o', '--output', help='Output file to Edit 0 Set dst...', required=True)
    parser.add_argument('-v', '--variable', help='Set device to this argument', required=True)
    args = parser.parse_args()

    main(args.input, args.output, args.variable)
