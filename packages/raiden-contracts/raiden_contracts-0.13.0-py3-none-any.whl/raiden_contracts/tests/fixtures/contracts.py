import pytest
import logging

log = logging.getLogger(__name__)


@pytest.fixture
def deploy_tester_contract(
        web3,
        contracts_manager,
        deploy_contract,
        contract_deployer_address,
        get_random_address,
):
    """Returns a function that can be used to deploy a named contract,
    using conract manager to compile the bytecode and get the ABI"""
    def f(contract_name, libs=None, args=None):
        json_contract = contracts_manager.get_contract(contract_name)
        contract = deploy_contract(
            web3,
            contract_deployer_address,
            json_contract['abi'],
            json_contract['bin'],
            args,
        )
        return contract
    return f


@pytest.fixture
def deploy_contract_txhash(revert_chain):
    """Returns a function that deploys a compiled contract, returning a txhash"""
    def fn(
            web3,
            deployer_address,
            abi,
            bytecode,
            args,
    ):
        if args is None:
            args = []
        contract = web3.eth.contract(abi=abi, bytecode=bytecode)
        return contract.constructor(*args).transact({'from': deployer_address})
    return fn


@pytest.fixture
def deploy_contract(revert_chain, deploy_contract_txhash):
    """Returns a function that deploys a compiled contract"""
    def fn(
            web3,
            deployer_address,
            abi,
            bytecode,
            args,
    ):
        contract = web3.eth.contract(abi=abi, bytecode=bytecode)
        txhash = deploy_contract_txhash(web3, deployer_address, abi, bytecode, args)
        contract_address = web3.eth.getTransactionReceipt(txhash).contractAddress
        web3.testing.mine(1)

        return contract(contract_address)
    return fn


@pytest.fixture
def deploy_tester_contract_txhash(
        web3,
        contracts_manager,
        deploy_contract_txhash,
        contract_deployer_address,
        get_random_address,
):
    """Returns a function that can be used to deploy a named contract,
    but returning txhash only"""
    def f(contract_name, libs=None, args=None):
        json_contract = contracts_manager.get_contract(contract_name)
        txhash = deploy_contract_txhash(
            web3,
            contract_deployer_address,
            json_contract['abi'],
            json_contract['bin'],
            args,
        )
        return txhash
    return f


@pytest.fixture
def utils_contract(deploy_tester_contract):
    """Deployed Utils contract"""
    return deploy_tester_contract('Utils')
