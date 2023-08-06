from sdkboil.exception import SdkException, SdkHttpException


class ChainsideSdkHttpException(SdkHttpException):
    error_code = None


class ChainsideSdkException(SdkException):
    pass
