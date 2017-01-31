#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_django-bitfield-manager
------------

Tests for `django-bitfield-manager` models module.
"""
from django.test import TestCase

from tests.models import ParentTestModel, ChildTestModel1, ChildTestModel2, ChildTestModel3, \
    Unrelated, ChildChildTestModel, ChildManyToManyTestModel, BrokenChildTestModel


def create_default_parent(name):
    return ParentTestModel.objects.create(name=name, status=0, secondary_status=0)


def get_parent(name):
    return ParentTestModel.objects.filter(name=name).first()


class TestBrokenChildModel(TestCase):
    def test_parent_not_found(self):
        with self.assertRaises(AttributeError) as e:  # noqa: F841
            BrokenChildTestModel.objects.create()


class TestUnsetFunctionsOnParent(TestCase):
    def setUp(self):
        p = create_default_parent('parent1')
        p.set_flag('status', 2)
        p.set_flag('status', 0)
        p.set_flag('bitfield_status', ParentTestModel.bitfield_status.status_child1)
        p.set_flag('bitfield_status', ParentTestModel.bitfield_status.status_child3, save=True)

    def _base_test(self):
        p = get_parent('parent1')
        self.assertEqual(p.status, 5)
        self.assertEqual(int(p.bitfield_status), 5)

    def test_unset_flag_raw(self):
        self._base_test()
        p = get_parent('parent1')
        p.unset_flag('status', 0)
        self.assertEqual(p.status, 4)

    def test_unset_flag_bitfield(self):
        self._base_test()
        p = get_parent('parent1')
        p.unset_flag('bitfield_status', ParentTestModel.bitfield_status.status_child1, save=True)
        self.assertEqual(int(p.bitfield_status), 4)

    def test_unset_flag_mix(self):
        self._base_test()
        p = get_parent('parent1')
        p.unset_flag('bitfield_status', 0)
        p.unset_flag('status', ParentTestModel.bitfield_status.status_child1)
        self.assertEqual(int(p.bitfield_status), 4)
        self.assertEqual(p.status, 4)


class TestSetFunctionsOnParent(TestCase):
    def setUp(self):
        create_default_parent('parent1')

    def _base_test(self):
        p = get_parent('parent1')
        self.assertEqual(p.status, 0)
        self.assertEqual(int(p.bitfield_status), 0)

    def test_set_flag_raw(self):
        self._base_test()
        p = get_parent('parent1')
        p.set_flag('status', 2)
        self.assertEqual(p.status, 4)
        p.set_flag('status', 0, save=True)
        self.assertEqual(p.status, 5)

    def test_set_flag_bitfield(self):
        self._base_test()
        p = get_parent('parent1')
        p.set_flag('bitfield_status', ParentTestModel.bitfield_status.status_child2)
        self.assertEqual(int(p.bitfield_status), 2)
        p.set_flag('bitfield_status', ParentTestModel.bitfield_status.status_child1, save=True)
        self.assertEqual(int(p.bitfield_status), 3)

    def test_set_flag_mix(self):
        self._base_test()
        p = get_parent('parent1')
        p.set_flag('bitfield_status', 1)
        p.set_flag('status', ParentTestModel.bitfield_status.status_child2)
        self.assertEqual(int(p.bitfield_status), 2)
        self.assertEqual(p.status, 2)


class TestM2M(TestCase):
    def setUp(self):
        create_default_parent('parent1')
        create_default_parent('parent2')

    def test_one_parent(self):
        p1 = get_parent('parent1')
        p2 = get_parent('parent2')
        self.assertEqual(p1.status, 0)
        self.assertEqual(p2.status, 0)
        c = ChildManyToManyTestModel.objects.create()
        c.parent.add(p1)
        p1.force_status_refresh()
        self.assertEqual(p1.status, 16)  # only 4th flag set
        self.assertEqual(p2.status, 0)

    def test_one_parent_delete(self):
        p1 = get_parent('parent1')
        self.assertEqual(p1.status, 0)
        c = ChildManyToManyTestModel.objects.create()
        c.parent.add(p1)
        p1.force_status_refresh()
        self.assertEqual(p1.status, 16)  # only 4th flag set
        c.delete()
        p1.force_status_refresh()
        self.assertEqual(p1.status, 0)  # no flags set

    def test_two_parents(self):
        p1 = get_parent('parent1')
        p2 = get_parent('parent2')
        self.assertEqual(p1.status, 0)
        self.assertEqual(p2.status, 0)
        c = ChildManyToManyTestModel.objects.create()
        c.parent.add(p1)
        p1.force_status_refresh()
        self.assertEqual(p1.status, 16)  # only 4th flag set
        self.assertEqual(p2.status, 0)

        c.parent.add(p2)
        p2.force_status_refresh()
        self.assertEqual(p1.status, 16)
        self.assertEqual(p2.status, 16)

    def test_clear(self):
        self.test_two_parents()
        p1 = get_parent('parent1')
        p2 = get_parent('parent2')
        p1.childmanytomanytestmodels.clear()
        p1.force_status_refresh()
        self.assertEqual(p1.status, 0)
        self.assertEqual(int(p1.bitfield_status), 0)
        self.assertEqual(p2.status, 16)
        self.assertEqual(int(p2.bitfield_status), 16)

    def test_delete(self):
        self.test_two_parents()
        p1 = get_parent('parent1')
        p2 = get_parent('parent2')

        ChildManyToManyTestModel.objects.filter(parent=p1).delete()
        p1.force_status_refresh(related_models=[ChildManyToManyTestModel])
        p2.force_status_refresh(related_models=[ChildManyToManyTestModel])
        self.assertEqual(p1.status, 0)
        self.assertEqual(p2.status, 0)


class TestMultipleLevelsDeep(TestCase):
    def setUp(self):
        p1 = create_default_parent('parent1')
        c = ChildTestModel1.objects.create(parent=p1)
        ChildChildTestModel.objects.create(child=c)

    def test_status(self):
        # should be 1001 or 9
        p1 = get_parent('parent1')
        self.assertEqual(p1.status, 9)

    def test_delete(self):
        p1 = get_parent('parent1')
        c = ChildChildTestModel.objects.filter(child__parent=p1).first()
        c.delete()
        p1.refresh_from_db()
        self.assertEqual(p1.status, 1)

    def test_multi_model_delete(self):
        p1 = get_parent('parent1')
        c = ChildTestModel1.objects.filter(parent=p1).first()
        ChildChildTestModel.objects.create(child=c)
        # so we have parent -> child -> 2 child child
        self.assertEqual(p1.status, 9)
        ChildChildTestModel.objects.filter(child__parent=p1).delete()
        p1.force_status_refresh(search_depth=2)
        self.assertEqual(p1.status, 1)


class TestWithUnrelatedChildModels(TestCase):
    def setUp(self):
        p1 = create_default_parent('parent1')
        ChildTestModel1.objects.create(parent=p1)
        Unrelated.objects.create(parent=p1)

    def test_delete(self):
        p1 = get_parent('parent1')
        self.assertEqual(p1.status, 1)
        self.assertEqual(int(p1.bitfield_status), p1.status)
        Unrelated.objects.filter(parent=p1).first().delete()
        p1.force_status_refresh()
        self.assertEqual(p1.status, 1)
        self.assertEqual(int(p1.bitfield_status), p1.status)


class TestWithMultipleParentStatus(TestCase):
    def setUp(self):
        p1 = create_default_parent('parent1')
        ChildTestModel1.objects.create(parent=p1)
        ChildTestModel3.objects.create(parent=p1)

    def test_secondary(self):
        p1 = get_parent('parent1')
        self.assertEqual(p1.status, 5)
        self.assertEqual(p1.secondary_status, 4)
        self.assertEqual(int(p1.bitfield_status), p1.status)


class TestBitfieldMultiForeignKeys(TestCase):
    def setUp(self):
        p1 = create_default_parent('parent1')
        create_default_parent('parent2')
        for x in range(2):
            ChildTestModel1.objects.create(parent=p1)
        ChildTestModel2.objects.create(parent=p1)
        ChildTestModel3.objects.create(parent=p1)

    def _base_test(self):
        p1 = get_parent('parent1')
        p2 = get_parent('parent2')

        self.assertEqual(p1.name, 'parent1')
        self.assertEqual(p2.name, 'parent2')

        self.assertEqual(p1.status, 7)  # flags 111
        self.assertEqual(p2.status, 0)  # flags 000
        self.assertEqual(int(p1.bitfield_status), p1.status)
        self.assertEqual(int(p2.bitfield_status), p2.status)

    def test_delete_one_but_not_all(self):
        self._base_test()
        p1 = get_parent('parent1')
        ChildTestModel1.objects.filter(parent=p1).first().delete()

        self._base_test()
        self.assertEqual(ChildTestModel1.objects.filter(parent=p1).count(), 1)

    def test_update_force_refresh(self):
        self._base_test()
        p1 = get_parent('parent1')
        p2 = get_parent('parent2')

        ChildTestModel1.objects.filter(parent__name='parent1').update(parent=p2)
        p1 = p1.force_status_refresh()
        p2 = p2.force_status_refresh()
        self.assertEqual(p1.status, 6)
        self.assertEqual(p2.status, 1)
        self.assertEqual(int(p1.bitfield_status), p1.status)
        self.assertEqual(int(p2.bitfield_status), p2.status)

    def test_delete_both(self):
        self._base_test()
        p1 = get_parent('parent1')
        ChildTestModel1.objects.filter(parent=p1).all().delete()
        # ChildTestModel1.objects.filter(parent=p1).first().delete()
        self.assertEqual(ChildTestModel1.objects.filter(parent=p1).count(), 0)
        p1.force_status_refresh()
        self.assertEqual(p1.status, 6)
        self.assertEqual(int(p1.bitfield_status), p1.status)

    def test_child_counts(self):
        self._base_test()
        p1 = get_parent('parent1')
        self.assertEqual(ChildTestModel1.objects.filter(parent=p1).count(), 2)
        self.assertEqual(ChildTestModel2.objects.filter(parent=p1).count(), 1)
        self.assertEqual(ChildTestModel3.objects.filter(parent=p1).count(), 1)


class TestBitfieldManager(TestCase):
    def setUp(self):
        p1 = create_default_parent('parent1')
        create_default_parent('parent2')
        ChildTestModel1.objects.create(parent=p1)
        ChildTestModel3.objects.create(parent=p1)

    def test_model_create(self):
        self._base_test()

    def _base_test(self):
        p1 = get_parent('parent1')
        p2 = get_parent('parent2')
        self.assertEqual(p1.status, 5)  #
        self.assertEqual(p1.name, 'parent1')
        self.assertEqual(p2.status, 0)
        self.assertEqual(p2.name, 'parent2')

        self.assertEqual(int(p1.bitfield_status), p1.status)
        self.assertEqual(int(p2.bitfield_status), p2.status)

    def test_manual_status_set(self):
        p1 = get_parent('parent1')
        self.assertEqual(p1.status, 5)
        ParentTestModel.objects.filter(id=p1.id).update(status=4)  # so it is like ChildTestModel1 is unset
        p1.refresh_from_db()
        self.assertEqual(p1.status, 4)
        ChildTestModel1.objects.get(parent=p1).delete()
        p1.refresh_from_db()  # status does not change
        self.assertEqual(p1.status, 4)

    def test_model_destory(self):
        p1 = get_parent('parent1')
        ChildTestModel1.objects.get(parent=p1).delete()
        # self.assertEqual(p1.status, 4)
        p1.refresh_from_db()
        self.assertEqual(p1.status, 4)
        self.assertEqual(int(p1.bitfield_status), p1.status)

    def test_model_switch(self):
        c = ChildTestModel1.objects.get(id=1)
        p1 = get_parent('parent1')
        p2 = get_parent('parent2')
        self.assertEqual(c.parent, p1)
        self.assertEqual(p2.status, 0)
        self.assertEqual(p1.status, 5)
        self.assertEqual(int(p1.bitfield_status), p1.status)
        self.assertEqual(int(p2.bitfield_status), p2.status)
        c.parent = p2
        c.save()

        p1.force_status_refresh(related_models=[ChildTestModel1, ChildTestModel3])
        p2.force_status_refresh(related_models=[ChildTestModel1, ChildTestModel3])
        self.assertEqual(p1.status, 4)  # p1 now only has child 3
        self.assertEqual(p2.status, 1)  # p2 has child 1
        self.assertEqual(int(p1.bitfield_status), p1.status)
        self.assertEqual(int(p2.bitfield_status), p2.status)

    def test_force_refresh(self):
        p1 = get_parent('parent1')
        p2 = get_parent('parent2')
        self._base_test()  # nothing should change
        p1.force_status_refresh()
        p2.force_status_refresh()
        self._base_test()  # nothing should change
