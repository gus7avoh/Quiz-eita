from uuid import uuid4


def generate_quiz_uuid() -> str:
    return str(uuid4())