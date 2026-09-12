"""
One-time script to seed the Temple Arts & Heritage site with:
  - A handful of starter blog posts (written from general knowledge,
    not copied from any website) covering common Kerala temple rituals,
    art forms, and festivals
  - A few upcoming temple festival events with real, sourced dates

Run this once after setting up the site:
    python seed_content.py

Everything created here can be edited or corrected by anyone visiting
the site, so treat this as a community starting point, not a finished
reference.
"""

from datetime import date
from app import app
from models import db, BlogPost, TempleEvent

BLOG_SEED = [
    {
        "title": "Theyyam: When the Divine Walks Among the Living",
        "category": "Rituals",
        "content": (
            "Theyyam is one of the most striking ritual art forms of North Kerala, "
            "practised mainly in the Kolathunadu region (today's Kannur and Kasaragod "
            "districts). In a Theyyam performance, a chosen performer undergoes an "
            "elaborate transformation through costume, face painting, and headgear, "
            "and is believed to become a living vessel for a deity, ancestor spirit, "
            "or local hero during the ritual.\n\n"
            "Performances usually take place in kavus (sacred groves) or small "
            "shrines rather than large temples, and each Theyyam has its own origin "
            "story, song (thottam), and set of movements passed down within specific "
            "families of performers. The ritual often runs through the night, with "
            "drumming, fire, and the performer working themselves into an intense, "
            "trance-like state before blessing devotees individually.\n\n"
            "Unlike many temple rituals that are led by Brahmin priests, Theyyam is "
            "traditionally performed by people from specific communities, and it is "
            "considered one of the few ritual spaces in Kerala where caste hierarchies "
            "are symbolically reversed for the duration of the performance. If you've "
            "witnessed a Theyyam yourself, please add your own account below — regional "
            "variations are numerous and this is meant to grow with your knowledge."
        ),
    },
    {
        "title": "Kalamezhuthu: Drawing the Deity on the Temple Floor",
        "category": "Temple Arts",
        "content": (
            "Kalamezhuthu is a ritual art form in which intricate images of deities "
            "— most commonly Kali, Ayyappan, or serpent gods (Nagas) — are drawn "
            "directly on the floor using natural coloured powders: rice flour for "
            "white, turmeric for yellow, charcoal for black, and burnt husk or "
            "leaves for other shades.\n\n"
            "The artist, usually from a Kurup or Theeyattu family trained in the "
            "tradition, works freehand and from memory, often completing a large, "
            "detailed image in a few hours. Once finished, the Kalam is worshipped "
            "with lamps, offerings, and often an accompanying song performance "
            "(Kalamezhuthu Pattu), before being ritually erased — a reminder that "
            "the image is not meant to last, only to serve as a temporary seat for "
            "the deity during the ritual.\n\n"
            "This tradition is especially associated with temples and sacred groves "
            "in central and northern Kerala. If your family temple performs this "
            "ritual with variations not mentioned here, please edit this post to add them."
        ),
    },
    {
        "title": "Panchavadyam: The Five-Instrument Temple Orchestra",
        "category": "Music & Dance",
        "content": (
            "Panchavadyam is a temple percussion ensemble built around five "
            "traditional instruments: thimila, maddalam, ilathalam (cymbals), "
            "kombu (a curved horn), and idakka. Despite the name meaning "
            "'five instruments,' performances are usually dominated by large "
            "numbers of thimila and maddalam players alongside a smaller number "
            "of the others.\n\n"
            "A full Panchavadyam performance is structured in clearly defined "
            "stages, starting at a slow, meditative tempo and gradually building "
            "in speed and intensity over roughly ninety minutes to two hours, "
            "reaching a thunderous climax before ending abruptly. It is most "
            "often heard during temple processions, especially alongside "
            "caparisoned elephants during festivals such as Thrissur Pooram.\n\n"
            "Training in Panchavadyam is intensive and often begins in childhood "
            "under a guru, with players expected to internalise complex rhythmic "
            "cycles (talas) over years of practice. Community members with deeper "
            "knowledge of specific talas or regional styles are encouraged to "
            "expand this post."
        ),
    },
    {
        "title": "Onam: Kerala's Harvest Homecoming",
        "category": "History",
        "content": (
            "Onam is Kerala's best-known festival, celebrated across the state "
            "regardless of religion, and centres on the legend of the just king "
            "Mahabali, who is believed to return once a year to visit the people "
            "he once ruled. According to the story, the god Vishnu, in his dwarf "
            "form Vamana, sent Mahabali to the netherworld out of humility, but "
            "granted him an annual visit to the land and people he loved.\n\n"
            "The festival spans about ten days, beginning on Atham and reaching "
            "its peak on Thiruvonam day, both determined by nakshatra (lunar "
            "mansion) rather than a fixed date, which is why Onam falls on a "
            "different Gregorian date each year. Celebrations include the "
            "Pookalam (intricate flower carpets laid at the entrance of homes), "
            "the Onasadya (an elaborate vegetarian feast served on a banana leaf "
            "with an odd number of dishes, traditionally around 26), boat races "
            "such as the Vallamkali, and performances like Pulikali (tiger dance) "
            "in Thrissur.\n\n"
            "If your family or region has Onam customs not mentioned here, please add them."
        ),
    },
    {
        "title": "Guruvayur Ekadasi and the Tradition of Fasting Days",
        "category": "Rituals",
        "content": (
            "Ekadasi — the eleventh day of each lunar fortnight — is observed as "
            "a fasting and worship day across much of Hindu India, and Kerala's "
            "temples, especially the Guruvayur Sree Krishna Temple, mark it with "
            "particular devotion. Vrishchika Ekadasi (falling in the Malayalam "
            "month of Vrischikam) is considered the most significant of these at "
            "Guruvayur and draws especially large crowds of pilgrims.\n\n"
            "Observant devotees typically avoid grains and certain foods on "
            "Ekadasi, spend the day in prayer or temple visits, and some observe "
            "a complete fast until the following morning. At major temples, the "
            "day often includes special processions, extended darshan hours, and "
            "cultural performances held through the night.\n\n"
            "Fasting customs vary quite a bit by family and region in Kerala — "
            "please edit this post to include practices you follow that aren't "
            "captured here."
        ),
    },
    {
        "title": "Thrissur Pooram: The Festival of All Festivals",
        "category": "History",
        "content": (
            "Thrissur Pooram is widely considered the grandest of Kerala's temple "
            "festivals, held annually at the Thekkinkadu Maidan around the "
            "Vadakkunnathan Temple in Thrissur. Its date is fixed by the Pooram "
            "nakshatra falling in the Malayalam month of Medam, so like most "
            "temple festivals here it shifts on the Gregorian calendar from year "
            "to year.\n\n"
            "The festival is best known for its two rival processions, from the "
            "Paramekkavu and Thiruvambady temples, each featuring rows of richly "
            "caparisoned elephants carrying ceremonial umbrellas that are "
            "exchanged in a dazzling display called Kudamattam. The processions "
            "are accompanied by massive percussion ensembles, including "
            "Panchavadyam, and the event traditionally runs for around 36 hours, "
            "closing with an all-night fireworks display at dawn.\n\n"
            "The festival in its current form is credited to Sakthan Thampuran, "
            "the Maharaja of Cochin, who in the late 18th century brought "
            "together the smaller poorams of surrounding temples into one shared "
            "celebration. If you've attended and want to add first-hand detail, "
            "please do."
        ),
    },
]

