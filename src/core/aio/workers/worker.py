from ..base_worker import BaseWorker
from ..worker_signals import WorkerSignals

class Worker(BaseWorker):
    def __init__(self, method, *args, context=None, **kwargs):
        super().__init__()
        self.method = method
        self.args = args
        self.kwargs = kwargs
        self.context = context

    def run(self):
        try:
            # 1. Correctly unpack both positional and keyword arguments
            result = self.method(*self.args, **self.kwargs)

            # 2. Emit only the result and the context (no complex UI objects!)
            self.signals.result_ready.emit(result, self.context)
        except Exception as e:
            # Important: Catching errors here prevents the worker from crashing silently
            # or causing the C++ runtime to fail during stack unwinding.
            print(f"UniversalWorker Error: {e}")
