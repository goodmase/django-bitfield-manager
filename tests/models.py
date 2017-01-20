from django.db import models
from bitfield_manager.models import ParentBitfieldModelMixin


class BaseTestModel(ParentBitfieldModelMixin, models.Model):
    """
    Base for test models that sets app_label, so they play nicely.
    """
    class Meta:
        app_label = 'tests'
        abstract = True


    def save(self, *args, **kwargs):
        super(BaseTestModel, self).save(*args, **kwargs)


class ParentTestModel(BaseTestModel):

    STATUS_CHILD1 = 0
    STATUS_CHILD2 = 1
    STATUS_CHILD3 = 2

    name = models.CharField(max_length=255)
    status = models.BigIntegerField()

    def __str__(self):
        return "name: %s status: %i" % (self.name, self.status)


class ChildTestModel1(BaseTestModel):
    parent = models.ForeignKey('ParentTestModel', related_name='childtestmodels1', null=True)

    class BitfieldMeta:
        parent_models = [('parent', 'status', ParentTestModel.STATUS_CHILD1)]


class ChildTestModel2(BaseTestModel):
    parent = models.ForeignKey('ParentTestModel', related_name='childtestmodels2')

    class BitfieldMeta:
        parent_models = [('parent', 'status', ParentTestModel.STATUS_CHILD2)]


class ChildTestModel3(BaseTestModel):
    parent = models.ForeignKey('ParentTestModel', related_name='childtestmodels3')

    class BitfieldMeta:
        parent_models = [('parent', 'status', ParentTestModel.STATUS_CHILD3)]


class Unrelated(BaseTestModel):
    parent = models.ForeignKey('ParentTestModel', related_name='unrelatedmodels3')
