from helpers import HiddenPrints
from tests import ALL_TESTS

if __name__ == "__main__":
    print("Starting tests...")
    for test in ALL_TESTS:
        print("Running: " + test.__name__)
        # Prevents prints in the terminal inside the 'with' block
        with HiddenPrints():
            test()
    print("Passed all tests!")