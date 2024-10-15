BlockchianSpider is an open source tool for collecting Ethereum data.

We use this tool to get all related addresses in depth of 1 from source contract.


Base model is pre-trained on 711,874 addresses and 14,867,678,031 transactions 

To run the finetuned model, the default args is 

args = [
    "--init_checkpoint=add_Mev_Airdrop/model_299534",
    "--bizdate=add_Mev_Airdrop",
    "--max_seq_length=100",
    "--checkpointDir=tmp"
]