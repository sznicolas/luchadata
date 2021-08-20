#!/usr/bin/env python3

"""
Get data onchain from the Luchadores.io contract,
Requierements:
    - web3.py
    - export WEB3_INFURA_PROJECT_ID which contains a valid Infura API key
Use the '-h' flag for help.
"""

import sys
import json
import argparse
import csv
from web3 import Web3
from os import getenv
from pathlib import Path
import lucha_utils

# defaults
csvpath = Path("./lucha_id_to_dna.csv")

# first to last block containing a GenerateLuchador event
firstblock = 12450223
lastblock = 13046665

# Contracts data
lucha_contract_addr = lucha_utils.lucha_contract_addr
lucha_abi = lucha_utils.lucha_abi


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
    parser = argparse.ArgumentParser(description='Query onchain Luchadores')
    parser.add_argument('-o',  dest='csvfile', default=csvpath, help=f"saves data into a file (default: {csvpath}")
    return parser.parse_args()


def main():
    args = parse_args()
    # Get contracts informations
    web3 = set_web3_connexion()
    lucha_contract = web3.eth.contract(
        address=lucha_contract_addr, abi=json.loads(lucha_abi)
    )

    event_filter = lucha_contract.events.GenerateLuchador.createFilter(fromBlock=firstblock, toBlock=lastblock)
    print("Getting Lucha's dna onchain... please wait...", file=sys.stderr)
    events = event_filter.get_all_entries()
    print("Done", file=sys.stderr)

    # Get the dna
    luchas_dna = {}
    for e in events:
        luchas_dna[e.args.id] = e.args.dna
    # sort and store them
    fcsv = open(args.csvfile, 'w', encoding='UTF8')
    csv_writer = csv.writer(fcsv, delimiter=',', quotechar='"')
    csv_writer.writerow(["id", "dna"])
    for i in range(1, lucha_contract.functions.totalSupply().call() + 1):
        csv_writer.writerow([i, luchas_dna[i]])
    fcsv.close()

if __name__ == '__main__':
    main()
