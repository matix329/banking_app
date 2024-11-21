import pytest
from banking_core.services.limits.limit_validator import LimitValidator

def test_validate_limit_amount():
    with pytest.raises(ValueError):
        LimitValidator.validate_limit_amount(-1)

    with pytest.raises(ValueError):
        LimitValidator.validate_limit_amount("100")

    with pytest.raises(ValueError):
        LimitValidator.validate_limit_amount(0)

    try:
        LimitValidator.validate_limit_amount(100)
    except ValueError:
        pytest.fail("validate_limit_amount() raised ValueError unexpectedly!")

    
def test_validate_limit_change_attempts():
    with pytest.raises(ValueError):
        LimitValidator.validate_limit_change_attempts(5, 5)

    with pytest.raises(ValueError):
        LimitValidator.validate_limit_change_attempts(6, 5)

    try:
        LimitValidator.validate_limit_change_attempts(4, 5)
    except ValueError:
        pytest.fail("validate_limit_change_attempts() raised ValueError unexpectedly!")