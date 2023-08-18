# Publication Fetcher

## Set up

- Set up a virtual environment: `python3 -m venv venv` or `python -m venv venv`
- Activate the virtual environment: `source venv/bin/activate` (Linux) or `venv\Scripts\activate` (Windows)
- Install dependencies: `pip install -r requirements.txt`
- Rename the `config.json.example` file to `config.json` and fill in the values of `apikey` and `insttoken` with your own valuee. You can get them from [Elsevier Developer Portal](https://dev.elsevier.com/apikey/manage)

## Retrieve SCOPUS ID

- Get the authors name (first and last) in a Excel (`.xlsx`) file
- Run `python get_scopus_id.py` with the following arguments:

  - `input_file`: path to the input file (`.xlsx`)
  - `output_file`: path to the output file (`.xlsx`)

  Example:

  - `python get_scopus_id.py --input_file authors.xlsx --output_file authors_with_scopus_id.xlsx`

## Retrieve publications

- Run `python get_papers.py` with the following arguments:

  - `input`: path to the input file (`.xlsx`)
  - `output`: path to the output file (`.xlsx`)
  - `author_type`: type of author. Can be `student`, `post-doc` or `professor`
  - `month`: month of the year such as `01` or `06`
  - `year`: year such as `2020`

  Example:

  - `python get_papers.py --input authors.xlsx --output papers_student.txt --author_type student --month 01 --year 2020`
