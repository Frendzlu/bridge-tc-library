from bridge_movement.movement.howell import HowellMovement
from bridge_movement.tournament.auto_tournament import AutoTournament
from bridge_movement.core import Table, BoardGroup
import pandas as pd

# Create tournament with enough pairs for all sectors (2*(2+3+4+5)=28 pairs)
t = AutoTournament(total_pairs=28)

# Helper to allocate board numbers for a sector: returns list of board_rounds (one per round)
def allocate_board_rounds(total_boards, rounds):
	# split 1..total_boards into `rounds` equal consecutive chunks
	per_round = total_boards // rounds
	board_rounds = []
	start = 1
	for _ in range(rounds):
		end = start + per_round - 1
		# For each table we'll assign the same group (boards played that round)
		board_rounds.append({})  # filled later per-sector
		start = end + 1
	return board_rounds, per_round

# Sector definitions: (name, num_tables, rounds)
sectors_def = [
	("A", 2, 3),  # 3 rounds of 105 => 315 total
	("B", 3, 5),  # 5 rounds of 63
	("C", 4, 7),  # 7 rounds of 45
	("D", 5, 9),  # 9 rounds of 35
]

# Total deals as requested
TOTAL_DEALS = 315

# Build sectors manually to set boards_per_round and board_rounds
start_board = 1
for name, num_tables, rounds in sectors_def:
	# allocate pairs from generated pool
	available_pairs = [p for p in t.generated_pairs if p not in t.used_pairs]
	ns_pairs = available_pairs[:num_tables]
	ew_pairs = available_pairs[num_tables:num_tables*2]
	for p in ns_pairs + ew_pairs:
		t.used_pairs.add(p)

	# create tables
	tables = [Table(f"{name}{i+1}") for i in range(num_tables)]

	# create movement
	movement = HowellMovement(tables=tables, ns_pairs=ns_pairs, ew_pairs=ew_pairs)

	# allocate board rounds: each round uses TOTAL_DEALS/rounds boards per table
	per_round = TOTAL_DEALS // rounds
	board_rounds = []
	for r in range(rounds):
		end = start_board + per_round - 1
		group = tuple(range(start_board, end + 1))
		# map each table to the same group (boards stationary at table)
		mapping = {tbl: BoardGroup(group) for tbl in tables}
		board_rounds.append(mapping)
		start_board = end + 1

	# attach board_rounds to movement
	movement.board_rounds = board_rounds

	# create sector
	from bridge_movement.tournament.sector import Sector
	sector = Sector(name, tables, movement, boards_per_round=per_round)
	sector.set_initial_state(movement.get_first_round(), board_rounds[0])
	t.add_sector(sector)

# --- Run tournament ---
if __name__ == "__main__":
	while True:
		try:
			for sector in t.sectors:
				df = pd.DataFrame([
					{
						"Table": table_obj.name,
						"NS": sector.current_pairs_round[(table_obj, 'NS')].id,
						"EW": sector.current_pairs_round[(table_obj, 'EW')].id,
						"Deal(s)": sector.current_boards_round[table_obj].boards
					}
					for table_obj in sector.tables
				])
				print(f"{sector.name}, round {sector.round_number}")
				print(df)
				print("-"*60)
			t.next_deal()
		except StopIteration:
			break
