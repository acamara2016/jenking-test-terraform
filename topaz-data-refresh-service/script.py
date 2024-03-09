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

     endpoints = [
                 "mtv.de",
                 "mtv.es",
                 "mtv.it",
                 "mtv.nl",
                 "mtv.latam",
                 "mtvla.com",
                 "mtv.com.br",
                 "web.supertv.it",
                 "isleofmtv.com.mt",
                 "miaw.mtvla.com",
                 "web.mama.mtvafrica.com",
                 "jp.mtvvma.com",
                 "kca.mundonick.com.br",
                 "kca.mundonick.com",
                 "kca.la.mundonick.mx",
                 "kca.la.mundonick.com.br",
                 "kca.nickelodeonarabia.com",
                 "kca.nickelodeonabudhabi.com",
                 "web.slimefest.nick.co.uk",
                 "isleofmtv.com.tv",
                 "miaw.mtv.com.br",
                 "kca.nickelodeonafrica.com",
                 "kca.nick-asia.com",
                 "kca.nickelodeon.com.au",
                 "kca.nickelodeon.be",
                 "nickelodeon.com.br",
                 "kca.nickelodeon.dk",
                 "kca.nickelodeon.ee",
                 "kca.nickelodeon.fr",
                 "kca.nick.de",
                 "kca.nick.tv",
                 "kca.nickelodeon.gr",
                 "kca.nickelodeon.hu",
                 "kca.nicktv.it",
                 "kca.mundonick.com",
                 "kca.nickelodeon.lv",
                 "kca.nickelodeon.lt",
                 "kca.nickelodeonabudhabi.com",
                 "kca.nickelodeonarabia.com",
                 "kca.nickelodeon.nl",
                 "kca.nickelodeon.no",
                 "kca.nick.com.pl",
                 "kca.nickelodeon.pt",
                 "kca.nickelodeon.ro",
                 "kca.nickelodeon.ru",
                 "kca.nickelodeon.es",
                 "kca.nickelodeon.se",
                 "kca.nick.co.uk",
                 "kca.nickelodeon.ua",
                 "base.mtvema.com",
                 "asia.mtvema.com",
                 "br.mtvema.com",
                 "fr.mtvema.com",
                 "de.mtvema.com",
                 "tv.mtvema.com",
                 "hu.mtvema.com",
                 "in.mtvema.com",
                 "il.mtvema.com",
                 "it.mtvema.com",
                 "jp.mtvema.com",
                 "nl.mtvema.com",
                 "nordics.mtvema.com",
                 "pl.mtvema.com",
                 "pt.mtvema.com",
                 "ru.mtvema.com",
                 "es.mtvema.com",
                 "uk.mtvema.com",
                 "northamerica.mtvema.com",
                 "la.mtvema.com","logotv.com",
                 "ws.logo.com","cmt.com",
                 "ws.cmt.com","shared.smithsonian.us",
                 "ws.smithsonian.com","plutotv.com",
                 "showtime.com","shared.southpark.br",
                 "shared.southpark.br.en-us",
                 "shared.southpark.us.es",
                 "shared.southpark.uk",
                 "shared.southpark.global",
                 "shared.southpark.gsa.de",
                 "shared.southpark.gsa.en",
                 "shared.southpark.latam",
                 "shared.southpark.latam.en-us",
                 "shared.southpark.nordics",
                 "shared.southpark.us.en"]

    endpoint = sys.argv[1]
    host = "10.242.87.102"
    port = 6379

    startup_nodes = [{"host": host, "port": port}]
    r = RedisCluster(startup_nodes=startup_nodes, decode_responses=True, skip_full_coverage_check=True)

    fetch_and_process(endpoint, r)
