import React, { useState, useEffect, useRef } from 'react'; // 1. Add useRef
import axios from 'axios';
import PlusIcon from "./components/PlusIcon"; 
import './index.css';

// Define a type for our file objects for type safety
interface UploadedFile {
  id: string;
  filename: string;
  uploaded_at: string;
}

// The new UploadBox component
const UploadBox = () => {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isUploading, setIsUploading] = useState(false); // State for upload progress
  const [error, setError] = useState<string | null>(null);

  // 2. Create a ref to access the hidden file input element
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Function to fetch files, which we can now reuse
  const fetchFiles = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get('http://localhost:8000/api/files/', {
        withCredentials: true,
      });
      setFiles(response.data);
      setError(null); // Clear previous errors on success
    } catch (err) {
      setError('Failed to fetch files.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  // Fetch files when the component first mounts
  useEffect(() => {
    fetchFiles();
  }, []);

  // 3. Function to handle the actual file upload
  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('file', selectedFile);

    setIsUploading(true);
    setError(null);

    try {
      await axios.post('http://localhost:8000/api/files/', formData, {
        withCredentials: true,
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      // After a successful upload, refresh the list to show the new file
      await fetchFiles();
    } catch (err) {
      setError('File upload failed. Please try again.');
      console.error(err);
    } finally {
      setIsUploading(false);
    }
  };

  // 4. Function to trigger the hidden input when the button is clicked
  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className='flex flex-col items-center w-96'>
      <div className='flex justify-center items-center bg-transparent border-2 border-[#6A6363] w-48 h-8'>
        Uploaded
      </div>
      <div className='border-1 border-[#6A6363] h-3'></div>
      <div className='border-t-2 border-[#6A6363] w-full mt-[-1px]'></div>
      <div className='flex flex-col p-4 bg-transparent border-2 border-t-0 border-[#6A6363] w-full h-96 overflow-y-auto'>
        {isLoading && <p>Loading...</p>}
        {isUploading && <p>Uploading file...</p>}
        {error && <p className="text-red-500">{error}</p>}
        
        {/* Only show the list or upload prompt when not loading */}
        {!isLoading && !isUploading && !error && (
          files.length > 0 ? (
            <ul className="space-y-2">
              {files.map(file => (
                <li key={file.id} className="p-2 bg-[#D4DCE6] rounded-md text-black text-sm">
                  {file.filename}
                </li>
              ))}
            </ul>
          ) : (
            <div className="flex justify-center items-center h-full">
              {/* 5. Add onClick to this div */}
              <div 
                className="flex items-center gap-2 p-2 rounded-md bg-[#D4DCE6] cursor-pointer hover:bg-gray-300 transition-colors"
                onClick={handleUploadClick}
              >
                <PlusIcon className="w-4 h-4" />
                <p className="text-black text-sm opacity-50">click or drag to upload files</p>
              </div>
            </div>
          )
        )}
      </div>
      {/* 6. Add the hidden file input element */}
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileUpload}
        className="hidden"
      />
    </div>
  );
};

// A placeholder for the ConvertedBox
const ConvertedBox = () => {
  return (
    <div className='flex flex-col items-center w-96'>
       <div className='flex justify-center items-center bg-transparent border-2 border-[#6A6363] w-48 h-8'>
        Converted
      </div>
      <div className='border-1 border-[#6A6363] h-3'></div>
      <div className='border-t-2 border-[#6A6363] w-full mt-[-1px]'></div>
      <div className='flex justify-center items-center p-4 bg-transparent border-2 border-t-0 border-[#6A6363] w-full h-96'>
        <p className="text-gray-500">Converted files will appear here.</p>
      </div>
    </div>
  );
}


function App() {
  return (
    <>
      <section className="flex flex-col items-center bg-[#E6E2E2] min-h-screen font-jura">
        <div className='bg-[#D4DCE6] h-16 w-full items-center flex justify-center text-2xl'>
          alchemy
        </div>
        <div className="flex flex-row justify-center items-start gap-20 mt-20">
          <UploadBox />
          <ConvertedBox />
        </div>
      </section>
    </>
  )
}

export default App;
