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
    "Thar she blows!",
    "A whale surfaces!",
    "Big splash in the VKAX sea!",
    "Massive VKAX movement spotted!",
    "A leviathan emerges!",
    "Whale ahoy!",
    "VKAX tidal wave detected!",
    "Huge VKAX transfer incoming!",
    "Whopper of a transaction!",
    "Someone's making waves with VKAX!",
    "A big fish swims by!",
    "Deep sea VKAX movement!",
    "Colossal VKAX transfer alert!",
    "Whale making a splash!",
    "VKAX storm brewing!",
    "Sea monster spotted!",
    "Gigantic VKAX transfer!",
    "Ocean of VKAX moved!",
    "Whale breaches the surface!",
    "VKAX whale on the move!",
    "Kraken stirs in the VKAX depths!",
    "Enormous VKAX migration detected!",
    "Whale spouts spotted on the horizon!",
    "Splash! Whale activity in VKAX waters!",
    "The VKAX ocean just rippled big time!",
    "A deep dive reveals massive VKAX movement!",
    "Leviathan on the loose with VKAX!",
    "Wave after wave of VKAX splashes ashore!",
    "Whale tail spotted breaking VKAX waters!",
    "A monstrous VKAX exchange brews!",
    "Gigantic VKAX surge detected!",
    "Humpback-sized VKAX transaction!",
    "VKAX tides rise with this massive splash!",
    "Spectacular VKAX breach underway!",
    "Underwater VKAX explosion detected!",
    "Whale sighting confirmed in VKAX currents!",
    "Deep-sea VKAX avalanche incoming!",
    "A great white of VKAX just swam by!",
    "VKAX waters churn as whales emerge!",
    "Megalodon-sized VKAX transfer detected!",
    "A VKAX tsunami is in motion!",
    "Orca pod on the VKAX move!",
    "Whales gather for a VKAX feeding frenzy!",
    "The VKAX sea just shifted dramatically!",
    "Massive VKAX current detected in the depths!",
    "Titanic VKAX movement surges forward!",
    "A hidden VKAX treasure trove surfaces!",
    "A wave of VKAX magnitude shakes the sea!",
    "An ancient VKAX beast awakens!",
    "Monumental VKAX splash echoes across waters!",
    "Thundering VKAX transfer roars ashore!",
    "Whale watchers report massive VKAX stirrings!",
    "Big fin sighted in the VKAX waters!",
    "Churning seas of VKAX activity observed!",
    "Depth charge of VKAX makes an impact!",
    "Humpback VKAX breach leaves a wake!",
    "A tide-turning VKAX transaction!",
    "Massive VKAX pod makes waves!",
    "The VKAX deep just yielded a giant catch!",
    "A behemoth VKAX movement shatters the calm!",
    "Poseidon's VKAX bounty unleashed!",
    "Mysterious VKAX transfer breaks the surface!",
    "The VKAX abyss just shifted profoundly!",
    "Colossus-class VKAX spotted in the wild!",
    "An aquatic marvel of VKAX magnitude!",
    "Herculean VKAX transfer detected!",
    "Depths tremble as VKAX leviathan stirs!",
    "Cataclysmic VKAX splash hits the radar!",
    "Deep-sea VKAX vortex spinning wildly!",
    "Gigantic VKAX footprint on the horizon!",
    "A cascade of VKAX in the sea's embrace!",
    "Behemoth VKAX flow reported in waters!",
    "Astronomical VKAX splash shakes observers!",
    "Immense VKAX whale breaches surface calm!",
    "An empire's worth of VKAX moves!",
    "Cascading VKAX energies breach the ocean!",
    "Massive VKAX flurry detected!",
    "A torrent of VKAX erupts from the abyss!",
    "Whale watchers marvel at VKAX spectacle!",
    "A surge of VKAX majesty breaks out!",
    "Awe-inspiring VKAX movement across seas!",
    "Megaton VKAX transfer shakes the ocean floor!",
    "Tectonic VKAX activity ripples through!",
    "The VKAX ledger roars with this transfer!",
    "A monumental VKAX cascade observed!",
    "Vast VKAX riches move beneath the waves!",
    "Titanic VKAX surge shocks the surface!",
    "An unprecedented VKAX journey underway!",
    "Legends tell of VKAX movements like these!",
    "Awe-striking VKAX transfer rocks the sea!",
    "History-making VKAX splash recorded!",
    "Legendary VKAX transfer in the annals!",
    "The VKAX ocean speaks of great depths moved!"
] * 5  # Extend to ensure there are enough desired phrases

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
        phrase = random.choice(WHALE_PHRASES)

        tx_title = ET.SubElement(item, "title")
        tx_title.text = f"{phrase} TX {short_txid} ({amount_in_millions:.2f}M)"

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
