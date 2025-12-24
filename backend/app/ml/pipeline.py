"""
ML Pipeline for Image Quality Assessment and Enhancement
Implements BRISQUE, NIQE quality metrics and adaptive enhancement algorithms
"""

import numpy as np
import cv2
from typing import Dict, Tuple, Optional
import time
from scipy.ndimage import gaussian_filter, uniform_filter
from scipy.signal import convolve2d
import asyncio


class QualityAssessmentModel:
    """
    Multi-image quality assessment model
    Implements BRISQUE (Blind/Referenceless Image Spatial Quality Evaluator) 
    and NIQE (Natural Image Quality Evaluator)
    """
    
    def __init__(self):
        """Initialize the quality assessment model"""
        self.kernel_size = 7
        self.sigma = 7/6
    
    def _assess_brisque_score(self, image: np.ndarray) -> float:
        """
        Calculate BRISQUE score (0-100, lower is better)
        Approximated using local statistics
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        gray = gray.astype(np.float32) / 255.0
        
        # Laplacian variance (sharpness)
        laplacian = cv2.Laplacian(gray, cv2.CV_32F)
        sharpness = np.var(laplacian)
        
        # Contrast (standard deviation)
        contrast = np.std(gray)
        
        # Local standard deviation (texture)
        kernel = cv2.getGaussianKernel(5, 1.5)
        kernel = kernel @ kernel.T
        mu = convolve2d(gray, kernel, mode='valid')
        mu_sq = convolve2d(gray**2, kernel, mode='valid')
        texture = np.mean(np.sqrt(np.abs(mu_sq - mu**2)))
        
        # Combine features into quality score
        quality_score = (sharpness * 0.4 + contrast * 0.3 + texture * 0.3)
        
        # Convert to 0-100 scale
        brisque_score = 100 * (1 - np.tanh(quality_score / 10))
        return float(max(0, min(100, brisque_score)))
    
    def _assess_niqe_score(self, image: np.ndarray) -> float:
        """
        Calculate NIQE score (naturalness assessment)
        Measures how natural the image looks (0-100, higher is better)
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        gray = gray.astype(np.float32) / 255.0
        
        # Compute local contrast
        kernel_size = 7
        kernel = cv2.getGaussianKernel(kernel_size, kernel_size/6)
        kernel = kernel @ kernel.T
        
        mu = convolve2d(gray, kernel, mode='valid')
        mu_sq = convolve2d(gray**2, kernel, mode='valid')
        sigma = np.sqrt(np.abs(mu_sq - mu**2 + 1e-8))
        
        # MSCN coefficients
        mscn = (gray - mu) / (sigma + 1e-8)
        
        # Naturalness features
        mscn_energy = np.mean(np.abs(mscn))
        mscn_var = np.std(mscn)
        
        # Naturalness score
        niqe_score = 100 * np.exp(-mscn_energy / 2) * (1 + 1/(1 + mscn_var))
        
        return float(max(0, min(100, niqe_score)))
    
    async def assess_quality(self, image: np.ndarray) -> Dict[str, float]:
        """
        Assess image quality metrics
        
        Returns:
            {
                "sharpness": float (0-100),
                "contrast": float (0-100),
                "noise": float (0-100),
                "natural": float (0-100),
                "overall_score": float (0-100)
            }
        """
        # Validate input
        if image is None or image.size == 0:
            return {
                "sharpness": 0.0,
                "contrast": 0.0,
                "noise": 0.0,
                "natural": 0.0,
                "overall_score": 0.0
            }
        
        # Convert image to 8-bit if needed
        if image.dtype != np.uint8:
            image = np.clip(image, 0, 255).astype(np.uint8)
        
        gray = image if len(image.shape) == 2 else cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Compute Laplacian for sharpness
        laplacian = cv2.Laplacian(gray, cv2.CV_32F)
        sharpness = float(100 * np.tanh(np.var(laplacian) / 100))
        
        # Compute contrast
        contrast = float(100 * np.std(gray.astype(np.float32)) / 255)
        
        # Compute noise (inverse of local smoothness)
        kernel = cv2.getGaussianKernel(5, 1.0)
        kernel = kernel @ kernel.T
        smoothed = convolve2d(gray[2:-2, 2:-2].astype(np.float32) / 255, kernel, mode='valid')
        original = gray[4:-4, 4:-4].astype(np.float32) / 255
        if original.size > 0 and smoothed.size > 0:
            noise = float(max(0, 100 * (1 - np.mean(np.abs(smoothed - original)))))
        else:
            noise = 50.0
        
        # NIQE score for naturalness
        natural = self._assess_niqe_score(image)
        
        # Overall score (weighted average)
        overall = (sharpness * 0.3 + contrast * 0.2 + noise * 0.2 + natural * 0.3)
        
        return {
            "sharpness": float(np.clip(sharpness, 0, 100)),
            "contrast": float(np.clip(contrast, 0, 100)),
            "noise": float(np.clip(noise, 0, 100)),
            "natural": float(np.clip(natural, 0, 100)),
            "overall_score": float(np.clip(overall, 0, 100))
        }
    
    async def compare_images(self, image1: np.ndarray, image2: np.ndarray) -> Dict:
        """
        Compare quality metrics between two images
        
        Returns quality metrics and comparison
        """
        metrics1 = await self.assess_quality(image1)
        metrics2 = await self.assess_quality(image2)
        
        # Calculate differences
        differences = {}
        for key in metrics1.keys():
            differences[key] = metrics2[key] - metrics1[key]
        
        return {
            "image1_metrics": metrics1,
            "image2_metrics": metrics2,
            "differences": differences,
            "comparison": "image2_better" if metrics2["overall_score"] > metrics1["overall_score"] else "image1_better"
        }


