

from graffunc import graffunc, InconvertibleError


class BiologicalObject():
    """Biological entity abstract class"""

    def __init__(self, id, structure=None):
        self.id = id
        self.structure = structure

    def __repr__(self):
        return "id:{}, struct:{}".format(self.id, self.structure)


class BIGG(BiologicalObject):

    def __repr__(self):
        return "{}: id:{}, struct:{}".format('BIGG', self.id, self.structure)


class METACYC(BiologicalObject):

    def __repr__(self):
        return "{}: id:{}, struct:{}".format('METACYC', self.id, self.structure)


def bigg_to_metacyc(bigg):
    """Return metacyc mapping for the given id"""

    old_id = bigg.id
    data = {  # Imagine that this object contains lot of other attributes…
        'csn': 'CYTOSINE',
    }

    try:
        return {'metacyc': METACYC(data[old_id])}
    except KeyError:
        raise InconvertibleError("'{}' not found in database."
                                 "".format(bigg.id))


def chemical_class_to_metacyc(bigg):
    """Return the nearest known metacyc class for the given chemical class"""

    # There is no chemical information for this object
    if not bigg.structure:
        raise InconvertibleError(
                "'{}' has no chemical data.".format(bigg.id)
              )

    chemical_struct = bigg.structure

    # Mock similarity computing on all known SMILES
    data = {
        'C1(NC(=O)N=C(N)C=1)': ['a pyrimidine base', 'a nucleobase',
                                'a pyrimidine', 'a diazine',
                                'a nucleic acid component'],
    }

    try:
        return {'metacyc': METACYC(data[chemical_struct], 'closest_struct_found')}
    except KeyError:
        raise InconvertibleError("'{}' not found in database."
                                 "".format(chemical_struct))


def play_with_graffunc():
    grfc = graffunc()
    # dynamic modification of the object
    grfc.add(bigg_to_metacyc, sources={'bigg'}, targets={'metacyc'})
    grfc.add(chemical_class_to_metacyc, sources={'bigg'}, targets={'metacyc'})

    data = {'bigg': BIGG('csn', structure='C1(NC(=O)N=C(N)C=1)')}
    print('HQWAOG:', grfc.convert(sources=data, targets={'metacyc'}))


if __name__ == "__main__":

    ret = bigg_to_metacyc(BIGG('csn'))
    print(ret)

    ret = chemical_class_to_metacyc(
        BIGG('csn', structure='C1(NC(=O)N=C(N)C=1)')
    )
    print(ret)

    obj = BIGG('csn', 'C1(NC(=O)N=C(N)C=1)')
    print(obj)

    play_with_graffunc()
