from ..entities import Person


def person_factory(id="123", name="Smith"):
    return Person(id=id, name=name)
