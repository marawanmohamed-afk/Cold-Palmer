# ============================================================
# LOAD ALL 2023 SEASON CLUB SQUADS INTO INDIVIDUAL VARIABLES
# Memory-friendly: reads each CSV once, assigns to named variable
# Total data ~120 KB — well within RAM limits
# ============================================================

from pathlib import Path
import pandas as pd

SEASON_DIR = Path("data/DATA_CSV/Season_2023")

# ---- dtype spec: avoids inference overhead, keeps memory low ----
DTYPES = {
    "position": "category",
    "foot": "category",
    "status": "string",
    "joinedOn": "string",
    "name": "string",
    "height": "Int16",
    "id": "Int32",
    "nationality": "string",
    "marketValue": "Int64",
    "signedFrom": "string",
    "age": "Int8",
    "dateOfBirth": "string",
    "currentClub": "string",
    "jerseyNumber": "Int8",
    "ageAtSeasonStart": "Int8",
    "isLoan": "boolean",
    "loanedFrom": "string",
}

# ---- Helper: load single club CSV with dtype + club column ----
def _load_club(csv_path: Path) -> pd.DataFrame:
    """Read one club file, add 'club' column from filename."""
    club_name = csv_path.stem.rsplit("_", 2)[0].replace("_", " ")
    df = pd.read_csv(csv_path, dtype=DTYPES)
    df["club"] = club_name
    return df

# ============================================================
# LOOP THROUGH ALL 20 FILES AND CREATE ONE VARIABLE PER CLUB
# Variable names: <club_name>_2023  (spaces → underscores, lowercase)
# ============================================================
for csv_path in sorted(SEASON_DIR.glob("*_2023.csv")):
    club_key = csv_path.stem.rsplit("_", 2)[0].lower().replace(" ", "_") + "_2023"
    globals()[club_key] = _load_club(csv_path)
    print(f"Loaded {club_key}: {len(globals()[club_key])} rows")

# ============================================================
# RESULT: 20 variables now exist in your namespace, e.g.:
#   arsenal_2023, chelsea_2023, liverpool_2023, ...
# Each is a DataFrame with 34–56 rows × 17 columns
# ============================================================

# ---- Quick sanity checks (run any of these) ----
# arsenal_2023.head()
# chelsea_2023[["name", "position", "marketValue"]].sort_values("marketValue", ascending=False).head(10)
# liverpool_2023.groupby("position").size()
# manchester_city_2023["nationality"].value_counts()