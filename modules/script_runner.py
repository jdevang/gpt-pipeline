import signal
import sys
import subprocess

def handler(signum, frame):
        raise Exception("The script took too long to execute for the given input")

signal.signal(signal.SIGALRM, handler)

def run_script():
    subprocess_args = (
        [sys.executable, "temp.py"]
    )

    try:
        signal.alarm(10)
        result = subprocess.Popen(subprocess_args, stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=False)
        with open("temp.in", "rb") as f:
             input_ = f.read()
        out, err = result.communicate(input=input_)
        if err:
            return err.decode("utf-8"), 1
    except subprocess.CalledProcessError as error:
        return error.output.decode("utf-8"), 1
    except  subprocess.TimeoutExpired as error:
         return error.output.decode("utf-8"), 1
    except Exception as e:
        return e, 1
    return str(out.decode("utf-8")), 0

if __name__ == "__main__":
     print(run_script())