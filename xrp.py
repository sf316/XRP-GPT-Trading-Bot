if __name__ == "__main__":
    # Define the network client
    from xrpl.clients import JsonRpcClient

    JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
    client = JsonRpcClient(JSON_RPC_URL)

    # Create a wallet using the testnet faucet:
    # https://xrpl.org/xrp-testnet-faucet.html
    from xrpl.wallet import generate_faucet_wallet

    test_wallet = generate_faucet_wallet(client, debug=True)
    print(test_wallet)