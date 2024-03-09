import sys
import requests
from rediscluster import RedisCluster
import xml.etree.ElementTree as ET
import json
from tqdm import tqdm

def get_feed_url(endpoint, page_number):
    return f"https://feeds.mtvnservices.com/od/feed/google-dai-od?namespace={endpoint}&ingestdomain=topaz.viacomcbs.digital&page={page_number}&stage=live"

def fetch_and_process(endpoint, r):
    processed_pages = 0
    total_items_processed = 0
    new_items_refreshed = 0
    existing_items_refreshed = 0

    while True:
        url = get_feed_url(endpoint, processed_pages + 1)
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch data from {url}")
            break

        root = ET.fromstring(response.content)

        items = root.findall('.//item')
        if not items:
            print("No more items found. Exiting.")
            break

        with tqdm(total=len(items), desc="Processing pages", unit="item") as pbar:
            for item in items:
                content_id = item.find('.//dfpvideo:contentID', namespaces={'dfpvideo': 'http://api.google.com/dfpvideo'}).text
                fw_caid = item.find('.//dfpvideo:fw_caid', namespaces={'dfpvideo': 'http://api.google.com/dfpvideo'}).text
                last_modified_date = item.find('.//dfpvideo:lastModifiedDate', namespaces={'dfpvideo': 'http://api.google.com/dfpvideo'}).text

                refresh_key = f"refresh_{endpoint}_{fw_caid}"
                cached_entry = r.get(refresh_key)

                if cached_entry:
                    cached_data = json.loads(cached_entry)
                    if last_modified_date > cached_data["lastModifiedDate"]:
                        cached_data["lastModifiedDate"] = last_modified_date
                        r.set(refresh_key, json.dumps(cached_data))
                        existing_items_refreshed += 1
                else:
                    cached_data = {"lastModifiedDate": last_modified_date, "contentID": content_id}
                    r.set(refresh_key, json.dumps(cached_data))
                    new_items_refreshed += 1

                total_items_processed += 1
                pbar.set_description(f"Processed (page {processed_pages + 1}): {total_items_processed}, New: {new_items_refreshed}, Existing: {existing_items_refreshed}")
                pbar.update(1)

        next_link = root.find('.//{http://www.w3.org/2005/Atom}link[@rel="next"]')
        if next_link is None:
            break
        
        processed_pages += 1

# Example usage
if __name__ == "__main__":
    # if len(sys.argv) != 4:
    #     print(sys.argv)
    #     print("Usage: python script.py <endpoint> <host> <port>")
    #     sys.exit(1)

    endpoint = sys.argv[1]
    host = "10.242.87.102"
    port = 6379

    startup_nodes = [{"host": host, "port": port}]
    r = RedisCluster(startup_nodes=startup_nodes, decode_responses=True, skip_full_coverage_check=True)

    fetch_and_process(endpoint, r)
