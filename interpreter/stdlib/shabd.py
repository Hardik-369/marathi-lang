# marathi-lang/interpreter/stdlib/shabd.py

class ShabdModule:
    def मोठे(self, text):
        return text.upper()

    def लांबी(self, text):
        return len(text)

    def विभाजित(self, text, sep):
        return text.split(sep)
