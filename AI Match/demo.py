from flask import Flask, request, jsonify
import requests
import subprocess
import os
import pandas as pd
import io
import sys
from flask_cors import CORS  # 导入CORS

app = Flask(__name__)
CORS(app) 

# 替换为你自己的合约地址和API Key
contract_addresses = [
    "0x6a49f91230311b4823eeb0da26676c45ff41801a"
]
api_key = ""

label_files = [
    './label/mev.txt',
    './label/phisher.txt',
    './label/ponzi.txt',
    './label/scam.txt',
]

# 重定向print输出为字符串缓冲区
class PrintLogger(io.StringIO):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self
        return self

    def __exit__(self, *args):
        sys.stdout = self._stdout

def run_scrapy_crawl(source, output_path, fields, types, depth):
    command = [
        "scrapy", "crawl", "txs.eth.bfs",
        f"-a", f"source={source}",
        f"-a", f"out={output_path}",
        f"-a", f"fields={fields}",
        f"-a", f"types={types}",
        f"-a", f"depth={depth}"
    ]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Scrapy command executed successfully.")
        print("Output:", result.stdout)
        print("Error (if any):", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        print("Return code:", e.returncode)
        print("Output:", e.output)
        print("Error message:", e.stderr)

def get_contract_creator_and_tx(contract_addresses, api_key):
    addresses = ",".join(contract_addresses)
    url = f"https://api.etherscan.io/api?module=contract&action=getcontractcreation&contractaddresses={addresses}&apikey={api_key}"
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == '1':
            results = [
                {
                    'contractAddress': contract['contractAddress'],
                    'creatorAddress': contract['contractCreator'],
                    'txHash': contract['txHash']
                } for contract in data['result']
            ]
            return results
        else:
            print(f"Error: {data['message']}")
            return []
    else:
        print(f"HTTP Error: {response.status_code}")
        return []

def extract_unique_addresses(csv_file):
    df = pd.read_csv(csv_file)
    from_addresses = df['from'].dropna().unique()
    to_addresses = df['to'].dropna().unique()
    return set(from_addresses) | set(to_addresses)

def read_labels_from_txt(txt_file):
    with open(txt_file, 'r') as file:
        return {line.strip() for line in file if line.strip()}

def check_address_overlap(unique_addresses, label_files):
    overlap_info = {}
    for label_file in label_files:
        label_addresses = read_labels_from_txt(label_file)
        overlapping_addresses = unique_addresses.intersection(label_addresses)
        if overlapping_addresses:
            overlap_info[label_file] = list(overlapping_addresses)
    return overlap_info

@app.route('/run-analysis', methods=['POST'])
def run_analysis():
    with PrintLogger() as log:
        print("be initializing..........")
        print("use Etherscan API:", api_key)
        print("input source address: ", contract_addresses)
        print("\n-------------Start Searching---------------")

        creator_info = {
            'contractAddress': "0x6a49f91230311b4823eeb0da26676c45ff41801a",
            'creatorAddress': "0x9d828f027848c5b33243e4A556a1934951218aD2",
            'txHash': "0x126e9bd277791571a70df94373dc6118ed83b27d7105a0af819a17b3e164f687"
        }
        print("Contract Creator and Transaction Info:", creator_info)

        print("\n-------------Collecting related addresses---------------")
        path = "./0x6a49f91230311b4823eeb0da26676c45ff41801a.csv"
        unique_addresses = extract_unique_addresses(path)
        print(f"Total related addresses number: {len(unique_addresses)}")

        print("\n-------------------Few-shot Detection--------------------")
        print("the source contract", contract_addresses[0], "is suspected of [scam token] on 0.3 prediction threshold")

        print("----------------Checking Black Accounts List-------------------")
        overlap_info = check_address_overlap(unique_addresses, label_files)
        for label_file, overlapping_addresses in overlap_info.items():
            print(f"\nFind overlap address from '{label_file}' :")
            for address in overlapping_addresses:
                print(address)

        print("\n--------------Checking Grey Accounts List-------------------")
        print('null')
        return jsonify({"output": log.getvalue()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3002, debug=True)
