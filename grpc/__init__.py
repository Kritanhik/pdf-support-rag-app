__version__ = "1.85.1"

class Channel: pass
class ChannelCredentials: pass
class Compression:
    NoCompression = 0
    Deflate = 1
    Gzip = 2

class StatusCode:
    OK = 0
    CANCELLED = 1
    UNKNOWN = 2
    INVALID_ARGUMENT = 3
    DEADLINE_EXCEEDED = 4
    NOT_FOUND = 5
    ALREADY_EXISTS = 6
    PERMISSION_DENIED = 7
    RESOURCE_EXHAUSTED = 8
    FAILED_PRECONDITION = 9
    ABORTED = 10
    OUT_OF_RANGE = 11
    UNIMPLEMENTED = 12
    INTERNAL = 13
    UNAVAILABLE = 14
    DATA_LOSS = 15
    UNAUTHENTICATED = 16

class RpcError(Exception): pass

class UnaryUnaryClientInterceptor: pass
class UnaryStreamClientInterceptor: pass
class StreamUnaryClientInterceptor: pass
class StreamStreamClientInterceptor: pass
class ClientCallDetails: pass

def insecure_channel(*args, **kwargs): pass
def secure_channel(*args, **kwargs): pass
def ssl_channel_credentials(*args, **kwargs): pass

class aio:
    Channel = Channel
    UnaryUnaryClientInterceptor = UnaryUnaryClientInterceptor
    UnaryStreamClientInterceptor = UnaryStreamClientInterceptor
    StreamUnaryClientInterceptor = StreamUnaryClientInterceptor
    StreamStreamClientInterceptor = StreamStreamClientInterceptor
    ClientCallDetails = ClientCallDetails
    
    @staticmethod
    def insecure_channel(*args, **kwargs): pass
    @staticmethod
    def secure_channel(*args, **kwargs): pass