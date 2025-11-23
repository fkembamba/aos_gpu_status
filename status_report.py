# status_report.py
import subprocess
from message import Message

class Status_Report(Message):
    def __init__(self):
        total, used = self.get_gpu_memory()
        payload = {
            "memory_total_mb": total,
            "memory_used_mb": used,
        }
        super().__init__("STATUS_REPORT", payload=payload)

    @staticmethod
    def get_gpu_memory():
        try:
            result = subprocess.run(
                [
                    "nvidia-smi",
                    "--query-gpu=memory.total,memory.used",
                    "--format=csv,noheader,nounits"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode != 0:
                raise RuntimeError(result.stderr.strip())

            # Handle single or multiple GPUs: take the first line (GPU 0)
            lines = [line.strip() for line in result.stdout.strip().splitlines()]
            first_line = lines[0]
            total_str, used_str = [x.strip() for x in first_line.split(",")]

            total = int(total_str)
            used = int(used_str)
            return total, used

        except Exception as e:
            print("Error in get_gpu_memory():", e)
            return None, None
