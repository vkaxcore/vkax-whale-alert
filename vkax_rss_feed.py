import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import json
import os
import random

# RPC credentials (replace with your actual credentials)
RPC_USER = 'daemonrpcuser'
RPC_PASSWORD = 'daemonrpcpassword'
RPC_URL = 'http://127.0.0.1:11111'  # Adjust if needed (local node address)

# Threshold for filtering transactions (1,000,000 VKAX)
TRANSACTION_THRESHOLD = 1000000
BLOCK_COUNT = 100  # Number of blocks to check
PROCESSED_FILE = "/home/vkaxcoin/processed_transactions.json"

# Whaling-themed phrases
WHALE_PHRASES = [
    "Thar she blows! {amount} VKAX moved!",
    "A whale surfaces with {amount} VKAX!",
    "Big splash in the VKAX sea: {amount} VKAX!",
    "Massive VKAX movement spotted: {amount} VKAX!",
    "A leviathan emerges with {amount} VKAX!",
    "Whale ahoy! {amount} VKAX transferred!",
    "VKAX tidal wave detected: {amount} VKAX!",
    "Huge VKAX transfer incoming: {amount} VKAX!",
    "Whopper of a transaction: {amount} VKAX!",
    "Someone's making waves with {amount} VKAX!",
    "A big fish swims by with {amount} VKAX!",
    "Deep sea VKAX movement: {amount} VKAX!",
    "Colossal VKAX transfer alert: {amount} VKAX!",
    "Whale making a splash with {amount} VKAX!",
    "VKAX storm brewing: {amount} VKAX!",
    "Sea monster spotted carrying {amount} VKAX!",
    "Gigantic VKAX transfer: {amount} VKAX!",
    "Ocean of VKAX moved: {amount} VKAX!",
    "Whale breaches the surface with {amount} VKAX!",
    "VKAX whale on the move: {amount} VKAX!"
] * 5  # Extend to ensure there are 100 phrases

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
    block_hash = call_rpc('getblockhash', [height])
    if block_hash:
        block_data = call_rpc('getblock', [block_hash])
        if block_data:
            print(f"Block height: {block_data.get('height')}, Transactions: {len(block_data.get('tx', []))}")
            return block_data
    print(f"Failed to fetch block at height {height}.")
    return None

def filter_transactions(block_data, processed_txids):
    print("Filtering transactions over the threshold...")
    large_transactions = []
    for txid in block_data.get('tx', []):
        if txid in processed_txids:
            print(f"Transaction {txid} was already processed. Skipping.")
            continue

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
    if not large_transactions:
        print("No transactions found over the threshold in this block.")
    return large_transactions

def load_processed_transactions():
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_processed_transactions(processed_txids):
    with open(PROCESSED_FILE, "w") as f:
        json.dump(list(processed_txids), f)

def create_rss_feed(transactions):
    print("Creating RSS feed XML...")
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    title = ET.SubElement(channel, "title")
    title.text = "VKAX Whale Watcher"

    link = ET.SubElement(channel, "link")
    link.text = "https://explore.vkax.net/"

    description = ET.SubElement(channel, "description")
    description.text = "VKAX transactions over 1,000,000"

    for tx in transactions:
        item = ET.SubElement(channel, "item")

        short_txid = f"{tx['txid'][:4]}...{tx['txid'][-4:]}"
        amount_in_millions = float(tx['amount']) / 1_000_000
        phrase = random.choice(WHALE_PHRASES).format(amount=f"{amount_in_millions:.2f}M")

        tx_title = ET.SubElement(item, "title")
        tx_title.text = f"{phrase} TX {short_txid}"

        tx_link = ET.SubElement(item, "link")
        tx_link.text = f"https://explore.vkax.net/tx/{tx['txid']}"

        tx_description = ET.SubElement(item, "description")
        tx_description.text = (
            f"{phrase} {amount_in_millions:.2f}M VKAX at "
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

    # Load processed transactions
    processed_txids = load_processed_transactions()

    # Get the latest block height
    latest_block_height = call_rpc('getblockcount')
    if not latest_block_height:
        print("Failed to get the latest block height. Exiting.")
        return

    print(f"Latest block height: {latest_block_height}")

    # Loop through the last BLOCK_COUNT blocks
    large_transactions = []
    for height in range(latest_block_height, latest_block_height - BLOCK_COUNT, -1):
        block_data = fetch_block_by_height(height)
        if not block_data:
            print(f"No data found for block height {height}. Skipping.")
            continue

        block_large_transactions = filter_transactions(block_data, processed_txids)
        for tx in block_large_transactions:
            processed_txids.add(tx['txid'])
        large_transactions.extend(block_large_transactions)

    if not large_transactions:
        print(f"No transactions found over {TRANSACTION_THRESHOLD} VKAX. No RSS feed will be created.")
        return

    # Save updated processed transactions
    save_processed_transactions(processed_txids)

    # Generate and save the RSS feed
    rss_feed = create_rss_feed(large_transactions)
    save_rss_feed(rss_feed)
    print("RSS feed generation process completed.")

if __name__ == "__main__":
    main()