class EnhancementAlgorithm:
    """
    Adaptive enhancement algorithm
    Implements sharpening, denoising, contrast enhancement, and color correction
    """
    
    def __init__(self):
        """Initialize the enhancement algorithm"""
        pass
    
    async def enhance_image(self, image: np.ndarray, enhancement_params: Dict[str, float]) -> np.ndarray:
        """
        Apply targeted enhancements to image
        
        Args:
            image: Input image array (BGR)
            enhancement_params: {
                "sharpness": float (0-1),
                "contrast": float (0-1),
                "denoise": float (0-1),
                "color": float (0-1),
                "brightness": float (0-1)
            }
        
        Returns:
            Enhanced image array
        """
        enhanced = image.copy().astype(np.float32)
        
        # Brightness adjustment
        if enhancement_params.get("brightness", 0) > 0.01:
            brightness = enhancement_params["brightness"]
            enhanced = np.clip(enhanced * (1 + brightness * 0.5), 0, 255)
        
        # Denoise first
        if enhancement_params.get("denoise", 0) > 0.01:
            denoise_strength = int(enhancement_params["denoise"] * 10)
            if len(enhanced.shape) == 3:
                enhanced = cv2.bilateralFilter(enhanced.astype(np.uint8), 5, 50 * denoise_strength / 10, 50 * denoise_strength / 10).astype(np.float32)
            else:
                enhanced = cv2.bilateralFilter(enhanced.astype(np.uint8), 5, 50 * denoise_strength / 10, 50 * denoise_strength / 10).astype(np.float32)
        
        # Contrast enhancement
        if enhancement_params.get("contrast", 0) > 0.01:
            contrast = enhancement_params["contrast"]
            mean = np.mean(enhanced)
            enhanced = np.clip(mean + (enhanced - mean) * (1 + contrast), 0, 255)
        
        # Sharpening (Unsharp masking)
        if enhancement_params.get("sharpness", 0) > 0.01:
            sharpness = enhancement_params["sharpness"]
            kernel = cv2.getGaussianKernel(5, 1.0)
            kernel = kernel @ kernel.T
            if len(enhanced.shape) == 3:
                for i in range(enhanced.shape[2]):
                    blurred = convolve2d(enhanced[:, :, i], kernel, mode='same')
                    enhanced[:, :, i] = np.clip(enhanced[:, :, i] + (enhanced[:, :, i] - blurred) * sharpness, 0, 255)
            else:
                blurred = convolve2d(enhanced, kernel, mode='same')
                enhanced = np.clip(enhanced + (enhanced - blurred) * sharpness, 0, 255)
        
        # Color enhancement
        if enhancement_params.get("color", 0) > 0.01 and len(enhanced.shape) == 3:
            color_strength = enhancement_params["color"]
            enhanced_uint = enhanced.astype(np.uint8)
            hsv = cv2.cvtColor(enhanced_uint, cv2.COLOR_BGR2HSV).astype(np.float32)
            hsv[:, :, 1] = np.clip(hsv[:, :, 1] * (1 + color_strength * 0.5), 0, 255)
            enhanced = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)
        
        # Final clip and convert
        enhanced = np.clip(enhanced, 0, 255).astype(np.uint8)
        
        return enhanced
    
    async def generate_enhancement_params(self, quality_diff: Dict[str, float], 
                                         enhancement_level: float = 0.5) -> Dict[str, float]:
        """
        Generate enhancement parameters based on quality differences
        
        Args:
            quality_diff: Differences in quality metrics (image2 - image1)
            enhancement_level: User control (0-1, where 0.5 is normal)
        
        Returns:
            Enhancement parameters dictionary
        """
        params = {
            "sharpness": 0.0,
            "contrast": 0.0,
            "denoise": 0.0,
            "color": 0.0,
            "brightness": 0.0
        }
        
        # Adjust based on differences and user level
        if quality_diff.get("sharpness", 0) < -5:  # Need sharpening
            params["sharpness"] = min(0.8, abs(quality_diff["sharpness"]) / 100 * enhancement_level)
        
        if quality_diff.get("contrast", 0) < -5:  # Need more contrast
            params["contrast"] = min(0.6, abs(quality_diff["contrast"]) / 100 * enhancement_level)
        
        if quality_diff.get("noise", 0) < -5:  # Too noisy
            params["denoise"] = min(0.7, abs(quality_diff["noise"]) / 100 * enhancement_level)
        
        if quality_diff.get("natural", 0) < -5:  # Less natural
            params["color"] = min(0.5, abs(quality_diff["natural"]) / 100 * enhancement_level)
        
        # Manual brightness adjustment
        if quality_diff.get("overall_score", 0) < -10:
            params["brightness"] = 0.2 * enhancement_level
        
        return params


