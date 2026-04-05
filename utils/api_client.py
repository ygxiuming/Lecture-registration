# -*- coding: UTF-8 -*-
"""
API客户端模块
封装所有HTTP请求
"""
import json
import logging
from typing import Optional, Dict, Any, List

import requests

from .constants import API_BASE_URL, API_ENDPOINTS, HEADERS
from .security import generate_auth_signature
from .validators import validate_token, validate_eid

logger = logging.getLogger(__name__)


class APIClient:
    """API客户端类"""

    def __init__(self, token: Optional[str] = None):
        """
        初始化API客户端
        Args:
            token: 用户认证token（可选）
        """
        self.token = token
        self.session = requests.Session()
        # 启用SSL验证以确保安全
        self.session.verify = True

    def set_token(self, token: str):
        """设置认证token"""
        if validate_token(token):
            self.token = token
        else:
            raise ValueError("Invalid token format")

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        发送HTTP请求
        Args:
            method: HTTP方法 (GET, POST等)
            endpoint: API端点
            **kwargs: requests的额外参数

        Returns:
            响应JSON数据

        Raises:
            requests.exceptions.RequestException: 请求失败时
        """
        url = f"{API_BASE_URL}{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP错误: {e}, URL: {url}")
            raise
        except requests.exceptions.ConnectionError as e:
            logger.error(f"连接错误: {e}, URL: {url}")
            raise
        except requests.exceptions.Timeout as e:
            logger.error(f"超时错误: {e}, URL: {url}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析错误: {e}, URL: {url}")
            raise

    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """
        获取用户信息
        Returns:
            用户信息字典，失败返回None
        """
        if not self.token:
            logger.error("未设置token")
            return None

        try:
            response_data = self._request(
                "GET",
                API_ENDPOINTS['userinfo'],
                params={"access_token": self.token},
                headers=HEADERS['login']
            )
            return response_data.get('data') if response_data.get('msg') == 'ok' else None
        except Exception as e:
            logger.error(f"获取用户信息失败: {e}")
            return None

    def get_user_history(self) -> Optional[List[Dict[str, Any]]]:
        """
        获取用户浏览历史
        Returns:
            历史活动列表，失败返回None
        """
        if not self.token:
            logger.error("未设置token")
            return None

        try:
            response_data = self._request(
                "GET",
                API_ENDPOINTS['user_history'],
                params={"access_token": self.token},
                headers=HEADERS['login']
            )
            return response_data.get('data') if response_data.get('msg') == 'ok' else None
        except Exception as e:
            logger.error(f"获取历史记录失败: {e}")
            return None

    def get_registration_requirements(self, eid: str) -> Optional[List[Dict[str, Any]]]:
        """
        获取报名所需信息
        Args:
            eid: 活动ID

        Returns:
            报名信息字段列表，失败返回None
        """
        if not validate_eid(eid):
            logger.error("无效的活动ID")
            return None

        if not self.token:
            logger.error("未设置token")
            return None

        try:
            response_data = self._request(
                "GET",
                API_ENDPOINTS['req_detail'],
                params={"access_token": self.token, "eid": eid},
                headers=HEADERS['login']
            )
            return response_data.get('data', {}).get('req_info', [])
        except Exception as e:
            logger.error(f"获取报名信息失败: {e}")
            return None

    def submit_registration(
        self,
        eid: str,
        info: List[Dict[str, Any]],
        on_behalf: int = 0
    ) -> tuple[bool, str]:
        """
        提交报名
        Args:
            eid: 活动ID
            info: 报名信息列表
            on_behalf: 是否代报名 (0或1)

        Returns:
            (是否成功, 消息)
        """
        if not validate_eid(eid):
            return False, "无效的活动ID"

        if not self.token:
            return False, "未设置token"

        try:
            _a, _s = generate_auth_signature(eid, self.token)

            payload = {
                "access_token": self.token,
                "eid": eid,
                "info": info,
                "on_behalf": on_behalf,
                "items": [],
                "referer": "",
                "fee_type": "",
                "from": "xcx",
                "_a": _a,
                "_s": _s
            }

            response_data = self._request(
                "POST",
                API_ENDPOINTS['enroll'],
                headers=HEADERS['submit'],
                json=payload  # 使用json参数自动序列化
            )

            msg = response_data.get('msg', '')
            return (True, msg) if msg in ['', '提交次数超过限制', '活动期间，只允许提交1次'] else (False, msg)

        except Exception as e:
            logger.error(f"提交报名失败: {e}")
            return False, str(e)

    def add_extra_info(self, name: str, value: str) -> tuple[bool, str]:
        """
        添加预填信息
        Args:
            name: 字段名
            value: 字段值

        Returns:
            (是否成功, 消息)
        """
        if not self.token:
            return False, "未设置token"

        try:
            payload = {
                "access_token": self.token,
                "name": [name],
                "value": value
            }

            response_data = self._request(
                "POST",
                API_ENDPOINTS['extra_info'],
                headers=HEADERS['login'],
                json=payload
            )

            data = response_data.get('data', [])
            return (True, response_data.get('msg', '')) if len(data) > 0 else (False, response_data.get('msg', ''))

        except Exception as e:
            logger.error(f"添加预填信息失败: {e}")
            return False, str(e)

    def delete_extra_info(self, key: str) -> bool:
        """
        删除预填信息
        Args:
            key: 要删除的字段ID

        Returns:
            是否成功
        """
        if not self.token:
            return False

        try:
            payload = {
                "access_token": self.token,
                "name": key
            }

            self._request(
                "POST",
                API_ENDPOINTS['extra_info'],
                headers=HEADERS['login'],
                json=payload
            )
            return True

        except Exception as e:
            logger.error(f"删除预填信息失败: {e}")
            return False
