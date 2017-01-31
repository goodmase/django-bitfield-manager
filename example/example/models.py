from django.db import models
from bitfield_manager.models import ParentBitfieldModelMixin, ChildBitfieldModelMixin
from bitfield import BitField


class Person(ParentBitfieldModelMixin, models.Model):
    name = models.CharField(max_length=255)
    status = BitField(flags=(
        ('has_children', 'Has Children'),
        ('has_a_home', 'Has a Home'),
        ('has_a_car', 'Has a car')
    ))

    def __str__(self):
        return "NAME: %s STATUS: %s" % (self.name, ",".join([str(s) for s in self.status]))


class Car(ChildBitfieldModelMixin, models.Model):
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    owner = models.ForeignKey('Person')

    class BitfieldMeta:
        parent_models = [('owner.status', Person.status.has_a_car)]


class Child(ChildBitfieldModelMixin, models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('Person')

    class BitfieldMeta:
        parent_models = [('parent.status', Person.status.has_children)]


class Home(ChildBitfieldModelMixin, models.Model):
    owner = models.ForeignKey('Person')

    class BitfieldMeta:
        parent_models = [('owner.status', Person.status.has_a_home)]
