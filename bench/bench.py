import time

from nested_multipart_parser import NestedParser


def bench(data, count):
    v = []
    for _ in range(count):
        start = time.perf_counter()
        parser = NestedParser(data)
        parser.is_valid()
        validate_data = parser.validate_data
        end = time.perf_counter()
        v.append(end - start)

    return sum(v) / len(v)


def big(count):
    data = {
        "title": "title",
        "date": "time",
        "langs[0].id": "id",
        "langs[0].title": "title",
        "langs[0].description": "description",
        "langs[0].language": "language",
        "langs[1].id": "id1",
        "langs[1].title": "title1",
        "langs[1].description": "description1",
        "langs[1].language": "language1",
        "test.langs[0].id": "id",
        "test.langs[0].title": "title",
        "test.langs[0].description": "description",
        "test.langs[0].language": "language",
        "test.langs[1].id": "id1",
        "test.langs[1].title": "title1",
        "test.langs[1].description": "description1",
        "test.langs[1].language": "language1",
        "deep.nested.dict.test.langs[0].id": "id",
        "deep.nested.dict.test.langs[0].title": "title",
        "deep.nested.dict.test.langs[0].description": "description",
        "deep.nested.dict.test.langs[0].language": "language",
        "deep.nested.dict.test.langs[1].id": "id1",
        "deep.nested.dict.test.langs[1].title": "title1",
        "deep.nested.dict.test.langs[1].description": "description1",
        "deep.nested.dict.test.langs[1].language": "language1",
        "deep.nested.dict.with.list[0].test.langs[0].id": "id",
        "deep.nested.dict.with.list[0].test.langs[0].title": "title",
        "deep.nested.dict.with.list[1].test.langs[0].description": "description",
        "deep.nested.dict.with.list[1].test.langs[0].language": "language",
        "deep.nested.dict.with.list[1].test.langs[1].id": "id1",
        "deep.nested.dict.with.list[1].test.langs[1].title": "title1",
        "deep.nested.dict.with.list[0].test.langs[1].description": "description1",
        "deep.nested.dict.with.list[0].test.langs[1].language": "language1",
    }
    return bench(data, count)


def small(count):
    data = {
        "title": "title",
        "date": "time",
        "langs[0].id": "id",
        "langs[0].title": "title",
        "langs[0].description": "description",
        "langs[0].language": "language",
        "langs[1].id": "id1",
        "langs[1].title": "title1",
        "langs[1].description": "description1",
        "langs[1].language": "language1",
    }
    return bench(data, count)


count = 10_000
print(f"{small(count)=}")
print(f"{big(count)=}")
