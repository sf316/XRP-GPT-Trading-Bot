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

    # Create an account str from the wallet
    test_account = test_wallet.address

    # Look up info about your account
    from xrpl.models.requests.account_info import AccountInfo
    acct_info = AccountInfo(
        account=test_account,
        ledger_index="validated",
        strict=True,
    )
    response = client.request(acct_info)
    result = response.result
    print("response.status: ", response.status)
    
    import json
    print(json.dumps(response.result, indent=4, sort_keys=True))