# Real, sourced dates for well-known Kerala temple festivals.
# NOTE: These dates shift every year because they're fixed by nakshatra/solar
# events, not a fixed Gregorian date. Please update annually.
EVENT_SEED = [
    {
        "temple_name": "Statewide (Kerala)",
        "title": "Vishu",
        "description": (
            "Malayalam solar new year, marked by the Vishukkani (an auspicious "
            "arrangement viewed first thing at dawn) and Vishukkaineetam (elders "
            "gifting money to children). Falls on Medam 1 each year."
        ),
        "gregorian_date": date(2027, 4, 15),
        "malayalam_month": "Medam",
        "malayalam_day": 1,
        "nakshatram": "",
        "location": "Kerala, India",
    },
    {
        "temple_name": "Vadakkunnathan Temple, Thrissur",
        "title": "Thrissur Pooram",
        "description": (
            "Kerala's grandest temple festival: rival processions from "
            "Paramekkavu and Thiruvambady temples with caparisoned elephants, "
            "Kudamattam (umbrella exchange), massive percussion ensembles, and "
            "an all-night fireworks finale. Date fixed by the Pooram nakshatra "
            "in the month of Medam."
        ),
        "gregorian_date": date(2027, 4, 17),
        "malayalam_month": "Medam",
        "malayalam_day": None,
        "nakshatram": "Pooram",
        "location": "Thrissur, Kerala",
    },
    {
        "temple_name": "Statewide (Kerala)",
        "title": "Thiruvonam (main Onam day)",
        "description": (
            "The main day of the Onam harvest festival, marking the legendary "
            "annual homecoming of King Mahabali. Celebrated with the Onasadya "
            "feast, Pookalam flower carpets, and cultural events across Kerala."
        ),
        "gregorian_date": date(2027, 9, 12),
        "malayalam_month": "Chingam",
        "malayalam_day": None,
        "nakshatram": "Thiruvonam",
        "location": "Kerala, India",
    },
]


def seed():
    with app.app_context():
        db.create_all()

        created_posts = 0
        for post in BLOG_SEED:
            exists = BlogPost.query.filter_by(title=post["title"]).first()
            if exists:
                continue
            db.session.add(BlogPost(
                title=post["title"],
                category=post["category"],
                content=post["content"],
                author_name="Temple Committee",
            ))
            created_posts += 1

        created_events = 0
        for ev in EVENT_SEED:
            exists = TempleEvent.query.filter_by(
                title=ev["title"], gregorian_date=ev["gregorian_date"]
            ).first()
            if exists:
                continue
            db.session.add(TempleEvent(
                temple_name=ev["temple_name"],
                title=ev["title"],
                description=ev["description"],
                gregorian_date=ev["gregorian_date"],
                malayalam_month=ev["malayalam_month"],
                malayalam_day=ev["malayalam_day"],
                nakshatram=ev["nakshatram"] or None,
                location=ev["location"],
                author_name="Temple Committee",
            ))
            created_events += 1

        db.session.commit()
        print(f"Seeded {created_posts} blog post(s) and {created_events} event(s).")
        print("Re-running this script later will skip anything already added.")


if __name__ == "__main__":
    seed()
