// src/app/page.tsx
'use client';

import Link from 'next/link';

export default function HomePage() {
    return (
        <div>
            <h2>Welcome to the CSV to XML Tax Reporting Tool</h2>
            <p>Please start by uploading your CSV file.</p>
            <Link href="/upload">
                <button>Get Started</button>
            </Link>
        </div>
    );
}
