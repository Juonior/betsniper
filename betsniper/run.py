from fonbet.scanner import main as fonbet_scanner
from olimp.scanner import main as olimp_scanner

import time
sports = ["basketball"]

if __name__ == "__main__":
    s = fonbet_scanner(requested_sports = sports)
    g = olimp_scanner(requested_sports = sports)