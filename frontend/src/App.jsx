import { useState, useEffect } from 'react'
import axios from 'axios'
import { Download, CheckCircle, Database } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { Header } from './components/Header'
import { UploadCard } from './components/UploadCard'
import { ResultsTable } from './components/ResultsTable'

function App() {
  const [files, setFiles] = useState([])
  const [isUploading, setIsUploading] = useState(false)
  const [data, setData] = useState(null)
  const [allData, setAllData] = useState([])
  const [downloadUrl, setDownloadUrl] = useState(null)
  const [error, setError] = useState(null)

  const fetchAllData = async () => {
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/data`)
      setAllData(response.data.data)
    } catch (err) {
      console.error("Failed to fetch all data", err)
    }
  }

  useEffect(() => {
    fetchAllData()
  }, [])

  const handleFileChange = (e) => {
    if (e.target.files) {
      setFiles(Array.from(e.target.files))
    }
  }

  const handleUpload = async () => {
    if (files.length === 0) return

    setIsUploading(true)
    setError(null)
    setData(null)
    setDownloadUrl(null)

    const formData = new FormData()
    files.forEach(file => {
      formData.append('files', file)
    })

    try {
      const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      setData(response.data.data)
      setDownloadUrl(response.data.download_url)
      // Refresh all data list
      fetchAllData()
    } catch (err) {
      console.error(err)
      setError("Failed to process files. Please try again.")
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="min-h-screen p-8 font-sans bg-slate-50">
      <div className="max-w-7xl mx-auto space-y-8">

        <Header />

        <UploadCard
          files={files}
          isUploading={isUploading}
          error={error}
          onFileChange={handleFileChange}
          onUpload={handleUpload}
        />

        {/* Current Results */}
        <AnimatePresence>
          {data && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <ResultsTable
                data={data}
                title="Extraction Complete"
                icon={CheckCircle}
                downloadUrl={downloadUrl}
                onDownload={
                  <>
                    <Download className="w-4 h-4" />
                    Download Excel
                  </>
                }
              />
            </motion.div>
          )}
        </AnimatePresence>

        {/* All Historical Data */}
        {allData.length > 0 && (
          <div className="pt-8 border-t border-slate-200">
            <ResultsTable
              data={allData}
              title="All Uploaded Data"
              icon={Database}
            />
          </div>
        )}

      </div>
    </div>
  )
}

export default App
