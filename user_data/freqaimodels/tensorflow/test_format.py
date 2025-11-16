import sys
import json
import pathlib
import operator

# REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent.parent
REPO_ROOT = pathlib.Path('./freqtrade/user_data/data/')

def main():
    if len(sys.argv) > 1:
        exchanges = (sys.argv[1], )
    else:
        # exchanges = ("binance", "kucoin")
        exchanges = ("binance")
    for exchange in exchanges:
        for path in REPO_ROOT.joinpath(exchange).rglob("*.json"):
            data = json.loads(path.read_text())
            path.write_text(
                json.dumps(
                    sorted(data, key=operator.itemgetter(0)),
                    separators=(',', ':')
                )
            )


if __name__ == "__main__":
    main()
