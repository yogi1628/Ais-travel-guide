def is_json_schema_error(e: Exception) -> bool:
    msg = str(e).lower()
    return (
        "json_validate_failed" in msg
        or "failed to generate json" in msg
        or "failed_generation" in msg
    )
