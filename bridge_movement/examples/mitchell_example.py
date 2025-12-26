from bridge_movement.movement import MitchellMovement
from bridge_movement.tournament.auto_tournament import AutoTournament
import pandas as pd

tournament = AutoTournament(total_pairs=20, total_boards=30)

sector_A = tournament.add_sector_auto("A", num_tables=5, movement_cls=MitchellMovement, boards_per_round=2)
sector_B = tournament.add_sector_auto("B", num_tables=5, movement_cls=MitchellMovement, boards_per_round=2)

# --- Run tournament ---
while True:
	try:
		for sector in tournament.sectors:
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
		tournament.next_deal()
	except StopIteration:
		break