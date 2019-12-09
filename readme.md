# CSI 516 - Computer Communication Networks

## Class Specific

## Structure
- `scripts/` - Project wide scripts that are general purpose
- `data/` - Data files; once data is cleaned and placed into the standard format, results should go here
- `docs/` - Project wide documentation (final report, working docs, etc...)
- `analysis/` - Data analysis
- #### Class Specific
  - `docs/final_report.pdf` - Written final report 
  - `docs/notebook.html` - Jupyter notebook exported as a web page. No need for installation of Jupyter for read-only purposes.
  - `analysis/bharghav-analysis` - Files created and owned by Bharghav

## Cleaned data format
- All active nodes should be updated and maintained in the `active_nodes.md` file. This will allow us to uniquely identify each node, and ensure that we do not confuse files when it comes time to merge all the data together.
- The raw output of `ping` or `traceroute` creates a new file on the node. This file has the format `<type>_<src>-<dest>_<Y-M-D>_<H-M-S>`.


## Usages
- `scripts/ping.py` - ping the urls in the file `scripts/nodes.txt` and see if there is a response. All valid URLs go into a tabular format in `valid_nodes.md`. Some tweaking may need to be done to the working directory, depending on where the file is ran and what the current working directory is. Worst case, hardcode the filepath argument and comment out the `os.chdir...` line. **Warning:** This script makes a best effort attempt at identifying countries. The country may not be correct. 
- `scripts/traceroute.sh` - generalized script to execute a traceroute and output a file on the remote server. The output file will be in the home directory. **Tweak the output path for personal use**. File name will be `<src>-<dest>_timestamp.txt`
- To start the Jupyter notebook containing the data analysis, ensure to have Python 3.6+ installed and all requirements. To install the requirements, run the command `pip install -r requirements.txt` from the project root. If you have multiple versions of Python installed, you may need to use the command `pip3 install -r requirements.txt`.
