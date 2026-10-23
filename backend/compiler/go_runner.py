"""
Go Toolchain Sandboxing Environment
"""
import os

class GoRunnerConfig:
    @staticmethod
    def get_sandbox_env(workspace_path: str) -> dict:
        env = dict(os.environ)
        env["CGO_ENABLED"] = "0"
        env["GOPATH"] = os.path.join(workspace_path, ".go")
        env["GOCACHE"] = os.path.join(workspace_path, ".cache")
        env["GO111MODULE"] = "auto"
        return env
