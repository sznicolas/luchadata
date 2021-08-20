#!/usr/bin/env python3

"""
Calculate, display and store luchadores after they dna

Requieres:
    - web3.py
    - export WEB3_INFURA_PROJECT_ID which contains a valid Infura API key (optional, if option to get owner and names are set (not implemented yet)
    - a csv file containing :
        - a header. Format : "id,dna"
        - at least one data line
The csv file can be downloaded in this repo, or built with get_dna_onchain.py in this repo.

Use the '-h' flag for help.
"""

import sys
import json
import argparse
import xml.dom.minidom
import csv
from web3 import Web3
from os import getenv
from pathlib import Path
import lucha_utils
from luchadores import Lucha

# defaults
adn_path = Path("./lucha_id_to_dna.csv")
csv_path = Path("luchadores.csv")

# Contracts data
lucha_contract_addr = lucha_utils.lucha_contract_addr
luchanames_contract_addr = lucha_utils.luchanames_contract_addr
luchanames_abi = lucha_utils.luchanames_abi


def set_web3_connexion():
    """Tries to connect to the mainnet
    Returns a web3 object or raises an error
    """
    try:
        infura_url = "https://mainnet.infura.io/v3/" + getenv('WEB3_INFURA_PROJECT_ID')
    except:
        print("You must export a valid WEB3_INFURA_PROJECT_ID environment variable")
        sys.exit(1)
    web3 = Web3(Web3.HTTPProvider(infura_url))
    if not web3.isConnected():
        print("Web3 could not connect to Infura.")
        sys.exit(2)
    return web3


def parse_args():
    parser = argparse.ArgumentParser(description='Display Luchadores infos')
#    parser.add_argument('-d', dest='output_dir', help="extracts svg images in folder")
    parser.add_argument('-i', dest='adn_file', default=adn_path, help=f"get id,adn from an ordered csv file 'id, dna' (default {adn_path}")
#    parser.add_argument('-a', dest='adn', help="generate from adn")
    parser.add_argument('-o',  dest='csv_file', help=f"saves data into a file")
#    parser.add_argument('-n', dest='names', help="dispplay names on chain (requires WEB3_INFURA_PROJECT_ID exported)")
#    parser.add_argument('-w', dest='owner', help="display owner (requires WEB3_INFURA_PROJECT_ID)")
#    parser.add_argument('-s', dest='silent', help="silent mode. Useful with -o or -d)
    parser.add_argument('ids', nargs='*', type=int, help=f'List of Luchadores Id (defalut: get them all)')
    return parser.parse_args()

def main():
    args = parse_args()
    # get id => dna mapping
    try:
        with open(args.adn_file, 'r') as adn_file:
            csv_reader = csv.reader(adn_file)
            dna = []
            for row in csv_reader:
                dna.append(row[1]) 
    except FileNotFoundError as e:
        print(e, " You can build the file mapping the Ids and the dna with 'get_dna_onchain.py")
        sys.exit(1)
    # setup luchadores' id list
    if args.ids:
        luchadores_id_list = args.ids
    else:
        luchadores_id_list = range(1, Lucha.totalSupply() + 1)

    # prepare output
    if args.csv_file:
        csv_header = ["id"] + Lucha.attributes_names() + Lucha.colored_part_names()
        fcsv = open(args.csv_file, 'w', encoding='UTF8')
        csv_writer = csv.writer(fcsv, delimiter=',', quotechar='"')
        csv_writer.writerow(csv_header)

    # print Header
    print("Name          : attrs count")
    for a in Lucha.attributes_names():
        print(f"{a or '-':<12}", end = '')
    print()
    for a in Lucha.colored_part_names():
        print(f"{a or '-':<12}", end = '')
    print(f" <------ Colors")

    # Print Data
    for i in luchadores_id_list:
        lucha = Lucha(lucha_id=i, dna=dna[i])
        print(f"{lucha.get_realname():<14} : {lucha.count_attributes()} attrs")
        for a in list(lucha.get_attributes().values()):
            print(f"{a or '-':<12}", end = '')
        print()
        for a in lucha.get_colored_parts():
            print(f"{a or '-':<12}", end = '')
        print()
        if args.csv_file:
            csv_writer.writerow(
                    [i] + list(lucha.get_attributes().values()) + \
                    lucha.get_colored_parts()
                    )
    if args.csv_file:
        fcsv.close()

if __name__ == '__main__':
    main()
