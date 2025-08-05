import subprocess

js_code = """
function _f(n)  {
//BEGIN
let m = n % 100;
//END
return m;
}
if (_f(1234589) != 89) 
   throw new Error('Wrong');
if (_f(23456) != 56) 
   throw new Error('Wrong');
throw new Error('OK');
"""

def execJS(js_code, timeout):
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

print(execJS(js_code, 1))