import uuid

def uuid_log():
    return str(uuid.uuid4()).replace("-", "")[:12]

