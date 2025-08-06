import subprocess


def exec(js_code, timeout):
    try:
        # Виконуємо node з кодом через stdin
        result = subprocess.run(
            ['node'],
            input=js_code,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True
        )
        return "OK. " + result.stdout
    except subprocess.TimeoutExpired:
        return "❌ Перевищений ліміт часу."
    except subprocess.CalledProcessError as e:
        if e.stderr.find("new Error('OK')") != -1:
            return "OK"
        if e.stderr.find("new Error('Wrong") != -1:
            return "Wrong"
        return "Error. " + e.stderr
    except FileNotFoundError:
        return "Node.js не встановлений або не доданий до PATH."

