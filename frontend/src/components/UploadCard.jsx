import React from 'react'
import { Upload, Loader2, AlertCircle } from 'lucide-react'

export function UploadCard({ files, isUploading, error, onFileChange, onUpload }) {
    return (
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-8 max-w-3xl mx-auto">
            <div className="flex flex-col items-center justify-center border-2 border-dashed border-slate-300 rounded-xl p-12 hover:bg-slate-50 transition-colors relative group cursor-pointer">
                <input
                    type="file"
                    multiple
                    accept=".pdf"
                    onChange={onFileChange}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                />
                <div className="bg-blue-50 p-4 rounded-full mb-4 group-hover:scale-110 transition-transform">
                    <Upload className="w-8 h-8 text-blue-600" />
                </div>
                <p className="text-lg font-medium text-slate-900">
                    {files.length > 0 ? `${files.length} files selected` : "Drop PDF files here or click to upload"}
                </p>
                <p className="text-slate-500 mt-1">Supports multiple files</p>
            </div>

            {files.length > 0 && (
                <div className="mt-6 flex items-center justify-between">
                    <div className="text-sm text-slate-500">
                        {files.map(f => f.name).join(', ')}
                    </div>
                    <button
                        onClick={onUpload}
                        disabled={isUploading}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2.5 rounded-lg font-medium flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-md hover:shadow-lg"
                    >
                        {isUploading ? (
                            <>
                                <Loader2 className="w-4 h-4 animate-spin" />
                                Processing...
                            </>
                        ) : (
                            <>
                                Start Extraction
                            </>
                        )}
                    </button>
                </div>
            )}

            {error && (
                <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-lg flex items-center gap-2 border border-red-100">
                    <AlertCircle className="w-5 h-5" />
                    {error}
                </div>
            )}
        </div>
    )
}
