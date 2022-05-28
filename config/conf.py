#!/usr/bin/env python3
# -*- coding: utf-8 -*-

TOR_PORT=9050
TOR_CTRL_PORT=9051
TOR_PROX_HOST="127.0.0.1"

# Tor default local proxy
PROXIES = {
    'http': 'socks5://'+TOR_PROX_HOST+':'+str(TOR_PORT),
    'https': 'socks5://'+TOR_PROX_HOST+':'+str(TOR_PORT)
}

