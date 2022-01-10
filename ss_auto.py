import argparse

parser = argparse.ArgumentParser(description='Scan some files')
parser.add_argument('--file', help='Provide path for file to scan', required=True)
args = parser.parse_args()
argsdict = vars(args)

if argsdict['file']  is not None:
    file_to_scan = argsdict['file']



# SHIT THAT LEFT
# re.search(r"(^https://downloads.wordpress.org/plugin/)([\w+.-]+.zip)", url)
# file = open("list_to_scan.txt", "r") # to replace with array