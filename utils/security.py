# -*- coding: UTF-8 -*-
"""
安全认证模块
包含签名生成、加密等功能
"""
import hashlib
import random
import time


def generate_random_key(length: int = 4) -> str:
    """
    生成随机密钥（兼容原有逻辑）
    Args:
        length: 密钥长度

    Returns:
        4位十六进制字符串
    """
    n = int(65536 * (1 + random.random()))
    return hex(n)[-length:]


def generate_auth_signature(eid: str, token: str) -> tuple[str, int]:
    """
    生成微信小程序认证签名（38位版本）
    Args:
        eid: 活动ID
        token: 用户token

    Returns:
        (_a 签名, _s 时间戳)
    """
    # 随机部分
    rand_part = generate_random_key()

    # 拼接 token前2位
    k = rand_part + token[:2]

    # 计算 I = md5(eid)
    i_value = hashlib.md5(eid.encode()).hexdigest()

    # 毫秒时间戳
    timestamp = int(time.time() * 1000)

    # 计算签名
    signature = k + hashlib.md5(f"{i_value}{timestamp}qwrq2w".encode()).hexdigest()

    return signature, timestamp


def sanitize_user_input(user_input: str) -> str:
    """
    清理用户输入，防止注入攻击
    Args:
        user_input: 用户输入字符串

    Returns:
        清理后的字符串
    """
    if not user_input:
        return ""

    # 移除危险字符
    dangerous_chars = ['<', '>', '"', "'", '&', '\x00', '\n', '\r']
    sanitized = user_input
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')

    return sanitized.strip()
