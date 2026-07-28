import subprocess
import threading
import time

class TerminalRunner:
    def __init__(self, output_callback, status_callback, stop_flag_ref):
        """
        output_callback: function(text, is_error)
        status_callback: function(text, color)
        stop_flag_ref: callable that returns a boolean (True = stop requested)
        """
        self.output_callback = output_callback
        self.status_callback = status_callback
        self.stop_flag_ref = stop_flag_ref
        self.process = None

    def run_cmd(self, command):
        self.status_callback("Status: Running CMD command...", "orange")
        # Use shell=True for cmd to handle internal commands
        threading.Thread(target=self._execute_process, args=(command, "cmd"), daemon=True).start()

    def run_powershell(self, command):
        self.status_callback("Status: Running PowerShell command...", "orange")
        ps_command = ["powershell", "-NoProfile", "-Command", command]
        threading.Thread(target=self._execute_process, args=(ps_command, "powershell"), daemon=True).start()

    def _execute_process(self, cmd, shell_type):
        try:
            if shell_type == "cmd":
                self.process = subprocess.Popen(
                    cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    text=True, encoding="utf-8", errors="ignore"
                )
            else:
                self.process = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    text=True, encoding="utf-8", errors="ignore"
                )

            # Monitor output while checking stop flag
            while True:
                if self.stop_flag_ref():
                    self.process.terminate()
                    self.status_callback("Status: Stopped by user.", "red")
                    return

                # Read output line by line
                line = self.process.stdout.readline()
                if line:
                    self.output_callback(line, False)

                err_line = self.process.stderr.readline()
                if err_line:
                    self.output_callback(err_line, True)

                # Break when process ends
                if self.process.poll() is not None:
                    # Read remaining output
                    stdout, stderr = self.process.communicate()
                    if stdout:
                        self.output_callback(stdout, False)
                    if stderr:
                        self.output_callback(stderr, True)
                    break

                time.sleep(0.05)  # Prevent busy loop

            self.status_callback("Status: Execution Complete.", "lime")
        except Exception as e:
            self.output_callback(f"[-] Error executing process: {e}\n", True)
            self.status_callback("Status: Execution Failed.", "red")
        finally:
            self.process = None