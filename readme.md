# CSI 516 - Computer Communication Networks

## Structure
- `scripts/` - Project wide scripts that are general purpose
- `data/` - Data files; once data is cleaned and placed into the standard format, results should go here
- `<UAlbany NetID>/` - Individual's folders, node-specific scripts should go here

## Cleaned data format
- TBD


## Usages
- `scripts/ping.py` - ping the urls in the file `scripts/nodes.txt` and see if there is a response. All valid URLs go into a tabular format in `valid_nodes.md`. Some tweaking may need to be done to the working directory, depending on where the file is ran and what the current working directory is. Worst case, hardcode the filepath argument and comment out the `os.chdir...` line. **Warning:** This script makes a best effort attempt at identifying countries. The country may not be correct. 