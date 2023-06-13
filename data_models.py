import math


class ValidResponseDirect:
    def __init__(self, lat, lon, rel_tol=0):
        self.lat = lat
        self.lon = lon
        self.rel_tol = rel_tol

    def __eq__(self, other):
        # Поля lat и lon (широта и долгота) в ответе не точно совпадают с полями в запросе, поэтому необходимо
        # сравнивать их с определённым допуском, например, 0.001
        return False if self.__class__ != other.__class__ else (
                math.isclose(float(self.lat), float(other.lat), rel_tol=max(self.rel_tol, other.rel_tol))
                and math.isclose(float(self.lon), float(other.lon), rel_tol=max(self.rel_tol, other.rel_tol)))


class ValidResponseReverse:
    def __init__(self, display_name, city, country, lat, lon, rel_tol=0):
        self.display_name = display_name
        self.city = city
        self.country = country
        self.lat = lat
        self.lon = lon
        self.rel_tol = rel_tol

    def __eq__(self, other):
        # Поле display_name включает в себя развернутую информацию - наименование места, полный адрес, индекс, страну,
        # порядок следования информации может измениться, что сломает тест, поэтому целосообразнее проверять наличие
        # наименования места в поле display_name; поля lat и lon (широта и долгота) в ответе не точно совпадают с полями
        # в запросе, поэтому необходимо сравнивать их с определённым допуском, например, 0.001
        return False if self.__class__ != other.__class__ else (
                (self.display_name in other.display_name or other.display_name in self.display_name)
                and self.city == other.city and self.country == other.country
                and math.isclose(float(self.lat), float(other.lat), rel_tol=max(self.rel_tol, other.rel_tol))
                and math.isclose(float(self.lon), float(other.lon), rel_tol=max(self.rel_tol, other.rel_tol)))


class ErrorResponse:
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __eq__(self, other):
        return self.code == other.code and other.message == self.message
