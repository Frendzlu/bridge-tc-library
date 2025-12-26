from bridge_movement.movements.generator import MovementGenerator


class DummyMovement(MovementGenerator):
    def __init__(self):
        self.num_tables = 1
        super().__init__()

    def initial_round(self):
        return {(1, 'NS'): 'A', (1, 'EW'): None}

    def step(self, round_map):
        # toggles between A and B
        if round_map[(1, 'NS')] == 'A':
            return {(1, 'NS'): 'B', (1, 'EW'): None}
        return {(1, 'NS'): 'A', (1, 'EW'): None}


def test_pairs_for_round_modulo():
    d = DummyMovement()
    r1 = d.get_round_sitting(1)
    r2 = d.get_round_sitting(2)
    r3 = d.get_round_sitting(3)
    assert r1 != r2
    assert r3 == r1

