#!/usr/bin/env python3
"""Add scroll reveal classes to section headers in service pages."""
import re

files = ['direct.html', 'seo.html', 'serm.html', 'sites.html', 'ai.html', 'leads.html', 'farpost.html', 'outreach.html']

for fname in files:
    fpath = f'/Users/mak/Downloads/dare-site/{fname}'
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Add reveal to section headers (sh class) if not already there
    # <div class="sh"> → <div class="sh reveal">
    html = html.replace('<div class="sh">', '<div class="sh reveal">')
    # <div class="g2"> → <div class="g2 reveal">
    html = html.replace('<div class="g2">', '<div class="g2 reveal">')
    # price grids
    html = html.replace('<div class="price-grid3">', '<div class="price-grid3 reveal">')
    html = html.replace('<div class="price-grid">', '<div class="price-grid reveal">')
    # proc list
    html = html.replace('<div class="proc">', '<div class="proc reveal">')
    # feat list
    html = html.replace('<ul class="feat-list">', '<ul class="feat-list reveal">')

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'✓ {fname}')

print('Done!')
