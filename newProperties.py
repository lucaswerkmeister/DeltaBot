# !/usr/bin/python
# -*- coding: UTF-8 -*-
# licensed under CC-Zero: https://creativecommons.org/publicdomain/zero/1.0

from __future__ import unicode_literals
import datetime
import pywikibot
import re
import requests

site = pywikibot.Site('wikidata', 'wikidata')
repo = site.data_repository()
page = pywikibot.Page(site, 'Wikidata:Status updates/Next')

lastweek = pywikibot.Timestamp.today() - datetime.timedelta(days=7)
payload = {
    'action': 'query',
    'list': 'recentchanges',
    'rctype': 'new',
    'rcnamespace': '120',
    'rclimit': 100,
    'rcend': str(lastweek),
    'format': 'json'
}

r = requests.get('https://www.wikidata.org/w/api.php', params=payload)
data = r.json()

if len(data['query']['recentchanges']) == 0:
    text = 'none'
else:
    props = []
    for m in data['query']['recentchanges']:
        entity = pywikibot.PropertyPage(repo, m['title'].replace('Property:', ''))
        entity.get()
        if 'en' in entity.labels:
            props.append('[[:d:{0}|{1}]]'.format(m['title'], entity.labels['en']))
        else:
            props.append('[[:d:{0}|{1}]]'.format(m['title'], m['title'].replace('Property:', '')))
    text = ', '.join(props)

header = '<!-- NEW PROPERTIES DO NOT REMOVE -->'
footer = '<!-- END NEW PROPERTIES -->'
pretext = '* Newest [[d:Special:ListProperties|properties]]: '

newtext = re.sub(header + '.*' + footer, header + '\n' + pretext + text + '\n' + footer, page.get(), flags=re.DOTALL)
page.put(newtext, 'Bot: Updating list of new properties')
