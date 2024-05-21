import time

def generateTransactionReference(merchantId=None):
    """ This is a helper function for generating unique transaction  references.\n
         Parameters include:\n
        merchantId (string) -- (optional) You can specify a merchant id to start references e.g. merchantId-12345678
    """
    rawTime = round(time.time() * 1000)
    timestamp = int(rawTime)
    if merchantId:
        return merchantId + "-" + str(timestamp)
    else:
        return "MC-" + str(timestamp)