from enums import Symbol


def test_symbol():
    symbol: Symbol = Symbol('EOS')
    assert symbol.base == "EOS"
