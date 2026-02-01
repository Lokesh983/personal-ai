from .schemas import ALLOWED_RECORD_TYPES
from .storage import load_all_records, append_record


def write_record(
    *,
    record_id,
    record_type,
    payload,
    source_module,
    schema_version,
):
    if record_type not in ALLOWED_RECORD_TYPES:
        raise ValueError("Invalid record_type")

    record = {
        "record_id": record_id,
        "record_type": record_type,
        "payload": payload,
        "source_module": source_module,
        "schema_version": schema_version,
    }

    append_record(record)


def read_records(
    *,
    record_type,
    filters,
    limit=None,
):
    records = load_all_records()

    results = [
        r for r in records
        if r["record_type"] == record_type
        and all(r["payload"].get(k) == v for k, v in filters.items())
    ]

    if limit is not None:
        results = results[:limit]

    return results
