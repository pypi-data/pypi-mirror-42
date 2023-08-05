# GO Quant Data Client API v1
Build local csv database and get stock daily open, high, low, close, volume.
Client also support all original API function of quandl and jqdata.

version 0.0.4
## Install
```bash
pip install goquantdata
```
## Usage
#### Quick Start
Example 1. Build Local DB and Get symbol open, close, high, low, volume
```python
from datetime import datetime
import goquantdata
from os.path import expanduser
import goquantdata.local.private_config as cfg

client = goquantdata.LocalClient(db_dir=expanduser("~") + '/data/localdb/',
                                 key_quandl=cfg.CONFIG_QUANDL['api_key'],
                                 jq_password=cfg.CONFIG_JQDATA['password'],
                                 jq_username=cfg.CONFIG_JQDATA['username'],
                                 key_alpha_vantage=cfg.CONFIG_ALPHA_VANTAGE['api_key'])
start_date = datetime.strptime("20190102", "%Y%m%d")
end_date = datetime.strptime("20190120", "%Y%m%d")
ids_us = ["AAPL", "AMD", "TD"]
ids_cn = ["ZN9999.XSGE", "ZC9999.XZCE"]

client.build_db(start_date=start_date,
                end_date=end_date,
                ids_us=ids_us,
                ids_cn=ids_cn)

df = client.get_price(market="us",
                      ids=["TD", "AMD"],
                      start_date=start_date,
                      end_date=end_date)
print(df)

df = client.get_price(market="cn",
                      ids=["ZC9999.XZCE"],
                      start_date=start_date,
                      end_date=end_date)
print(df)
```
Example 2. use original sdk function
To use original sdk function, for jqdata use "jq_{name of function}",
for quandl, use "ql_{name of function}"
```python
# use original sdk function
df = client.jq_get_price(security=["601228.XSHG"],
                         start_date=start_date,
                         end_date=end_date,
                         frequency='daily',
                         fields=None,
                         skip_paused=False,
                         fq='pre',
                         count=None)
print(df)
```
## Output Format
- get_price return dataframe

| symbol      | date        | open        | high        | low         | close       | volume      | market |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| AAPL        | 2017-01-03  | 114.369701  | 114.893155  | 113.342546  | 114.715378  | 28781865.0  | us |

## Data Source
| Market      | Client Type | Default Universe | Source |
| ----------- | ----------- | ----------- | ----------- |
| cn stock    | local | xshg300 | [JQData](https://www.joinquant.com/help/api/help?name=Stock) |
| us stock  | local | sp500 | [Alpha Vantage](https://alpha-vantage.readthedocs.io/en/latest/source/alpha_vantage.html) |
