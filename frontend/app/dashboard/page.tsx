'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store/authStore';
import { imageAPI } from '@/lib/api/endpoints';
import ImageUpload from '@/components/ImageUpload';
import ImageGallery from '@/components/ImageGallery';

export default function DashboardPage() {
  const router = useRouter();
  const { isAuthenticated, logout } = useAuthStore();
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('upload');

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/auth/login');
      return;
    }

    loadImages();
  }, [isAuthenticated, router]);

  const loadImages = async () => {
    try {
      setLoading(true);
      const response = await imageAPI.getUserImages();
      setImages(response.images || []);
    } catch (error) {
      console.error('Failed to load images:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleImageUploaded = () => {
    loadImages();
  };

  const handleLogout = () => {
    logout();
    router.push('/auth/login');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Image Quality Optimizer</h1>
          <button
            onClick={handleLogout}
            className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg"
          >
            Logout
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Tabs */}
        <div className="flex gap-4 mb-8">
          <button
            onClick={() => setActiveTab('upload')}
            className={`px-6 py-2 rounded-lg font-semibold transition ${
              activeTab === 'upload'
                ? 'bg-blue-600 text-white'
                : 'bg-white text-gray-700 border border-gray-300'
            }`}
          >
            Upload Images
          </button>
          <button
            onClick={() => setActiveTab('gallery')}
            className={`px-6 py-2 rounded-lg font-semibold transition ${
              activeTab === 'gallery'
                ? 'bg-blue-600 text-white'
                : 'bg-white text-gray-700 border border-gray-300'
            }`}
          >
            Gallery
          </button>
        </div>

        {/* Content */}
        {activeTab === 'upload' && <ImageUpload onUploadSuccess={handleImageUploaded} />}
        {activeTab === 'gallery' && (
          <ImageGallery images={images} loading={loading} onRefresh={loadImages} />
        )}
      </main>
    </div>
  );
}
