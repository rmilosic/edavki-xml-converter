import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

const DataFramePreview = ({ data , columnMapping}) => {
  if (!data || Object.keys(data).length === 0) {
    return (
      <Card className="w-full">
        <CardContent className="p-6">
          <p className="text-gray-500">No data available</p>
        </CardContent>
      </Card>
    );
  }

  // Convert dictionary format to array of objects
  const columns = Object.keys(data);
  const rowCount = Object.keys(Object.values(data)[0]).length
  const rows = Array.from({ length: rowCount }, (_, rowIndex) => {
    const row = {};
    columns.forEach(column => {
      row[column] = data[column][rowIndex];
    });
    return row;
  });

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>DataFrame Preview</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr>
                {columns.map(column => (
                  <th 
                    key={column}
                    className="p-2 text-left border-b-2 border-gray-200 bg-gray-50 font-medium"
                  >
                    {column}
                  </th>
                ))}
              </tr>
              <tr>
                {columns.map(column => (
                    <th key={column}
                    className="p-2 text-left border-b-2 border-gray-200 bg-gray-50 font-medium">
                        <select>
                            <option disabled selected> -- select an option -- </option>
                          <option value="Date">Date</option>
                          <option value="Currency">Currency</option>
                          <option value="Amount">Amount</option>
                          <option value="ISIN">ISIN</option>
                        </select>
                    </th>
                ))}
              </tr>
              <tr>
                {columns.map(column => (
                    <th key={column}
                    className="p-2 text-left border-b-2 border-gray-200 bg-gray-50 font-medium">
                        {columnMapping[column]}
                    </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((row, index) => (
                <tr 
                  key={index}
                  className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}
                >
                  {columns.map(column => (
                    <td 
                      key={`${index}-${column}`}
                      className="p-2 border-b border-gray-200"
                    >
                      {row[column]?.toString()}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  );
};

export default DataFramePreview;