# graphviz-post-process
DOT file post-processing for the RAGE attack graph generator (see ag-gen)  

### Current working version is v3, tested on fresh Debian install.

## Requirements
- `python3`
- `pip`

```sh
sudo apt install python3 python3-pip
```
## Setup
Install `pipenv` using `pip`:
```sh
sudo -H pip3 install -U pipenv
```
Then, in project directory, install requirements from `Pipfile`:
```sh
pipenv install
```
Activate the virtual environment:
```sh
pipenv shell
```
...and finally run the program using the provided `testing.dot`:
```sh
./graphviz_tools_v3.py testing.dot testing_out.dot -t 3
```
If all goes well, the output should be:
```sh
Reading from testing.dot
Generated dot file to testing_out.dot
Shortest paths to target edge 3 are:
[['1', '7'], ['14'], ['57']]
[['2', '8'], ['21'], ['74']]
```
Exit the virtual environment when done.
```sh
exit
```
