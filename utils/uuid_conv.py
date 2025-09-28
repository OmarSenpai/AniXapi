from uuid import UUID, uuid4


def binary_to_uuid(binary_uuid:bytes) -> str:
    return str(UUID(bytes=binary_uuid))


def uuid_to_binary(uuid_str:str) -> bytes | None:
    if uuid_str is None:
        return None
    try:
        return UUID(uuid_str).bytes
    except ValueError:
        return None
