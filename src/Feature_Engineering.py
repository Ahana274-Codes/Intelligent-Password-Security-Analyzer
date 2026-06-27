import math
import pandas as pd
from collections import Counter


def extract_password_features(password_string):
    """
    Transforms a raw password string into the clean mathematical features
    expected by the machine learning model.
    """
    password_string = str(password_string) if not pd.isna(password_string) else ""
    length = len(password_string)

    lowercase_count = sum(1 for c in password_string if c.islower())
    uppercase_count = sum(1 for c in password_string if c.isupper())
    digit_count = sum(1 for c in password_string if c.isdigit())
    special_count = sum(1 for c in password_string if not c.isalnum())
    unique_chars = len(set(password_string))

    types_present = sum(
        [lowercase_count > 0, uppercase_count > 0, digit_count > 0, special_count > 0]
    )
    diversity_ratio = types_present / 4.0 if length > 0 else 0.0

    if length > 0:
        counts = Counter(password_string)
        entropy = -sum(
            (count / length) * math.log2(count / length) for count in counts.values()
        )
    else:
        entropy = 0.0

    return {
        "length": length,
        "lowercase_count": lowercase_count,
        "uppercase_count": uppercase_count,
        "digit_count": digit_count,
        "special_count": special_count,
        "unique_chars": unique_chars,
        "diversity_ratio": diversity_ratio,
        "entropy": entropy,
    }
