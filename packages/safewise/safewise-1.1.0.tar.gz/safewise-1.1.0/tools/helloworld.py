#!/usr/bin/env python3
from safewiselib.client import SafeWISEClient
from safewiselib.transport import get_transport
from safewiselib.tools import parse_path
from safewiselib import btc
from safewiselib.ui import ClickUI


def main():
    # Use first connected device
    transport = get_transport()

    # Creates object for manipulating SafeWISE

    ui = ClickUI()
    client = SafeWISEClient(transport, ui)

    # Print out SafeWISE's features and settings
    print(client.features)

    # Get the first address of first BIP44 account
    # (should be the same address as shown in wallet.safewise.io)
    bip32_path = parse_path("44'/0'/0'/0/0")
    address = btc.get_address(client, 'Bitcoin', bip32_path, True)
    print('Bitcoin address:', address)

    client.close()


if __name__ == '__main__':
    main()
