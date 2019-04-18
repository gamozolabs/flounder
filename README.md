# Usage

First generate a list of URLs using a Bing search with flounder:

`python3 flounder.py <bing api key> <bing api search term>`

Then download the files:

`python3 download.py <founder URL list> <file extension>`

# Download.py

`download.py` implements a filter in Python to delete files which do not match a given criteria. Right now it's an example that has an RTF filter, but feel free to add whatever filter you dream of.

# Example

```
python3 flounder.py YOURBINGAPIKEY filetype:rtf
python3 download.py urllog_1555546041.8930097.txt
```

And that's it! The `urllog` file varies based on the time so, and `download.py` just downloads all files in the `urllog` and filter them accordingly (in this case checks for an RTF header)

# Dependencies

You need requests `python3 -m pip install requests`

