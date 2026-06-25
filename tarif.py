from functools import total_ordering


@total_ordering
class Tarif:

    def __init__(self, montant, devise="EUR"):
        if montant < 0:
            raise ValueError()

        self._montant = float(montant)
        self._devise = devise

    @property
    def montant(self):
        return self._montant

    @property
    def devise(self):
        return self._devise

    def __eq__(self, autre):
        if not isinstance(autre, Tarif):
            return NotImplemented
        return self.montant == autre.montant and self.devise == autre.devise

    def __hash__(self):
        return hash((self.montant, self.devise))

    def __lt__(self, autre):
        if not isinstance(autre, Tarif):
            return NotImplemented
        if self.devise != autre.devise:
            raise ValueError()
        return self.montant < autre.montant

    def __add__(self, autre):
        if not isinstance(autre, Tarif):
            return NotImplemented
        if self.devise != autre.devise:
            raise ValueError()
        return Tarif(self.montant + autre.montant, self.devise)

    def __str__(self):
        return f"{self.montant:.2f} {self.devise}"

    def __repr__(self):
        return f"Tarif({self.montant!r}, {self.devise!r})"   