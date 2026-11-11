from pathlib import Path

import duckdb
import pandas as pd


class BankingRepository:
    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir

    def _read(self, filename: str) -> pd.DataFrame:
        path = (self.data_dir / filename).as_posix().replace("'", "''")
        return duckdb.sql(f"SELECT * FROM read_csv_auto('{path}', header=true)").df()

    def customers(self) -> pd.DataFrame:
        return self._read("customers.csv")

    def customer(self, customer_id: str) -> dict:
        frame = self.customers()
        rows = frame.loc[frame["customer_id"] == customer_id]
        if rows.empty:
            raise KeyError(f"Unknown fictional customer: {customer_id}")
        return rows.iloc[0].to_dict()

    def history(self, filename: str, customer_id: str, as_of_month: str) -> pd.DataFrame:
        frame = self._read(filename)
        frame["month"] = pd.to_datetime(frame["month"])
        cutoff = pd.Timestamp(as_of_month)
        return frame.loc[
            (frame["customer_id"] == customer_id) & (frame["month"] <= cutoff)
        ].sort_values("month")

    def snapshot(self, filename: str, customer_id: str, as_of_month: str) -> dict:
        history = self.history(filename, customer_id, as_of_month)
        month = pd.Timestamp(as_of_month)
        rows = history.loc[history["month"] == month]
        if rows.empty:
            raise KeyError(f"No {filename} snapshot for {customer_id} at {as_of_month}")
        return rows.iloc[0].to_dict()
