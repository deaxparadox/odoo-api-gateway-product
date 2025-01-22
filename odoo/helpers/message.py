def message_collector():
    messages = []
    def collect(mes: str = None):
        nonlocal messages
        if mes:
            messages.append(mes)
            return
        return messages
    return collect