#!/usr/local/bin/python3

""" 
Terminal program to convert Trello's json-exports to markdown table format
Based on: https://github.com/phipsgabler/trello2md
"""

import sys
import argparse
import json
import re


# a url in a line (obligatory starting with the protocol part)
find_url = re.compile('(^|.* )([a-zA-Z]{3,4}://[^ ]*)(.*)$')

################################################################################
def unlines(line):
    """Remove all newlines from a string."""

    return line.translate(str.maketrans('\n', ' '))

################################################################################
def prepare_content(content):
    """Prepare nested markdown in content of a card."""
    
    result = []
    for line in content.splitlines():
        # turn urls into actual links
        match = find_url.match(line)
        if match:
           line = '{0}[{1}]({1}){2}'.format(match.group(1), match.group(2), match.group(3))

        # TBD: escape '|' character to protect table integrity.
           
        # correct heading levels (add two)
        if line.startswith('#') and line.endswith('#'):
            result.append('##{0}##'.format(unlines(line)))
        else:
            result.append(line)
    
    return '<br>'.join(result)

################################################################################
def print_card(card_id, data):
    """Print name, content and owners of a card."""

    # get card and pre-format content
    card = next(c for c in data['cards'] if c['id'] == card_id)
    content = prepare_content(card['desc'])

    # format labels
    labels = []
    if card['labels']:
        for label in card['labels']:
            label_string = '<font color="{clr}">_{lbl}_</font>'.format(
                lbl = (label['name'] or label['color']), clr = label['color'])
            labels.append(label_string)
    labels_string = ', '.join(labels)

    # format people (dereference their IDs)
    members = []
    if card['idMembers']:
        for mem_id in card['idMembers']:
            member = next(mm for mm in data['members'] if mm['id'] == mem_id)
            members.append(member['fullName'])
        members_string = ', '.join(members)
    else:
        members_string = '_Unassigned_'

    # put it together
    return '| {name} | {cntnt} | {lbls} | {mmbrs} |\n'.format(
                                          name = unlines(card['name']),
                                          cntnt = content,
                                          lbls = labels_string,
                                          mmbrs = members_string)

################################################################################
def main():
    
    parser = argparse.ArgumentParser(description = 'Convert a JSON export from Trello to Markdown.')
    parser.add_argument('inputfile', help = 'The input JSON file')
    parser.add_argument('-o', '--output', help = 'The output file to create')
    parser.add_argument('-i', '--header', help = 'Include header page',
                        action = 'store_true')
    parser.add_argument('-a', '--archived', help = 'Include archived lists',
                        action = 'store_true')
    parser.add_argument('-e', '--encoding', help = 'File encoding to te used',
                        default = 'utf8')

    args = parser.parse_args()

    # load infile to 'data'
    try:
        with open(args.inputfile, 'r', encoding = args.encoding) as inf:
            data = json.load(inf)
    except IOError as e:
        sys.exit('I/O error({0}): {1}'.format(e.errno, e.strerror))

    
    markdown = []

    # optionally, include header page
    if args.header:
        markdown.append('**Board name: {0}**\n\n'.format(data['name']))
        markdown.append('Short URL: [{0}]({0})  \n'.format(data['shortUrl']))
        markdown.append('Number of lists: {0}  \n'.format(len(data['lists'])))
        markdown.append('Number of cards in lists: {0}  \n'.format(len(data['cards'])))
        markdown.append('Last change: {0}\n\n\n'.format(data['dateLastActivity']))

    # process all lists in 'data', respecting closedness
    for lst in data['lists']:
        if not lst['closed'] or args.archived:
            # format list header
            markdown.append('# {0} #\n\n'.format(unlines(lst['name'])))
            # copy/paste of generated HTML breaks with Confluence, so don't have a proper header row
            markdown.append('|  |  |  |  |\n')
            markdown.append('| -- | ---------- | :-----: | :----: |\n')
            markdown.append('| **Feature** | **Description** | **Drivers** | **Product Manager** |\n')
            # process all cards in current list
            for card in data['cards']:
                if (not card['closed'] or args.archived) and (card['idList'] == lst['id']):
                    markdown.append(print_card(card['id'],
                                               data))
##            markdown.append('\n\n----\n\n')

    # save result to file
    if (args.output):
        outputfile = args.output
    else:
        outputfile = args.inputfile.replace('.json', '.md')
        if outputfile == args.inputfile:
            outputfile += '.md'

    try:
        with open(outputfile, 'w', encoding = args.encoding) as of:
            of.write(''.join(markdown))

        print('Sucessfully translated to "{0}"!'.format(outputfile))

    except IOError as e:
        sys.exit('I/O error({0}): {1}'.format(e.errno, e.strerror))

################################################################################
if __name__ == '__main__':
    main()

