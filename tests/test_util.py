from django.test import TestCase
from bitfield_manager import utils


class TestBitfieldUtil(TestCase):
    def test_flag_set(self):
        status_1 = 0
        status_1 = utils.set_flag_for_status(status_1, (1 << 5))

        status_2 = 0
        status_2 = utils.set_flag_field_for_status(status_2, 5)
        self.assertEqual(status_1, status_2)
        self.assertEqual(status_1, 32)
        self.assertEqual(utils.is_flag_field_set_for_status(status_2, 5), True)
        self.assertEqual(utils.is_flag_field_set_for_status(status_1, 6), False)
        self.assertEqual(utils.is_flag_set_for_status(status_1, (1 << 5)), True)

    def test_multi_flag_set(self):
        status_2 = utils.set_flag_field_for_status(0, 5)
        multi_mask_flag = (1 << 5) | (1 << 2)
        status_3 = utils.set_flag_field_for_status(multi_mask_flag, 3)

        # should be false because not all elements match
        self.assertEqual(utils.is_flag_set_for_status(status_2, multi_mask_flag), False)
        self.assertEqual(utils.is_flag_set_for_status(status_3, multi_mask_flag), True)

    def test_flag_unset(self):
        status = (1 << 5) | (1 << 2)
        s1 = utils.unset_flag_field_for_status(status, 5)
        self.assertEqual(utils.is_flag_field_set_for_status(s1, 5), False)
        self.assertEqual(utils.is_flag_field_set_for_status(s1, 2), True)
        self.assertEqual(utils.is_flag_set_for_status(s1, (1 << 5)), False)
        self.assertEqual(utils.is_flag_set_for_status(s1, (1 << 2)), True)

    def test_multi_flag_unset(self):
        status = 0
        for i in range(5):
            status |= (1 << i)
        for i in range(5):
            self.assertEqual(utils.is_flag_field_set_for_status(status, i), True)
        multi_mask_flag = (1 << 4) | (1 << 2)
        s1 = utils.unset_flag_for_status(status, multi_mask_flag)
        self.assertEqual(utils.is_flag_field_set_for_status(s1, 4), False)
        self.assertEqual(utils.is_flag_field_set_for_status(s1, 3), True)
        self.assertEqual(utils.is_flag_field_set_for_status(s1, 2), False)
        self.assertEqual(utils.is_flag_field_set_for_status(s1, 1), True)
        self.assertEqual(utils.is_flag_field_set_for_status(s1, 0), True)
