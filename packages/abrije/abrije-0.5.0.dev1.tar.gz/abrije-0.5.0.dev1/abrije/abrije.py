#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
abrije
======

abrije is a generic log parser and summariser.


Working from a directory tree, the
A list of globs and regexes

list of globs. Used to locate input files.

Each glob is used by ``abrije`` to build a list of input files to parse.

list of regexes. Used to provide metadata and tell abrije how to parse the file.
The path of each input file is tested against each regex for a match. Upon
finding a match (i.e. the first matching regex is used), the named groups
within the regex are used as follows:
label, labelXXXX, or label_XXXX = used for grouping log files
type, typeXXXX, or type_XXXX = used for specifying log type, former group content gives type, otherwise use XXXX
tag, tagXXXX, or tag_XXXX = used to tag log data in heading, former tags with 'tagged', otherwise tag with XXXX
detail, detailXXXX or detail_XXXX
first underscore before XXXX ignored
labelXXXX__YYYY YYYY used as content instead of group_contents

provide ``abrije`` with key data about the file
# provide list of regex
#  how to match regex to file? simplest would be to use first regex that matches
# regex has named groups
#  label or label_x -> used to match data to a line
#  type or type_xxx
#    if group name is type, group match gives type_name
#    otherwise, group name gives is type_name(xxx); actual match ignored, allows regex definition to define type, as filename may not have discernable type
#    used to define the parser, will call type_parse(file)
#    expected to return a dict containing headings>data
#  tag_xxxx
#   tags headings with xxxx (group match value ignored)
#  other groups tag headings with groupname=value
#

 path of each input file is tested against each regex for a match.


