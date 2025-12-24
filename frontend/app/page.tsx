import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-4xl font-bold text-gray-900">Image Quality Optimizer</h1>
        </div>
      </header>

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h2 className="text-5xl font-bold text-gray-900 mb-4">
            Compare and Enhance Image Quality
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Use advanced ML algorithms to assess and improve your images with precise control
          </p>

          <div className="flex gap-4 justify-center">
            <Link
              href="/auth/login"
              className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-semibold transition"
            >
              Login
            </Link>
            <Link
              href="/auth/register"
              className="bg-white border border-blue-600 text-blue-600 hover:bg-blue-50 px-8 py-3 rounded-lg font-semibold transition"
            >
              Register
            </Link>
          </div>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-8 mt-16">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-3">Quality Assessment</h3>
            <p className="text-gray-600">
              Advanced algorithms assess sharpness, contrast, noise, and color accuracy
            </p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-3">Smart Enhancement</h3>
            <p className="text-gray-600">
              Adaptive algorithms enhance specific quality aspects with user control
            </p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-3">Cloud Storage</h3>
            <p className="text-gray-600">
              Secure storage of images on AWS S3 with easy access and management
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
