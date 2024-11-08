import random, string

def random_alphanum(n: int) -> str:
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))