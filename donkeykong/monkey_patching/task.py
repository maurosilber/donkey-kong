import luigi

# Monkey patching
luigi.Task.open = lambda self: self
luigi.Task.close = lambda self: None
luigi.Task.__enter__ = lambda self: self.open()
luigi.Task.__exit__ = lambda self, exc_type, exc_val, exc_tb: self.close()
