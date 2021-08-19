# LuchaData

## Puspose
Get onchain (luchadores)[https://luchadores.io/] data.

## Requirements
* Python3
* Web3.py
* An Infura API key (or another Web3 provider). `export WEB3_INFURA_PROJECT_ID=1234abcd...`

Tested on Linux.

## Quickstart
```bash
./getLuchadoresData.py -h                                       
usage: getLuchadoresData.py [-h] [-o OUTPUT_DIR] [-s CSV_FILE] [ids [ids ...]]

Query onchain Luchadores

positional arguments:
  ids            List of Luchadores Id (defalut: get them all)

optional arguments:
  -h, --help     show this help message and exit
  -o OUTPUT_DIR  extracts svg images in folder
  -s CSV_FILE    saves data into /path/file.csv
``` 

## Output
```bash
 ./getLuchadoresData.py 6 7509 
Luchador #6    : (3 attrs) owner: 0x147B8869655Bc09f226955cc676fF78efe240cA8  -~-~-===( El Rosado )===-~-~-
Spirit       Cape         Torso        Arms         Mask         Mouth        Bottoms      Boots       
 -           Classic       -           Gloves       Classic       -            -            -           
Luchador #7509 : (1 attrs) owner: 0x52434Cd9e4e4F965a20c8576841CbAAC4b2bA30e  
Spirit       Cape         Torso        Arms         Mask         Mouth        Bottoms      Boots       
 -            -            -            -           Fierce        -            -            -
```

### Use it with VisiData
If the `-s file.csv` flag is used, we can explore the output with [VisiData](https://www.visidata.org/).  

### Embed a Lucha in a webpage
Extract the svg in a file:
```bash
./getLuchadoresData.py -o /tmp 7509
Luchador #7509 : (1 attrs) owner: 0x52434Cd9e4e4F965a20c8576841CbAAC4b2bA30e /tmp/luchador7509.svg 
Spirit       Cape         Torso        Arms         Mask         Mouth        Bottoms      Boots       
 -            -            -            -           Fierce        -            -            -
```

Then include it in a html file or embed it (here /tmp/luchador7509.svg).

![](./luchador7509.svg | width=120)
