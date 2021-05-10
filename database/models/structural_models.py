from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class ModelSet(models.Model):
    """
    A model to represent a set of objects.
    Used by:
        (1) Courses to represent a group of courses (for example the set of classes that is sent to gather student
            interest)
        (2) Sets of preferences to group them for convenience sake.
    """
    name = models.CharField(max_length=256, blank=False, null=False, unique=True)

    # this limits the obj_type selections
    limit = models.Q(app_label='database', model='course') | \
            models.Q(app_label='database', model='student') | \
            models.Q(app_label='database', model='preference')

    obj_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=limit)

    def __str__(self):
        return self.name


class SetMembership(models.Model):
    """
    A model to represent that a given model belongs to the given model set.
    """
    set = models.ForeignKey(ModelSet, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    member_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return str(self.member_object) + " is member of " + str(self.set)


class Preference(models.Model):
    """
    True: Positive Preference (I.e 2 classes must be offered at the same time)
    False: Negative Preference (I.e 2 classes have to be offered at different times)
    """
    weight = models.BooleanField()

    limit = models.Q(app_label='database', model='course') | \
            models.Q(app_label='accounts', model='baseuser') | \
            models.Q(app_label='database', model='timeblock') | \
            models.Q(app_label='database', model='section')

    object_1_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True,
                                              related_name="object_1_content_type", limit_choices_to=limit)
    object_1_id = models.PositiveIntegerField(null=True, blank=True)
    object_1 = GenericForeignKey('object_1_content_type', 'object_1_id')
    object_2_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True,
                                              related_name="object_2_content_type", limit_choices_to=limit)
    object_2_id = models.PositiveIntegerField(null=True, blank=True)
    object_2 = GenericForeignKey('object_2_content_type', 'object_2_id')

    sets = GenericRelation(SetMembership, related_query_name='preference')

    def __str__(self):
        weight_sentiment = " - Negative"
        if self.weight:
            weight_sentiment = " - Positive"

        return str(self.object_1) + " & " + str(self.object_2) + weight_sentiment

    class Meta:
        verbose_name_plural = "preferences"


class Department(models.Model):
    """
    An academic department.
    """
    abbreviation = models.CharField(max_length=4, blank=False, null=False)
    name = models.CharField(max_length=256, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name + ": " + self.abbreviation

    def natural_key(self):
        return self.name


class Registration(models.Model):
    """
    Relationship to signify a students registration for a course section (not necessarily successful)
    """
    section = models.ForeignKey("database.Section", on_delete=models.CASCADE)
    student = models.ForeignKey("database.Student", on_delete=models.CASCADE)
    approval = models.BooleanField(default=False)
    approving_teacher = models.ForeignKey("database.Teacher", on_delete=models.CASCADE)

    def __str__(self):
        return self.student.user.get_full_name() + " registration for " + self.section.__str__()

    class Meta:
        verbose_name_plural = "registrations"
