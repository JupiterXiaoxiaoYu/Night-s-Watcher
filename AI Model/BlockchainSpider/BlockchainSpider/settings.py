from scrapy.utils.reactor import install_reactor

BOT_NAME = 'BlockchainSpider'

SPIDER_MODULES = ['BlockchainSpider.spiders']
NEWSPIDER_MODULE = 'BlockchainSpider.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 8

# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 5
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'contrib.mots.middlewares.MoTSMiddleware': 500,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'BlockchainSpider.middlewares.RequestCacheMiddleware': 901,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html

ITEM_PIPELINES = {
    'contrib.mots.pipelines.MoTSPipeline': 666,
    # 'contrib.rabbit.pipelines.RabbitMQPipeline': 666,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = './cache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# HTTPCACHE_GZIP = True

# Setting the fingerprinting algorithm is used
# See https://docs.scrapy.org/en/latest/topics/request-response.html#request-fingerprinter-implementation
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'

# Enable asyncio
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')

# Log configure
LOG_LEVEL = 'INFO'

# The response size (in bytes) that downloader will start to warn.
DOWNLOAD_WARNSIZE = 33554432 * 2

# APIKey configure
APIKEYS_BUCKET = 'BlockchainSpider.utils.bucket.StaticAPIKeyBucket'
APIKEYS = {
    "eth": [
        "SZMBES7CQFTJUAEMXI9UE8Y4AR72AD5461",
        "BNXWEKCK5DNVGSA9KRYTWI1I2PJ63BAPDU",
        "YRP34NGT3KFDAFS1TE6D5TNETR17IU3ZHM",
        "PH6H16TYXDP8ACIFFNKTFFR1KMU1NUR62G",
        "R7WY9SXGD6AKYPFN3WA64BFUCNYVTIF5IH",
        "M1U6VZWV3Y1H2FP1F9YQEAJZU92Y4IIWZJ",
        "VGE6P9D2QHCIGVJ1N8E9K5VXQE356HV3NV",
        "SMS3QDADNW43G2YRPG37YNRUCAA676Y1FK",
        "G3ZIVCIZM1IDMK9KIFFQ3DEV3N1ATR63ST",
        "Y5HNVNC3HVB6KWJ88ZI2T2QI5ZM3MURC6Y",		
        "ZX7V88H6QH7T5KGUKSSMDY7PR9KEIWSUN6",		
        "5K7RZ2FKPI5BDY2QI5WU97DHZQF12USBP7",		
        "FIS4U3YTGMPEC7RBV57368BGNIJIG7UWN9",		
        "F8D1QN711ZBX4PJH2R7M98VVC63PJT5GAU",		
        "QHXPMXZCRZWY9VS64IQ5THK1BFWATXWEPE",		
        "MCRVIUP78EC1PWP4UV5THI39HEU4DKPZGN",		
        "7P2HINXXNWMBTNINSIJVQPMT14UTJ37NW6",		
        "IXSCKB1CNMBKDT1TE2HK5WAZBGH8SKEPQ7",		
        "MC1WFBAA6EKQ3DWEICAI7YJUZGSBMHD7RS",		
        "SP4ND94WT3UXJSQUH6FR1T5APXHS9BPM7S",		
        "SMPBJNCHC7CHZD15IUKD6ZGENM6J91HRA7",
        "MCDE2ZV3GVKQBRSJ5V4VE82NHT32NM4A2Z",
        "99B5J7A8RGP7ZQDSHSMN428NMS59J4DD51",
        "7MM6JYY49WZBXSYFDPYQ3V7V3EMZWE4KJK",
        "G52EVP68FSC4SDA79RVG5G1QW878RIJJRT",
        "3RDEEN6RNS694NQTCTENUKQPI7FY147KIA",
        "AZI8P3UZBWIFY93UKDHUPN8QC9MVH26N2E",
        "9DHD6VRXGI5747TFE6D8F2RAIY79ZST16I",
        "VUX7GADFQWS3ZY667FIBU8M7U8PGYPQ42J",
        "C7JHK7ZBEQJWMKC6AYTRUIMIJMMIFAF7K3",
        "1S6HVVBYA9A1TH4UJ1HFPH5MXAATIZT3ER",
        "64GTQD9HUSDKACZQ1H4AAPYWWF4GZUYA7I",
        "XA7QR77WE59MEFSSZJ81QB6RCA9YKE8TYJ",
        "H2WU5N2A1CQFCBA5N6MHJ7V4HWE3QK4VHS",
        "KC2IM55M9UR13FC2JWW86EGY2SR3XNRWIA",
        "NYKKBPHV8N2UCWE1PYU7Y31KJ599TMCCF6",
        "DUM1U31ZYKVDWQQ7KQR3U6372ZSM4TPBF5",
        "2K9CQID285Q7MY73NW9UNXUNQ2KYDQVUEB",
        "YB3M2RCUW6R6TFFUJE8XKS8HU79SYQ7Q1Z",
        "65DV9K3BPC8PC1W6IXMWVF22D5CSS8N865",
        "5USX9X1EGX465153FFZRJ9D6XTT3YTF6UF",
        "WZ3C94VZJSQCMIYWI8B8QMMXEFAT2SBJH7",
        "PBRY8UVZRZWGG1TW9H2VD2QTISI3YYNBYA",
        "QCYY2WIM6D7Y4HZ7K4K3WG5FGSU34RZPSY",
        "K6RUECSWGECECWGJGXG7Y42ACMHPSREPMD",
        "RUWQ2V5ITFRV7AHQSF7AHNTJDFDGS213AU",
        "9IFSB7F6GG22TSFV2AAWDUV4PD2ZWPZP48",
        "F41FGE4HT87SNBZVXYEN3M7XR4D5N48IPE",
        "VV6KJGKF4G87WQMF8SMJNAP9UG3FTZ9PIG",
        "Z96MYW6TGFT6S7BJFXPAAE9S5GNCNW6AI4",
        "KYCTC2BSPWWIVBDQ9SR757PKPVEY4UPK1S",
        "BZADKXPEID1H8K7IFBVGJ5APPPHQAQQFHF",
        "JA4EQX42NSJNS2B4HS7U5UFSTPTPCQ7XD9",
        "6SGZF33DG97FQT4W84KUDBCQ7RAE1R292F",
        "FCF985TYGX2QYR2JE6Z7E51R3GWEYQVSPI",
        "KWET6J3AUJUAARYIFJ612FHGDV9VNI4X4C",	
        "BQJZJI433H55FM9FV3SGIV74KP98EJE724",	
        "T921ENEDV25HPXJZSQ37CV2YEQD7YCNXGJ",	
        "V4SY6NY4K37DYP2I7NE2KGIN28J5NRVV1Q",	
        "ESMPJ739FQSW2D5KSGSQEX8YMBNXMPUVWC",	
        "Y1XVCP4RPY3KBBWENQW1D1SZ91265Z56RZ",	
        "Q2X2BIYTCZ79P1474JZXUYACEQVFETDBNY",	
        "59MANEJQDUE6MMPQ1GPWX6Z9VYI4AKF3IN",	
        "XSWB86X8RGRBFUBJCYXIIRTKEANTX52PSS",	
        "CZ467K91AI4K891VRRQYSWIN391JITIEFI",	
        "5C75FD2M6HC99BJ1ACYMFAUJ36CG3DYXTQ",	
        "RW1XNX21E2KDYGCABNYAMG1FWGKJX14PJ8",	
        "A2QJSZN6H444F8GWJN41MPPC3MEIYBAC1U",	
        "8JGH17Y493XI95SEUJ6B6IV5FESF5XSKHF",	
        "A25355QDB1WU8HK63T6M9S61NQD99D8ABT",
        "JADI9EF9T9NCI4AX9FI79KBT89VFMIH7FM",		
        "5J8F14UAQJ8VPSE3B6DH8J9F8S7DP731F2",		
        "33AGZ34PTPX4JQUKZ9H9JIUW98WQ1KMVPH",		
        "ZPM5464NMFWFWZVJC15NZDR3RIVZ4MXDG2",		
        "I959FK6ZNSNGJGNBQGMUZ6I2HVP7V1UA1I",		
        "EQKEC5RR3C2IIIXSDIRAM97IXFGJW2HSHZ",		
        "H144MGMVY5ZFBBAJZ6R6KJBJ8PBYNM51CB",		
        "1R23E1HH7RJ2B22D5WSZUGFGWRPJUKKJP1",		
        "NA1CD2XSPK3UFIS571H5D6WJHNCCY41H5F",		
        "HHIYG6C7RZGG8HIUXCREJZ3Y4RX4RSKY1K",		
        "3R3JZ9CVNFEMEISZTTBC93P4F8C96VUGMU",		
        "1AHNVWUGE9K6HYHVHQIG5DUCHP7AM421GQ",
        "HBV2JXKQ9P4BGWGCB7DJB5GJIVRB45N3UR",
        "TE92WJABYJZV7IKEQGSE7PYPHYUZ8TVX2F",
        "4JX4TB3WQTJH3J4D182NAFEZS9W19MAIZ9",
        "5CSBM4RN3ICD73ZZ431VUMCP3K9XYTASTY",
        "S2A6CXIBC6JHZRRVCX5H5TZU7N6RTF1UGH",
        "NIJTT9QT87YKGETBY6JU8DYXHQGYCC21ZS",
        "HY983ZXH29HNBV8KFMTQZ41CRCIY6Q8HNJ",
        "DGUZ6UZ242U7R6HU2W9NBAGG8TA2VETCI7"					
    ],
    "bsc": [
        "NYYFYM2GM9FPCFETAMHHBXN67X7PU46EB9"
    ],
    "polygon": [
        "7BTFI86WFGAAD91X2AGSF7YWBWC3M4R39S"
    ],
    "heco": [
        "7SMM4F12EQRRGKYCN2VK6I48R7M8CFNE8R"
    ]
}

PROVIDERS = {
    'eth': [
        "https://eth-mainnet.alchemyapi.io/v2/UOD8HE4CVqEiDY5E_9XbKDFqYZzJE3XP",
        "https://eth-mainnet.alchemyapi.io/v2/AgKT8OzbNsYnul856tenwnsnL3Pm7WRB",
        "https://eth-mainnet.alchemyapi.io/v2/gwlaWGMm1YWliQTvWtEHcjjfNXQ3W0lK",
    ]
}