plugins can use logger 'abrije'
"""


###
# smart parse files
# provide list of files
# provide list of regex
#  how to match regex to file? simplest would be to use first regex that matches
# regex has named groups
#  label or label_x -> used to match data to a line
#  type or type_xxx
#    if group name is type, group match gives type_name
#    otherwise, group name gives is type_name(xxx); actual match ignored, allows regex definition to define type, as filename may not have discernable type
#    used to define the parser, will call type_parse(file)
#    expected to return a dict containing headings>data
#  tag_xxxx
#   tags headings with xxxx (group match value ignored)
#  other groups tag headings with groupname=value
#

import csv
import re
import pathlib
import glob
from collections import defaultdict,OrderedDict
import importlib
import argparse
import sys
import logging
import pprint
import traceback
import os

# not currently used
# dict which allows access using dot
# https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary
class AttributeDict(defaultdict):
    def __init__(self):
        super(AttributeDict, self).__init__(AttributeDict)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value

# parsers should take a single parameter which is the input file object
# and return an OrderedDict of columns:values

# build-in parsers

# csv where first line is heading
# second line is row of values, only first value row used
# whitespace is stripped
def csv_firstrow_parse(infile,delimiter = ','):
    reader = csv.DictReader(infile, delimiter=delimiter)
    read_data_dict = OrderedDict()
    for row in reader:
        break # only first row of interest
    for key in row.keys():
        # create a new dict, stripping whitespace
        read_data_dict[key.strip()] = row[key].strip()
    return read_data_dict

# csv with:
# heading1, value1
# heading2, value2
# ...
# whitespace is stripped
def csv_rows_parse(infile,delimiter = ','):
    reader = csv.reader(infile, delimiter=delimiter)
    read_data_dict = OrderedDict()
    for row in reader:
        if len(row)>0:
            heading,item = row
            read_data_dict[heading.strip()] = item.strip()
    return read_data_dict

# as above but tsv
def tsv_firstrow_parse(infile):
    return csv_firstrow_parse(infile,'\t')

# as above but tsv
def tsv_rows_parse(infile):
    return csv_rows_parse(infile,'\t')

# parser for umi_tools dedup.log
# umi_tools dedup.log, interested in the following lines:
# ...various lines
# 2018-09-26 00:04:11,626 INFO Reads: Input Reads: 7068280, Single end unmapped: 81625
    # start parsing here
# 2018-09-26 00:04:11,627 INFO Number of reads out: 5388284
    # parse all info lines for heading: value (findall)
# 2018-09-26 00:04:11,627 INFO Total number of positions deduplicated: 2478039
# 2018-09-26 00:04:11,627 INFO Mean number of unique UMIs per position: 2.17
# 2018-09-26 00:04:11,627 INFO Max. number of unique UMIs per position: 2904
# job finished in 564 seconds at Wed Sep 26 00:04:11 2018 -- 562.90  6.03  0.00  0.00 -- 3fba981a-1f17-4401-b63a-ea3e22049358
    # eof
def umi_tools_dedup_parse(infile):
    output_dict = OrderedDict()
    info_line_re = re.compile('[0-9\-:, ]+ INFO (.*)')
    start_parsing_re = re.compile('Reads: ')
    data_entry_re = re.compile('(?P<heading>[^\:]+): (?P<value>[0-9.]+)')
    parsing = False
    for line in infile:
        match = info_line_re.match(line)
        if not match: continue # if no replacement, line is not an INFO line
        line_details = match.group(1)
        if not parsing and start_parsing_re.search(line_details): parsing = True
        if parsing:
            for match in data_entry_re.finditer(line_details):
                heading = match.group('heading').strip(' ,')
                value = match.group('value')
                output_dict[heading] = value
    return output_dict

"""
Function for parsing hisat2 summary files, for use by abrije.
"""
def hisat2_summary_parse(infile):
    output_dict = OrderedDict()
    for line in infile:
        the_re = re.search('\W*(.+): ([0-9.%]*)[ (]*([0-9.%]*)',line)
        if the_re:
            #print (the_re.groups())
            heading = the_re.group(1)
            output_dict[heading] = the_re.group(2)
            group_3 = the_re.group(3)
            if group_3!='': output_dict[heading+' percent'] = group_3
    return output_dict

# INITIALISATION
# parameter parsing and building input file list

_PROGRAM_NAME = 'abrije'
_PROGRAM_VERSION = '0.5'

def main():
    parser = argparse.ArgumentParser(prog=_PROGRAM_NAME,
        description='abrije is a generic log parser and summariser.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--version', action='version', version='{} {}'.format(_PROGRAM_NAME,_PROGRAM_VERSION))
    parser.add_argument('-v','--verbose', action='count',
                        help='increase verbose (v=info, vv=debug)')
    parser.add_argument('-g','--glob', action='store', nargs='+', required=True,
                        help='globs to use to find input files, stored internally as posix paths')
    parser.add_argument('-r','--regex', action='store', nargs='+', required=True,
                        help='regexes to use to process input files')
    parser.add_argument('-o','--output', action='store',
                        help='output filename, will not replace unless -f specified; stdout if not given')
    parser.add_argument('-p','--parser', action='store', nargs='+',
                        help='import parsers defined in PARSER.py')
    parser.add_argument('-f','--force', action='store_true',
                        help='force overwriting of OUTPUT')
    parser.add_argument('--navalue', action='store', default='',
                        help='value to write where no data present')
    parser.add_argument('--in_encoding', action='store', default='utf-8',
                        help='encoding used for opening input files')
    parser.add_argument('--out_encoding', action='store', default='utf-8',
                        help='encoding used for writing output file (for Excel, use "utf-8_sig")')
    parser.add_argument('--shorterfirst', action='store_true',
                        help='sort so shorter label subsets sorted first (e.g. A1>B1, A1>B1>C1, A1>B2, A1>B2>C1...); '
                        'default is longer first (e.g. A1>B1>C1, A1>B1, A1>B2>C1, A1>B2, ...)')
    args = parser.parse_args()

    # logging, create a stderr and stdout handler
    logger = logging.getLogger(_PROGRAM_NAME) # script logger
    logger.setLevel(logging.DEBUG) # top-level logs everything

    stderr_handler = logging.StreamHandler(sys.stderr)
    logger.addHandler(stderr_handler)
    stderr_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stderr_handler.setFormatter(stderr_formatter)
    stderr_handler.setLevel(logging.WARNING)

    stdout_handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(stdout_handler)
    stdout_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stdout_handler.setFormatter(stdout_formatter)
    stdout_handler.setLevel(logging.CRITICAL)

    # verbosity controls output to stdout handler
    if not args.verbose: args.verbose = 0 # if not set defaults to None
    _DEBUG = False
    if args.verbose>=2:
        stdout_handler.setLevel(logging.DEBUG)
        _DEBUG = True
            # if verbosity is debug, traceback of handled exceptions will be output as logger.error
    elif args.verbose>=1:
        stdout_handler.setLevel(logging.INFO)

    # pretty formatter, wrap in object so not called unless needed
    pformat = pprint.PrettyPrinter(indent=2,  width=120).pformat
    class PrettyLog():
        def __init__(self, obj):
            self.obj = obj
        def __repr__(self):
            #if isinstance(self.obj,OrderedDict):
                # special handling for OrderedDict, as not handled by pformat by default
            #    return pformat([(key,value) for (key,value) in self.obj.items()])
            # pprint SEEMS to work in Python 3.6
            return pformat(self.obj)

    logger.info('Input glob:')
    logger.info(PrettyLog(args.glob))
    logger.info('Input regex:')
    logger.info(PrettyLog(args.regex))
    output_filename = args.output # None -> write to stdout
    overwrite_output = args.force
    logger.info('Output file: {}'.format(output_filename))
    sort_shorter_first = args.shorterfirst
    logger.info('Sort shorter first? {}'.format(sort_shorter_first))
    na_value = args.navalue
    logger.info('NA value: {}'.format(na_value))
    input_encoding = args.in_encoding
    logger.info('Input encoding: {}'.format(input_encoding))
    output_encoding = args.out_encoding
    logger.info('Output encoding: {}'.format(output_encoding))


    def check_output_exists(): # reused just before writing
        if output_filename:
            if os.path.isfile(output_filename) and not overwrite_output:
                logger.error('Output file exists, delete or use -f')
                sys.exit(1)
    check_output_exists()

    # create list of input_files
    # file list is sorted within a glob, but files from each glob added in order given
    logger.debug('Globbing input globs:')
    input_files = []
    for the_glob in args.glob:
        logger.debug(' Globbing {}'.format(the_glob))
        new_files = sorted([pathlib.PurePath(path).as_posix() for path in glob.glob(the_glob)])
            # convert to posix to ensure consistent regex matching
        logger.debug('  Globbed the following files:')
        logger.info(PrettyLog(new_files))
        input_files.extend(new_files)

    logger.info('Obtained list of input files:')
    logger.info(PrettyLog(input_files))

    # pre-compile regexes
    # main reason for doing so is to error-check the supplied regexes
    input_regexes = []
    for arg_regex in args.regex:
        try:
            input_regex = re.compile(arg_regex)
            input_regexes.append(input_regex)
        except re.error as error:
            logger.error('Error in input regex "{}": {}'.format(arg_regex,error))
            if _DEBUG: logger.error(traceback.format_exc())
            sys.exit(1)

    # import any specified parsers
    parser_modules = []
    if args.parser:
        for arg_parser in args.parser:
            logger.debug('Importing parser module "{}"'.format(arg_parser))
            try:
                the_module = importlib.__import__(arg_parser)
            except Exception as error:
                logger.error('Could not import module "{}": {}'.format(arg_parser,error))
                if _DEBUG: logger.error(traceback.format_exc())
                sys.exit(1)
            parser_modules.append(the_module)

    # PROCESSING
    # main algorithm

    # to get a clean pythonic name of a string
    # https://stackoverflow.com/questions/3303312/how-do-i-convert-a-string-to-a-valid-variable-name-in-python
    clean_name = lambda varStr: re.sub('\W|^(?=\d)','_', varStr)

    # maintain set of all headings, maintain set as OrderedDict to preserve order
    all_label_headings = OrderedDict()
    all_label_headings['full_label'] = True
    all_other_headings = OrderedDict()

    # regex to match group names
    groupname_re = re.compile('(?P<prefix>label|type|tag|detail)(?:_|)(?P<suffix>.*)')

    # for storing rows of data
    rows = OrderedDict()

    # 1. iterate list of files
    logger.info('Iterating input files...')
    for input_file in input_files:
        logger.debug('Processing file "{}"'.format(input_file))
        # 2. find first regex that matches, else exception
        found_match = False
        for input_regex in input_regexes:
            logger.debug(' Testing against regex "{}"'.format(input_regex.pattern))
            the_match = input_regex.match(input_file)
            if the_match:
                logger.debug('  Matched regex.')
                # 3. processed named groups from regex
                groupdict = the_match.groupdict()
                label_dict = {}
                input_type = None
                tag_list = []
                detail_dict = OrderedDict()

                for key in groupdict.keys():
                    groupname_match = groupname_re.match(key)
                    if groupname_match:
                        groupname_prefix = groupname_match.group('prefix')
                        groupname_suffix = groupname_match.group('suffix')
                        groupname_full = groupname_match.group(0)
                        group_provided_contents = None
                        # if '__' in suffix, this means contents provided in group name
                        if '__' in groupname_suffix:
                            groupname_suffix,group_provided_contents = groupname_suffix.rsplit('__',1)
                            groupname_full = groupname_full.rsplit('__',1)[0]
                        group_actual_contents = groupdict[key]
                        logger.debug('   Processing regex group {}, fullname:{}. prefix:{}, suffix:{}, provided contents:{}, contents:{}'.format(
                            key,groupname_full,groupname_prefix,groupname_suffix,group_provided_contents,group_actual_contents))
                        if group_actual_contents is None:
                            logger.debug('    Contents is None, group did not capture. Ignoring.')
                                # only use groups that have actually captured
                            continue
                        if group_provided_contents:
                            group_contents = group_provided_contents # use provided contents if any
                        else:
                            group_contents = group_actual_contents # otherwise use actual
                        if groupname_prefix=='label':
                            # this is a 'label' group
                            # this is used to combine data from different input files into columns
                            label_dict[groupname_full] = group_contents # use full group name as heading, and contents as label
                            logger.info('   Found label "{}" content "{}"'.format(groupname_full, group_contents))
                        elif groupname_prefix=='type':
                            # this is a 'type' group
                            # this is used to determine how to parse input file
                            if input_type:
                                logger.warning('Previous detected input type "{}" is being replaced - is this the intention?'.format(input_type))
                            input_type = None
                            input_specified_encoding = None # reset
                            if group_provided_contents: # if provided contents, parse as additional info
                                # format: xxx_IS_aaa_b_AND_yyy_IS_ccc
                                # currently only encodingISxxx supported
                                logger.debug('   Parsing all input additional info "{}"'.format(group_provided_contents))
                                type_infos = group_provided_contents.split("_AND_")
                                for type_info in type_infos:
                                    logger.debug('    Parsing input additional info part "{}"'.format(type_info))
                                    tokens = type_info.split("_IS_")
                                    if len(tokens)!=2:
                                        logger.warning('Malformed additional info part, expected format xxx_IS_aaa_b_AND_yyy_IS_ccc.')
                                    else:
                                        type_info_name,type_info_value = tokens
                                        if type_info_name=="encoding":
                                            input_specified_encoding = type_info_value
                                            logger.debug('    Read type encoding "{}":"{}"'.format(type_info_name,input_specified_encoding))
                                        else:
                                            logger.warning('Ignoring unknown type info "{}":"{}"'.format(type_info_name,type_info_value))
                            if groupname_suffix: # if group name suffix present, use as input_type
                                input_type = groupname_suffix
                            else:
                                input_type = group_contents # otherwise use group content
                            logger.info('   Found input type "{}"'.format(input_type))
                        elif groupname_prefix=='tag':
                            # this is a 'tag' group
                            # tags are appended to data column headings
                            # groupname_suffix used as tag_name, and content used as tag_content
                            # if both non-empty, format as tag_name:tag_content
                            # otherwise just use tag_name or tag_content
                            # based on this logic groupname 'tag' will tag with group contents alone
                            # groupname 'tag___xxx' will tag with xxx alone
                            if groupname_suffix and group_contents:
                                tag_value = '{}={}'.format(groupname_suffix,group_contents)
                            else:
                                tag_value = '{}{}'.format(groupname_suffix,group_contents)
                                    # if either is empty, it simply won't be added!
                            if not tag_value: logger.warning('Obtained an empty tag, ignoring. Tag requires tag_name and/or content.')
                            else:
                                tag_list.append(tag_value)
                                logger.info('   Found tag "{}"'.format(tag_value))
                        elif groupname_prefix=='detail':
                            # this is a 'detail' group
                            # detail are columns prepended output columns
                            # groupname_suffix is detail column name ('detail' if missing)
                            # contents is detail column value (may be empty)
                            # detail columns are also tagged
                            # NB: Order of columns is not necessarily maintained,
                            #     since there is a common set of columns for all files,
                            #     tagging detail columns can help maintain order
                            detail_colname = groupname_suffix if groupname_suffix else 'detail'
                            if detail_colname in detail_dict:
                                logger.warning('Detail column "{}" is being replaced. Each detail column should have a unique name.'.format(detail_colname))
                            detail_dict[detail_colname] = group_contents
                            logger.info('   Found detail column "{}"->"{}"'.format(detail_colname,group_contents))
                        else:
                            # shouldn't get here, all possible named groups processed above
                            raise AssertionError('Unexpected flow when parsing a named group')
                    else:
                        logger.warning('Named group "{}" is ignored as it is not in correct format.'.format(key))
                # finished for loop for named regex groups
                # now prepare output for input file

                # 'label' values are used to match output by common 'labels'
                # ensure labels are sorted by names so that we have deterministic ordering
                label_ordereddict = OrderedDict([(key,label_dict[key]) for key in sorted(label_dict.keys())])
                    # sorting ensures we can order by headings
                if len(label_ordereddict)==0:
                    logger.error('No label parsed for "{}". Ensure at least one "label" named group is present in regex'.format(input_file))
                    sys.exit(1)
                all_label_headings.update(label_ordereddict)  # add label headings to set of all label headings
                full_label = '>'.join(label_ordereddict.values())
                logger.info(' From label headings "{}", full label is "{}"'.format('>'.join(label_ordereddict.keys()),full_label))
                # 'type' determines parsing function
                if not input_type:
                    logger.error('No type parsed for {}, ensure named group "type" is present in regex'.format(input_file))
                    sys.exit(1)

                input_parser_name = clean_name(input_type+'_parse') # convert to pythonic name
                logger.info(' File type is "{}", parser name is "{}"'.format(input_type,input_parser_name))
                # locate the parsing function
                input_parser_func = None
                if input_parser_name in globals():
                    input_parser_func =  globals()[input_parser_name]
                else:
                    for parser_module in parser_modules:
                        if input_parser_name in parser_module.__dict__:
                            input_parser_func =  parser_module.__dict__[input_parser_name]
                            break
                if input_parser_func is None:
                    logger.error('Could not find parsing function "{}" as built-in function or in parser modules.'.format(input_parser_name))
                    sys.exit(1)

                # details
                logger.debug(' Obtained these details to include:')
                logger.debug(PrettyLog(detail_dict))

                # 4. open file and parse
                # to parse, call input_parser_func(infile), return OrderedDict headings>data
                try:
                    if not input_specified_encoding: input_specified_encoding = input_encoding # default to script option
                    logger.info(' Parsing input file "{}" as "{}"'.format(input_file,input_specified_encoding))
                    if input_specified_encoding == 'binary':
                        open_params = {'mode': 'rb'}
                    else:
                        open_params = {'mode':'r', 'encoding':input_specified_encoding}
                    with open(input_file, **open_params) as infile:
                        read_data_dict = input_parser_func(infile)
                        if not isinstance(read_data_dict , OrderedDict):
                            logger.error('Parsing function "{}" did not return an OrderedDict as expected'.format(input_parser_name))
                            sys.exit(1)
                        logger.debug(' Parsed file, obtained these data:')
                        logger.debug(PrettyLog(read_data_dict))
                except (OSError, FileNotFoundError) as error:
                    logger.error('Could not read file "{}"'.format(input_file))
                    if _DEBUG: logger.error(traceback.format_exc())
                    sys.exit(1)

                # create a dict with all relevant data for file
                all_file_data_dict = OrderedDict()
                all_file_data_dict['filename'] = input_file
                    # add filename to top of data for file

                all_file_data_dict.update(detail_dict) # add details from regexes
                all_file_data_dict.update(read_data_dict) # add read data

                # 5. create an OrderedDict for full processed output
                full_output_dict = OrderedDict()
                # add labels to output
                full_output_dict['full_label'] = full_label
                full_output_dict.update(label_ordereddict)

                # add data from input file to output
                # remembering to add any relevant tags
                heading_tags_str = ', '.join(tag_list) # create combined tags
                logger.debug(' Heading tags: {}'.format(heading_tags_str))

                # add tags to file data
                tagged_all_file_data_dict = \
                    OrderedDict([('{} > {}'.format(heading_tags_str,key),
                                  value) for (key,value) in all_file_data_dict.items()
                                ])

                # add tagged read data to full output
                full_output_dict.update(tagged_all_file_data_dict)
                # update set of all non-label headings
                all_other_headings.update(tagged_all_file_data_dict)

                #logger.debug(' Tagged data for output:')
                #logger.debug(PrettyLog(tagged_all_file_data_dict))

                logger.debug(' Full data for output:')
                logger.debug(PrettyLog(full_output_dict))
                #logger.debug(PrettyLog(all_label_headings))
                #logger.debug(PrettyLog(all_other_headings))

                # 6. combine current output to a previous row if they have matching full_label
                if full_label in rows: # already have a row with full_label
                    logger.info(' Combining data with previous for row "{}"'.format(full_label))
                    row = rows[full_label]
                    # don't use update as we want to check for duplicates rather than silently replace
                    for (key,value) in full_output_dict.items():
                        if key in row and row[key]!=full_output_dict[key]:
                            # if duplicate heading, and different value, show warning
                            logger.warning('Column "{}" already exists for row "{}", not replacing'.format(key,full_label))
                        else:
                            row[key] = full_output_dict[key]
                else: # just make a new row
                    logger.info(' Data is for new row "{}"'.format(full_label))
                    rows[full_label] = full_output_dict

                logger.debug(' Current full row for output:')
                logger.debug(PrettyLog(rows[full_label]))

                found_match = True
                break # only look for first match
            # END if the_match:
        # END for input_regex in input_regexes:
        if not found_match:
            logger.error('Input file "{}" didn\'t match any regex!'.format(input_file))
            sys.exit(1)

    logger.debug('Full output rows:')
    logger.debug(PrettyLog(rows))

    # 7. Write as csv

    #      Determine all headings
    all_headings = list(all_label_headings.keys()) + list(all_other_headings.keys())
    logger.debug('Full column list (total {}):'.format(len(all_headings)))
    logger.debug(PrettyLog(all_headings))

    #      Sort full_label,label_1,label_2,original order
    if sort_shorter_first:
        sorted_rownames = sorted(rows.keys()) # default string sorting
    else:
        sorted_rownames = sorted(rows.keys(),key=lambda string: string+"?")
        # ? is after '>' in char table, so this ensures shorter labels are sorted
        # after longer labels
    logger.debug('Sorted rows (total {}):'.format(len(sorted_rownames)))
    logger.debug(PrettyLog(sorted_rownames))

    #      Write rows, blank if no data for heading (handled by DictWriter)
    logger.info('Writing output file "{}" as "{}"'.format(output_filename,output_encoding))
    check_output_exists()
    try:
        csvfile = open(output_filename, 'w', newline='', encoding=output_encoding) if output_filename else sys.stdout
        csv_writer = csv.DictWriter(csvfile, restval=na_value, delimiter='\t', fieldnames = all_headings)
        logger.debug(' Writing header, total {} columns'.format(len(all_headings)))
        csv_writer.writeheader()
        for full_label in sorted_rownames:
            data = rows[full_label]
            logger.debug(' Writing row "{}", total {} valid values'.format(full_label,len(data)))
            csv_writer.writerow(data)
        if csvfile is not sys.stdout:
            csvfile.close()
    except (OSError, FileNotFoundError) as error:
        logger.error('Could not write to file "{}"'.format(output_filename))
        if _DEBUG: logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    main()
