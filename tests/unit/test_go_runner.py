import unittest
from backend.compiler.go_runner import GoRunnerConfig

class TestGoRunner(unittest.TestCase):
    def test_sandbox_env_variables(self):
        env = GoRunnerConfig.get_sandbox_env("/tmp/sandbox")
        self.assertEqual(env["CGO_ENABLED"], "0")
        self.assertIn(".go", env["GOPATH"])
        self.assertIn(".cache", env["GOCACHE"])
        self.assertEqual(env["GO111MODULE"], "auto")

    def test_env_isolation(self):
        env1 = GoRunnerConfig.get_sandbox_env("/tmp/s1")
        env2 = GoRunnerConfig.get_sandbox_env("/tmp/s2")
        self.assertNotEqual(env1["GOPATH"], env2["GOPATH"])

    def test_non_empty(self):
        env = GoRunnerConfig.get_sandbox_env("/path")
        self.assertTrue(len(env) > 4)

if __name__ == "__main__":
    unittest.main()
