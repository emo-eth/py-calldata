from seaport_enums import *
from dataclasses import dataclass
from typing import List

@dataclass
class OrderComponents:
    offerer: str
    zone: str
    offer: List[OfferItem]
    consideration: List[ConsiderationItem]
    orderType: OrderType
    startTime: int
    endTime: int
    zoneHash: str
    salt: int
    conduitKey: str
    counter: int

@dataclass
class OfferItem:
    itemType: ItemType
    token: str
    identifierOrCriteria: int
    startAmount: int
    endAmount: int

@dataclass
class ConsiderationItem:
    itemType: ItemType
    token: str
    identifierOrCriteria: int
    startAmount: int
    endAmount: int
    recipient: str

@dataclass
class SpentItem:
    itemType: ItemType
    token: str
    identifier: int
    amount: int

@dataclass
class ReceivedItem:
    itemType: ItemType
    token: str
    identifier: int
    amount: int
    recipient: str

@dataclass
class BasicOrderParameters:
    considerationToken: str
    considerationIdentifier: int
    considerationAmount: int
    offerer: str
    zone: str
    offerToken: str
    offerIdentifier: int
    offerAmount: int
    basicOrderType: BasicOrderType
    startTime: int
    endTime: int
    zoneHash: str
    salt: int
    offererConduitKey: str
    fulfillerConduitKey: str
    totalOriginalAdditionalRecipients: int
    additionalRecipients: List[AdditionalRecipient]
    signature: str

@dataclass
class AdditionalRecipient:
    amount: int
    recipient: str

@dataclass
class OrderParameters:
    offerer: str
    zone: str
    offer: List[OfferItem]
    consideration: List[ConsiderationItem]
    orderType: OrderType
    startTime: int
    endTime: int
    zoneHash: str
    salt: int
    conduitKey: str
    totalOriginalConsiderationItems: int

@dataclass
class Order:
    parameters: OrderParameters
    signature: str

@dataclass
class AdvancedOrder:
    parameters: OrderParameters
    numerator: int
    denominator: int
    signature: str
    extraData: str

@dataclass
class OrderStatus:
    isValidated: bool
    isCancelled: bool
    numerator: int
    denominator: int

@dataclass
class CriteriaResolver:
    orderIndex: int
    side: Side
    index: int
    identifier: int
    criteriaProof: List[str]

@dataclass
class Fulfillment:
    offerComponents: List[FulfillmentComponent]
    considerationComponents: List[FulfillmentComponent]

@dataclass
class FulfillmentComponent:
    orderIndex: int
    itemIndex: int

@dataclass
class Execution:
    item: ReceivedItem
    offerer: str
    conduitKey: str

@dataclass
class ZoneParameters:
    orderHash: str
    fulfiller: str
    offerer: str
    offer: List[SpentItem]
    consideration: List[ReceivedItem]
    extraData: str
    orderHashes: List[str]
    startTime: int
    endTime: int
    zoneHash: str

@dataclass
class Schema:
    id: int
    metadata: str