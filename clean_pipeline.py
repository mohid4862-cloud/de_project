import re

dirty_data = {
    "PKR": "278.01",
    "EUR": None,
    "GBP": -0.74,
    "AED": "  3.67  ",
    "SAR": "  3.75abc  ",
}

print("--- Cleaning dirty data ---")
for currency, rate in dirty_data.items():

    if rate is None:
        print(f"{currency}: missing value — set to 0.0")
        continue

    if isinstance(rate, str):
        rate = rate.strip()
        rate = re.sub(r'[^0-9.]', '', rate)
        rate = float(rate)

    if rate < 0:
        rate = abs(rate)
        print(f"{currency}: negative rate fixed to {rate}")
        continue

    print(f"{currency}: {round(rate, 2)}")