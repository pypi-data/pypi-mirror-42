# python-safewise


Python library and commandline client for communicating with SafeWISE
Hardware Wallet

See <https://safewise.io> for more information

## Install

Python-safewise requires Python 3.3 or higher, and libusb 1.0. The easiest
way to install it is with `pip`. The rest of this guide assumes you have
a working `pip`; if not, you can refer to [this
guide](https://packaging.python.org/tutorials/installing-packages/).


In addition to the above, you need to install development headers for
HIDAPI.

#### Debian / Ubuntu

On a Debian or Ubuntu based system, you can install these:

```sh
sudo apt-get install python3-dev python3-pip cython3 libusb-1.0-0-dev libudev-dev
```

#### Windows

On a Windows based system, you can install these (for more info on choco, refer to [this](https://chocolatey.org/install)):

```sh
choco install vcbuildtools python3 protoc
refreshenv
pip3 install protobuf
```

When installing the safewise library, you need to specify that you want
`hidapi`:

```sh
pip3 install --upgrade setuptools
pip3 install safewise[hidapi]
```

### Ethereum support

Ethereum requires additional python packages. Instead of
`pip3 install safewise`, specify `pip3 install safewise[ethereum]`.

You can combine it with the above, to get both HIDAPI and Ethereum
support:

```sh
pip3 install safewise[ethereum,hidapi]
```

### FreeBSD

On FreeBSD you can install the packages:

```sh
pkg install security/py-safewise
```

or build via ports:

```sh
cd /usr/ports/security/py-safewise
make install clean
```

## Command line client (safewisectl)

The included `safewisectl` python script can perform various tasks such as
changing setting in the SafeWISE, signing transactions, retrieving account
info and addresses. See the [docs/](docs/) sub folder for detailed
examples and options.


## Python Library

You can use this python library to interact with a SafeWISE and
use its capabilities in your application. See examples here in the
[tools/](tools/) sub folder.

## PIN Entering

When you are asked for PIN, you have to enter scrambled PIN. Follow the
numbers shown on SafeWISE display and enter the their positions using the
numeric keyboard mapping:

|   |   |   |
|---|---|---|
| 7 | 8 | 9 |
| 4 | 5 | 6 |
| 1 | 2 | 3 |

Example: your PIN is **1234** and SafeWISE is displaying the following:

|   |   |   |
|---|---|---|
| 2 | 8 | 3 |
| 5 | 4 | 6 |
| 7 | 9 | 1 |

You have to enter: **3795**

