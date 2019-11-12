import os
import pycountry

# ping each of the available nodes, and output
def check_nodes(filename='nodes.txt'):
    
    # make this file's dir the pwd
    os.chdir(os.path.dirname(__file__))

    with open('nodes.txt') as f:
        urls = [line.split('\t')[0] for line in f]

    with open('valid_nodes.md', 'w') as f:

        # markdown table header
        f.write('|URL|Country|\n|-|-|\n')
        for url in urls:

            # for each server, give them one second to respond with one packet
            # if successful, write to file
            if os.system(f'sudo ping -f -c 1 -t 1 {url} > /dev/null') == 0:
                try:
                    tld = url.split('.')[-1].upper()
                    country = pycountry.countries.get(alpha_2=tld).name
                except:
                    country = 'US'
                    if tld == 'UK':
                        country = 'United Kingdom'
                print(f'success: {url}')
                f.write(f'|{url}|{country}|\n')
    

    

if __name__ == '__main__':
    check_nodes()
