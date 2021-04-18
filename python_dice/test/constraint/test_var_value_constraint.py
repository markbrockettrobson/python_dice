import random
import typing
import unittest
import unittest.mock as mock

import hypothesis
import hypothesis.strategies as strategies

from python_dice.interface.constraint.i_constraint import IConstraint
from python_dice.interface.constraint.i_constraint_factory import IConstraintFactory
from python_dice.src.constraint.var_value_constraint import VarValueConstraint


class TestVarValueConstraint(unittest.TestCase):
    def setUp(self) -> None:
        self._mock_constraint_factory = mock.create_autospec(IConstraintFactory)
        self._mock_constraint = mock.create_autospec(IConstraint)
        self._mock_constraint_factory.var_value_constraint.return_value = self._mock_constraint

    @hypothesis.given(
        var_values=strategies.dictionaries(keys=strategies.text(), values=strategies.sets(strategies.integers())),
        name=strategies.text(),
        int_set=strategies.sets(strategies.integers()),
    )
    def test_complies_true_not_in_var_values(
        self, var_values: typing.Dict[str, int], name: str, int_set: typing.Set[int]
    ):
        hypothesis.assume(name not in var_values)
        constraint = VarValueConstraint(name=name, values=int_set, constraint_factory=self._mock_constraint_factory)
        self.assertTrue(constraint.complies(var_values=var_values))

    @hypothesis.given(
        var_values=strategies.dictionaries(
            keys=strategies.text(), values=strategies.sets(strategies.integers()), min_size=1
        ),
        name=strategies.text(),
        int_set=strategies.sets(strategies.integers(), min_size=1),
    )
    def test_complies_true_in_var_values(self, var_values: typing.Dict[str, int], name: str, int_set: typing.Set[int]):
        var_values[name] = random.sample(int_set, 1)[0]
        constraint = VarValueConstraint(name=name, values=int_set, constraint_factory=self._mock_constraint_factory)
        self.assertTrue(constraint.complies(var_values=var_values))

    @hypothesis.given(
        var_values=strategies.dictionaries(
            keys=strategies.text(), values=strategies.sets(strategies.integers()), min_size=1
        ),
        name=strategies.text(),
        int_set=strategies.sets(strategies.integers(), min_size=1),
        test_int=strategies.integers(),
    )
    def test_complies_false_not_in_var_values(
        self, var_values: typing.Dict[str, int], name: str, int_set: typing.Set[int], test_int: int
    ):
        hypothesis.assume(test_int not in int_set)
        var_values[name] = test_int
        constraint = VarValueConstraint(name=name, values=int_set, constraint_factory=self._mock_constraint_factory)
        self.assertFalse(constraint.complies(var_values=var_values))

    @hypothesis.given(
        name=strategies.text(),
        int_set_one=strategies.sets(strategies.integers()),
        int_set_two=strategies.sets(strategies.integers()),
    )
    def test_can_merge_constraint_true(self, name: str, int_set_one: typing.Set[int], int_set_two: typing.Set[int]):
        constraint = VarValueConstraint(name=name, values=int_set_one, constraint_factory=self._mock_constraint_factory)
        second_constraint = VarValueConstraint(
            name=name, values=int_set_two, constraint_factory=self._mock_constraint_factory
        )
        self.assertTrue(constraint.can_merge(second_constraint))

    @hypothesis.given(
        name=strategies.text(),
        int_set=strategies.sets(strategies.integers()),
    )
    def test_can_merge_constraint_false(
        self,
        name: str,
        int_set: typing.Set[int],
    ):
        constraint = VarValueConstraint(name=name, values=int_set, constraint_factory=self._mock_constraint_factory)
        merge_constraint = mock.create_autospec(IConstraint)
        self.assertFalse(constraint.can_merge(merge_constraint))

    @hypothesis.given(
        name=strategies.text(),
        int_set_one=strategies.sets(strategies.integers()),
        int_set_two=strategies.sets(strategies.integers(), min_size=1),
    )
    def test_merge_constraint_some_overlap(self, name: str, int_set_one: typing.Set[int], int_set_two: typing.Set[int]):
        self._mock_constraint_factory.reset_mock()
        int_set_one.add(random.sample(int_set_two, 1)[0])
        constraint = VarValueConstraint(name=name, values=int_set_one, constraint_factory=self._mock_constraint_factory)
        second_constraint = VarValueConstraint(
            name=name, values=int_set_two, constraint_factory=self._mock_constraint_factory
        )
        self.assertEqual(self._mock_constraint, constraint.merge(second_constraint))
        self._mock_constraint_factory.var_value_constraint.assert_called_once_with(
            name=name, values=int_set_one.intersection(int_set_two)
        )

    @hypothesis.given(name=strategies.text(), int_set=strategies.sets(strategies.integers(), min_size=4))
    def test_merge_constraint_no_overlap(
        self,
        name: str,
        int_set: typing.Set[int],
    ):
        int_set_one = set(random.sample(int_set, len(int_set) // 2))
        int_set_two = int_set - int_set_one
        hypothesis.assume(len(int_set_one.intersection(int_set_two)) == 0)

        self._mock_constraint_factory.reset_mock()
        constraint = VarValueConstraint(name=name, values=int_set_one, constraint_factory=self._mock_constraint_factory)
        second_constraint = VarValueConstraint(
            name=name, values=int_set_two, constraint_factory=self._mock_constraint_factory
        )
        self.assertEqual(self._mock_constraint_factory.impossible_constraint, constraint.merge(second_constraint))

    def test_merge_false(self):
        self._mock_constraint_factory.reset_mock()
        constraint = VarValueConstraint(name="mock", values={1, 2, 3}, constraint_factory=self._mock_constraint_factory)
        second_constraint = mock.create_autospec(IConstraint)
        with self.assertRaises(ValueError):
            constraint.merge(second_constraint)

    def test_merge_false_after_can_merge(self):
        self._mock_constraint_factory.reset_mock()
        constraint = VarValueConstraint(name="mock", values={1, 2, 3}, constraint_factory=self._mock_constraint_factory)
        constraint.can_merge = mock.Mock()
        constraint.can_merge.return_value = True
        second_constraint = mock.create_autospec(IConstraint)
        with self.assertRaises(ValueError):
            constraint.merge(second_constraint)

    @hypothesis.given(name=strategies.text(), int_set=strategies.sets(strategies.integers()))
    def test_eq_true(self, name: str, int_set: typing.Set[int]):
        constraint = VarValueConstraint(name=name, values=int_set, constraint_factory=self._mock_constraint_factory)
        second_constraint = VarValueConstraint(
            name=name, values=int_set, constraint_factory=self._mock_constraint_factory
        )
        self.assertEqual(constraint, second_constraint)

    @hypothesis.given(
        name_one=strategies.text(), name_two=strategies.text(), int_set=strategies.sets(strategies.integers())
    )
    def test_eq_false_name(self, name_one: str, name_two: str, int_set: typing.Set[int]):
        hypothesis.assume(name_one != name_two)
        constraint = VarValueConstraint(name=name_one, values=int_set, constraint_factory=self._mock_constraint_factory)
        second_constraint = VarValueConstraint(
            name=name_two, values=int_set, constraint_factory=self._mock_constraint_factory
        )
        self.assertNotEqual(constraint, second_constraint)

    @hypothesis.given(
        name=strategies.text(),
        int_set_one=strategies.sets(strategies.integers()),
        int_set_two=strategies.sets(strategies.integers()),
    )
    def test_eq_false_set(self, name: str, int_set_one: typing.Set[int], int_set_two: typing.Set[int]):
        hypothesis.assume(int_set_one != int_set_two)
        constraint = VarValueConstraint(name=name, values=int_set_one, constraint_factory=self._mock_constraint_factory)
        second_constraint = VarValueConstraint(
            name=name, values=int_set_two, constraint_factory=self._mock_constraint_factory
        )
        self.assertNotEqual(constraint, second_constraint)

    @hypothesis.given(name=strategies.text(), int_set=strategies.sets(strategies.integers()))
    def test_str(self, name: str, int_set: typing.Set[int]):
        constraint = VarValueConstraint(name=name, values=int_set, constraint_factory=self._mock_constraint_factory)
        self.assertEqual(f"VarValueConstraint: name={name}, values={int_set}", str(constraint))
