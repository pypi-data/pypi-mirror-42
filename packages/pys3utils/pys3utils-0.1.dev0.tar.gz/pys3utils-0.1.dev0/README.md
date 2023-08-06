# pys3_utils

(Python s3 scripts and utilities). This library is intended to 
help push/pull resources from s3.

## Usage

To recursively sync a directory to s3 -- only syncing those files 
have been recently updated -- write:
```
python setup.py sdist
```
```bash
python push_project_to_s3.py MY_DIRECTORY MY_BUCKET
``` 