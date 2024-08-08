from src.services import investment_bank


def test_investment_bank(test_transactions):
    test_month = "2023-06"
    test_limit = 50
    expected = 74.5
    result = investment_bank(test_month, test_transactions, test_limit)

    assert result == expected
