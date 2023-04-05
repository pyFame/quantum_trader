from typing import Final, Union
import os

DEV: Final[str] = "dev"
PROD: Final[str] = "prod"
TEST: Final[str] = "test"

mode: Union[DEV, PROD, TEST] = PROD

modes = {
    DEV: 2,
    PROD: 0,
    TEST: 1,
}

mode = os.getenv("mode", mode)
