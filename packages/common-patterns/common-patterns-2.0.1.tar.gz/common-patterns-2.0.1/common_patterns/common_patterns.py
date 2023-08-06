#!/usr/bin/env python
# encoding: utf-8

import re

PATTERN_ASN = r'ASN?([0-9]+)'
PATTERN_SSR_URL = r'ssr?://[A-Za-z0-9\-_]+'
PATTERN_WEB_URL = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'


def is_ip_address(ip: str):
    """
    Returns whether it is an IP address

    :param str ip: String
    :return: bool
    """
    try:
        import IPy
        _ = IPy.IP(ip)
        return True
    except:
        return False


def is_private_ip(ip: str):
    """
    Returns whether it is a private IP address

    :param str ip: String
    :return: bool
    """
    try:
        import IPy
        if 'PRIVATE' == IPy.IP(ip).iptype():
            return True
        return False
    except:
        return False


def is_reserved_ip(ip: str):
    """
    Returns whether it is a reserved IP address

    :param str ip: String
    :return: bool
    """
    try:
        import IPy
        if 'RESERVED' == IPy.IP(ip).iptype():
            return True
        return False
    except:
        return False


def is_public_ip(ip: str):
    """
    Returns whether it is a public IP address

    :param str ip: String
    :return: bool
    """
    try:
        import IPy
        if 'PUBLIC' == IPy.IP(ip).iptype():
            return True
        return False
    except:
        return False


def find_asn(string: str):
    """
    Returns a autonomous system number or None

    :param str string: String
    :return: int or None
    """
    match = re.search(PATTERN_ASN, string)
    if match:
        return int(match.group(1))
    return None


def findall_ssr_urls(string: str):
    """
    Returns SS/SSR URL(s)

    :param str string: Text
    :return: list
    """
    pattern = re.compile(PATTERN_SSR_URL)
    return pattern.findall(string)


def findall_web_urls(string: str):
    """
    Returns http/https URL(s)

    :param str string: Text
    :return: list
    """
    pattern = re.compile(PATTERN_WEB_URL)
    return pattern.findall(string)

