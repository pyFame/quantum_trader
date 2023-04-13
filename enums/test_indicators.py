from enums.indicators import Message_Signal


def test_Message_Signal():
    msg_signal = Message_Signal(indicator='MACD', signal='BUY', low=28100.0, high=28336.3, indicator_value=None)
    # filters=[{200, 'SMA'}])

    assert msg_signal.json == alogmsg_signal)
