// src/components/FileUpload.tsx
'use client';

import { useState } from 'react';
import { processFile } from '@/services/api';
import { useRouter } from 'next/navigation';

export default function FileUpload() {
    const [file, setFile] = useState<File | null>(null);
    const router = useRouter();

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            setFile(e.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (file) {
            try {
                await processFile(file);
                router.push('/upload/mapping');
            } catch (error) {
                console.error('Upload failed:', error);
            }
        }
    };

    return (
        <div>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload} disabled={!file}>
                Upload & Proceed to Mapping
            </button>
        </div>
    );
}
