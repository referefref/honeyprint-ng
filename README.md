Honeyprint
==========

* Forked from Lukas' original Printer honeypot PoC - migrated to Python3 with added verbosity.
* pkipplib was never ported to Python3, as a result a port has been included in this project

## Installation
```
git clone https://github.com/referefref/honeyprint-ng.git
cd honeyprint-ng
pip3 install -r requirements.txt
chmod +x honeyprint.py
./honeyprint.py
```

## Execution
* Runs as default on port 9100 (LPR TCP direct printing)
* Can be tested with CUPS tooling like ipptool

``` ipptool -v ipp://${IPADDRESS}:9100/ipp/print get-printer-attributes.test ```
![image](https://github.com/referefref/honeyprint-ng/assets/56499429/cd73e929-1653-4453-903c-d77df8169708)
