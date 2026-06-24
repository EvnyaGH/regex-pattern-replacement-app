import type { DataRow } from "../types/api";

interface DataTableProps {
  columns: string[];
  rows: DataRow[];
  emptyLabel: string;
}

export function DataTable({ columns, rows, emptyLabel }: DataTableProps) {
  if (columns.length === 0 || rows.length === 0) {
    return <div className="empty-state">{emptyLabel}</div>;
  }

  return (
    <div className="table-shell">
      <table>
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column}>{column}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {columns.map((column) => (
                <td key={column}>{formatCell(row[column])}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function formatCell(value: DataRow[string]) {
  if (value === null || value === undefined) {
    return "";
  }
  return String(value);
}
