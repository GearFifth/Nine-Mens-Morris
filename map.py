"""
Modul sadrzi implementaciju asocijativnog niza
"""


class MapElement(object):
    """
    Klasa modeluje element asocijativnog niza
    """
    __slots__ = '_key', '_value'

    def __init__(self, key, value):
        self._key = key
        self._value = value

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Map(object):
    """
    Klasa modeluje asocijativni niz
    """
    def __init__(self):
        self._data = []

    def __getitem__(self, key):
        """
        Pristup elementu sa zadatim kljucem

        Metoda vrsi pristup elementu sa zadatim kljucem. U slucaju
        da element postoji u mapi, metoda vraca njegovu vrednost, dok
        u suprotnom podize odgovarajuci izuzetak.

        Argument:
        - `key`: kljuc elementa kome se pristupa
        """
        for item in self._data:
            if key == item.key:
                return item.value

        raise KeyError('Ne postoji element sa kljucem %s' % str(key))

    def __setitem__(self, key, value):
        """
        Postavljanje vrednosti elementa sa zadatim kljucem

        Metoda najpre pretrazuje postojece elemente po vrednosti kljuca.
        Ukoliko trazeni kljuc vec postoji, vrsi se azuriranje vrednosti
        postojeceg elementa. U suprotnom, kreira se novi element koji se
        dodaje u mapu.

        Argumenti:
        - `key`: kljuc elementa koji se kreira ili azurira
        - `value`: nova vrednost elementa
        """
        for item in self._data:
            if key == item.key:
                item.value = value
                return

        # element nije pronadjen, zapisi ga u mapu
        self._data.append(MapElement(key, value))

    def __delitem__(self, key):
        """
        Brisanje elementa sa zadatim kljucem

        Metoda pretrazuje elemente po vrednosti kljuca. Ukoliko element
        sa zadatim kljucem postoji u mapi, vrsi se njegovo brisanje. U
        suprotnom se podize odgovarajuci izuzetak.

        Argument:
        - `key`: kljuc elementa za brisanje
        """
        length = len(self._data)
        for i in range(length):
            if key == self._data[i].key:
                self._data.pop(i)
                return

        raise KeyError('Ne postoji element sa kljucem %s' % str(key))

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        """
        Metoda vrsi proveru postojanja kljuca u mapi

        Argument:
        - `key`: kljuc koji se trazi
        """
        for item in self._data:
            if key == item.key:
                return True

        return False

    def __iter__(self):
        for item in self._data:
            yield item.key

    def items(self):
        for item in self._data:
            yield item.key, item.value

    def keys(self):
        """
        Metoda vraca sve kljuceve u mapi
        """
        keys = []
        for key in self:
            keys.append(key)

        return keys

    def values(self):
        """
        Metoda vraca sve vrednosti u mapi
        """
        values = []
        for key in self:
            values.append(self[key])

        return values

    def clear(self):
        """
        Metoda uklanja sve elemente iz mape
        """
        self._data = []


if __name__ == '__main__':
    table = Map()
    table[3] = 10
    table['x'] = 11
    table['asd'] = 'abcdefg'

    # pristup elementima
    print(table['asd'])
    print(table.values())
    print(table.keys())

    # metoda __contains__
    if 'y' in table:
        print('Tabela sadrzi kljuc y.')
    else:
        print('Tabela ne sadrzi kljuc y.')

    # iteracija kroz tabelu
    for item in table:
        print(item, table[item])

    # brisanje elementa
    del table['asd']
    print(len(table) == 2)

    # clear metoda
    table.clear()
    print(len(table) == 0)
