import json

def extract_cid_from_json(basefile, targetfile, limit=None):
    """
    Extracts CIDs from a JSON file and writes them to a CSV file.

    Parameters:
    - basefile (str): The path to the input JSON file.
    - targetfile (str): The path to the output CSV file.
    - limit (int, optional): The maximum number of CIDs to write to the CSV file. If None, all CIDs are written.
    """
    with open(basefile) as f:
        d = json.load(f)
        d = d["Annotations"]["Annotation"]

    with open(targetfile, 'w') as f:
        for count, i in enumerate(d):
            if limit is not None and count >= limit:
                break
            cid = str(i["LinkedRecords"]["CID"][0])
            f.write(cid + '\n')