class MLPipeline:
    """
    Complete ML pipeline for image quality assessment and enhancement
    """
    
    def __init__(self):
        """Initialize the ML pipeline"""
        self.quality_model = QualityAssessmentModel()
        self.enhancement = EnhancementAlgorithm()
    
    async def process_images(self, image1: np.ndarray, image2: np.ndarray, 
                            enhancement_level: float = 0.5) -> Dict:
        """
        Complete pipeline: compare and enhance images
        
        Args:
            image1: First image
            image2: Second image
            enhancement_level: User control level (0-1)
        
        Returns:
            Processing results with enhanced image
        """
        start_time = time.time()
        
        # Assess and compare quality
        comparison = await self.quality_model.compare_images(image1, image2)
        
        # Determine which image to enhance
        if comparison["image2_metrics"]["overall_score"] > comparison["image1_metrics"]["overall_score"]:
            # Enhance image1 to match image2
            target_image = image1
            quality_diff = {k: comparison["image2_metrics"][k] - comparison["image1_metrics"][k] 
                          for k in comparison["image1_metrics"].keys()}
        else:
            # Enhance image2 to match image1
            target_image = image2
            quality_diff = {k: comparison["image1_metrics"][k] - comparison["image2_metrics"][k] 
                          for k in comparison["image2_metrics"].keys()}
        
        # Generate enhancement parameters
        enhancement_params = await self.enhancement.generate_enhancement_params(
            quality_diff, 
            enhancement_level
        )
        
        # Apply enhancement
        enhanced_image = await self.enhancement.enhance_image(target_image, enhancement_params)
        
        # Assess enhanced image
        enhanced_metrics = await self.quality_model.assess_quality(enhanced_image)
        
        processing_time = time.time() - start_time
        
        return {
            "image1_metrics": comparison["image1_metrics"],
            "image2_metrics": comparison["image2_metrics"],
            "enhanced_metrics": enhanced_metrics,
            "enhancement_params": enhancement_params,
            "processing_time": processing_time,
            "improvements": {
                k: enhanced_metrics[k] - (comparison["image1_metrics"][k] if target_image is image1 else comparison["image2_metrics"][k])
                for k in enhanced_metrics.keys()
            },
            "enhanced_image": enhanced_image
        }


# Global pipeline instance
ml_pipeline = MLPipeline()
