import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# RPC credentials (replace with your actual credentials)
RPC_USER = 'daemonrpcuser'
RPC_PASSWORD = 'daemonrpcpassword'
RPC_URL = 'http://127.0.0.1:11111'  # Adjust if needed (local node address)

# Threshold for filtering transactions (1000000 VKAX)
TRANSACTION_THRESHOLD = 1000000
BLOCK_COUNT = 100  # Number of blocks to check

# Helper function to call the local blockchain RPC
def call_rpc(method, params=[]):
    headers = {'Content-Type': 'application/json'}
    data = {
        "jsonrpc": "1.0",
        "id": "python-rpc",
        "method": method,
        "params": params
    }
    try:
        response = requests.post(RPC_URL, json=data, headers=headers, auth=(RPC_USER, RPC_PASSWORD))

        if response.status_code == 200:
            return response.json().get('result', None)
        else:
            print(f"RPC error ({method}): {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"RPC request failed ({method}): {e}")
        return None

def fetch_block_by_height(height):
    print(f"Fetching block at height {height}...")
    block_data = call_rpc('getblockhash', [height])
    if block_data:
        block_data = call_rpc('getblock', [block_data])
        if block_data:
            print(f"Block height: {block_data.get('height')}, Transactions: {len(block_data.get('tx', []))}")
        return block_data
    else:
        print(f"Failed to fetch block at height {height}.")
        return None

def filter_transactions(block_data):
    print("Filtering transactions over the threshold...")
    large_transactions = []
    for txid in block_data['tx']:
        print(f"Processing transaction ID: {txid}")
        raw_tx = call_rpc('getrawtransaction', [txid, True])
        if raw_tx and 'vout' in raw_tx:
            for output in raw_tx['vout']:
                if 'value' in output and float(output['value']) > TRANSACTION_THRESHOLD:
                    print(f"Transaction {txid} has an output of {output['value']} VKAX, exceeding the threshold.")
                    large_transactions.append({
                        'txid': txid,
                        'amount': output['value'],
                        'time': block_data.get('time', 0)
                    })
        else:
            print(f"Failed to decode transaction {txid} or no outputs found.")
    return large_transactions

def create_rss_feed(transactions):
    print("Creating RSS feed XML...")
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    # Updated Title and Link
    title = ET.SubElement(channel, "title")
    title.text = "VKAX Whale Watcher"

    link = ET.SubElement(channel, "link")
    link.text = "https://explore.vkax.net/"

    # Updated Description
    description = ET.SubElement(channel, "description")
    description.text = "VKAX transactions over 1,000,000"

    for tx in transactions:
        item = ET.SubElement(channel, "item")

        # Shortened transaction ID (first 4 and last 4 characters)
        short_txid = f"{tx['txid'][:4]}...{tx['txid'][-4:]}"

        # Format the amount in millions and make sure it shows as 2m instead of 2000000.0M
        amount_in_millions = float(tx['amount']) / 1_000_000
        tx_title = ET.SubElement(item, "title")
        tx_title.text = f"TX {short_txid} ({amount_in_millions:.2f}M)"

        # Full transaction ID for the link
        tx_link = ET.SubElement(item, "link")
        tx_link.text = f"https://explore.vkax.net/tx/{tx['txid']}"

        # Description with formatted amount
        tx_description = ET.SubElement(item, "description")
        tx_description.text = (
            f"{amount_in_millions:.2f}M VKAX at "
            f"{datetime.utcfromtimestamp(tx['time']).strftime('%Y-%m-%d %H:%M')} UTC"
        )

    print("RSS feed creation complete.")
    return ET.tostring(rss, encoding="utf-8")

def save_rss_feed(rss_feed):
    filename = "vkax_high_value_transactions.xml"
    with open(filename, "wb") as f:
        f.write(rss_feed)
    print(f"RSS feed saved to {filename}")

def main():
    print("Starting RSS feed generation process...")

    # Get the latest block height
    latest_block_height = call_rpc('getblockcount')
    if not latest_block_height:
        print("Failed to get the latest block height. Exiting.")
        return

    # Loop through the last 100 blocks
    large_transactions = []
    for height in range(latest_block_height, latest_block_height - BLOCK_COUNT, -1):
        block_data = fetch_block_by_height(height)
        if not block_data:
            print(f"No data found for block height {height}. Skipping.")
            continue

        # Filter the transactions for the current block
        block_large_transactions = filter_transactions(block_data)
        large_transactions.extend(block_large_transactions)

    if not large_transactions:
        print(f"No transactions found over {TRANSACTION_THRESHOLD} VKAX. No RSS feed will be created.")
        return

    rss_feed = create_rss_feed(large_transactions)
    save_rss_feed(rss_feed)
    print("RSS feed generation process completed.")

if __name__ == "__main__":
    main()
