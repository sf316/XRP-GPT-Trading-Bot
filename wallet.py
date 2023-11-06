from xrpl.wallet import generate_faucet_wallet
from xrpl.models.requests.account_info import AccountInfo

def import_user_wallet(client, address):

    # if not address:
    #     # Create a wallet using the testnet faucet if not having one:
    #     # https://xrpl.org/xrp-testnet-faucet.html
    #     test_wallet = generate_faucet_wallet(client, debug=True)
    
    #     # Create an account str from the wallet
    #     test_account = test_wallet.address
    # else:
    test_account = address
    
    # Look up info about your account
    acct_info = AccountInfo(
        account=test_account,
        ledger_index="validated",
        strict=True,
    )

    response = client.request(acct_info)

    return response.result