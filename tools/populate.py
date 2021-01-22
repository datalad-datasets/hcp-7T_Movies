#!/usr/bin/env python3

import os.path as op
import sys
import xml.dom.minidom

import datalad.api as dl
from datalad.support.network import download_url

ds = dl.Dataset(op.dirname(op.dirname(op.realpath(__file__))))

if 'datalad' not in ds.repo.get_remotes():
    from datalad.customremotes.base import init_datalad_remote
    init_datalad_remote(ds.repo, 'datalad', autoenable=True)

# doc = xml.dom.minidom.parse('/tmp/outi-7T.xml')
topurl = 'https://db.humanconnectome.org/data/archive/projects/HCP_Resources/resources/7T_Movies/'
doc = xml.dom.minidom.parseString(download_url(topurl))

files = [{f: e.getAttribute(f) for f in ('ID', 'URI', 'digest', 'name')}
         for e in doc.getElementsByTagName("cat:entry")]
# from pprint import pprint
# pprint(files)
added = list(ds.addurls(files, topurl + 'files/{URI}', '{URI}', fast=False, save=False))
print(f"Processed {len(added)} entries")
