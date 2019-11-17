# CSI 516 - Computer Communication Networks

## Structure
- `scripts/` - Project wide scripts that are general purpose
- `data/` - Data files; once data is cleaned and placed into the standard format, results should go here
- `<UAlbany NetID>/` - Individual's folders, node-specific scripts should go here

## Cleaned data format
- All active nodes should be updated and maintained in the `active_nodes.md` file. This will allow us to uniquely identify each node, and ensure that we do not confuse files when it comes time to merge all the data together.


## Usages
- `scripts/ping.py` - ping the urls in the file `scripts/nodes.txt` and see if there is a response. All valid URLs go into a tabular format in `valid_nodes.md`. Some tweaking may need to be done to the working directory, depending on where the file is ran and what the current working directory is. Worst case, hardcode the filepath argument and comment out the `os.chdir...` line. **Warning:** This script makes a best effort attempt at identifying countries. The country may not be correct. 
- `scripts/traceroute.sh` - generalized script to execute a traceroute and output a file on the remote server. The output file will be in the home directory. **Tweak the output path for personal use**. File name will be `<src>-<dest>_timestamp.txt`
