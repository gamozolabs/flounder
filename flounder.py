import requests, json, time, sys

# This script takes in a search query and a bing subscription key and
# generates a file containing all the links from the query. This file with
# links can then be used by download.py to download the files mentioned by
# the links

market_codes = [
    "es-AR",
    "en-AU",
    "de-AT",
    "nl-BE",
    "fr-BE",
    "pt-BR",
    "en-CA",
    "fr-CA",
    "es-CL",
    "da-DK",
    "fi-FI",
    "fr-FR",
    "de-DE",
    "zh-HK",
    "en-IN",
    "en-ID",
    "it-IT",
    "ja-JP",
    "ko-KR",
    "en-MY",
    "es-MX",
    "nl-NL",
    "en-NZ",
    "no-NO",
    "zh-CN",
    "pl-PL",
    "en-PH",
    "ru-RU",
    "en-ZA",
    "es-ES",
    "sv-SE",
    "fr-CH",
    "de-CH",
    "zh-TW",
    "tr-TR",
    "en-GB",
    "en-US",
    "es-US",
]

if len(sys.argv) < 3:
    print("""
Usage:
    For non-image files: flounder.py <bing subscription key> <search query>
    For image files:     flounder.py <bing subscription key> <search query> --imagesearch=<image file type>

For example: flounder.py BINGKEYHERE \"filetype:rtf\"
For searching for images: flounder.py BINGKEYHERE bananas --imagesearch=png
""")
    quit()

subscription_key = sys.argv[1]

image_search = None
if len(sys.argv) == 4:
    assert sys.argv[3].startswith("--imagesearch=")
    image_search = sys.argv[3].split("--imagesearch=", maxsplit=1)[1]

url_log = open("urllog_%s.txt" % time.time(), "wb")

for offset in range(0, 1000000, 50):
    for market in market_codes:
        if image_search == None:
            search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search?count=50&mkt=%s&offset=%d" % (market, offset)
        else:
            search_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search?count=50&mkt=%s&offset=%d" % (market, offset)

        search_term = sys.argv[2] # Example: "some keywords filetype:rtf"

        headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
        params  = {"q": search_term, "textDecorations":True, "textFormat":"HTML"}
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()

        #print(json.dumps(search_results, indent=4, sort_keys=True))

        if search_results["_type"] == "SearchResponse":
            for result in search_results["webPages"]["value"]:
                print(result["url"])
                url_log.write(result["url"].encode() + b"738ced42e85db6ed9095b29dc94b9253")
                url_log.flush()

            time.sleep(0.5)
        elif search_results["_type"] == "Images":
            for result in search_results["value"]:
                # Filter to only save images of the type requested
                if "encodingFormat" in result and result["encodingFormat"] == image_search:
                    print(result["contentUrl"])
                    url_log.write(result["contentUrl"].encode() + b"738ced42e85db6ed9095b29dc94b9253")
                    url_log.flush()
        else:
            assert 1==2, "Unexpected search result type"

