'use client';

import ColumnMapper from '@/components/ColumnMapper';
import DataFramePreview from '@/components/DataFramePreview';
import { useRouter } from 'next/navigation';
import { useState } from 'react';

export default function UploadPage() {
    const [year, setYear] = useState('');
    const [broker, setBroker] = useState('degiro');
    const [mode, setMode] = useState('dividend');
    const [file, setFile] = useState<File | null>(null);
    const [columnMap, setColumnMapping] = useState<null | object>(null);
    const [message, setMessage] = useState('');
    const [previewDataFrame, setPreviewDataFrame] = useState<object | null>(null)


    const router = useRouter();
    
    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            setFile(e.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!file || !year || !broker || !mode) {
            setMessage('Please fill all fields and select a file.');
            return;
        }

        const formData = new FormData();
        formData.append('year', year);
        formData.append('broker', broker);
        formData.append('mode', mode);
        formData.append('file', file);

        try {
            const response = await fetch('http://localhost:8000/upload/', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();
            const columnMap = data.details.column_types
            setMessage(`Successfully loaded csv`);
            console.log("data", data);
            setColumnMapping(columnMap)

            setPreviewDataFrame(data.details.data_preview)
            let queryParams = {
                year: year,
                mode: mode,
                broker: broker,
            }
            const params = new URLSearchParams(queryParams);

            // router.push(`/upload/mapping?${params}`);
        } catch (error) {
            console.error('Error uploading file:', error);
            setMessage('Failed to upload file.');
        }
    };

    return (
        <div className="p-8">
            <h1 className="text-2xl font-bold mb-4">Upload CSV</h1>
            <div className="mb-4">
                <label>Year:</label>
                <input
                    type="text"
                    value={year}
                    onChange={(e) => setYear(e.target.value)}
                    className="border p-2 ml-2"
                />
            </div>
            <div className="mb-4">
                <label>Broker:</label>
                <select
                    value={broker}
                    onChange={(e) => setBroker(e.target.value)}
                    className="border p-2 ml-2"
                >
                 <option value="degiro">Degiro</option>
                 <option value="portu">Portu</option>
                </select>
            </div>
            <div className="mb-4">
                <label>Mode:</label>
                <select
                    value={mode}
                    onChange={(e) => setMode(e.target.value)}
                    className="border p-2 ml-2"
                >
                    <option value="dividend">Dividend</option>
                    <option value="stock">Stock</option>
                </select>
            </div>
            <div className="mb-4">
                <label>CSV File:</label>
                <input
                    type="file"
                    accept=".csv"
                    onChange={handleFileChange}
                    className="ml-2"
                />
            </div>
            <button
                onClick={handleUpload}
                className="bg-blue-500 text-white px-4 py-2 rounded"
            >
                Upload
            </button>
            {message && <p className="mt-4">{message}</p>}

            { previewDataFrame ? (
                <DataFramePreview data={previewDataFrame} columnMapping={columnMap}/>
            ) : null}

            {/* { columnMapping ? (
                <table border="1">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Data Type</th>
                    <th>Target Data</th>
                  </tr>
                </thead>
                <tbody>
                  {columnMapping.map((row, index) => (
                      <tr key={index}>
                      <td>{row.key}</td>
                      <td>{row.value}</td>
                      <td>
                        <select defaultValue={row.targetData}>
                          <option value="Date">Date</option>
                          <option value="Currency">Currency</option>
                          <option value="Amount">Amount</option>
                        </select>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : null} */}
        </div>



    );
}
