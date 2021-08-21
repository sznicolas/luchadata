#!/usr/bin/env python3

"""
Calculate, display and store luchadores after they dna

Requierements:
    - web3.py
    - a csv file containing :
        - a header. Format : "id,dna"
        - at least one data line
    (optional, if option to get owner and names are set):
    - export WEB3_INFURA_PROJECT_ID which contains a valid Infura API key

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
dna_path = Path("./lucha_id_to_dna.csv")
csv_path = Path("luchadores.csv")


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
    parser.add_argument('-d', dest='output_dir', help="generate svg images and save it in folder")
    parser.add_argument(
            '-i', dest='dna_file', default=dna_path,
            help=f"get id,adn from an ordered csv file (default {dna_path})"
    )
#    parser.add_argument('-a', dest='adn', help="generate from adn")
    parser.add_argument('-r',  dest='readable_svg', action="store_true",
            help="use with '-d'. Saves svg file in an human readable format (parsed and indented by xml lib")
    parser.add_argument('-o',  dest='csv_file', help=f"saves data into a file")
    parser.add_argument(
            '-n', dest='names', action='store_true',
            help="get names onchain (requires WEB3_INFURA_PROJECT_ID exported)"
    )
    parser.add_argument(
            '-w', dest='owner', action='store_true',
            help="display owner (requires WEB3_INFURA_PROJECT_ID)"
    )
#    parser.add_argument('-s', dest='silent', help="silent mode. Useful with -o or -d)
    parser.add_argument(
            'ids', nargs='*', type=int,
            help=f'List of Luchadores Id (defalut: get them all)'
    )
    return parser.parse_args()

def write_svg(lucha, outfile, readable=None):
    flucha = open(outfile, "w")
    svg = lucha.to_svg()
    if readable:
        dom = xml.dom.minidom.parseString(svg)
        svg = dom.toprettyxml()
    flucha.write(svg)
    flucha.close()

def get_dna(dna_file):
    """ read a dna.csv file and returns a list of dna
    First element's id = 1 as [0] contains the header
    """
    try:
        with open(dna_file, 'r') as dna_file:
            csv_reader = csv.reader(dna_file)
            dna = []
            for row in csv_reader:
                dna.append(row[1])
    except FileNotFoundError as e:
        print(e, " You can build the mapping file with 'get_dna_onchain.py (line='id,dna')")
        sys.exit(1)
    if (len(dna)) != Lucha.totalSupply() + 1:
        raise ValueError(f"'{dna_file}' should contain {Lucha.totalSupply() +1} lines (header + luchas)")
    return dna

def main():
    args = parse_args()
    # init Web3
    if args.owner or args.names:
        web3 = set_web3_connexion()
    if args.owner:
        lucha_contract = web3.eth.contract(
            address=lucha_utils.lucha_contract_addr,
            abi=json.loads(lucha_utils.lucha_abi)
        ).functions
    if args.names:
        lucha_contract_addr = lucha_utils.lucha_contract_addr
        luchanames_contract = web3.eth.contract(
            address=lucha_utils.luchanames_contract_addr,
            abi=json.loads(lucha_utils.luchanames_abi)
        ).functions

    # get id => dna mapping
    dna = get_dna(args.dna_file)
    # setup luchadores' id list
    if args.ids:
        luchadores_id_list = args.ids
    else:
        luchadores_id_list = range(1, Lucha.totalSupply() + 1)

    # prepare output
    if args.csv_file:
        csv_header = ["id", "owner", "name"]
        csv_header += Lucha.attributes_names() + Lucha.colored_part_names()
        fcsv = open(args.csv_file, 'w', encoding='UTF8')
        csv_writer = csv.writer(fcsv, delimiter=',', quotechar='"')
        csv_writer.writerow(csv_header)
    # print Header
    print("Name          : attrs count (owner and/or name if asked)")
    for a in Lucha.attributes_names():
        print(f"{a or '-':<12}", end = '')
    print("\n", "Color codes ...")
    print("-" * 92)
    # Print Data
    lucha_owner = ""
    lucha_name = ""
    svg_file = ""
    for i in luchadores_id_list:
        lucha = Lucha(lucha_id=i, dna=dna[i])
        if args.output_dir:
            svg_file = (Path(args.output_dir, f"luchador{i}.svg"))
            write_svg(lucha, svg_file, readable=args.readable_svg)
        if args.owner:
            lucha_owner = lucha_contract.ownerOf(i).call()
            lucha.set_owner(lucha_owner)
        if args.names:
            lucha_name = luchanames_contract.getName(lucha_contract_addr, i).call()
            lucha.set_name(lucha_name)
        print(
            f"--- {lucha.get_realname():<14} --- {lucha.count_attributes()} attrs -- "
            f"{lucha.short_owner()} -------- {lucha.fancy_name()} {svg_file}"
        )
        for a in list(lucha.get_attributes().values()):
            print(f"{a or '-':<12}", end = '')
        print()
        colors = lucha.get_colored_parts()
        print(" " * 6, f"base: #{colors[0]}   alt: #{colors[1]}  eyes: #{colors[2]}  skin: #{colors[3]}")
        if args.csv_file:
            csv_writer.writerow(
                    [i, lucha_owner, lucha_name] + list(lucha.get_attributes().values()) + \
                    lucha.get_colored_parts()
                    )
    if args.csv_file:
        fcsv.close()

if __name__ == '__main__':
    main()
