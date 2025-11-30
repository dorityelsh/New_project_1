
import xml.etree.ElementTree as ET
import csv

xml_file = "/Users/idan/Downloads/apple_health_export 2/ייצוא.xml"     # שם קובץ ה-XML
csv_file = "all_data_app.csv"      # שם קובץ ה-CSV שיווצר

tree = ET.parse(xml_file)
root = tree.getroot()

records = root.findall(".//Record")

# steps_data = []
# for r in records:
#     if r.get("type") == "HKQuantityTypeIdentifierStepCount":
#         steps_data.append([
#             r.get("startDate"),
#             r.get("endDate"),
#             r.get("value")
#         ])
all_keys = set()

for r in records:
    for key in r.attrib.keys():
        all_keys.add(key)

# הופכים לרשימה ומסדרים
all_keys = list(all_keys)

# כתיבת הנתונים ל-CSV
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    # writer.writerow(["startDate", "endDate", "steps"])
    # writer.writerows(steps_data)
    writer.writerow(all_keys)  # כותבים את כותרות העמודות
    for r in records:
        row = [r.get(k, "") for k in all_keys]
        writer.writerow(row)
print("Done! Created:", csv_file)
