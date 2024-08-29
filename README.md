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

1. Extract CIDs from JSON

Use the extract-cid command to extract PubChem CIDs from a source JSON file.

The JSON file can be downloaded from https://pubchem.ncbi.nlm.nih.gov/source/15362#data=Annotations

```

ct-rdf extract-cid --basefile <source_json_file> --targetfile <output_cid_file>
```

Example:

```
ct-rdf extract-cid --basefile clinical_trials.json --targetfile extracted_cids.csv
```

2. Fetch Clinical Trial Data from PubChem

Use the pubchem-from-cid command to fetch clinical trial data from PubChem using the extracted CIDs.

```
ct-rdf pubchem-from-cid --cidfile <input_cid_file> --targetfolder <output_folder>
```

Example:

```bash

ct-rdf pubchem-from-cid --cidfile extracted_cids.csv --targetfolder pubchem_data/
```

3. Build RDF from JSON Data

Use the build-rdf command to convert the fetched clinical trial data into RDF format.

```bash

ct-rdf build-rdf --inputfolder <json_input_folder> --ttlfile <output_rdf_ttl_file>
```
Example:

```bash

ct-rdf build-rdf --inputfolder pubchem_data/ --ttlfile clinical_trials_data.ttl
```

## Source Data

Please refer to the following links to obtain the source data files used for extracting PubChem CIDs:

    Link to JSON file with clinical trials and PubChem IDs (ClinicalTrials.gov)
    Link to JSON file with clinical trials and PubChem IDs (EU Clinical Trials Register)
    Link to JSON file with clinical trials and PubChem IDs (NIPH Clinical Trials Search of Japan)

## License

This project is licensed under the MIT License.

## Contributing

If you have suggestions for improvements or new features, please create an issue or submit a pull request.
Contact

