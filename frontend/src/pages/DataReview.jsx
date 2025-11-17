import "./DataReview.css";
import { useEffect, useMemo, useState } from "react";
import { useTable, useSortBy, usePagination } from "react-table";
import { fetchDataPreview, fetchUploadedFiles } from "../api/dataReview";
import { uploadDataset, listUploadedFiles, deleteFile } from "../api/upload";

export default function DataReview() {
  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [selectedUploadedFile, setSelectedUploadedFile] = useState(null);
  const [uploadedFiles, setUploadedFiles] = useState([]);

  // Load uploaded files on mount
  useEffect(() => {
    const loadFiles = async () => {
      try {
        const fileList = await fetchUploadedFiles();
        setFiles(fileList);
        setUploadedFiles(fileList);
        if (fileList.length > 0) {
          setSelectedFile(fileList[0]);
          setSelectedUploadedFile(fileList[0]);
        }
      } catch (err) {
        console.error(err);
      }
    };
    loadFiles();
  }, []);

  // Fetch preview when selectedFile changes
  useEffect(() => {
    if (!selectedFile) return;

    const loadPreview = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetchDataPreview(selectedFile);
        setData(res.preview || []);
      } catch (err) {
        console.error(err);
        setError(err.response?.data?.error || "Failed to fetch data");
      } finally {
        setLoading(false);
      }
    };

    loadPreview();
  }, [selectedFile]);

  // react-table columns
  const columns = useMemo(() => {
    if (data.length === 0) return [];
    return Object.keys(data[0]).map((key) => ({
      Header: key,
      accessor: key,
      Cell: ({ value }) => (value === null || value === undefined ? "" : String(value)),
    }));
  }, [data]);

  const tableInstance = useTable(
    { columns, data },
    useSortBy,
    usePagination
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
    page,
    nextPage,
    previousPage,
    canNextPage,
    canPreviousPage,
    pageOptions,
    state: { pageIndex },
    gotoPage,
  } = tableInstance;

  // Stub for deleting uploaded files
  const handleDelete = async (filename) => {
    if (!window.confirm(`Are you sure you want to delete ${filename}?`)) return;
    try {
      await deleteFile(filename);
      setUploadedFiles(uploadedFiles.filter(f => f !== filename));
      if (selectedUploadedFile === filename) setSelectedUploadedFile("");
      window.location.reload();
    } catch (err) {
      console.error(err);
      alert("Failed to delete file.");
    }
  };

  return (
    <div className="data-review-container">
      <h2>Data Review</h2>
      <p>Select a file to inspect your uploaded dataset.</p>

      {/* File selector */}
      <div className="file-selector">
        {files.length === 0 ? (
          <p>No uploaded files yet.</p>
        ) : (
          <select
            value={selectedFile || ""}
            onChange={(e) => setSelectedFile(e.target.value)}
          >
            {files.map((file) => (
              <option key={file} value={file}>
                {file}
              </option>
            ))}
          </select>
        )}
      </div>

      {/* Uploaded Files Panel */}
      <div className="uploaded-files-panel">
        <h4>Uploaded Files</h4>
        <ul>
          {uploadedFiles.map((file) => (
            <li key={file} className="uploaded-file-item">
              <span
                className={selectedUploadedFile === file ? "selected" : ""}
                onClick={() => {
                  setSelectedUploadedFile(file);
                  setSelectedFile(file);
                }}
              >
                {file}
              </span>
              <button className="delete-btn" onClick={() => handleDelete(file)}>×</button>
            </li>
          ))}
        </ul>
      </div>

      {loading && <p className="loading">Loading preview...</p>}
      {error && <p className="error">{error}</p>}

      {data.length > 0 && (
        <div className="data-preview">
          {/* Pagination */}
          <div className="pagination">
            <button onClick={() => gotoPage(0)} disabled={!canPreviousPage}>
              {"<<"}
            </button>
            <button onClick={() => previousPage()} disabled={!canPreviousPage}>
              Previous
            </button>
            <span>
              Page {pageIndex + 1} of {pageOptions.length}
            </span>
            <button onClick={() => nextPage()} disabled={!canNextPage}>
              Next
            </button>
            <button
              onClick={() => gotoPage(pageOptions.length - 1)}
              disabled={!canNextPage}
            >
              {">>"}
            </button>
          </div>

          <table {...getTableProps()}>
            <thead>
              {headerGroups.map((headerGroup) => (
                <tr {...headerGroup.getHeaderGroupProps()}>
                  {headerGroup.headers.map((column) => (
                    <th {...column.getHeaderProps(column.getSortByToggleProps())}>
                      {column.render("Header")}
                      <span>
                        {column.isSorted
                          ? column.isSortedDesc
                            ? " 🔽"
                            : " 🔼"
                          : ""}
                      </span>
                    </th>
                  ))}
                </tr>
              ))}
            </thead>
            <tbody {...getTableBodyProps()}>
              {page.map((row) => {
                prepareRow(row);
                return (
                  <tr {...row.getRowProps()}>
                    {row.cells.map((cell) => (
                      <td {...cell.getCellProps()}>{cell.render("Cell")}</td>
                    ))}
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
