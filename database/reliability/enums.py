FRESHMAN = 'FR'
SOPHOMORE = 'SO'
JUNIOR = 'JR'
SENIOR = 'SR'
GRADUATE = 'GR'

YEAR_IN_SCHOOL_CHOICES = [
    (FRESHMAN, 'Freshman'),
    (SOPHOMORE, 'Sophomore'),
    (JUNIOR, 'Junior'),
    (SENIOR, 'Senior'),
    (GRADUATE, 'Graduate'),
]

FALL = 1
WINTER = 2
SPRING = 3
SUMMER = 4

SEASONS = (
    (FALL, "Fall"),
    (WINTER, "Winter"),
    (SPRING, "Spring"),
    (SUMMER, "Summer")
)

MONDAY = "M"
TUESDAY = "Tu"
WEDNESDAY = "W"
THURSDAY = "Th"
FRIDAY = "F"

WEEKDAYS = (
    (MONDAY, "Monday"),
    (TUESDAY, "Tuesday"),
    (WEDNESDAY, "Wednesday"),
    (THURSDAY, "Thursday"),
    (FRIDAY, "Friday")
)

POSSIBLE_HOURS = (
    ("00", 0),
    ("01", 1),
    ("02", 2),
    ("03", 3),
    ("04", 4),
    ("05", 5),
    ("06", 6),
    ("07", 7),
    ("08", 8),
    ("09", 9),
    ("10", 10),
    ("11", 11),
    ("12", 12)
)

POSSIBLE_MINUTES = (
    ("00", 0),
    ("05", 5),
    ("10", 10),
    ("15", 15),
    ("20", 20),
    ("25", 25),
    ("30", 30),
    ("35", 35),
    ("40", 40),
    ("45", 45),
    ("50", 50),
    ("55", 55)
)
