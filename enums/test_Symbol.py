from enums import Symbol


def test_symbol():
    symbol: Symbol = Symbol('EOS')

    json_str = symbol.json

    assert symbol.base == "EOS"

    assert symbol.Loads(json_str) == symbol

    assert symbol.Parse(json_str) == symbol
