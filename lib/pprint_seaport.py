import subprocess
import re
from dataclasses import dataclass
from typing import List, Tuple, Iterable, Optional
from enum import Enum
from pprint import pprint
import sys
from seaport_enums import *
from seaport_structs import *

def call_cast(command: str, input: str) -> str:
    """Call the cast command and return the output."""
    return (
        subprocess.check_output(" ".join(["cast", command, input]), shell=True)
        .decode()
        .strip()
    )


def call_cast_tx(tx_hash: str) -> str:
    """Call the cast command and return the output."""
    return call_cast("tx", tx_hash)


def parse_cast_tx(tx_hash: str) -> str:
    """Call the cast command and return the output."""
    output = call_cast_tx(tx_hash)
    return output.split("input")[1].split("nonce")[0].strip()


def call_cast_4bd(calldata: str) -> str:
    """Call the cast command and return the output."""
    return call_cast("4bd", calldata)


def parse_token(string, start) -> Tuple[Optional[List | Tuple | str | int], int]:
    # Ignore spaces, tabs, and newlines
    if string[start] in " \t\n":
        return None, start + 1

    # Ignore commas
    if string[start] == ",":
        return None, start + 1

    # Parse lists
    if string[start] == "[":
        lst, pos = parse_list(string, start + 1)
        return lst, pos

    # Parse tuples
    if string[start] == "(":
        tpl, pos = parse_tuple(string, start + 1)
        return tpl, pos

    # Ignore closing brackets and parentheses
    if string[start] == "]" or string[start] == ")":
        return None, start

    # Parse string literals
    if string[start] == '"' or string[start] == "'":
        m = re.match(r'(["\'])(.*?)\1', string[start:])
        if m:
            return m.group(2), start + len(m.group(0))

    # Parse hexadecimal numbers
    m = re.match(r"0x[0-9a-fA-F]+", string[start:])
    if m:
        return m.group(0), start + len(m.group(0))

    # Parse numbers
    m = re.match(r"[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?", string[start:])
    if m:
        return int(m.group(0)), start + len(m.group(0))

    # Parse words
    m = re.match(r"\w+", string[start:])
    if m:
        return m.group(0), start + len(m.group(0))

    raise ValueError(f"Invalid character at position {start}: {string[start]}")


def parse_list(string, start=0):
    result = []
    while start < len(string):
        item, pos = parse_token(string, start)
        if item is None:
            start = pos
            continue

        result.append(item)

        if string[pos] == "]":
            return result, pos + 1

        start = pos

    raise ValueError("List not terminated")


def parse_tuple(string, start=0):
    result = []
    while start < len(string):
        item, pos = parse_token(string, start)
        if item is None:
            start = pos
            continue

        result.append(item)

        if string[pos] == ")":
            return tuple(result), pos + 1

        start = pos

    raise ValueError("Tuple not terminated")


def parse_decode_data(output: str) -> Tuple[str, str]:
    _, orders, fulfillments = [x.strip() for x in output.strip().split("\n")]
    return orders, fulfillments



def parse_offer_item(offer_item_data: tuple) -> OfferItem:
    item_type = ItemType(offer_item_data[0])
    args = [item_type, *offer_item_data[1:]]
    return OfferItem(*args)


def parse_offer_items(offer_items_iter: Iterable[tuple]) -> List[OfferItem]:
    return [parse_offer_item(offer_item_data) for offer_item_data in offer_items_iter]


def parse_consideration_item(consideration_item_data: tuple) -> ConsiderationItem:
    item_type = ItemType(consideration_item_data[0])
    args = [item_type, *consideration_item_data[1:]]
    consideration_item = ConsiderationItem(*args)
    return consideration_item


def parse_consideration_items(
    consideration_items_iter: Iterable[tuple],
) -> List[ConsiderationItem]:
    return [
        parse_consideration_item(consideration_item_data)
        for consideration_item_data in consideration_items_iter
    ]


def parse_order_parameters(order_parameters_data: tuple) -> OrderParameters:
    args = [
        *order_parameters_data[:2],
        parse_offer_items(order_parameters_data[2]),
        parse_consideration_items(order_parameters_data[3]),
        *order_parameters_data[4:],
    ]
    return OrderParameters(*args)


def parse_order_parameters_array(
    order_parameters_iter: Iterable[tuple],
) -> List[OrderParameters]:
    return [
        parse_order_parameters(order_parameters_data)
        for order_parameters_data in order_parameters_iter
    ]


def parse_order(order_data: tuple) -> Order:
    parameters_data, signature = order_data
    parameters = parse_order_parameters(parameters_data)
    return Order(parameters, signature)


def parse_orders(orders_list: List[tuple]) -> List[Order]:
    return [parse_order(order_data) for order_data in orders_list]


def parse_fulfillments(fulfillments_list: List[tuple]) -> List[Fulfillment]:
    fulfillments = []
    for fulfillment_data in fulfillments_list:
        offer_fulfillment = [
            FulfillmentComponent(*offer_index_data)
            for offer_index_data in fulfillment_data[0]
        ]
        consideration_fulfillment = [
            FulfillmentComponent(*consideration_index_data)
            for consideration_index_data in fulfillment_data[1]
        ]
        fulfillment = Fulfillment(offer_fulfillment, consideration_fulfillment)
        fulfillments.append(fulfillment)
    return fulfillments


def call_and_print(tx_hash: str):
    calldata = parse_cast_tx(
        tx_hash
    )
    output = call_cast_4bd(calldata)
    orders_raw, fulfillments_raw = parse_decode_data(output)
    orders_tup, _ = parse_token(orders_raw, 0)
    fulfillments_tup, _ = parse_token(fulfillments_raw, 0)
    orders = parse_orders(orders_tup)
    fulfillments = parse_fulfillments(fulfillments_tup)
    pprint(orders)
    pprint(fulfillments)


if __name__ == "__main__":
    # grab tx hash from command line
    tx_hash = sys.argv[1]
    call_and_print(tx_hash)



# call_and_print()
