# Clinical Trials RDF Converter

## Overview

This software brings together data about clinical trials from various sources and converts it into RDF (Resource Description Framework) format. By extracting relevant information and mapping it to RDF, this tool helps make clinical trial data more accessible and interoperable for semantic web applications.

## Features

- **Extract PubChem CIDs from JSON files**: Extracts Compound Identifiers (CIDs) from JSON files containing clinical trial data.
- **Fetch clinical trial data from PubChem using CIDs**: Uses extracted CIDs to query PubChem and retrieve detailed clinical trial information.
- **Convert clinical trial data to RDF**: Transforms the clinical trial data into RDF format, making it compatible with semantic web standards.

## Installation

```bash
git clone <repository-url>
cd clinical-trials-rdf-converter
pip install .
```

## Usage

### Extract CIDs from JSON

Use the extract-cid command to extract PubChem CIDs from a source JSON file.

The JSON file can be downloaded from https://pubchem.ncbi.nlm.nih.gov/source/15362#data=Annotations

```

ct-rdf extract-cid --basefile <source_json_file> --targetfile <output_cid_file>
```

Example:

```
ct-rdf extract-cid --basefile clinical_trials.json --targetfile extracted_cids.csv
```

### Fetch Clinical Trial Data from PubChem

Use the pubchem-from-cid command to fetch clinical trial data from PubChem using the extracted CIDs.

```
ct-rdf pubchem-from-cid --cidfile <input_cid_file> --targetfolder <output_folder>
```

Example:

```bash

ct-rdf pubchem-from-cid --cidfile extracted_cids.csv --targetfolder pubchem_data/
```

### Build RDF from JSON Data

Use the build-rdf command to convert the fetched clinical trial data into RDF format.

```bash

ct-rdf build-rdf --inputfolder <json_input_folder> --ttlfile <output_rdf_ttl_file>
```
Example:

```bash

ct-rdf build-rdf --inputfolder pubchem_data/ --ttlfile clinical_trials_data.ttl
```

### Fetch Clinical Trials Data

The `ct-rdf fetch-ct` command is used to fetch data from the ClinicalTrials.gov API and convert it to RDF format. This command processes a list of clinical trial identifiers, retrieves detailed information from ClinicalTrials.gov, and generates an RDF file containing the data.

To use this command, you need to specify the following arguments:

- `inputfile`: The CSV file containing the list of clinical trial identifiers.
- `start`: The starting index for processing the identifiers.
- `end`: The ending index for processing the identifiers.
- `outputfolder`: The folder where the resulting Turtle (.ttl) file will be saved.

**Command Syntax:**

```sh
ct-rdf fetch-ct inputfile.csv outputfile.ttl --start <start> --end <end> 
```

## Load into Triple Store

You can now load the newly generated .ttl files to your favorite triple store. You can run Jena with Fuseki using 

```
docker run -it -p 3030:3030 stain/jena-fuseki
```

## Example queries

TODO

## Source Data

Please refer to the following links to obtain the source data files used for extracting PubChem CIDs:


## License

This project is licensed under the MIT License.

Data from ClinicalTrials.gov may be subject to copyright

## Contributing

If you have suggestions for improvements or new features, please create an issue or submit a pull request.
Contact

