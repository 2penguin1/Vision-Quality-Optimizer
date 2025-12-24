import apiClient from './client';

export const authAPI = {
  register: async (email: string, password: string, name: string) => {
    const response = await apiClient.post('/auth/register', {
      email,
      password,
      name,
    });
    return response.data;
  },

  login: async (email: string, password: string) => {
    const response = await apiClient.post('/auth/login', {
      email,
      password,
    });
    return response.data;
  },

  refreshToken: async (refreshToken: string) => {
    const response = await apiClient.post('/auth/refresh', {
      refresh_token: refreshToken,
    });
    return response.data;
  },
};

export const imageAPI = {
  uploadImage: async (file: File, description?: string) => {
    const formData = new FormData();
    formData.append('file', file);
    if (description) formData.append('description', description);

    const response = await apiClient.post('/images/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  getUserImages: async (skip?: number, limit?: number) => {
    const params = new URLSearchParams();
    if (skip !== undefined) params.append('skip', skip.toString());
    if (limit !== undefined) params.append('limit', limit.toString());

    const response = await apiClient.get(`/images/my-images?${params}`);
    return response.data;
  },

  getImage: async (imageId: string) => {
    const response = await apiClient.get(`/images/${imageId}`);
    return response.data;
  },

  deleteImage: async (imageId: string) => {
    const response = await apiClient.delete(`/images/${imageId}`);
    return response.data;
  },

  compareImages: async (image1Id: string, image2Id: string, enhancementLevel?: number) => {
    const response = await apiClient.post('/images/compare', {
      image1_id: image1Id,
      image2_id: image2Id,
      enhancement_level: enhancementLevel || 0.5,
    });
    return response.data;
  },
};
