import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# RPC credentials (replace with your actual credentials)
RPC_USER = 'daemonrpcuser'
RPC_PASSWORD = 'daemonrpcpassword'
RPC_URL = 'http://127.0.0.1:11111'  # Adjust if needed (local node address)

# Threshold for filtering transactions (1M VKAX)
TRANSACTION_THRESHOLD = 1000000
BLOCK_COUNT = 100  # Number of blocks to check

# Helper function to call the local blockchain RPC
def call_rpc(method, params=[]):
    """Call the local blockchain RPC and handle errors."""
    headers = {'Content-Type': 'application/json'}
    data = {
        "jsonrpc": "1.0",
        "id": "python-rpc",
        "method": method,
        "params": params
    }
    try:
        response = requests.post(RPC_URL, json=data, headers=headers, auth=(RPC_USER, RPC_PASSWORD))
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.json().get('result', None)
    except requests.exceptions.RequestException as e:
        print(f"RPC request failed ({method}): {e}")
        return None

def fetch_block_by_height(height):
    """Fetch block data by its height."""
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
    """Filter transactions over the threshold."""
    print("Filtering transactions over the threshold...")
    large_transactions = []
    for txid in block_data.get('tx', []):
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
    """Create the RSS feed XML."""
    print("Creating RSS feed XML...")
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    title = ET.SubElement(channel, "title")
    title.text = "VKAX High Value Transactions"
    link = ET.SubElement(channel, "link")
    link.text = "https://your-site-url.com"
    description = ET.SubElement(channel, "description")
    description.text = "Feed for VKAX transactions over 1,000,000 VKAX"

    for tx in transactions:
        item = ET.SubElement(channel, "item")
        tx_title = ET.SubElement(item, "title")
        tx_title.text = f"Transaction {tx['txid']}"
        
        # Use space-saving notation (e.g., "10K" instead of "10,000")
        amount = float(tx['amount'])
        formatted_amount = f"{amount / 1000000:.2f}M" if amount >= 1000000 else f"{amount / 1000:.2f}K" if amount >= 1000 else str(amount)

        tx_link = ET.SubElement(item, "link")
        tx_link.text = f"https://explore.vkax.net/tx/{tx['txid']}"
        
        tx_description = ET.SubElement(item, "description")
        tx_description.text = (
            f"Transaction of {formatted_amount} VKAX at "
            f"{datetime.utcfromtimestamp(tx['time']).strftime('%Y-%m-%d %H:%M:%S')} UTC"
        )

    print("RSS feed creation complete.")
    return ET.tostring(rss, encoding="utf-8")

def save_rss_feed(rss_feed):
    """Save the generated RSS feed to a file."""
    filename = "vkax_high_value_transactions.xml"
    with open(filename, "wb") as f:
        f.write(rss_feed)
    print(f"RSS feed saved to {filename}")

def main():
    """Main function to generate the RSS feed."""
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
