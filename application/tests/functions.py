def print_colored_text(text, color):
    color_codes = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
    }

    reset_code = "\033[0m"
    print(f"{color_codes.get(color, reset_code)}{text}{reset_code}")
