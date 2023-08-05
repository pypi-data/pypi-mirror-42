from functools import wraps
from logging import getLogger
from typing import Dict, Union

import requests
from ethereum.utils import (check_checksum, checksum_encode, ecrecover_to_pub,
                            privtoaddr, sha3)
from hexbytes import HexBytes
from web3 import HTTPProvider, Web3
from web3.middleware import geth_poa_middleware
from web3.utils.threads import Timeout

from gnosis.eth.constants import NULL_ADDRESS

from .contracts import get_erc20_contract

logger = getLogger(__name__)


class TransactionAlreadyImported(ValueError):
    pass


class ReplacementTransactionUnderpriced(ValueError):
    pass


class FromAddressNotFound(ValueError):
    pass


class InvalidNonce(ValueError):
    pass


class InsufficientFunds(ValueError):
    pass


class EtherLimitExceeded(ValueError):
    pass


class SenderAccountNotFoundInNode(ValueError):
    pass


def tx_with_exception_handling(func):
    error_with_exception: Dict[str, Exception] = {
        'Transaction with the same hash was already imported': TransactionAlreadyImported,
        'replacement transaction underpriced': ReplacementTransactionUnderpriced,
        'from not found': FromAddressNotFound,
        'correct nonce': InvalidNonce,
        'insufficient funds': InsufficientFunds,
        "doesn't have enough funds": InsufficientFunds,
        'sender account not recognized': SenderAccountNotFoundInNode,
    }

    @wraps(func)
    def with_exception_handling(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as exc:
            str_exc = str(exc).lower()
            for reason, custom_exception in error_with_exception.items():
                if reason.lower() in str_exc:
                    raise custom_exception(str(exc)) from exc
            raise exc
    return with_exception_handling


class EthereumServiceProvider:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            from django.conf import settings
            cls.instance = EthereumService(settings.ETHEREUM_NODE_URL)
        return cls.instance


class EthereumService:
    NULL_ADDRESS = NULL_ADDRESS

    def __init__(self, ethereum_node_url: str):
        self.ethereum_node_url = ethereum_node_url
        self.w3 = Web3(HTTPProvider(self.ethereum_node_url))
        try:
            if self.w3.net.chainId != 1:
                self.w3.middleware_stack.inject(geth_poa_middleware, layer=0)
            # For tests using dummy connections (like IPC)
        except (ConnectionError, FileNotFoundError):
            self.w3.middleware_stack.inject(geth_poa_middleware, layer=0)

    def get_nonce_for_account(self, address, block_identifier=None):
        return self.w3.eth.getTransactionCount(address, block_identifier=block_identifier)

    @property
    def current_block_number(self):
        return self.w3.eth.blockNumber

    def estimate_gas(self, from_: str, to: str, value: int, data: bytes, block_identifier=None):
        data = data or b''
        params = [
            {"from": from_,
             "to": to,
             "data": HexBytes(data).hex(),
             "value": "0x{:x}".format(value),  # No leading zeroes
             },
        ]
        if block_identifier:
            params.append(block_identifier)

        payload = {
            "method": "eth_estimateGas",
            "params": params,
            "jsonrpc": "2.0",
            "id": 1
        }

        response = requests.post(url=self.ethereum_node_url, json=payload)
        response_json = response.json()
        if 'error' in response_json:
            # When using `pending`, Geth returns
            """
            {
                "jsonrpc": "2.0",
                "id": 1,
                "error": {
                    "code": -32602,
                    "message": "too many arguments, want at most 1"
                }
            }
            """
            if response_json['error']['code'] == -32602:
                return self.w3.eth.estimateGas({
                    "from": from_,
                    "to": to,
                    "data": data,
                    "value": value,
                })
            else:
                raise ValueError(response_json['error'])
        else:
            return int(response_json['result'], 16)

    @staticmethod
    def estimate_data_gas(data: bytes):
        if isinstance(data, str):
            data = HexBytes(data)

        gas = 0
        for byte in data:
            if not byte:
                gas += 4  # Byte 0 -> 4 Gas
            else:
                gas += 68  # Any other byte -> 68 Gas
        return gas

    def get_balance(self, address: str, block_identifier=None):
        return self.w3.eth.getBalance(address, block_identifier)

    def get_erc20_balance(self, address: str, erc20_address: str):
        return get_erc20_contract(self.w3, erc20_address).functions.balanceOf(address).call()

    def get_transaction(self, tx_hash):
        return self.w3.eth.getTransaction(tx_hash)

    def get_transaction_receipt(self, tx_hash, timeout=None):
        if not timeout:
            tx_receipt = self.w3.eth.getTransactionReceipt(tx_hash)
        else:
            try:
                tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash, timeout=timeout)
            except Timeout:
                return None

        # Parity returns tx_receipt even is tx is still pending, so we check `blockNumber` is not None
        return tx_receipt if tx_receipt and tx_receipt['blockNumber'] is not None else None

    def get_block(self, block_number, full_transactions=False):
        return self.w3.eth.getBlock(block_number, full_transactions=full_transactions)

    @tx_with_exception_handling
    def send_transaction(self, transaction_dict: Dict[str, any]) -> bytes:
        return self.w3.eth.sendTransaction(transaction_dict)

    @tx_with_exception_handling
    def send_raw_transaction(self, raw_transaction) -> bytes:
        return self.w3.eth.sendRawTransaction(bytes(raw_transaction))

    def send_unsigned_transaction(self, tx: Dict[str, any], private_key: Union[None, str]=None,
                                  public_key: Union[None, str]=None, retry: bool=False,
                                  block_identifier: Union[None, str]=None) -> bytes:
        """
        Send a tx using an unlocked public key in the node or a private key. Both `public_key` and
        `private_key` cannot be `None`
        :param tx:
        :param private_key:
        :param public_key:
        :param retry: Retry if a problem with nonce is found
        :param block_identifier:
        :return:
        """
        if private_key:
            address = self.private_key_to_address(private_key)
        elif public_key:
            address = public_key
        else:
            logger.error('No ethereum account provided. Need a public_key or private_key')
            raise ValueError("Ethereum account was not configured or unlocked in the node")

        if tx.get('nonce') is None:
            tx['nonce'] = self.get_nonce_for_account(address, block_identifier=block_identifier)

        number_errors = 5
        while number_errors >= 0:
            try:
                if private_key:
                    signed_tx = self.w3.eth.account.signTransaction(tx, private_key=private_key)
                    logger.debug('Sending %d wei from %s to %s', tx['value'], address, tx['to'])
                    return self.send_raw_transaction(signed_tx.rawTransaction)
                elif public_key:
                    tx['from'] = address
                    return self.send_transaction(tx)
            except ReplacementTransactionUnderpriced as e:
                if not retry or not number_errors:
                    raise e
                logger.error('address=%s Tx with nonce=%d was already sent, retrying with nonce + 1',
                             address, tx['nonce'])
                tx['nonce'] += 1
            except InvalidNonce as e:
                if not retry or not number_errors:
                    raise e
                logger.error('address=%s Tx with invalid nonce=%d, retrying recovering nonce again',
                             address, tx['nonce'])
                tx['nonce'] = self.get_nonce_for_account(address, block_identifier=block_identifier)
                number_errors -= 1

    def send_eth_to(self, private_key: str, to: str, gas_price: int, value: int, gas: int=22000,
                    retry: bool = False, block_identifier=None, max_eth_to_send: int = 0) -> bytes:
        """
        Send ether using configured account
        :param to: to
        :param gas_price: gas_price
        :param value: value(wei)
        :param gas: gas, defaults to 22000
        :param retry: Retry if a problem is found
        :param block_identifier: None default, 'pending' not confirmed txs
        :return: tx_hash
        """

        assert check_checksum(to)
        if max_eth_to_send and value > self.w3.toWei(max_eth_to_send, 'ether'):
            raise EtherLimitExceeded('%d is bigger than %f' % (value, max_eth_to_send))

        tx = {
            'to': to,
            'value': value,
            'gas': gas,
            'gasPrice': gas_price,
        }

        return self.send_unsigned_transaction(tx, private_key=private_key, retry=retry,
                                              block_identifier=block_identifier)

    def check_tx_with_confirmations(self, tx_hash: str, confirmations: int) -> bool:
        """
        Check tx hash and make sure it has the confirmations required
        :param w3: Web3 instance
        :param tx_hash: Hash of the tx
        :param confirmations: Minimum number of confirmations required
        :return: True if tx was mined with the number of confirmations required, False otherwise
        """
        tx_receipt = self.w3.eth.getTransactionReceipt(tx_hash)
        if not tx_receipt or tx_receipt['blockNumber'] is None:
            # If tx_receipt exists but blockNumber is None, tx is still pending (just Parity)
            return False
        else:
            return (self.w3.eth.blockNumber - tx_receipt['blockNumber']) >= confirmations

    @staticmethod
    def private_key_to_address(private_key):
        return checksum_encode(privtoaddr(private_key))

    @staticmethod
    def get_signing_address(hash, v, r, s) -> str:
        """
        :return: checksum encoded address starting by 0x, for example `0x568c93675A8dEb121700A6FAdDdfE7DFAb66Ae4A`
        :rtype: str
        """
        encoded_64_address = ecrecover_to_pub(hash, v, r, s)
        address_bytes = sha3(encoded_64_address)[-20:]
        return checksum_encode(address_bytes)
