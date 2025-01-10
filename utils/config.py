# -*- coding: UTF-8 -*-
'''
@File    ：config.py
@IDE     ：PyCharm 
@Author  ：修明
@Email   ：lzmpt@qq.com
@Date    ：2024/12/25 0025 21:28 
@Detail  ：api 相关配置信息
'''
api_prod = "https://api-xcx-qunsou.weiyoubot.cn"
Config = {
            # vip登录
            "vipLogin": '/xcx/enroll/v1/vip/login',
            # 报名详情接口(新)
            "api_detail": "/xcx/enroll/v3/detail",
            # 预约项目数据
            "api_item_detail": "/xcx/enroll/v2/item_detail",
            # 选座项目数据
            "api_seat_detail": "/xcx/enroll/v1/item_detail",
            # 游客模式查看详情
            "api_noLogin_detail": '/xcx/enroll/v1/short_detail',
            # 详情填写字段接口
            "api_req_detail": '/xcx/enroll/v1/req_detail',
            # 微信服务通知信息
            "api_wx_notice_info": '/xcx/enroll/v2/notice/detail',
            # 报名数据接口
            "api_user_list": "/xcx/enroll/v1/user_list",
            # 团购列表
            "team_list": "/xcx/enroll/v1/teams",
            # 团购结果详情
            "team_result_detail": "/xcx/enroll/v1/team_detail",
            # 我的报名数据接口
            "api_my_enroll": "/xcx/enroll/v1/my_enroll",
            # 上次提交记录
            "api_period_detail": '/xcx/enroll/v1/period_detail',
            # 报名用户详情列表
            "api_user_detail": "/xcx/enroll/v1/user_detail",
            # 修改报名信息
            "api_update_enroll": "/xcx/enroll/v1/user_update",
            # 转让参与记录
            "api_move_info": '/xcx/enroll/v1/user/enrol_info_move',
            # 退出报名
            "api_exit_enroll_merch": '/xcx/enroll/ecom/v1/exit',
            # 取消退出报名
            "api_refun_exit": "/xcx/enroll/ecom/v1/cancel_refund",
            # 查看报名
            "api_enroll": "/xcx/enroll/v5/enroll",
            "api_enroll_merch": "/xcx/enroll/ecom/v1/enroll",
            "api_list_info": '/xcx/enroll/refund/v1/list_by_info',
            # 退款详情
            "refund_detail": '/xcx/enroll/v1/refund_detail',
            # 请求支付参数
            "api_enroll_pay": "/xcx/enroll/platform/v1/pay",
            # pc获取支付结果
            "api_order_info": '/xcx/enroll/ecom/v1/order_info',
            # 获取留言列表
            "api_detail_message_list": "/xcx/enroll/v2/message",
            # 公开 or 置顶
            "api_msg_control": "/xcx/enroll/v1/msg_control",
            # 留言回复
            "api_replay_message": "/xcx/enroll/v1/msg_reply",
            # 获取座位图信息
            "api_seat_info": '/xcx/enroll/v1/booked/detail',
            # 绑定手机号
            "api_bind_phone": '/xcx/enroll/v1/bind_phone',
            # 重置登录密码
            "api_reset_pwd": '/xcx/enroll/v1/reset_login_pwd',
            # 解绑手机号
            "api_unbind_phone": '/xcx/enroll/v2/unbind_phone',
            "api_change_phone": '/xcx/enroll/v1/user_rep_phone',
            # 微信上传文件
            "api_upload_file": "/xcx/enroll_web/v1/upload",
            # 普通上传文件
            "api_common_upload": '/xcx/file/v1/upload',
            # 视频文件上传
            "api_video_upload": '/xcx/video/upload',
            # 查看报名凭证
            "api_cert_detail": "/xcx/enroll/v2/cert/detail",
            # 查看自定义报名详情
            "api_cert_custom": '/xcx/enroll/v1/follow/detail',
            # 删除快速填写信息
            "api_extra_info": '/xcx/enroll/v1/extra_info',
            # 回收站单次恢复活动
            "api_bak_pay": '/xcx/enroll/ecom/v2/download_enroll_bak_pay',
            # 查询活动恢复状态
            "api_bak_order": 'xcx/enroll/ecom/v1/download_enroll_bak_pay/order',
            # 分享图二维码生成
            "api_get_share": "/xcx/enroll/v2/share",
            "api_get_homepage_share": "/xcx/enroll/v1/homepage/share",
            "api_subscribe_homepage": "/xcx/enroll/v1/subscribe/switch",
            # 生成分享SchemeUrl
            "api_scheme_url": '/xcx/enroll/v1/scheme_url',
            "api_share_list": 'xcx/enroll/v1/user/info_share_list',
            # 提交账号申诉
            "api_black_appeal": '/xcx/enroll/v1/black_appeal',
            "api_appeal_detail": '/xcx/enroll/v1/black_appeal_detail',

            # 微信签名验证
            "api_wx_sign": "/xcx/enroll_web/v1/sign",

            # 获取TOKEN接口
            "api_wx_getToken": "/xcx/enroll_web/v1/login",
            # 获取用户登录信息
            "api_get_userInfo": "/xcx/enroll/v1/userinfo",
            # 获取用户认证信息
            "api_get_authInfo": "/xcx/enroll/v1/auth/info",
            "api_get_renewInfo": '/xcx/enroll/v1/renew/info',
            # 保存企业、组织、公众号信息
            "api_set_companyInfo": '/xcx/enroll/v3/auth/apply',
            "api_set_renewInfo": '/xcx/enroll/v3/renew/apply',
            "api_get_pc_payResult": '/xcx/enroll/v1/auth/order_info',
            # 获取短信验证码
            "api_get_code": '/xcx/enroll/v1/code',
            # 免登录获取验证码
            "api_pwd_code": '/xcx/enroll/v1/pwd_code',
            # 公众号code验证
            "api_validate_code": '/xcx/enroll/v1/auth/code',
            "api_validate_renewCode": '/xcx/enroll/v1/renew/code',
            # 最近浏览记录
            "api_user_history": '/xcx/enroll/v1/user/history',
            # 我管理的 + 我参与的
            "api_manage_list": '/xcx/enroll/v1/list',
            # 公开活动
            "api_enroll_public": '/xcx/enroll/v1/public',
            # 个人主页
            "api_homepage_info": '/xcx/enroll/v2/homepage/info',
            # 个人主页推荐
            "api_common_homepage": '/xcx/enroll/v1/common_homepage',
            # 个人主页接口（ 免登录）
            "api_homepage_info2": '/xcx/enroll/v3/homepage/share',
            # 公开活动列表
            "api_web_enroll": '/xcx/enroll/web/v1/list',
            # h5添加订阅消息次数
            "api_sub_notice": '/xcx/enroll/v1/h5_sub_notice/up',
            # 我关注的列表
            "api_sub_list": '/xcx/enroll/v1/subscribe/sub_list',
            # 会员卡详情
            "api_vip_card_detail": '/xcx/enroll/v1/vip_card_detail',
            # 会员卡详情2 （参与人从报名信息过来）
            "api_card_list": '/xcx/enroll/v1/my_vip_card_list',
            # 购买会员
            "api_vip_card_pay": '/xcx/enroll/v1/vip_card_pay',
            # 查看会员详情
            "api_user_vip_detail": '/xcx/enroll/v1/user_vip_detail',
            # 提交确认会员数据
            "api_verify_vip": '/xcx/enroll/v1/verify_share_vip',
            # 我加入的会员
            "api_my_join_vip": '/xcx/enroll/v1/my_join_vip_card',
            # 获取企业微信提醒开启状态
            "api_work_config": '/xcx/enroll/v2/user_webhook',
            # 获取企业微信token
            "api_work_token": '/xcx/enroll/v2/work_config/token',
            # 清除最近浏览记录
            "api_history_del": 'xcx/enroll/v1/user/history_del',
            # 注销账号
            "api_cancel_user": '/xcx/enroll/v1/cancel_user_data',
            # h5获取ticket
            "api_short_ticket": '/xcx/enroll/v1/short_ticket',
            # 拼团订单
            "api_cart_orders": '/xcx/enroll/v1/cart',
            # 举报接口
            "api_enroll_report": '/xcx/enroll_web/v1/report',
            # 编辑个人信息
            "api_user_edit": '/xcx/enroll/v1/user_info_edit',
            # 收款码付款
            "api_code_pay": '/xcx/enroll/user_cashier/v1/pay',
            # 授权code，获取openid
            "api_ext_openid": '/xcx/enroll/v1/user/ext_openid',
            # 测试下单
            "api_pay_test": '/xcx/enroll/v1/user/ext_pay_test',
            "api_pay_sign": '/xcx/enroll/v1/user/ext_pay_sign',
            # 收款码商户信息
            "api_cashier_detail": '/xcx/enroll/user_cashier/v1/detail',
            # 我领取的优惠券
            "api_coupon_list": '/xcx/enroll/v2/my_coupon/list',
            # 会员卡购买记录
            "api_vip_order_list": '/xcx/enroll/v1/user_vip_order_list',
            # 会员卡续费
            "api_vip_renew_pay": '/xcx/enroll/v1/renew/vip_card_pay',
            # 发起认证代付
            "api_apply_replace": '/xcx/enroll/v2/auth/apply_replace',
            # 发起续费代付
            "api_apply_renew_replace": '/xcx/enroll/v2/renew/apply_replace',
            # 代付链接详情
            "api_apply_replace_info": '/xcx/enroll/v2/auth/apply_replace_info',
            # 代付拉起支付
            "api_apply_replace_pay": '/xcx/enroll/v3/auth/apply_replace_pay',
            # 删除留言
            "api_msg_del": '/xcx/enroll/v1/msg_del',
            # 用户标记数据分享
            "api_info_share": '/xcx/enroll/v1/user/enrol_info_share',
            # 免登录查看付款价格配置
            "api_price_list": '/xcx/enroll/user_cashier/v1/price_list',
            # 回收站列表
            "api_bak_list": '/xcx/enroll/v1/bak_list',
            # 恢复活动
            "api_recover_enroll": '/xcx/enroll/v1/recover_enroll',
            # 彻底删除活动
            "api_direct_del": '/xcx/enroll/v1/direct_del',
            # 订阅消息场景值
            "api_scene_id": '/xcx/enroll/v1/notice/sub',
            "api_scene_notice": '/xcx/enroll/v1/notice/sub', # 订阅
            "api_cert_check": 'xcx/enroll/v1/cert/check', # 签到
            "api_enroll_token": '/xcx/enroll/v1/token', # 口令验证
            "api_ding_webhook": '/xcx/enroll/v2/user_ding_webhook',
            "api_edit_list": '/xcx/enroll/v1/info_edit_list', # 编辑历史记录
            "api_join_list": '/xcx/enroll/v1/user_join_list', # 最近六个月参与记录
            "api_search_token": '/xcx/enroll/v1/search_token', # 口令
                                                                # 代公众号登录获取token接口
            "api_business_getToken": '/api/platform/v1/login',
            # 代公众授权签名
            "api_business_sign": '/api/platform/v1/sign',
            # 记录操作日志
            "api_auth_log": '/xcx/enroll/v1/auth/log',
            "api_login_code": '/xcx/enroll_web/v1/pc_code',
            "api_pc_login": '/xcx/enroll_web/v1/pc_login', # 公众号登录
            "api_notice_switch": '/xcx/enroll/v1/notice/switch', # 订阅消息提醒开关
            "api_login_phone": '/xcx/enroll/v1/login_by_phone', # 手机号登录
            "api_check_code": '/xcx/enroll/v1/check_phone_code', # 校验手机号
            "api_order_complaint": '/xcx/enroll/ecom/v1/order_complaint', # 订单投诉 & 订单详情
            "api_complaint_msg": '/xcx/enroll/ecom/v1/order_complaint_msg', # 投诉订单留言
            "api_complaint_list": '/xcx/enroll/ecom/v1/order_complaint_msg_list', # 投诉订单留言列表
            "api_complaint_cancel": '/xcx/enroll/ecom/v1/cancel_order_complaint',
            "api_notice_all": 'xcx/enroll/v1/notice_all', # 获取所有的消息通知
            "api_reshipped_enroll": '/xcx/enroll/v1/reshipped', # 转载活动
            "api_group_share": '/xcx/enroll/v2/share', # 邀请参团
            "api_team_user": '/xcx/enroll/v1/team_user/enroll_list', # 共创列表
            # "api_order_detail": '/xcx/enroll/ecom/v1/order_detail', # 订单详情
            "api_risk_qrcode": 'xcx/enroll/v1/check_risk_qrcode', # 账号安全校验code
            "api_order_detail": 'xcx/enroll/v1/record/pay',
            "api_merchant_apply": '/xcx/enroll/ecom/v1/apply', # 商户信息
            "api_enroll_num": 'xcx/enroll/v1/user/enroll_num', # 查询进行中活动的数量
            "api_auth_replace": '/xcx/enroll/v1/user/auth_replace', # VIP权益转让
            "api_close_enroll": '/xcx/enroll/v1/user/close_enroll_all', # 一键截止所有活动
            "api_admin_history": '/xcx/enroll/v1/admin/history', # 管理员记录
            "api_bind_mch": '/xcx/enroll/ecom/v1/admin_bind_mch', # 转让商户
            "api_mch_rep_log": 'xcx/enroll/ecom/v1/mch_rep_log', # 商户转移记录
            "api_share_group": 'xcx/enroll/v1/share_group_stat',
            "api_auth_order": 'xcx/enroll/v1/user_auth_order', # VIP认证记录
            "api_copy_pay": '/xcx/enroll/ecom/v1/copy_ecom/pay', # 回收站复制创建活动
            "api_pay_order": '/xcx/enroll/ecom/v1/apply_pay/order', # 获取订单支付状态
            "api_black_detail": '/xcx/enroll/v1/black_detail', # 拉黑用户详情
            "api_check_white": '/xcx/enroll/v1/check_req_white', # 白名单校验
            "api_record_pay": 'xcx/enroll/v1/record/pay', # 付款记录
            "api_my_complaint_list": '/xcx/enroll/ecom/v1/my_order_complaint_list', # 订单投诉
            "api_my_complaint": '/xcx/enroll/ecom/v1/user/my_complaint', # 商户投诉
            "api_complaint_history": '/xcx/enroll/ecom/v1/user/complaint/history', # 商户投诉明细
            "api_save_new": '/xcx/enroll/v1/save_new_user', # 新用户时保存用户和昵称
            "api_pdf_export": '/mini/enroll/v1/user_pdf_export',
            'api_mch_apply': '/xcx/enroll/ecom/v1/apply', # 商户申请
            "api_balance": '/xcx/enroll/ecom/v1/balance', # 账户金额
            "api_merchant_stat": '/xcx/enroll/ecom/v1/merchant_stat', # 风险投诉数量
            "api_search_upload": '/will/v1/file/upload', # 会查上传文件
            "bm_domain": "false",

            # 数据接口读取超时时间
            "timeout": 20000,
            "pageCount": 1,
            "pageSize": 10,
            "appid": "wx7145c571b99a8368",
            "secretKey": "kljhakjsdnasdfyff",
            "bmAppid": "wxe2f0a4b9f48071f5",
            "businessId": 'wxe527a5b179a1a930',

            "wx_token_key": "WXACCESSTOKEN_KEY",
            "wx_code_key": "WXCODE_KEY",
}

login_headers = {
          'accept': 'application/json, text/plain, */*',
          'accept-language': 'zh-CN,zh;q=0.9',
          'cache-control': 'no-cache',
          'dnt': '1',
          'origin': 'https://p.baominggongju.com',
          'pragma': 'no-cache',
          'priority': 'u=1, i',
          'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"Windows"',
          'sec-fetch-dest': 'empty',
          'sec-fetch-mode': 'cors',
          'sec-fetch-site': 'cross-site',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
        }
