import csv
import requests
from StringIO import StringIO
import simplejson as json
from path import path


SPREADSHEET_CSV_URL_TEMPLATE = (
    'https://docs.google.com/spreadsheet/pub'
    '?key={key}&single=true&gid=0&output=csv'
)

def create_csv_url(key):
    return SPREADSHEET_CSV_URL_TEMPLATE.format(key=key)


def get_gdrive_csv(key):
    url = create_csv_url(key)
    resp = requests.get(url)
    assert resp.headers['Content-Type'] == 'text/csv'
    text = resp.content
    return csv.DictReader(StringIO(text))


new_data = {}
for row in get_gdrive_csv('0ApN4Tp2ea9EKdG8yWHB2VWxieGlTMkM4Nm1ENzhVc2c'):
    if row['id']:
        row['id'] = int(row['id'])
        new_data[row['id']] = row

p = path('biblioteci.geojson')
data = json.loads(p.text())
for feature in data['features']:
    properties = feature['properties']
    row = new_data[properties['id']]
    properties.update(row)

p.write_text(json.dumps(data, sort_keys=True, indent=4))
