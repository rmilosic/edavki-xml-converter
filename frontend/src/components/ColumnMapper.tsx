// src/components/ColumnMapper.tsx
'use client';

import { useState } from 'react';

export default function ColumnMapper() {
    const [mapping, setMapping] = useState<Record<string, string>>({});

    const handleMappingChange = (sourceColumn: string, targetColumn: string) => {
        setMapping((prev) => ({ ...prev, [sourceColumn]: targetColumn }));
    };

    const handleValidate = () => {
        console.log('Validating Mapping:', mapping);
        // Add validation logic here
    };

    return (
        <div>
            <h3>Column Mapping</h3>
            <div>
                <label>
                    Source Column:
                    <input type="text" onChange={(e) => handleMappingChange('source', e.target.value)} />
                </label>
                <label>
                    Target Column:
                    <input type="text" onChange={(e) => handleMappingChange('target', e.target.value)} />
                </label>
            </div>
            <button onClick={handleValidate}>Validate Mapping</button>
        </div>
    );
}
