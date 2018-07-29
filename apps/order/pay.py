from alipay import AliPay

from TmallProjects import settings


def singleton(cls, *args, **kw):
    instance = {}

    def _instance():
        if cls not in instance:
            instance[cls] = cls(*args, **kw)
        return instance[cls]


class PayManager:
    """
    支付宝支付接口
    """

    def __init__(self,
                 app_id=settings.APP_ID,
                 sign_type='RSA2',
                 return_url=None,
                 app_notify_url=None,
                 app_private_key_string=settings.ALIPAY_PUBLIC_PRIVATE_STRING,
                 alipay_public_key_string=settings.ALIPAY_PUBLIC_KEY_STRING,
                 debug=False):
        self.app_id = app_id
        # 支付成功后的url

        self.app_notify_url = app_notify_url
        # 生成支付链接参数的加密方式
        self.sign_type = sign_type
        self.app_private_key_string = app_private_key_string
        self.alipay_public_key_string = alipay_public_key_string
        self.return_url = return_url
        if debug is True:
            self.__gateway = "https://openapi.alipaydev.com/gateway.do"
        else:
            self.__gateway = "https://openapi.alipay.com/gateway.do"


def alpay():
    return AliPay(
        appid="",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=settings.APP_PRIVATE_STRING,
        alipay_public_key_string=settings.ALIPAY_PUBLIC_KEY_STRING,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=False  # 默认False
    )


def pay(subject, out_trade_no, total_amount):
    alpay.api_alipay_trade_page_pay(
        subject=subject,
        out_trade_no=out_trade_no,
        total_amount=total_amount
    )
