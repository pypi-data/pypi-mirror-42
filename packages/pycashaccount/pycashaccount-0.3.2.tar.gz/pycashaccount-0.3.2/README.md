# Cash Account Helper

You can already take payment information like an address and register a [cash account](https://gitlab.com/cash-accounts/specification) at [cashaccount.info](https://cashaccount.info).
I really recommend you do.

This CLI and library will help you prepare cash account registrations that you can broadcast yourself.


## Installation

Requires python3 for now.

`pip install pycashaccount`


## Status / ToDo

It is very basic still. Please file an issue if you have additional use cases for it.

- ~~OP_RETURN output for electron-cash op_return markdown~~
- ~~OP_RETURN hex-like output~~
- ~~p2sh output~~
- ~~support payment codes~~
- ~~generate raw hex output that common node CLIs can use~~
- support stealth addresses
- support lookup of cash accounts


## Note about Bip47 payment codes

[Bip47](https://github.com/bitcoin/bips/blob/master/bip-0047.mediawiki) payment codes are very interesting.
Please read [this introduction](https://honest.cash/emergent_reasons/what-is-a-payment-code-bip47-and-how-can-i-make-one-with-electron-cash-1919)
to them before using `pycashaccount` to register a payment code.
The payment code itself is non-trivial to generate so `pycashaccount` lets you create registration info
from the xpub as well as the payment code itself. Please be very careful with xpubs.
Please make absolutely sure you do not export and start copy-pasting an ***xpriv***.

## CLI (command line interface) usage after installation

For example, get the information required for a key hash and script hash accounts:

```bash
p2pkh="bitcoincash:qrme8l598x49gmjhn92dgwhk5a3znu5wfcf5uf94e9"
p2sh="bitcoincash:pp4d24pemra2k3mths8cjxpuu6yl3a5ctvcp8mdkm9"
paymentcode="PM8TJTLJbPRGxSbc8EJi42Wrr6QbNSaSSVJ5Y3E4pbCYiTHUskHg13935Ubb7q8tx9GVbh2UuRnBc3WSyJHhUrw8KhprKnn9eDznYGieTzFcwQRya4GA"
xpub="xpub6D3t231wUi5v9PEa8mgmyV7Tovg3CzrGEUGNQTfm9cK93je3PgX9udfhzUDx29pkeeHQBPpTSHpAxnDgsf2XRbvLrmbCUQybjtHx8SUb3JB"

cashaccount keyhash     name1 "$p2pkh"
cashaccount scripthash  name2 "$p2sh"           --format=opreturn
cashaccount paymentcode name4 from-xpub "$xpub" --format=electron-markdown
cashaccount paymentcode name3 from-code "$paymentcode"
```

Generally:

```bash
cashaccount payment_type name payment_info [--format]
```

Get help:

```bash
cashaccount --help

cashaccount keyhash --help
```


## CLI usage directly from repository

Same usage as the installed cli, except you can call it from the `cli` script at the repository root:

```bash
./cli --help
```


## Library usage

Look at `cashaccount/cli.py` for usage.

For example, create a registration from a name and payment information.

```python
from cashaccount import KeyHashInfo, Registration, opreturn

name = 'emergent_reasons'
info = KeyHashInfo('bitcoincash:qrme8l598x49gmjhn92dgwhk5a3znu5wfcf5uf94e9')
registration = Registration(name, info)
print(registration)
print(opreturn(registration))
```


## Contributions

Code contributions are welcome:

- Fork the repository and submit a pull request from your fork.
- Install test requirements `pip install -r requirements-test.txt`
- Update tests to cover any changes
- Confirm all tests pass before submitting a Pull Request (e.g. `pytest --cov-report term-missing --cov=cashaccount test/`)

Support donations are also welcome:

- `🌵emergent_reasons#100` (`bitcoincash:qz3aq0uhltztqyjy2esa0lshadg9pf87yu7yealu3a`)
- `☯Jonathan#100` for donations to the cashaccount project (`bitcoincash:qr4aadjrpu73d2wxwkxkcrt6gqxgu6a7usxfm96fst`)
- [Electron Cash (bottom of the page)](https://electroncash.org/) The team added a general OP_RETURN feature where you can use the opreturn formatting.
