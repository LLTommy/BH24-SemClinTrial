import argparse
from ct_rdf.cid_extractor import extract_cid_from_json
from ct_rdf.pubchem_fetcher import ask_json_from_cid
from ct_rdf.rdf_builder import build_rdf_from_json

def main():
    parser = argparse.ArgumentParser(description='Process PubChem and Clinical Trials data.')
    subparsers = parser.add_subparsers(dest='command')

    parser_extract = subparsers.add_parser('extract-cid', help='Extract CID from JSON file')
    parser_extract.add_argument('basefile', type=str, help='Input JSON file')
    parser_extract.add_argument('targetfile', type=str, help='Output CSV file')
    parser_extract.add_argument('--limit', type=int, required=False, help='Limit the number of CIDs to extract', default=None)

    parser_pubchem = subparsers.add_parser('pubchem-from-cid', help='Fetch PubChem data from CID list')
    parser_pubchem.add_argument('cid_filename', type=str, help='CSV file with CIDs')
    parser_pubchem.add_argument('targetfolder', type=str, help='Output folder for JSON files')

    parser_rdf = subparsers.add_parser('build-rdf', help='Build RDF from JSON files')
    parser_rdf.add_argument('inputfolder', type=str, help='Folder with input JSON files')
    parser_rdf.add_argument('ttlfilename', type=str, help='Output Turtle (.ttl) file')

    args = parser.parse_args()

    if args.command == 'extract-cid':
        extract_cid_from_json(args.basefile, args.targetfile, args.limit)
    elif args.command == 'pubchem-from-cid':
        ask_json_from_cid(args.cid_filename, args.targetfolder)
    elif args.command == 'build-rdf':
        build_rdf_from_json(args.inputfolder, args.ttlfilename)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
