import unittest

from luigi import Task, mock
from luigi.util import delegates

from ..invalidation import deps, invalidate, invalidate_downstream


class MockTask(Task):
    def output(self):
        return mock.MockTarget(self.task_family)

    def run(self):
        with self.output().open('w') as f:
            f.write(self.task_family)


class TaskA(MockTask):
    pass


class TaskB(MockTask):
    def requires(self):
        return TaskA()


@delegates
class TaskC(MockTask):
    def subtasks(self):
        return TaskB()


class TaskD(MockTask):
    def requires(self):
        return TaskA(), TaskC()


class TestDependencies(unittest.TestCase):
    def setUp(self) -> None:
        for task in deps.find_deps(TaskD(), None):
            task.run()

    def test_dependencies(self):
        self.assertSetEqual(deps.find_deps(TaskD(), 'TaskA'), {TaskA(), TaskB(), TaskC(), TaskD()})

        deps_BD = deps.find_deps(TaskD(), 'TaskB')
        self.assertSetEqual(deps_BD, {TaskB(), TaskC(), TaskD()})
        self.assertNotIn(TaskA(), deps_BD)

        deps_CD = deps.find_deps(TaskD(), 'TaskC')
        self.assertSetEqual(deps_CD, {TaskC(), TaskD()})
        self.assertNotIn(TaskA(), deps_CD)
        self.assertNotIn(TaskB(), deps_CD)

        deps_DD = deps.find_deps(TaskD(), 'TaskD')
        self.assertSetEqual(deps_DD, {TaskD()})
        self.assertNotIn(TaskA(), deps_DD)
        self.assertNotIn(TaskB(), deps_DD)
        self.assertNotIn(TaskC(), deps_DD)

    def test_single_invalidation(self):
        task = TaskD()
        self.assertTrue(task.output().exists(), 'Output does not exist')
        invalidate(task)
        self.assertFalse(task.output().exists(), 'Output was not invalidated.')

    def test_downstream_invalidation(self):
        tasks = [TaskA(), TaskB(), TaskC(), TaskD()]
        for task in tasks:
            self.assertTrue(task.output().exists())

        invalidate_downstream(tasks[-1], 'TaskB')

        self.assertTrue(tasks[0].output().exists())
        for task in tasks[1:]:
            self.assertFalse(task.output().exists())


if __name__ == '__main__':
    unittest.main()
