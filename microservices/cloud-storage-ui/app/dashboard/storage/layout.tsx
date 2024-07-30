import React from "react"
import FileTable from "@/app/ui/storage/storage-table"
import FileUploadButton from "@/components/ui/fileupload-button"

const mockFiles = [
  {
    id: 1,
    name: "file1.txt",
    size: "1.2 MB",
    virusCheck: "Clean",
    contentCheck: "Safe",
  },
  {
    id: 2,
    name: "file2.txt",
    size: "500 KB",
    virusCheck: "Infected",
    contentCheck: "Unsafe",
  },
  {
    id: 3,
    name: "file3.jpg",
    size: "2.5 MB",
    virusCheck: "Clean",
    contentCheck: "Safe",
  },
]

const HomePage: React.FC = () => {
  return (
    <div>
      <FileUploadButton></FileUploadButton>
      <FileTable files={mockFiles} />
    </div>
  )
}

export default HomePage
