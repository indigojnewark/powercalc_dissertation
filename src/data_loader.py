import openpyxl


def inspect_workbook(filepath: str, max_preview_rows: int = 3) -> None:
    """Print sheet names, dimensions, and a row preview for a given Excel file."""
    wb = openpyxl.load_workbook(filepath, read_only=True)
    if not wb.sheetnames:
        print(f"{filepath}: no sheets found.")
        return
    print(f"\n=== {filepath} ===")
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        print(f"Sheet: {sheet_name}, dims: {ws.dimensions}")
        rows = list(ws.iter_rows(max_row=max_preview_rows, values_only=True))
        for row in rows:
            print(row[:12])


def load_sheet(filepath: str, sheet_name: str) -> list:
    """Load all rows from a named sheet as a list of tuples."""
    wb = openpyxl.load_workbook(filepath, read_only=True)
    if sheet_name not in wb.sheetnames:
        raise ValueError(
            f"Sheet '{sheet_name}' not found in {filepath}. "
            f"Available: {wb.sheetnames}"
        )
    ws = wb[sheet_name]
    return list(ws.iter_rows(values_only=True))


def get_lfq_values(
    rows: list,
    group_a_cols: list,
    group_b_cols: list,
    min_valid: int = 2
) -> list:
    """
    Extract LFQ intensities for two groups from row data.

    Returns a list of (group_a_vals, group_b_vals) for proteins
    that have at least `min_valid` non-zero values in both groups.
    """
    data = []
    for row in rows[1:]:  # skip header
        a_vals = [row[i] for i in group_a_cols if row[i] and row[i] > 0]
        b_vals = [row[i] for i in group_b_cols if row[i] and row[i] > 0]
        if len(a_vals) >= min_valid and len(b_vals) >= min_valid:
            data.append((a_vals, b_vals))
    return data
