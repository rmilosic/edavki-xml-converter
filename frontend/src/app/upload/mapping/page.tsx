// src/app/upload/mapping/page.tsx
'use client';

import ColumnMapper from '@/components/ColumnMapper';

export default function MappingPage({year, mode, broker}) {
    return (
        <div>
            <h2>Map Your CSV Columns</h2>
            <ColumnMapper />
        </div>
    );
}
