![printerrobot](https://github.com/referefref/honeyprint-ng/assets/56499429/c27768c2-fa76-4716-b346-595563812b43)

* Forked from Lukas' (Glaslos) [***original Printer honeypot PoC***](https://github.com/glaslos/honeyprint) - migrated to Python3 with added verbosity.
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
