from pathlib import Path
import pandas as pd

SEASON_DIR = Path("data/DATA_CSV/Season_2023")

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

def iter_club_frames(season_dir: Path = SEASON_DIR, chunksize: int | None = None):
    """Yield (club_name, DataFrame) for each club CSV in the season directory."""
    for csv_path in sorted(season_dir.glob("*_2023.csv")):
        club_name = csv_path.stem.rsplit("_", 2)[0].replace("_", " ")
        if chunksize:
            reader = pd.read_csv(csv_path, dtype=DTYPES, chunksize=chunksize)
            for chunk in reader:
                chunk["club"] = club_name
                yield club_name, chunk
        else:
            df = pd.read_csv(csv_path, dtype=DTYPES)
            df["club"] = club_name
            yield club_name, df


def load_all_clubs(season_dir: Path = SEASON_DIR) -> pd.DataFrame:
    """Load and concatenate all club DataFrames (use if total fits in RAM)."""
    frames = [df.assign(club=club) for club, df in iter_club_frames(season_dir)]
    return pd.concat(frames, ignore_index=True)


def process_incremental(season_dir: Path = SEASON_DIR, func=None):
    """Process each club's data incrementally without holding all in memory.
    
    Args:
        func: Callable(club_name: str, df: pd.DataFrame) -> Any
    """
    results = {}
    for club, df in iter_club_frames(season_dir):
        results[club] = func(club, df) if func else df
    return results


if __name__ == "__main__":
    # Option 1: Load everything (fine for ~120KB total)
    # all_players = load_all_clubs()

    # Option 2: Stream & process per club (zero RAM growth)
    for club, df in iter_club_frames():
        print(f"{club}: {len(df)} players")
        # do your analysis here per club

    # Option 3: Chunked reading if files were huge
    # for club, chunk in iter_club_frames(chunksize=1000):
    #     process_chunk(chunk)