#!/usr/bin/env python

from path import path
from tempfile import mkdtemp
import subprocess

KML_URL = ('https://maps.google.com/maps/ms'
           '?ie=UTF8&authuser=0&msa=0&output=kml'
           '&msid=208998566086571369738.0004c43c4b29de7addc2f')

PROJECT_DIR = path(__file__).abspath().parent


def main():
    tmp = path(mkdtemp(dir=PROJECT_DIR))

    try:
        download_kml = tmp / 'download.kml'
        tmp_out = tmp / 'out.geojson'
        biblioteci_geojson = PROJECT_DIR / 'biblioteci.geojson'

        with open(download_kml, 'wb') as f:
            subprocess.check_call(['curl', KML_URL], stdout=f)

        subprocess.check_call([
            'ogr2ogr',
            '-f', 'geojson',
            tmp_out,
            download_kml,
        ])

        tmp_out.rename(biblioteci_geojson)

    finally:
        tmp.rmtree()


if __name__ == '__main__':
    main()
