from django.db import models
from bitfield_manager.models import ParentBitfieldModelMixin
from bitfield import BitField


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
    STATUS_CHILD_CHILD = 3

    name = models.CharField(max_length=255)
    status = models.BigIntegerField()
    secondary_status = models.BigIntegerField()
    bitfield_status = BitField(flags=(
        ('status_child1', 'Status Child 1'),
        ('status_child2', 'Status Child 2'),
        ('status_child3', 'Status Child 3'),
        ('status_child_child', 'Status Child Child')
    ))

    def __str__(self):
        return "name: %s status: %i" % (self.name, self.status)


class ChildTestModel1(BaseTestModel):
    parent = models.ForeignKey('ParentTestModel', related_name='childtestmodels1', null=True)

    class BitfieldMeta:
        parent_models = [('parent', 'status', ParentTestModel.STATUS_CHILD1),
                         ('parent', 'bitfield_status', ParentTestModel.bitfield_status.status_child1)]


class ChildTestModel2(BaseTestModel):
    parent = models.ForeignKey('ParentTestModel', related_name='childtestmodels2')

    class BitfieldMeta:
        parent_models = [('parent', 'status', ParentTestModel.STATUS_CHILD2),
                         ('parent', 'bitfield_status', ParentTestModel.bitfield_status.status_child2)]


class ChildTestModel3(BaseTestModel):
    parent = models.ForeignKey('ParentTestModel', related_name='childtestmodels3')

    class BitfieldMeta:
        parent_models = [('parent', 'status', ParentTestModel.STATUS_CHILD3),
                         ('parent', 'secondary_status', ParentTestModel.STATUS_CHILD3),
                         ('parent', 'bitfield_status', ParentTestModel.bitfield_status.status_child3)]


class ChildChildTestModel(BaseTestModel):
    child = models.ForeignKey('ChildTestModel1', related_name='childchildtestmodels')

    class BitfieldMeta:
        parent_models = [('child.parent', 'status', ParentTestModel.STATUS_CHILD_CHILD),
                         ('child.parent', 'bitfield_status', ParentTestModel.bitfield_status.status_child_child)]


class Unrelated(BaseTestModel):
    parent = models.ForeignKey('ParentTestModel', related_name='unrelatedmodels3')
