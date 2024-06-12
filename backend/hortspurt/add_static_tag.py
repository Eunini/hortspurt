"""
    This script adds static tag to url(), href, src, and poster html attributes
    Makes HTML file a valid Django template
    CLI Args:
        initialfile (str): file name that contains the code to be edited
        editedfile (str): The edited code is written into this file
        If CLI arguments aren't specified;
            initialfile defaults to inputfile.html
            editedfile defaults to outputfile.html
"""

import sys


try:
    initialfile = sys.argv[1]
except IndexError:
    initialfile = 'inputfile.html'

try:
    editedfile = sys.argv[2]
except IndexError:
    editedfile = 'outputfile.html'

try:
    # Opens input file
    file1 = open(initialfile, "r", encoding="utf8")
except (OSError, FileNotFoundError):
    print('could not open/read file ', initialfile, ' exiting now')
    exit()
try:
    # Opens output file
    file2 = open(editedfile, "w", encoding="utf8")
except (OSError, FileNotFoundError):
    print('could not open/read file ', editedfile, ' exiting now')
    exit()


# Reads all lines in initial file
#html_file = file1.readlines()
line_no = 0
# loops through all line of html in initial line
while True:
    line_no += 1
    line = file1.readline()
    # Breaks the loop and ends the script if all lines in the input file
    # have been read
    if not line:
        break
    joined_line = line
    try:
        # Checks for url() reference
        if 'url(' in line and not ('http' in line or 'www' in line):
            # path_idx is the beginning of the url path
            path_idx = line.index('url(') + 4
            # path_end_idx is the end of the url path + 1
            path_end_idx = line.index(')')
            # Add static tag to the url path
            joined_line = line[:path_idx] + "{% static \'" + line[path_idx:path_end_idx] + "\' %}" + line[path_end_idx:]

        if 'src=' in line or 'href=' in line or 'poster=' in line:
            # skips href, src and poster attributes that reference files on the web
            # also skips lines already containing a django tag
            if 'http' in line or 'www' in line or '{%' in line:
                file2.write(joined_line)
                continue
            # splits the line by an '=' sign
            split_line = line.split('=')
            # loops through each part of the split line
            for i in range(len(split_line)):
                # finds piece of the split line containing src, href or poster attributes
                # and edit the next piece of the split line because it contains
                # the static file reference
                if 'src' in split_line[i] or 'href' in split_line[i] or 'poster' in split_line[i]:
                    # skips if src, href or poster is part of a path and not an
                    # attribute
                    if '/src' in split_line[i] or '/href' in split_line[i] or '/poster' in split_line[
                            i] or 'src/' in split_line[i] or 'href/' in split_line[i] or 'poster/' in split_line[i]:
                        continue
                    # print(split_line)
                    # checks if single or double quote is used in line
                    # uses the opposite quote for static tag
                    used_quote = split_line[i + 1][0]
                    if used_quote == '\"':
                        static_quote = "\'"
                    elif used_quote == "\'":
                        static_quote = '\"'
                    else:
                        print('invalid quote at line ', line_no, line)
                        # raises an exception if single or double quote doesn't
                        # begin the reference path
                        raise Exception("Unsupported line format")
                    # Treats onclick=location.href attribute specially due to
                    # two quotes
                    if 'location.href' in split_line[i]:
                        # changes opening quote used in location.href
                        split_line[i] = used_quote + split_line[i][1:]
                        # quote_idx is the index of location.href closing quote
                        quote_idx = split_line[i + 1].index(static_quote)
                        # changes closing quote used in location.href
                        split_line[i + 1] = split_line[i + 1][:quote_idx] + \
                            used_quote + split_line[i + 1][quote_idx + 1:]
                    # adds static tag to the beginning of the path
                    split_line[i + 1] = static_quote + \
                        '{% static ' + split_line[i + 1]
                    # idx is the end of the path where %} is to be added to
                    # close the static tag
                    idx = [j for j in range(
                        len(split_line[i + 1])) if split_line[i + 1][j] == used_quote]
                    # print(line_no, idx, split_line[i + 1])
                    # closes the static tag
                    split_line[i + 1] = split_line[i + 1][:(
                        idx[1] + 1)] + ' %}' + static_quote + split_line[i + 1][idx[1] + 1:]
            # joins back the split line with an =
            joined_line = '='.join(split_line)
            print(line_no, ' ', joined_line)
    except Exception as err:
        print('Encountered', type(err).__name__, 'while parsing line', line_no)
        print(err)
        print(
            'Line',
            line_no,
            'will be left unchanged, It should be edited manually')
        file2.write(line)
        continue
    # writes the edited line into the output file
    file2.write(joined_line)
