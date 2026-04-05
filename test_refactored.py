# -*- coding: UTF-8 -*-
"""
测试模块
验证重构后的代码功能
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.validators import (
    validate_token,
    validate_eid,
    match_field_name,
    parse_delay_time,
    is_valid_index,
    is_valid_phone
)
from utils.security import (
    generate_random_key,
    generate_auth_signature,
    sanitize_user_input
)
from utils.formatters import format_timestamp


def test_validators():
    """测试验证函数"""
    print("=== 测试验证函数 ===")

    # 测试validate_token
    assert validate_token("test_token_123") is True
    assert validate_token("") is False
    assert validate_token("  ") is False
    print("[PASS] validate_token 测试通过")

    # 测试validate_eid
    assert validate_eid("test_eid") is True
    assert validate_eid("") is False
    print("[PASS] validate_eid 测试通过")

    # 测试match_field_name - 子集匹配
    extra_info = {"姓名": "修明"}
    assert match_field_name("姓", extra_info) == ("姓名", "修明")
    assert match_field_name("?姓！名", extra_info) == ("姓名", "修明")
    assert match_field_name("不匹配字段", extra_info) == (None, None)
    print("[PASS] match_field_name 测试通过")

    # 测试parse_delay_time
    assert parse_delay_time({"延迟时间": "2000"}) == 2000
    assert parse_delay_time({}) == 0
    assert parse_delay_time({"延迟时间": "invalid"}) == 0
    print("[PASS] parse_delay_time 测试通过")

    # 测试is_valid_index
    assert is_valid_index("1", 5) is True
    assert is_valid_index("6", 5) is False
    assert is_valid_index("abc", 5) is False
    print("[PASS] is_valid_index 测试通过")

    # 测试is_valid_phone
    assert is_valid_phone("13812345678") is True
    assert is_valid_phone("12345678901") is False
    assert is_valid_phone("1381234567") is False
    print("[PASS] is_valid_phone 测试通过")

    print()


def test_security():
    """测试安全函数"""
    print("=== 测试安全函数 ===")

    # 测试generate_random_key
    key = generate_random_key()
    assert len(key) == 4
    assert all(c in '0123456789abcdef' for c in key)
    print("[PASS] generate_random_key 测试通过")

    # 测试generate_auth_signature
    _a, _s = generate_auth_signature("test_eid", "test_token")
    assert len(_a) > 0
    assert isinstance(_s, int)
    print("[PASS] generate_auth_signature 测试通过")

    # 测试sanitize_user_input
    assert sanitize_user_input("<script>alert('xss')</script>") == "scriptalert('xss')/script"
    assert sanitize_user_input("normal text") == "normal text"
    print("[PASS] sanitize_user_input 测试通过")

    print()


def test_formatters():
    """测试格式化函数"""
    print("=== 测试格式化函数 ===")

    # 测试format_timestamp
    timestamp = 1735724700.0  # 2025-01-01 12:05:00
    formatted = format_timestamp(timestamp)
    assert formatted == "2025-01-01 12:05:00"
    print("[PASS] format_timestamp 测试通过")

    print()


def main():
    """主测试函数"""
    try:
        test_validators()
        test_security()
        test_formatters()

        print("\n" + "="*50)
        print("✅ [SUCCESS] 所有测试通过！")
        print("="*50)
        return 0
    except AssertionError as e:
        print(f"\n[FAIL] 测试失败: {e}")
        return 1
    except Exception as e:
        print(f"\n[ERROR] 测试异常: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
