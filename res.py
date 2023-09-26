
import re

title = "1537 restaurants"
# Use regex to match the number
match = re.search(r'\b(\d+)\b', title)

if match:
    restaurant_count = int(match.group(1))
    print("Number of restaurants:", restaurant_count)
else:
    print("No restaurant count found.")
