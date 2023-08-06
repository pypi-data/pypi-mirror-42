from pyopencell.client import Client
from pyopencell.resources.base_resource import BaseResource


class Subscription(BaseResource):
    _name = "subscription"
    _url_path = "/billing/subscription"

    auditable = {
        "created": None,
        "updated": None,
        "creator": "",
        "updater": "",
    }
    code = ""
    description = ""
    userAccount = ""
    updatedCode = ""
    offerTemplate = ""
    subscriptionDate = None
    terminationDate = None
    endAgreementDate = None
    customFields = []
    terminationReason = ""
    orderNumber = ""
    minimumAmountEl = ""
    minimumAmountElSpark = ""
    minimumLabelEl = ""
    minimumLabelElSpark = ""
    subscribedTillDate = None
    renewed = None
    renewalNotifiedDate = None
    renewalRule = {
        "initialyActiveFor": None,
        "initialyActiveForUnit": "",
        "autoRenew": None,
        "daysNotifyRenewal": None,
        "endOfTermAction": "",
        "terminationReasonCode": "",
        "renewFor": None,
        "renewForUnit": "",
        "extendAgreementPeriodToSubscribedTillDate": None
    }
    billingCycle = "",
    seller = "",
    autoEndOfEngagement = None,
    ratingGroup = ""

    @classmethod
    def get(cls, subscriptionCode):
        """
        Returns a subscription instance obtained by code.

        :param subscriptionCode:
        :return: Subscription:
        """
        response_data = Client().get(
            cls._url_path,
            subscriptionCode=subscriptionCode
        )

        return cls(**response_data[cls._name])

    @classmethod
    def create(cls, **kwargs):
        """
        Creates a subscription instance.

        :param kwargs:
        :return:
        """
        response_data = Client().post(cls._url_path, kwargs)

        return response_data

    def save(self):
        pass
