import React from 'react'

export function Header() {
    return (
        <header className="text-center space-y-2 py-8">
            <h1 className="text-4xl font-bold tracking-tight text-slate-900">Course Outline Extractor</h1>
            <p className="text-slate-500 text-lg">Upload PDF outlines to extract structured data into Excel.</p>
        </header>
    )
}
