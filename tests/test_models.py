#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_django-bitfield-manager
------------

Tests for `django-bitfield-manager` models module.
"""
from django.test import TestCase

from tests.models import ParentTestModel, ChildTestModel1, ChildTestModel2, ChildTestModel3, Unrelated


class TestWithUnrelatedChildModels(TestCase):
    def setUp(self):
        p1 = ParentTestModel.objects.create(name='parent1', status=0)
        ChildTestModel1.objects.create(parent=p1)
        Unrelated.objects.create(parent=p1)

    def test_delete(self):
        p1 = ParentTestModel.objects.get(name='parent1')
        self.assertEqual(p1.status, 1)
        Unrelated.objects.filter(parent=p1).delete()
        p1.force_status_refresh()
        self.assertEqual(p1.status, 1)

class TestBitfieldMultiForeignKeys(TestCase):
    def setUp(self):
        p1 = ParentTestModel.objects.create(name='parent1', status=0)
        ParentTestModel.objects.create(name='parent2', status=0)
        for x in range(2):
            ChildTestModel1.objects.create(parent=p1)
        ChildTestModel2.objects.create(parent=p1)
        ChildTestModel3.objects.create(parent=p1)

    def _base_test(self):
        p1 = ParentTestModel.objects.get(name='parent1')
        p2 = ParentTestModel.objects.get(name='parent2')

        self.assertEqual(p1.name, 'parent1')
        self.assertEqual(p2.name, 'parent2')

        self.assertEqual(p1.status, 7)  # flags 111
        self.assertEqual(p2.status, 0)  # flags 000

    def test_delete_one_but_not_all(self):
        self._base_test()
        p1 = ParentTestModel.objects.get(name='parent1')
        ChildTestModel1.objects.filter(parent=p1).first().delete()

        self._base_test()
        self.assertEqual(ChildTestModel1.objects.filter(parent=p1).count(), 1)

    def test_update_force_refresh(self):
        p1 = ParentTestModel.objects.get(name='parent1')
        p2 = ParentTestModel.objects.get(name='parent2')

        ChildTestModel1.objects.filter(parent__name='parent1').update(parent=p2)
        p1 = p1.force_status_refresh()
        p2 = p2.force_status_refresh()
        self.assertEqual(p1.status, 6)
        self.assertEqual(p2.status, 1)

    def test_delete_both(self):
        self._base_test()
        p1 = ParentTestModel.objects.get(name='parent1')
        ChildTestModel1.objects.filter(parent=p1).all().delete()
        # ChildTestModel1.objects.filter(parent=p1).first().delete()
        self.assertEqual(ChildTestModel1.objects.filter(parent=p1).count(), 0)
        p1.force_status_refresh()
        self.assertEqual(p1.status, 6)

    def test_child_counts(self):
        self._base_test()
        p1 = ParentTestModel.objects.get(name='parent1')
        self.assertEqual(ChildTestModel1.objects.filter(parent=p1).count(), 2)
        self.assertEqual(ChildTestModel2.objects.filter(parent=p1).count(), 1)
        self.assertEqual(ChildTestModel3.objects.filter(parent=p1).count(), 1)


class TestBitfieldManager(TestCase):
    def setUp(self):
        p1 = ParentTestModel.objects.create(name='parent1', status=0)
        ParentTestModel.objects.create(name='parent2', status=0)
        ChildTestModel1.objects.create(parent=p1)
        ChildTestModel3.objects.create(parent=p1)

    def test_model_create(self):
        self._base_test()

    def _base_test(self):
        p1 = ParentTestModel.objects.get(name='parent1')
        p2 = ParentTestModel.objects.get(name='parent2')
        self.assertEqual(p1.status, 5)  #
        self.assertEqual(p1.name, 'parent1')
        self.assertEqual(p2.status, 0)
        self.assertEqual(p2.name, 'parent2')

    def test_model_destory(self):
        p1 = ParentTestModel.objects.get(name='parent1')
        ChildTestModel1.objects.get(parent=p1).delete()
        # self.assertEqual(p1.status, 4)
        p1.refresh_from_db()
        self.assertEqual(p1.status, 4)

    def test_model_switch(self):
        c = ChildTestModel1.objects.get(id=1)
        p1 = ParentTestModel.objects.get(id=1)
        p2 = ParentTestModel.objects.get(id=2)
        self.assertEqual(p2.status, 0)
        self.assertEqual(p1.status, 5)
        c.parent = p2
        c.save()

        p1.force_status_refresh(related_models=[ChildTestModel1, ChildTestModel3])
        p2.force_status_refresh(related_models=[ChildTestModel1, ChildTestModel3])
        self.assertEqual(p1.status, 4)  # p1 now only has child 3
        self.assertEqual(p2.status, 1)  # p2 has child 1

    def test_force_refresh(self):
        p1 = ParentTestModel.objects.get(id=1)
        p2 = ParentTestModel.objects.get(id=2)
        self._base_test()  # nothing should change
        p1.force_status_refresh()
        p2.force_status_refresh()
        self._base_test()  # nothing should change

    def tearDown(self):
        pass
