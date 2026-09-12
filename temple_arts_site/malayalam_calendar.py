"""
Simple helper for working with the Malayalam (Kollam Era) calendar.

IMPORTANT: Converting between the Gregorian and Malayalam calendars accurately
requires solar-longitude / panchangam data, because Malayalam months begin
when the sun enters a particular zodiac sign (a solar event), not on a fixed
day every year. The function below gives an APPROXIMATE conversion only
(useful for showing a rough Malayalam date next to a Gregorian one). For
real temple events, always let the event creator type in the exact Malayalam
month/day themselves (the event form in this app supports that) rather than
relying purely on auto-conversion.
"""

from datetime import date

MALAYALAM_MONTHS = [
    "Chingam", "Kanni", "Thulam", "Vrischikam", "Dhanu", "Makaram",
    "Kumbham", "Meenam", "Medam", "Edavam", "Midhunam", "Karkidakam",
]

# Approximate Gregorian start-day-of-month for each Malayalam month
# (varies by 1-2 days year to year in reality; this is a rough guide only)
_APPROX_START = [
    (8, 17), (9, 17), (10, 17), (11, 16), (12, 16), (1, 14),
    (2, 13), (3, 15), (4, 14), (5, 15), (6, 15), (7, 17),
]

NAKSHATRAS = [
    "Ashwathi", "Bharani", "Karthika", "Rohini", "Makayiram", "Thiruvathira",
    "Punartham", "Pooyam", "Ayilyam", "Makam", "Pooram", "Uthram", "Atham",
    "Chithira", "Chothi", "Vishakham", "Anizham", "Thrikketta", "Moolam",
    "Pooradam", "Uthradam", "Thiruvonam", "Avittam", "Chathayam",
    "Pooruruttathi", "Uthrattathi", "Revathi",
]


def approximate_malayalam_date(gdate: date):
    """Return (month_name, approx_day) for a given Gregorian date.

    This is only a rough estimate (+/- a day or two) since it does not use
    real solar-longitude data. Good enough for display purposes only.
    """
    # Build a sorted list of (date_obj, month_index) covering the year around gdate
    candidates = []
    for offset_year in (gdate.year - 1, gdate.year, gdate.year + 1):
        for idx, (m, d) in enumerate(_APPROX_START):
            try:
                candidates.append((date(offset_year, m, d), idx))
            except ValueError:
                pass
    candidates.sort()

    month_name = MALAYALAM_MONTHS[0]
    approx_day = 1
    for i in range(len(candidates) - 1):
        start_d, idx = candidates[i]
        end_d, _ = candidates[i + 1]
        if start_d <= gdate < end_d:
            month_name = MALAYALAM_MONTHS[idx]
            approx_day = (gdate - start_d).days + 1
            break

    return month_name, approx_day
