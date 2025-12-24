'use client';

import { useState } from 'react';
import { imageAPI } from '@/lib/api/endpoints';

interface Image {
  _id: string;
  name: string;
  description?: string;
  s3_url: string;
  uploaded_at: string;
}

interface ImageGalleryProps {
  images: Image[];
  loading: boolean;
  onRefresh: () => void;
}

export default function ImageGallery({ images, loading, onRefresh }: ImageGalleryProps) {
  const [comparing, setComparing] = useState(false);
  const [selectedImages, setSelectedImages] = useState<string[]>([]);
  const [enhancementLevel, setEnhancementLevel] = useState(0.5);
  const [error, setError] = useState('');
  const [comparisonResult, setComparisonResult] = useState<any>(null);

  const toggleImageSelection = (imageId: string) => {
    setSelectedImages((prev) => {
      if (prev.includes(imageId)) {
        return prev.filter((id) => id !== imageId);
      }
      if (prev.length >= 2) {
        return [prev[1], imageId];
      }
      return [...prev, imageId];
    });
  };

  const handleCompare = async () => {
    if (selectedImages.length !== 2) {
      setError('Please select exactly 2 images');
      return;
    }

    setComparing(true);
    setError('');
    setComparisonResult(null);

    try {
      const result = await imageAPI.compareImages(
        selectedImages[0],
        selectedImages[1],
        enhancementLevel
      );
      setComparisonResult(result);
      console.log('Comparison Result:', result);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Comparison failed');
    } finally {
      setComparing(false);
    }
  };

  if (loading) {
    return <div className="text-center py-12">Loading images...</div>;
  }

  return (
    <div>
      {/* Controls */}
      {images.length >= 2 && (
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Image Comparison & Enhancement</h3>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Enhancement Level: {(enhancementLevel * 100).toFixed(0)}%
              </label>
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                value={enhancementLevel}
                onChange={(e) => setEnhancementLevel(parseFloat(e.target.value))}
                className="w-full"
              />
              <p className="text-xs text-gray-500 mt-1">
                {enhancementLevel < 0.3 ? 'Subtle' : enhancementLevel < 0.7 ? 'Moderate' : 'Aggressive'} enhancement
              </p>
            </div>

            <div className="text-sm text-gray-600">
              Selected Images: {selectedImages.length}/2
            </div>

            <button
              onClick={handleCompare}
              disabled={selectedImages.length !== 2 || comparing}
              className="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-semibold py-2 rounded-lg transition"
            >
              {comparing ? 'Analyzing & Enhancing...' : 'Compare & Enhance Selected Images'}
            </button>
          </div>
        </div>
      )}

      {/* Comparison Results */}
      {comparisonResult && (
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quality Analysis Results</h3>
          
          <div className="grid md:grid-cols-3 gap-4">
            {/* Image 1 Metrics */}
            <div className="border border-gray-200 rounded p-4">
              <h4 className="font-semibold text-gray-900 mb-3">Image 1 Quality Metrics</h4>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-700">Sharpness:</span>
                  <span className="font-semibold text-gray-900">{comparisonResult.image1_metrics?.sharpness?.toFixed(1)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-700">Contrast:</span>
                  <span className="font-semibold text-gray-900">{comparisonResult.image1_metrics?.contrast?.toFixed(1)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-700">Noise Level:</span>
                  <span className="font-semibold text-gray-900">{comparisonResult.image1_metrics?.noise?.toFixed(1)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-700">Naturalness:</span>
                  <span className="font-semibold text-gray-900">{comparisonResult.image1_metrics?.natural?.toFixed(1)}%</span>
                </div>
                <div className="border-t pt-2 mt-2 flex justify-between">
                  <span className="font-semibold text-gray-900">Overall Score:</span>
                  <span className="font-bold text-blue-600">{comparisonResult.image1_metrics?.overall_score?.toFixed(1)}%</span>
                </div>
              </div>
            </div>

            {/* Image 2 Metrics */}
            <div className="border border-gray-200 rounded p-4">
              <h4 className="font-semibold text-gray-900 mb-3">Image 2 Quality Metrics</h4>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-700">Sharpness:</span>
                  <span className="font-semibold text-gray-900">{comparisonResult.image2_metrics?.sharpness?.toFixed(1)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-700">Contrast:</span>
                  <span className="font-semibold text-gray-900">{comparisonResult.image2_metrics?.contrast?.toFixed(1)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-700">Noise Level:</span>
                  <span className="font-semibold text-gray-900">{comparisonResult.image2_metrics?.noise?.toFixed(1)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-700">Naturalness:</span>
                  <span className="font-semibold text-gray-900">{comparisonResult.image2_metrics?.natural?.toFixed(1)}%</span>
                </div>
                <div className="border-t pt-2 mt-2 flex justify-between">
                  <span className="font-semibold text-gray-900">Overall Score:</span>
                  <span className="font-bold text-blue-600">{comparisonResult.image2_metrics?.overall_score?.toFixed(1)}%</span>
                </div>
              </div>
            </div>

            {/* Processing Info */}
            <div className="border border-gray-200 rounded p-4 bg-blue-50">
              <h4 className="font-semibold text-gray-900 mb-3">Processing Information</h4>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-700">Processing Time:</span>
                  <span className="font-semibold text-gray-900">{comparisonResult.processing_time?.toFixed(2)}s</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-700">Enhancement Level:</span>
                  <span className="font-semibold text-gray-900">{(enhancementLevel * 100).toFixed(0)}%</span>
                </div>
                <div className="border-t pt-2 mt-2">
                  <p className="text-gray-700 mb-2">Enhancement Parameters:</p>
                  <div className="text-xs space-y-1">
                    <div>Sharpness: {(comparisonResult.enhancement_params?.sharpness * 100)?.toFixed(0)}%</div>
                    <div>Contrast: {(comparisonResult.enhancement_params?.contrast * 100)?.toFixed(0)}%</div>
                    <div>Denoise: {(comparisonResult.enhancement_params?.denoise * 100)?.toFixed(0)}%</div>
                    <div>Color: {(comparisonResult.enhancement_params?.color * 100)?.toFixed(0)}%</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Enhanced Metrics */}
          {comparisonResult.enhanced_metrics && (
            <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded">
              <h4 className="font-semibold text-gray-900 mb-3">Enhanced Image Quality (After Enhancement)</h4>
              <div className="grid md:grid-cols-5 gap-4 text-sm">
                <div>
                  <span className="text-gray-700">Sharpness:</span>
                  <div className="font-semibold text-gray-900">{comparisonResult.enhanced_metrics?.sharpness?.toFixed(1)}%</div>
                  <div className={`text-xs ${(comparisonResult.improvements?.sharpness || 0) > 0 ? 'text-green-600' : 'text-gray-500'}`}>
                    {((comparisonResult.improvements?.sharpness || 0) > 0 ? '+' : '')}{(comparisonResult.improvements?.sharpness)?.toFixed(1)}%
                  </div>
                </div>
                <div>
                  <span className="text-gray-700">Contrast:</span>
                  <div className="font-semibold text-gray-900">{comparisonResult.enhanced_metrics?.contrast?.toFixed(1)}%</div>
                  <div className={`text-xs ${(comparisonResult.improvements?.contrast || 0) > 0 ? 'text-green-600' : 'text-gray-500'}`}>
                    {((comparisonResult.improvements?.contrast || 0) > 0 ? '+' : '')}{(comparisonResult.improvements?.contrast)?.toFixed(1)}%
                  </div>
                </div>
                <div>
                  <span className="text-gray-700">Noise:</span>
                  <div className="font-semibold text-gray-900">{comparisonResult.enhanced_metrics?.noise?.toFixed(1)}%</div>
                  <div className={`text-xs ${(comparisonResult.improvements?.noise || 0) > 0 ? 'text-green-600' : 'text-gray-500'}`}>
                    {((comparisonResult.improvements?.noise || 0) > 0 ? '+' : '')}{(comparisonResult.improvements?.noise)?.toFixed(1)}%
                  </div>
                </div>
                <div>
                  <span className="text-gray-700">Natural:</span>
                  <div className="font-semibold text-gray-900">{comparisonResult.enhanced_metrics?.natural?.toFixed(1)}%</div>
                  <div className={`text-xs ${(comparisonResult.improvements?.natural || 0) > 0 ? 'text-green-600' : 'text-gray-500'}`}>
                    {((comparisonResult.improvements?.natural || 0) > 0 ? '+' : '')}{(comparisonResult.improvements?.natural)?.toFixed(1)}%
                  </div>
                </div>
                <div>
                  <span className="text-gray-700 font-semibold">Overall:</span>
                  <div className="font-bold text-green-600">{comparisonResult.enhanced_metrics?.overall_score?.toFixed(1)}%</div>
                  <div className={`text-xs ${(comparisonResult.improvements?.overall_score || 0) > 0 ? 'text-green-600' : 'text-gray-500'}`}>
                    {((comparisonResult.improvements?.overall_score || 0) > 0 ? '+' : '')}{(comparisonResult.improvements?.overall_score)?.toFixed(1)}%
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Gallery */}
      {images.length === 0 ? (
        <div className="bg-white rounded-lg shadow p-12 text-center">
          <p className="text-gray-600 text-lg">No images uploaded yet. Upload some images to get started!</p>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {images.map((image) => (
            <div
              key={image._id}
              onClick={() => toggleImageSelection(image._id)}
              className={`rounded-lg shadow overflow-hidden cursor-pointer transition transform hover:scale-105 ${
                selectedImages.includes(image._id)
                  ? 'ring-2 ring-blue-500 scale-105'
                  : ''
              }`}
            >
              <img
                src={image.s3_url}
                alt={image.name}
                className="w-full h-48 object-cover"
              />
              <div className="p-4 bg-white">
                <p className="font-semibold text-gray-900 truncate">{image.name}</p>
                {image.description && (
                  <p className="text-sm text-gray-600 line-clamp-2">{image.description}</p>
                )}
                <p className="text-xs text-gray-500 mt-2">
                  {new Date(image.uploaded_at).toLocaleDateString()}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
