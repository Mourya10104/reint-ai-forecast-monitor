import requests
from datetime import datetime, timedelta

def test_api():
    # Dates
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    
    # test FUELHH (B1620)
    # The Insights Solution API endpoint: https://data.elexon.co.uk/bmrs/api/v1/generation/outturn/summary
    # actually let's try https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH
    
    # Actually 'generation/outturn/summary' is fuel type outturn. Or 'generation/outturn/half-hourly'
    print("Fetching half-hourly generation by fuel type...")
    url = f"https://data.elexon.co.uk/bmrs/api/v1/generation/outturn/FUELHH" # this is a guess, let's use the explicit datasets endpoint
    
    url = f"https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH"
    params = {
        "publishTime": f"{yesterday.isoformat()}T00:00:00Z",
        "format": "json"
    }
    # For datasets it's usually settleDate or something, but let's just try settlementDate=yesterday
    params = {"settlementDate": yesterday.isoformat(), "format": "json"}
    res = requests.get(url, params=params)
    if res.status_code == 200 and 'data' in res.json():
        print("FUELHH:")
        data = res.json()['data']
        if data:
            print("Row 0 keys:", data[0].keys())
            print("Row 0 sample:", {k: data[0][k] for k in list(data[0].keys())[:5]})
    else:
        print("FUELHH dataset Error:", res.text[:200])

    print("Fetching WINDFOR...")
    url = f"https://data.elexon.co.uk/bmrs/api/v1/datasets/WINDFOR"
    res = requests.get(url, params=params)
    if res.status_code == 200 and 'data' in res.json():
        print("WINDFOR:")
        data = res.json()['data']
        if data:
            print("Row 0 keys:", data[0].keys())
            print("Row 0 sample:", {k: data[0][k] for k in list(data[0].keys())[:5]})
    else:
        print("WINDFOR Error:", res.text[:200])


if __name__ == "__main__":
    test_api()
