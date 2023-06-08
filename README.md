# Publication Fetcher

## Set up

- Set up a virtual environment: `python3 -m venv venv`
- Activate the virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

## Retrieve SCOPUS ID

- Get the authors name (first and last) in a Excel (`.xlsx`) file
- Run `python get_scopus_id.py` with the following arguments:

  - `input_file`: path to the `.xlsx` file
  - `output_file`: path to the output file (`.csv`)
  - `parallel`: Use parallel processing (default: `False`)

  Example:

  - Parallel run: `python get_scopus_id.py --input_file data/authors.xlsx --output_file data/scopus_id.csv --parallel`
  - Sequential run: `python get_scopus_id.py --input_file data/authors.xlsx --output_file data/scopus_id.csv`
