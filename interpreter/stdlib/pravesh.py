# marathi-lang/interpreter/stdlib/pravesh.py

class PraveshModule:
    def वाचा(self, prompt=""):
        return input(prompt)

    def फाइल_वाचा(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()

    def फाइल_लिहा(self, filename, content):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
