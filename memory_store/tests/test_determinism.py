import json
from memoy_store.store import write_record, read_records


def setup_empty_storage(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    tmp_path.joinpath("data").mkdir()
    tmp_path.joinpath("data/memory.json").write_text("[]")


def test_deterministic_append_order(tmp_path, monkeypatch):
    setup_empty_storage(tmp_path, monkeypatch)

    write_record(
        record_id="1",
        record_type="USER_FACT",
        payload={"k": "v"},
        source_module="test",
        schema_version=1,
    )

    write_record(
        record_id="2",
        record_type="USER_FACT",
        payload={"k": "v"},
        source_module="test",
        schema_version=1,
    )

    results = read_records(
        record_type="USER_FACT",
        filters={"k": "v"},
    )

    assert [r["record_id"] for r in results] == ["1", "2"]


def test_exact_match_filtering(tmp_path, monkeypatch):
    setup_empty_storage(tmp_path, monkeypatch)

    write_record(
        record_id="1",
        record_type="USER_FACT",
        payload={"lang": "python"},
        source_module="test",
        schema_version=1,
    )

    write_record(
        record_id="2",
        record_type="USER_FACT",
        payload={"lang": "java"},
        source_module="test",
        schema_version=1,
    )

    results = read_records(
        record_type="USER_FACT",
        filters={"lang": "python"},
    )

    assert len(results) == 1
    assert results[0]["record_id"] == "1"


def test_silent_read_failure(tmp_path, monkeypatch):
    setup_empty_storage(tmp_path, monkeypatch)

    results = read_records(
        record_type="USER_FACT",
        filters={"missing": "value"},
    )

    assert results == []


def test_invalid_record_type_raises(tmp_path, monkeypatch):
    setup_empty_storage(tmp_path, monkeypatch)

    try:
        write_record(
            record_id="x",
            record_type="INVALID",
            payload={},
            source_module="test",
            schema_version=1,
        )
        assert False, "Expected exception"
    except ValueError:
        assert True
