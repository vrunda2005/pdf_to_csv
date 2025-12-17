import React from 'react'

export function ResultsTable({ data, title, icon: Icon, downloadUrl, onDownload }) {
    if (!data || data.length === 0) return null

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between px-4">
                <h2 className="text-2xl font-semibold text-slate-900 flex items-center gap-2">
                    {Icon && <Icon className={`w-6 h-6 ${title.includes('Complete') ? 'text-green-500' : 'text-blue-500'}`} />}
                    {title}
                </h2>
                {downloadUrl && (
                    <a
                        href={`http://localhost:8000${downloadUrl}`}
                        className="bg-green-600 hover:bg-green-700 text-white px-5 py-2 rounded-lg font-medium flex items-center gap-2 shadow-sm transition-colors"
                    >
                        {onDownload}
                    </a>
                )}
            </div>

            <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
                <div className="overflow-x-auto max-h-[600px]">
                    <table className="w-full text-sm text-left">
                        <thead className="bg-slate-50 text-slate-500 font-medium border-b border-slate-200 sticky top-0 bg-slate-50 z-10">
                            <tr>
                                {Object.keys(data[0] || {}).map((key) => (
                                    <th key={key} className="px-6 py-4 whitespace-nowrap uppercase tracking-wider text-xs">{key}</th>
                                ))}
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                            {data.map((row, idx) => (
                                <tr key={idx} className="hover:bg-slate-50/50 transition-colors">
                                    {Object.values(row).map((val, i) => (
                                        <td key={i} className="px-6 py-4 min-w-[250px] whitespace-pre-wrap align-top text-slate-700">
                                            {val}
                                        </td>
                                    ))}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    )
}
