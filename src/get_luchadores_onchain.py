#!/usr/bin/env python3

"""
This is my first Web3.py script.
It requieres:
    - web3.py
    - export WEB3_INFURA_PROJECT_ID which contains a valid Infura API key
It gets data onchain from the Luchadores.io contract,
and is able to save locally the luchadore.svg image, since it's stored onchain.
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

# Contracts data
lucha_contract_addr = "0x8b4616926705Fb61E9C4eeAc07cd946a5D4b0760"
lucha_abi = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"dna","type":"uint256"}],"name":"GenerateLuchador","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"baseURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_quantity","type":"uint256"},{"internalType":"uint256","name":"_deadline","type":"uint256"}],"name":"generateLuchador","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"imageData","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"metadata","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pauseSale","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"requestId","type":"bytes32"},{"internalType":"uint256","name":"randomness","type":"uint256"}],"name":"rawFulfillRandomness","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_baseURI","type":"string"}],"name":"setBaseURI","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_LinkFee","type":"uint256"}],"name":"setLinkFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenOfOwnerByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"uniswapRouter","outputs":[{"internalType":"contract IUniswapV2Router02","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"unpauseSale","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
luchanames_contract_addr = "0x741f506e38ceA4e001f770eB14F6eC9B468D9899"
luchanames_abi = '[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"_originContract","type":"address"},{"indexed":true,"internalType":"address","name":"_sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"id","type":"uint256"},{"indexed":false,"internalType":"string","name":"name","type":"string"}],"name":"SetName","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"addressBlacklist","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_originContract","type":"address"},{"internalType":"address","name":"_address","type":"address"},{"internalType":"bool","name":"_bool","type":"bool"}],"name":"blacklistAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_originContract","type":"address"},{"internalType":"uint256","name":"_id","type":"uint256"}],"name":"blacklistName","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_originContract","type":"address"},{"internalType":"uint256","name":"_id","type":"uint256"}],"name":"getName","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_name","type":"string"}],"name":"isSafeName","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"string","name":"","type":"string"}],"name":"nameExists","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"nameFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"names","outputs":[{"internalType":"string","name":"name","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_originContract","type":"address"},{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"string","name":"_name","type":"string"}],"name":"set1Name","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"_originContract","type":"address"},{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"string","name":"_name1","type":"string"},{"internalType":"string","name":"_name2","type":"string"}],"name":"set2Names","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"_originContract","type":"address"},{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"string","name":"_name1","type":"string"},{"internalType":"string","name":"_name2","type":"string"},{"internalType":"string","name":"_name3","type":"string"}],"name":"set3Names","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"_originContract","type":"address"},{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"string","name":"_name1","type":"string"},{"internalType":"string","name":"_name2","type":"string"},{"internalType":"string","name":"_name3","type":"string"},{"internalType":"string","name":"_name4","type":"string"}],"name":"set4Names","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"_originContract","type":"address"},{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"string","name":"_name1","type":"string"},{"internalType":"string","name":"_name2","type":"string"},{"internalType":"string","name":"_name3","type":"string"},{"internalType":"string","name":"_name4","type":"string"},{"internalType":"string","name":"_name5","type":"string"}],"name":"set5Names","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_nameFee","type":"uint256"}],"name":"setNameFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'


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
    parser.add_argument('-d',  dest='output_dir', help="extracts svg images in folder")
    parser.add_argument('-o',  dest='csv_file', help="saves data into /path/file.csv")
    parser.add_argument('-r',  dest='readable_svg', action="store_true",
            help="saves svg file in an human readable format (parsed and indented by xml lib")
    parser.add_argument('ids', nargs='*', type=int, help='List of Luchadores Id (defalut: get them all)')
    return parser.parse_args()


def main():
    args = parse_args()

    # Get contracts informations
    web3 = set_web3_connexion()
    lucha_contract = web3.eth.contract(
        address=lucha_contract_addr, abi=json.loads(lucha_abi)
    ).functions
    luchanames_contract = web3.eth.contract(
        address=luchanames_contract_addr, abi=json.loads(luchanames_abi)
    ).functions
    attributes_template = ["Spirit", "Cape", "Torso", "Arms", "Mask", "Mouth", "Bottoms", "Boots"]

    if args.csv_file:
        csv_header = ["id", "name", "owner"] + attributes_template
        fcsv = open(args.csv_file, 'w', encoding='UTF8')
        csv_writer = csv.writer(fcsv, delimiter=',', quotechar='"')
        csv_writer.writerow(csv_header)
    # setup luchadores' id list
    if args.ids:
        luchadores_id_list = args.ids
    else:
        luchadores_id_list = range(1, lucha_contract.totalSupply().call() + 1)
    # retrieve and print data
    lucha_output = ""
    for i in luchadores_id_list:
        lucha_metadata = json.loads(lucha_contract.metadata(i).call())
        lucha_name = luchanames_contract.getName(lucha_contract_addr, i).call()
        lucha_pretty_name = f"-~-~-===( {lucha_name} )===-~-~-" if lucha_name else ''
        lucha_owner = lucha_contract.ownerOf(i).call()
        # transforms from {'trait_type': 'type_name', 'value': 'val_name'} to {'type_name': 'val_name'} :
        lucha_attributes = {l['trait_type']: l['value'] for l in lucha_metadata['attributes']}
        if args.output_dir:
            outfile = Path(args.output_dir, f"luchador{i}.svg")
            flucha = open(outfile, "w")
            svg_content = lucha_contract.imageData(i).call()
            if args.readable_svg:
                dom = xml.dom.minidom.parseString(svg_content)
                svg_content = dom.toprettyxml()
            flucha.write(svg_content)
            flucha.close()
            lucha_output = f"{outfile}"
        # output
        print(
            f"{lucha_metadata['name']:<14} : ({len(lucha_metadata['attributes'])} attrs)",
            f"owner: {lucha_owner} {lucha_output} {lucha_pretty_name}"
        )
        print(' '.join(map('{:<12}'.format, attributes_template)))
        traits = []
        for trait in attributes_template:
            print(f"{lucha_attributes.get(trait, ' -'):<12}", end=' ')
            traits.append(lucha_attributes.get(trait, ''))
#            print(f"{trait} = {lucha_attributes.get(trait, ' -'):<12}", end=' ')
        print() 
        if args.csv_file:
            csv_writer.writerow([i, lucha_name, lucha_owner] + traits)

    if args.csv_file:
        fcsv.close()


if __name__ == '__main__':
    main()
