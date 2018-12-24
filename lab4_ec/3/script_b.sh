#!/bin/bash
openssl ocsp -no_nonce -issuer Google_Internet_Authority_G3.pem -cert youtube_cert.pem -url http://ocsp.pki.goog/GTSGIAG3 -header Host ocsp.pki.goog -noverify