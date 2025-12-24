# Vision Quality Optimizer

**Comparative Image Quality Optimization with User-Controlled Enhancement**

Developed under the **SRIB-PRISM Program**.

## 📖 Overview

**Vision Quality Optimizer** is a full-stack web application designed to evaluate, compare, and enhance image quality. It allows users to upload images, analyze them using advanced Machine Learning metrics (Sharpness, Contrast, Noise, Color), and perform side-by-side comparisons. The system also offers an adaptive enhancement feature where users can control the level of improvement applied to their images.

## 🚀 Key Features

*   **User Authentication**: Secure JWT-based signup, login, and session management.
*   **Image Management**: Cloud-based storage (AWS S3) for secure image upload, retrieval, and deletion.
*   **Quality Assessment**: Automated analysis of image quality measuring:
    *   Sharpness
    *   Contrast
    *   Noise Levels
    *   Color Accuracy
*   **Smart Comparison**: Side-by-side visual comparison of images with detailed metric differences.
*   **Adaptive Enhancement**: Interactive tools to enhance image quality with user-adjustable intensity (0-100%).
*   **Responsive Dashboard**: A modern, sleek user interface built with Next.js and Tailwind CSS.

## 🛠️ Technology Stack

### Frontend
*   **Framework**: Next.js 14 (React 18)
*   **Styling**: Tailwind CSS
*   **State Management**: Zustand
*   **Language**: TypeScript
*   **HTTP Client**: Axios

### Backend
*   **Framework**: FastAPI
*   **Database**: MongoDB (Motor Async Driver)
*   **Storage**: AWS S3
*   **ML/Processing**: OpenCV, PyTorch, NumPy
*   **Containerization**: Docker & Docker Compose

## 📂 Project Structure

```bash
Vision-Quality-Optimizer/
├── backend/            # FastAPI server, ML pipeline, and Database logic
├── frontend/           # Next.js web application
├── config/             # Deployment scripts and configurations (EC2)
└── README.md           # This file
```

## 🏁 Getting Started

### Prerequisites
*   **Docker & Docker Compose** (Recommended for Backend)
*   **Node.js** (v18+) and **npm/yarn** (For Frontend)
*   **Python** (v3.9+) (If running backend locally without Docker)
*   An **AWS Account** with S3 bucket credentials.

### 1️⃣ Backend Setup

You can run the backend using Docker (easiest) or locally.

**Option A: Using Docker**
1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
2.  Configure environment variables:
    ```bash
    cp .env.example .env
    # Open .env and add your MongoDB URI, AWS Credentials, etc.
    ```
3.  Start the services:
    ```bash
    docker-compose up -d
    ```
    The Backend API will handle requests at `http://localhost:8000`.

**Option B: Running Locally**
Refer to [backend/README.md](./backend/README.md) for detailed local installation steps.

### 2️⃣ Frontend Setup

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    # or
    yarn install
    ```
3.  Configure environment variables:
    ```bash
    cp .env.local.example .env.local
    # Ensure NEXT_PUBLIC_API_URL is set to http://localhost:8000
    ```
4.  Start the development server:
    ```bash
    npm run dev
    ```
    Access the application at `http://localhost:3000`.

## 📖 Usage Guide

1.  **Register/Login**: Create an account to access your personal dashboard.
2.  **Upload**: Drag and drop images into the upload zone. Add descriptions if needed.
3.  **Gallery**: View your uploaded images. Select two images to enter **Comparison Mode**.
4.  **Compare & Enhance**: 
    *   View calculated quality metrics for both images.
    *   Use the enhancement slider to adjust the processing level.
    *   Apply changes and view the result in real-time.

## ☁️ Deployment

The project includes configurations for deploying to an AWS EC2 instance.
*   See `config/EC2_DEPLOYMENT.md` for a comprehensive guide.
*   A setup script `config/ec2-setup.sh` is provided to automate environment preparation.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

---
*Built for the SRIB-PRISM Program.*
