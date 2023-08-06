import json
import logging
import sys
import os

import datetime

import random
import string

from skale import Skale, BlockchainEnv
import skale.utils.helper as Helper
from skale.utils.account_tools import send_ether, send_tokens, check_skale_balance, check_ether_balance, \
    generate_account

from examples.schains.automation.helper import init_default_logger, init_wallet
from examples.schains.automation.config import ETH_AMOUNT, SKALE_AMOUNT, NUMBER_OF_ACCOUNTS, LONG_LINE, NUMBER_OF_PORTS, \
    PORTS_PER_SCHAIN, FOLDER_NAME

init_default_logger()
logger = logging.getLogger(__name__)


def get_filename(i, schain_name=''):
    time = datetime.datetime.now()
    return f'wallet_{i}_{schain_name}_{time}.json'


def save_wallet(wallet, filename):
    with open(filename, 'w') as outfile:
        logger.info(f'Saving wallet to {filename}')
        json.dump({'wallet': wallet}, outfile)


def save_info(filename, schain_info=None, wallet=None):
    info = {
        'schain_info': schain_info,
        'wallet': wallet
    }

    filepath = os.path.join(FOLDER_NAME, filename)
    with open(filepath, 'w') as outfile:
        logger.info(f'Saving info to {filename}')
        json.dump(info, outfile)


def generate_random_name(len=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=len))


def create_schain(skale, wallet):
    lifetime_years = 1
    lifetime_seconds = lifetime_years * 366 * 86400
    type_of_nodes = 4

    price_in_wei = skale.schains.get_schain_price(type_of_nodes, lifetime_seconds)

    name = generate_random_name()

    res = skale.manager.create_schain(lifetime_seconds, type_of_nodes, price_in_wei, name, wallet)
    receipt = Helper.await_receipt(skale.web3, res['tx'])
    Helper.check_receipt(receipt)

    schain_struct = skale.schains_data.get_by_name(name)
    schain_nodes = skale.schains_data.get_nodes_for_schain_config(name)

    # todo: tmp!
    for schain_node in schain_nodes:
        schain_node['basePort'] = get_schain_base_port(skale, name, schain_node['nodeID'],
                                                       schain_node['basePort'])
        schain_node['rpcPort'] = schain_node['basePort'] + NUMBER_OF_PORTS

    return {'schain_struct': schain_struct, 'schain_nodes': schain_nodes}


# todo: tmp!
def get_schain_base_port(skale, schain_name, node_id, node_port):
    schains = skale.schains_data.get_schains_for_node(node_id)
    schain_index = get_schain_index_in_node(schain_name, schains)
    return calc_schain_base_port(node_port, schain_index)


# todo: tmp!
def calc_schain_base_port(node_base_port, schain_index):
    return node_base_port + schain_index * PORTS_PER_SCHAIN


# todo: tmp!
def get_schain_index_in_node(schain_name, node_schains):
    for index, schain in enumerate(node_schains):
        if schain_name == schain['name']:
            return index
    return -1


def generate_accounts(skale, base_wallet, n, debug=True):
    for i in range(0, n):
        wallet = generate_account(skale.web3)

        send_tokens(skale, base_wallet, wallet['address'], SKALE_AMOUNT, debug)
        send_ether(skale.web3, base_wallet, wallet['address'], ETH_AMOUNT, debug)

        if debug:
            check_ether_balance(skale.web3, wallet['address'])
            check_skale_balance(skale, wallet['address'])

        schain_info = create_schain(skale, wallet)

        filename = get_filename(i, schain_info['schain_struct']['name'])
        save_info(filename, schain_info, wallet)

        logger.info(LONG_LINE)


if __name__ == "__main__":
    skale = Skale(BlockchainEnv.AWS)
    base_wallet = init_wallet()
    amount = sys.argv[1] or NUMBER_OF_ACCOUNTS
    generate_accounts(skale, base_wallet, int(amount))
