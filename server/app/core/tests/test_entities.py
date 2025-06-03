from ..entities import Person


class TestUser:
    def test_common(self):
        id = "1"
        name = "Smith"
        person = Person(id=id, name=name)
        assert person["id"] == id
        assert person["name"] == name
