# -*- coding: UTF-8 -*-
"""
认证服务模块
处理用户登录和token管理
"""
import logging
from typing import Optional, Dict, Any

from rich.console import Console

from utils.api_client import APIClient
from utils.validators import validate_token

console = Console(color_system='256', style=None)
logger = logging.getLogger(__name__)


class AuthService:
    """认证服务类"""

    def __init__(self):
        self.api_client = APIClient()
        self.user_info: Optional[Dict[str, Any]] = None
        self.extra_info: Dict[str, str] = {}

    def set_token(self, token: str) -> bool:
        """
        设置并验证token
        Args:
            token: 用户token

        Returns:
            是否成功
        """
        if not validate_token(token):
            console.print("[red]无效的token格式[/red]")
            return False

        try:
            self.api_client.set_token(token)
            return self._load_user_info()
        except Exception as e:
            logger.error(f"设置token失败: {e}")
            console.print(f"[red]设置token失败: {e}[/red]")
            return False

    def _load_user_info(self) -> bool:
        """
        加载用户信息和预填信息
        Returns:
            是否成功
        """
        user_info = self.api_client.get_user_info()
        if not user_info:
            console.print("[red]获取用户信息失败，请检查token是否有效[/red]")
            return False

        self.user_info = user_info

        # 提取预填信息
        extra_infos = user_info.get('extra_info', [])
        if extra_infos:
            for extra_info in extra_infos:
                field_name = extra_info.get('name', [])
                if isinstance(field_name, list) and len(field_name) > 0:
                    self.extra_info[field_name[0]] = extra_info.get('value', '')
                else:
                    self.extra_info[field_name] = extra_info.get('value', '')

        self._display_user_info()
        return True

    def _display_user_info(self):
        """显示用户信息"""
        console.print("[green]----------登录信息----------[/green]")
        name = self.user_info.get('name', 'N/A')
        phone = self.user_info.get('phone', 'N/A')
        console.print(f"[green]姓名：{name}[/green]")
        console.print(f"[green]电话：{phone}[/green]")
        console.print("[green]----------预填信息----------[/green]")

        if self.extra_info:
            for key, value in self.extra_info.items():
                console.print(f"[green]{key}: {value}[/green]")

        console.print("[green]---------------------------[/green]")

    def get_extra_info(self) -> Dict[str, str]:
        """获取预填信息"""
        return self.extra_info.copy()

    def get_user_name(self) -> str:
        """获取用户姓名"""
        return self.user_info.get('name', '') if self.user_info else ''

    def get_user_phone(self) -> str:
        """获取用户手机号"""
        return self.user_info.get('phone', '') if self.user_info else ''

    def add_extra_info(self, name: str, value: str) -> bool:
        """
        添加预填信息
        Args:
            name: 字段名
            value: 字段值

        Returns:
            是否成功
        """
        success, msg = self.api_client.add_extra_info(name, value)
        if success:
            self.extra_info[name] = value
            console.print(f"[green]添加预填信息成功: {name}={value}[/green]")
        else:
            console.print(f"[red]添加预填信息失败: {msg}[/red]")
        return success

    def delete_extra_info(self, key: str) -> bool:
        """
        删除预填信息
        Args:
            key: 字段ID

        Returns:
            是否成功
        """
        success = self.api_client.delete_extra_info(key)
        if success:
            self.extra_info.pop(key, None)
            console.print(f"[green]删除预填信息成功: {key}[/green]")
        else:
            console.print("[red]删除预填信息失败[/red]")
        return success
