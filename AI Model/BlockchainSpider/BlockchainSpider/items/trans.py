import scrapy

from BlockchainSpider.items.defs import ContextualItem


class BlockItem(ContextualItem):
    block_hash = scrapy.Field()  # str
    block_number = scrapy.Field()  # int
    parent_hash = scrapy.Field()  # str
    difficulty = scrapy.Field()  # int
    total_difficulty = scrapy.Field()  # int
    size = scrapy.Field()  # int
    gas_limit = scrapy.Field()  # int
    gas_used = scrapy.Field()  # int
    miner = scrapy.Field()  # str
    receipts_root = scrapy.Field()  # str
    timestamp = scrapy.Field()  # int
    logs_bloom = scrapy.Field()  # str
    nonce = scrapy.Field()  # int


class TransactionItem(ContextualItem):
    transaction_hash = scrapy.Field()  # str
    transaction_index = scrapy.Field()  # int
    block_hash = scrapy.Field()  # str
    block_number = scrapy.Field()  # int
    timestamp = scrapy.Field()  # int
    address_from = scrapy.Field()  # str
    address_to = scrapy.Field()  # str
    value = scrapy.Field()  # int
    gas = scrapy.Field()  # int
    gas_price = scrapy.Field()  # int
    nonce = scrapy.Field()  # int
    input = scrapy.Field()  # str


class TransactionReceiptItem(ContextualItem):
    transaction_hash = scrapy.Field()  # str
    transaction_index = scrapy.Field()  # int
    transaction_type = scrapy.Field()  # int
    block_hash = scrapy.Field()  # str
    block_number = scrapy.Field()  # int
    gas_used = scrapy.Field()  # int
    effective_gas_price = scrapy.Field()  # int
    created_contract = scrapy.Field()  # str
    is_error = scrapy.Field()  # bool


class EventLogItem(ContextualItem):
    transaction_hash = scrapy.Field()  # str
    log_index = scrapy.Field()  # int
    block_number = scrapy.Field()  # str
    timestamp = scrapy.Field()  # int
    address = scrapy.Field()  # str
    topics = scrapy.Field()  # [str]
    data = scrapy.Field()  # str
    removed = scrapy.Field()  # bool


class TraceItem(ContextualItem):
    transaction_hash = scrapy.Field()  # str
    trace_type = scrapy.Field()  # str
    trace_id = scrapy.Field()  # str
    block_number = scrapy.Field()  # int
    timestamp = scrapy.Field()  # int
    address_from = scrapy.Field()  # str
    address_to = scrapy.Field()  # str
    value = scrapy.Field()  # int
    gas = scrapy.Field()  # int
    gas_used = scrapy.Field()  # int
    input = scrapy.Field()  # str
    output = scrapy.Field()  # str


class ContractItem(ContextualItem):
    address = scrapy.Field()  # str
    code = scrapy.Field()  # str


class Token20TransferItem(ContextualItem):
    transaction_hash = scrapy.Field()  # str
    log_index = scrapy.Field()  # int
    block_number = scrapy.Field()  # int
    timestamp = scrapy.Field()  # int
    contract_address = scrapy.Field()  # str
    address_from = scrapy.Field()  # str
    address_to = scrapy.Field()  # str
    value = scrapy.Field()  # int


class Token721TransferItem(ContextualItem):
    transaction_hash = scrapy.Field()  # str
    log_index = scrapy.Field()  # str
    block_number = scrapy.Field()  # int
    timestamp = scrapy.Field()  # int
    contract_address = scrapy.Field()  # str
    address_from = scrapy.Field()  # str
    address_to = scrapy.Field()  # str
    token_id = scrapy.Field()  # int


class Token1155TransferItem(ContextualItem):
    transaction_hash = scrapy.Field()  # str
    log_index = scrapy.Field()  # int
    block_number = scrapy.Field()  # str
    timestamp = scrapy.Field()  # int
    contract_address = scrapy.Field()  # str
    address_operator = scrapy.Field()  # str
    address_from = scrapy.Field()  # str
    address_to = scrapy.Field()  # str
    token_ids = scrapy.Field()  # [int]
    values = scrapy.Field()  # [int]


class TokenApprovalItem(ContextualItem):
    transaction_hash = scrapy.Field()  # str
    log_index = scrapy.Field()  # int
    block_number = scrapy.Field()  # str
    timestamp = scrapy.Field()  # int
    contract_address = scrapy.Field()  # str
    address_from = scrapy.Field()  # str
    address_to = scrapy.Field()  # str
    value = scrapy.Field()  # int


class TokenApprovalAllItem(ContextualItem):
    transaction_hash = scrapy.Field()  # str
    log_index = scrapy.Field()  # int
    block_number = scrapy.Field()  # str
    timestamp = scrapy.Field()  # int
    contract_address = scrapy.Field()  # str
    address_from = scrapy.Field()  # str
    address_to = scrapy.Field()  # str
    approved = scrapy.Field()  # bool


class TokenPropertyItem(ContextualItem):
    contract_address = scrapy.Field()  # str
    name = scrapy.Field()  # str
    token_symbol = scrapy.Field()  # str
    decimals = scrapy.Field()  # int
    total_supply = scrapy.Field()  # int


class NFTMetadataItem(ContextualItem):
    transaction_hash = scrapy.Field()  # str
    log_index = scrapy.Field()  # int
    block_number = scrapy.Field()  # str
    timestamp = scrapy.Field()  # int
    contract_address = scrapy.Field()  # str
    token_id = scrapy.Field()  # int
    uri = scrapy.Field()  # str
    data = scrapy.Field()  # str


class DCFGItem(ContextualItem):
    transaction_hash = scrapy.Field()  # str
    blocks = scrapy.Field()  # [DCFGBlockItem]
    edges = scrapy.Field()  # [DCFGEdgeItem]


class DCFGBlockItem(ContextualItem):
    contract_address = scrapy.Field()  # str
    start_pc = scrapy.Field()  # int
    operations = scrapy.Field()  # [str]


class DCFGEdgeItem(ContextualItem):
    transaction_hash = scrapy.Field()  # str
    address_from = scrapy.Field()  # str
    start_pc_from = scrapy.Field()  # int
    address_to = scrapy.Field()  # str
    start_pc_to = scrapy.Field()  # int
    flow_type = scrapy.Field()  # str
    value = scrapy.Field()  # int
    gas = scrapy.Field()  # int
    selector = scrapy.Field()  # str
    index = scrapy.Field()  # int
