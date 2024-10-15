import requests
import subprocess
import os  
import pandas as pd
import re


def run_scrapy_crawl(source, output_path, fields, types, depth):
    # 构建命令列表
    command = [
        "scrapy", "crawl", "txs.eth.bfs",
        f"-a", f"source={source}",
        f"-a", f"out={output_path}",
        f"-a", f"fields={fields}",
        f"-a", f"types={types}",
        f"-a", f"depth={depth}"
    ]
    
    try:
        # 调用 subprocess.run 执行命令
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
    # 合约地址列表以逗号分隔（最多支持 5 个）
    addresses = ",".join(contract_addresses)
    
    # Etherscan API URL for contract creation info
    url = f"https://api.etherscan.io/api?module=contract&action=getcontractcreation&contractaddresses={addresses}&apikey={api_key}"
    
    response = requests.get(url, verify=False)

    # 检查请求是否成功
    if response.status_code == 200:
        data = response.json()
        # 检查返回结果的状态是否为 "OK"
        if data['status'] == '1':
            # 返回合约创建者地址和创建交易哈希
            results = []
            for contract in data['result']:
                contract_info = {
                    'contractAddress': contract['contractAddress'],
                    'creatorAddress': contract['contractCreator'],
                    'txHash': contract['txHash']
                }
                results.append(contract_info)
            return results
        else:
            return f"Error: {data['message']}"
    else:
        return f"HTTP Error: {response.status_code}"

# that is an example
contract_addresses = "0x6a49f91230311b4823eeb0da26676c45ff41801a"
api_key = "VGE6P9D2QHCIGVJ1N8E9K5VXQE356HV3NV" 
threshold = 0.3

print("be initializing..........")
print("use Etherscnan API:", api_key)
print("input source address: ", contract_addresses)
print("the prediction threshold", threshold)
print("\n-------------Start Searching---------------")
creator_info = get_contract_creator_and_tx(contract_addresses, api_key)

print("Contract Creator and Transaction Info:", creator_info)

print("\n-------------Collecting related addresses---------------")

if isinstance(creator_info, dict):
    # 从获取的创建者信息中提取创建者地址
    source = creator_info['contractAddress']  # 确保只提取字符串
    output_path = "./defending_demo/"
    
    # 检查输出路径是否存在，如果不存在则创建
    os.makedirs(output_path, exist_ok=True)

    fields = "hash,from,to,value,timeStamp,blockNumber,isError,input"
    types = "external,internal"
    depth = 1

    run_scrapy_crawl(source, output_path, fields, types, depth)
else:
    print("Failed to retrieve creator information.")

def extract_unique_addresses(csv_file):
    df = pd.read_csv(csv_file)
    
    from_addresses = df['from'].dropna().unique()  
    to_addresses = df['to'].dropna().unique()      
    
    unique_addresses = set(from_addresses) | set(to_addresses)
    
    return unique_addresses

path = "./BlockchainSpider/defending_demo/"+ contract_addresses +".csv"
unique_addresses = extract_unique_addresses(path)

unique_addresses = unique_addresses.copy()  # 复制第一个集合

print("All related addresses:")
for address in unique_addresses:
    print(address)

print(f"Total related addresses number: {len(unique_addresses)}")

def check_address_overlap(unique_addresses, label_files):
    overlap_info = {}   
    for label_file in label_files:
        label_addresses = read_labels_from_txt(label_file)
        # 找到重叠的地址
        overlapping_addresses = unique_addresses.intersection(label_addresses)
        
        if overlapping_addresses:
            overlap_info[label_file] = overlapping_addresses
    
    return overlap_info

print("-------------------Few-shot Detection--------------------")
#Use mev-bot as an example
import os
import subprocess
import re

def run_python_script_with_args(script_path, args):
    # 设置环境变量
    env = os.environ.copy()  # 复制当前的环境变量
    env["CUDA_VISIBLE_DEVICES"] = "0"  # 设置 CUDA_VISIBLE_DEVICES 环境变量

    try:
        # 调用 subprocess.run 来执行 Python 文件，并传入参数
        result = subprocess.run(["python", script_path] + args, check=True, capture_output=True, text=True, env=env)
        
        # 脚本执行成功，输出标准输出和错误输出
        print("Python script executed successfully.")
        print("Full Output:", result.stdout)
        print("Error (if any):", result.stderr)
        
        # 提取包含关键字 "agg_y_hat_list" 的行中的浮点数
        extract_floats_from_output(result.stdout, "agg_y_hat_list")

    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        print("Return code:", e.returncode)
        print("Error message:", e.stderr)

def extract_floats_from_output(output, keyword):
    # 按行拆分输出
    lines = output.splitlines()
    # 匹配浮点数的正则表达式
    float_pattern = r"[-+]?\d*\.\d+|\d+"

    for line in lines:
        # 检查行中是否包含关键词
        if keyword in line:
            # 提取该行中的所有浮点数
            floats = re.findall(float_pattern, line)
            # 将字符串转换为浮点数
            floats = [float(num) for num in floats]
            if floats:
                print(f"Line containing keyword '{keyword}': {line}")
                print(f"Extracted floats: {floats}")
                return floats

def extract_floats_from_output(output, keyword):
    lines = output.splitlines()
    float_pattern = r"[-+]?\d*\.\d+|\d+"

    for line in lines:
        if keyword in line:
            floats = re.findall(float_pattern, line)
            floats = [float(num) for num in floats]
            if floats:
                print(f"Line containing keyword '{keyword}': {line}")
                print(f"Extracted floats: {floats}")
                return floats


script_path = "./run_finetune_mev.py"  

args = [
    "--init_checkpoint=add_Mev_Airdrop/model_299534",
    "--bizdate=add_Mev_Airdrop",
    "--max_seq_length=100",
    "--checkpointDir=tmp"
]

script_path = "./run_finetune_mev.py"
output = run_python_script_with_args(script_path, args)
prediction = extract_floats_from_output(output, "agg_y_hat_list")

if prediction > threshold:
    print("the source contract: ", contract_addresses, "is suspected of"+ "[MEV-Bot]" +"on 0.3 prediction threshold")

print("\n----------------Checking Black Accounts List-------------------")
label_files = [
    './Data/mev_account.txt',
    './Data/phisher_account.txt',
    './Data/ponzi_account.txt',
    './Data/phisher_contract.txt'
]

def read_labels_from_txt(txt_file):
    with open(txt_file, 'r') as file:
        addresses = {line.strip() for line in file if line.strip()}  # 去掉空行
    return addresses

overlap_info = check_address_overlap(unique_addresses, label_files)

for label_file, overlapping_addresses in overlap_info.items():
    print(f"\nFind overlap address from '{label_file}' :")
    for address in overlapping_addresses:
        print(address)

print("--------------Checking Grey Accounts List-------------------")

#lack of dataset, updating....
