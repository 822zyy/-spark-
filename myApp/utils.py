def extract_city(address):
    """
    从地址中提取城市名
    """
    if not address:
        return None

    # 移除空格并分割地址（按照 - 分割）
    parts = address.strip().split('-')
    if parts:
        # 返回第一部分（城市名）
        return parts[0].strip()
    return None


def get_client_ip(request):
    """
    获取客户端IP地址
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip