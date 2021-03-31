from django.db import models


class Preference(models.Model):
    """
    True: Positive Preference (I.e 2 classes must be offered at the same time)
    False: Negative Preference (I.e 2 classes have to be offered at different times)
    """
    weight = models.BooleanField()

    """
    Possible Constraint Expressions:
        - Course / Other Course
            - Course overlaps and pre/co requisites are expressed this way.
        - Course / User 
            - Does a teacher / student want to teach / take the class.
        - Course / Timeblock
            - A course should / should not be offered during a timeblock.
        - Course / Other Course / Timeblock
            - The following two classes cannot be offered during the same timeblock.
        - User (Teacher) / Timeblock
            - The given user needs to / can't teach a class during the given timeblock.        
    """
    course = models.ForeignKey("database.Course", on_delete=models.CASCADE, null=True, blank=True)
    other_course = models.ForeignKey("database.Course", on_delete=models.CASCADE, related_name="other course+")
    user = models.ForeignKey("accounts.BaseUser", on_delete=models.CASCADE, null=True, blank=True)
    timeblock = models.ForeignKey("database.Timeblock", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "preferences"