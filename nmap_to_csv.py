import sys, pandas as pd
from lxml import etree

xml = etree.parse(sys.argv[1])
rows = []
for host in xml.xpath('//host'):
    addr = host.xpath('./address/@addr')
    ip = addr[0] if addr else ''
    for port in host.xpath('.//port'):
        proto = port.get('protocol')
        p = port.get('portid')
        state = port.xpath('./state/@state')[0]
        svc = port.xpath('./service/@name')
        product = port.xpath('./service/@product')
        rows.append({
            'ip': ip, 'protocol': proto, 'port': p,
            'state': state, 'service': svc[0] if svc else '',
            'product': product[0] if product else ''
        })
df = pd.DataFrame(rows)
out = sys.argv[2] if len(sys.argv)>2 else 'nmap.csv'
df.to_csv(out, index=False)
print(f'Wrote {out} with {len(df)} rows')
