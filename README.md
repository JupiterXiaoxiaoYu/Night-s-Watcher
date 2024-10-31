**Related Resources**
Demo Video: https://youtu.be/hqfbKLt9ll4
Abnormal Detection AI Model Files: https://drive.google.com/drive/folders/12sopwv0cmZBEruWX5bFA9G-QeUDdaEOG?usp=drive_link
AI Training and Inference Code: https://drive.google.com/drive/folders/1bBnUpREW3McGhp71Ml4tXjmVlb-lid-K?usp=drive_link

##Track
Chain agnostic track and ZettaBlock - AI/Web3 Bounty
Here's how Night’s Watcher meets the sponsor(ZettaBlock) requirements:

1. **dApp for AI-Driven On-Chain Trading Fraud Detection:** Night’s Watcher serves as a decentralized application specifically built for on-chain fraud detection. By integrating AI and Web3 data, it provides comprehensive monitoring and real-time risk alerts, identifying high-risk transactions, abnormal accounts, and potential vulnerabilities in smart contracts.

2. **Use of Web3 Data and AI Modeling:** The project employs extensive Web3 transaction data and combines it with an AI model trained to detect risky accounts. With fine-tuning to analyze specific tags, the model leverages blockchain data to identify malicious patterns in transactions and contract interactions.

3. **Innovative Fraud Detection with Small Sample Learning:** Night’s Watcher is unique in applying small sample learning to assess high-risk accounts and contracts, even with limited initial data. This enables efficient detection of trading fraud, such as phishing, rug pulls, and liquidity vulnerabilities.

## Project Overview
Night's Watcher is an innovative blockchain security monitoring tool that combines AI with formal verification to provide users with comprehensive risk identification and alerts. This tool focuses on detecting abnormal accounts and potential contract risks in blockchain transactions, aiming to ensure user security in new ecosystems, applications, and assets.

## Features

### Innovation in Small Sample Learning Application  
Night's Watcher is the first project in the industry to use small sample learning to identify high-risk accounts and smart contracts. By pre-training on a large dataset of Ethereum transactions and fine-tuning for four specific tags, Night's Watcher can accurately identify suspicious accounts. Even with limited sample data, it effectively detects potential risks.

### Multi-Dimensional Economic Security Formal Verification 
The project also innovatively integrates Certora formal verification technology to analyze and validate interactions related to economic security (such as AMM and lending protocols). This is one of the few tools in the industry that provides comprehensive formal verification of economic security properties for smart contract interactions, automatically detecting potential threats like liquidity vulnerabilities, phishing attacks, and rug pull risks.

## Progress and Effort

### Model Training and Fine-Tuning
We have completed model pre-training on large-scale Ethereum transaction data and fine-tuned it for four specific tags (e.g., blacklisted accounts, high-risk accounts). Through this training and optimization, Night's Watcher can accurately identify abnormal accounts, providing users with efficient risk alerts.

### Identification of Blacklisted Accounts and Risk Alerts/Reports
Night's Watcher can detect blacklisted accounts across a batch of smart contracts. Users simply input the addresses of interest, and the system will automatically analyze related high-risk accounts, providing risk alerts and detailed reports on these contracts.

### Formal Verification
The system supports formal verification for smart contracts in Solidity version 6.0 and above. The verification focuses on economic security properties such as liquidity vulnerabilities, phishing attack risks, and rug pull risks. Through formal verification, Night's Watcher can quantify the risk level and provide corresponding alerts and recommendations. (Sample Formal Verification Report)

## Feasibility and Future Development
Future development directions include:

1. **Network-Wide Transaction Processing**: We will gradually process network-wide transactions to enable the model to identify blacklisted accounts. By obtaining a comprehensive blacklist, we can offer more comprehensive risk alerts for the respective smart contracts.
   
2. **Expanding Formal Verification Categories**: As the system evolves, we will continue to add more smart contract and interaction scenarios for formal verification, further enhancing Night's Watcher’s security detection capabilities.

## Social Value
According to statistics, the blockchain industry lost $743 million to security vulnerabilities in Q3 2024, with the Ethereum ecosystem most affected. Night's Watcher empowers users with advanced capabilities to detect emerging risks, vulnerabilities, and suspicious accounts, providing robust security in exploring new ecosystems, applications, and assets.

By proactively identifying potential security threats and issuing risk alerts, Night's Watcher contributes to the healthy development of the blockchain ecosystem, helping reduce asset losses for users in emerging ecosystems.

## Code Modularity
Night's Watcher is built with a high-quality code architecture, utilizing a modular design to ensure code maintainability and scalability:

- **AI Training Module**: Manages model pre-training and fine-tuning, supporting iterative training and optimization with new data.
- **AI Inference Module**: Handles online inference, analyzing user-inputted contracts in real time and outputting detection results.
- **Blacklist/Whitelist Database Matching Module**: Stores and manages detected blacklisted accounts for efficient querying and risk assessment.
- **Frontend Module**: Provides a user-friendly interface displaying risk alerts, verification results, and reports.
- **Formal Verification Module**: Conducts Certora formal verification on smart contracts and outputs actionable verification reports.
- **AI Reporting Module**: Presents technical detection reports to users in an easy-to-understand format.

Night's Watcher's code design ensures efficient collaboration between modules and flexibility for future feature additions and evolving needs.

## Conclusion
Through innovative technology, powerful features, and a reliable code architecture, Night's Watcher is committed to providing comprehensive security for blockchain users. In the future, we will continue to improve model optimization and expand formal verification, creating a safer blockchain experience for users.

## License
This project is licensed under the MIT License. You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of this software, provided that the following conditions are met:

### Permission Notice
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the software.

### Warranty Disclaimer
This software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.
