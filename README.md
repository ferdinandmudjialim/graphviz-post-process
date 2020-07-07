# graphviz-post-process
DOT file post-processing for the RAGE attack graph generator (see ag-gen)  

Current working version is v3.

## Setup
Install pipenv using pip:
```sh
pip install pipenv
```
Then, in project directory:
```sh
pipenv install
```
Activate the virtual environment:
```sh
pipenv shell
```
...and finally run the program:
```sh
./graphviz_tools_v3.py in.dot out.dot -t 3
```
Exit the virtual environment when done.
```sh
exit
```
