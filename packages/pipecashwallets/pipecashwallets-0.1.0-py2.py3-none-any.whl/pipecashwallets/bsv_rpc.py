import logging

class BitcoinSV_RPC:
    '''A Bitcoin SV wallet '''

    def __init__(self):

        self.description = '''A bitcoin SV wallet that uses RPC to connect to a Bitcoin SV node.
        By default, it looks for a node on the local computer and the standard port.
        By default, it uses the default account on that node (no account name passed).
        To use it on a specific account, change the 'accountName' property in the options.

        By default it waits for 1 confirmation on transactions.
        Set 'minConf' in the options to 0 for instant transactions.
        Set it higher if you want more confirmations.

        By default the log level of the 3-rd party library is DEBUG
        Set 'rpcLogLevel' to 'INFO', 'WARN', or 'ERROR' to see less messages.

        To connect to the node, the secret variables for user and password must be provided.
        '''

        self.options = {}

        self.default_options = {
            "rpcaddress": "127.0.0.1",
            "rpcport": 8332,
            "rpcLogLevel": 'DEBUG',
            "accountName": "",
            "minConf": 1,
        }

        self.uses_secret_variables = [
            "BITCOIN_SV_RPC_WALLET_USER",
            "BITCOIN_SV_RPC_WALLET_PASSWORD"
        ]

        self.secrets = {}

    def start(self, log):
        from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

        self.log = log
        logging.basicConfig()
        logging.getLogger("BitcoinRPC").setLevel(self.options["rpcLogLevel"])

        addr = self.options["rpcaddress"]
        port = self.options["rpcport"]

        user = self.secrets["BITCOIN_SV_RPC_WALLET_USER"]
        password = self.secrets["BITCOIN_SV_RPC_WALLET_PASSWORD"]

        self.rpc = AuthServiceProxy("http://%s:%s@%s:%s" % (
            user, password, addr, port))
        self.rpc.getnetworkinfo()

    def validate_options(self):
        if type(self.options["rpcaddress"]) != str:
            raise AssertionError("rpcaddress should be str")

        self.__validate_option("rpcaddress", str)

        self.__validate_option(
            "rpcport", int, lambda p: 0 < p and p < 10000, "between 0 and 10000")

        self.__validate_option("rpcLogLevel", str,
            lambda l: l in ['DEBUG', 'INFO', 'WARN', 'ERROR'],
            "one of ['DEBUG', 'INFO', 'WARN', 'ERROR']")

        self.__validate_option("accountName", str)

        self.__validate_option("minConf", int, lambda i: i>=0, " 0 or bigger")

    def __validate_option(self, optionName, optionType, condition=None, conditionMessage=""):
        if type(self.options[optionName]) != optionType:
            raise AssertionError(optionName + " should be " + str(optionType))
        if condition is not None:
            if not condition(self.options[optionName]):
                raise AssertionError(optionName + " should be " + str(conditionMessage))

    def check_dependencies_missing(self):
        from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

    def checkBalance(self):
        self.__try(
            lambda: self.rpc.getbalance(self.options["accountName"]),
            "checkBalance")

    def send(self, amount, address):
        self.__try(
            lambda: self.rpc.sendfrom(self.options["accountName"], address, amount),
            "send")

    def getReceiveAddress(self):
        self.__try(
            lambda: self.rpc.getnewaddress(self.options["accountName"]),
            "getReceiveAddress")

    def getLatestTransactions(self, numOfTransactions=10, transactionsToSkip=0):
        self.__try(
            lambda: self.rpc.listtransactions(
                self.options["accountName"], numOfTransactions, transactionsToSkip),
            "getLatestTransactions")

    def __try(self, function, functionName):
        try:
            result = function()
            return function
        except Exception as ex:
            self.log.error("Error in %s.%s() : %s" % (
                self.__class__.__name__, str(ex)))

