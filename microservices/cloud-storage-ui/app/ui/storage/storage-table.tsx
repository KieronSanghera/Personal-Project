// components/FileTable.tsx
'use client' 

import React from 'react';
import Checkbox from '@/components/ui/checkbox';

interface File {
  id: number;
  name: string;
  size: string; // Example format: "1.2 MB"
  virusCheck: string; // Example values: "Clean", "Infected"
  contentCheck: string; // Example values: "Safe", "Unsafe"
}

interface FileTableProps {
  files: File[];
}

const FileTable: React.FC<FileTableProps> = ({ files }) => {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Files</h1>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Filename</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Filesize</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Virus Check</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Contents Check</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider flex justify-center items-center">Select</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {files.map(file => (
              <tr key={file.id}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{file.name}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{file.size}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    file.virusCheck === 'Clean' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {file.virusCheck}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    file.contentCheck === 'Safe' ? 'bg-blue-100 text-blue-800' : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {file.contentCheck}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <button className="text-blue-600 hover:text-blue-900">Edit</button>
                  <button className="ml-4 text-red-600 hover:text-red-900">Delete</button>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 flex justify-center items-center">

                  <Checkbox></Checkbox> 
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default FileTable;