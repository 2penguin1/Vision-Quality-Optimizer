# Image Quality Optimization - Frontend README

## Overview

This is the Next.js frontend for the Image Quality Optimization system. It provides:

- **User Authentication**: Register, login, token management
- **Image Upload**: Upload images with descriptions to cloud storage
- **Image Gallery**: Browse and manage uploaded images
- **Image Comparison**: Select two images and compare their quality metrics
- **Enhancement Control**: Adjust enhancement level during comparison

## Tech Stack

- **Framework**: Next.js 14 (React 18)
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Language**: TypeScript
- **Authentication**: JWT

## Installation

### Prerequisites

- Node.js 18+
- npm or yarn

### Local Development

1. **Install dependencies**

```bash
npm install
```

2. **Set up environment variables**

```bash
cp .env.local.example .env.local
```

Edit `.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. **Run development server**

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Production Build

```bash
# Build for production
npm run build

# Start production server
npm run start

# Or export as static site
npm run export
```

## Project Structure

```
frontend/
├── app/
│   ├── auth/
│   │   ├── login/
│   │   │   └── page.tsx        # Login page
│   │   └── register/
│   │       └── page.tsx        # Register page
│   ├── dashboard/
│   │   └── page.tsx            # Main dashboard
│   ├── page.tsx                # Home page
│   ├── layout.tsx              # Root layout
│   └── globals.css             # Global styles
├── components/
│   ├── ImageUpload.tsx         # Image upload component
│   └── ImageGallery.tsx        # Image gallery component
├── lib/
│   ├── api/
│   │   ├── client.ts           # Axios client with interceptors
│   │   └── endpoints.ts        # API endpoint functions
│   ├── store/
│   │   └── authStore.ts        # Zustand auth store
│   └── auth.ts                 # Auth utility functions
├── public/                     # Static assets
├── styles/                     # Additional stylesheets
├── package.json
├── tsconfig.json
├── next.config.js
├── tailwind.config.js
├── postcss.config.js
└── .env.local.example
```

## Pages

### Home Page (`/`)

Landing page with:
- Project overview
- Navigation to login/register
- Feature highlights

### Register Page (`/auth/register`)

User registration with:
- Email, password, name fields
- Password confirmation
- Form validation
- Error messages

### Login Page (`/auth/login`)

User login with:
- Email and password fields
- Form validation
- Error handling
- Redirect to dashboard on success

### Dashboard Page (`/dashboard`)

Main application with:
- Protected route (requires authentication)
- Two tabs: Upload and Gallery
- Image upload interface
- Image gallery with comparison

## Components

### ImageUpload

Handles image uploads with:
- File input with drag-and-drop preview
- Description field (optional)
- File size validation (max 50MB)
- Upload progress
- Success/error messages

```typescript
<ImageUpload onUploadSuccess={handleUploadSuccess} />
```

### ImageGallery

Displays user's images with:
- Grid layout
- Image selection (up to 2)
- Comparison controls
- Enhancement level slider
- Image metadata display

```typescript
<ImageGallery images={images} loading={loading} onRefresh={reloadImages} />
```

## State Management

### Authentication Store (Zustand)

```typescript
const { user, accessToken, isAuthenticated, setUser, setTokens, logout } = useAuthStore();
```

Features:
- User information
- Token storage (localStorage)
- Authentication state
- Logout functionality

## API Integration

### Authentication API

```typescript
authAPI.register(email, password, name)
authAPI.login(email, password)
authAPI.refreshToken(refreshToken)
```

### Image API

```typescript
imageAPI.uploadImage(file, description)
imageAPI.getUserImages(skip, limit)
imageAPI.getImage(imageId)
imageAPI.deleteImage(imageId)
imageAPI.compareImages(image1Id, image2Id, enhancementLevel)
```

### API Client Features

- **Request Interceptor**: Automatically adds JWT token
- **Response Interceptor**: Handles token refresh on 401
- **Error Handling**: Catches and processes errors
- **Base URL**: Configurable via environment variables

## Styling

### Tailwind CSS

Uses Tailwind CSS utility classes for:
- Responsive design
- Color scheme
- Component styling
- Animations

### Custom Styles

Global styles in `app/globals.css`:
- Custom scrollbar behavior
- Base element styling
- CSS resets

## Environment Variables

```
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Note**: Variables prefixed with `NEXT_PUBLIC_` are exposed to the browser.

## Build Optimization

### Image Optimization

Next.js optimizes images for:
- Different screen sizes
- Format conversion (WebP)
- Lazy loading
- Responsive images

### Code Splitting

- Route-based code splitting
- Dynamic imports for components
- Automatic optimization

## Performance

### Core Web Vitals

Optimized for:
- **LCP** (Largest Contentful Paint)
- **FID** (First Input Delay)
- **CLS** (Cumulative Layout Shift)

### Caching

- Automatic page caching
- API response caching in store
- Optimized dependency handling

## Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
CMD ["npm", "run", "start"]
```

### Manual EC2 Deployment

See `config/EC2_DEPLOYMENT.md` for detailed instructions.

## Security

1. **JWT Token Storage**
   - Stored in localStorage
   - Automatically included in requests
   - Validated on each request

2. **CORS**
   - Handled by backend
   - Browser enforces same-origin policy

3. **Input Validation**
   - Email validation
   - File type validation
   - Form field validation

4. **XSS Protection**
   - React automatically escapes content
   - No dangerouslySetInnerHTML used

## Browser Support

- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Development Guidelines

1. **Component Structure**
   - Functional components with hooks
   - Proper TypeScript types
   - Prop documentation

2. **State Management**
   - Zustand for global state
   - useState for local state
   - Proper cleanup in useEffect

3. **Error Handling**
   - Try-catch blocks
   - User-friendly error messages
   - Error logging

4. **Accessibility**
   - Semantic HTML
   - ARIA labels
   - Keyboard navigation

## Troubleshooting

### Blank Page

1. Check browser console for errors
2. Verify API_URL in `.env.local`
3. Ensure backend is running

### API Connection Errors

1. Check `NEXT_PUBLIC_API_URL` matches backend
2. Verify CORS settings on backend
3. Check network tab for blocked requests

### Authentication Issues

1. Clear localStorage
2. Check token expiry
3. Verify backend auth endpoints

### Styling Issues

1. Run `npm run build` to regenerate CSS
2. Check Tailwind config
3. Clear `.next` folder

## Future Enhancements

- [ ] Progressive Web App (PWA) support
- [ ] Offline image storage
- [ ] Advanced image editing features
- [ ] Real-time collaboration
- [ ] Mobile app with React Native
- [ ] Advanced filtering and search
- [ ] User settings dashboard
- [ ] Multi-language support

## Performance Optimization Tips

1. **Image Lazy Loading**
   - Next.js automatically optimizes images
   - Use `<Image>` component from next/image

2. **Code Splitting**
   - Dynamic imports for large components
   - Route-based splitting handled automatically

3. **Bundle Optimization**
   - Remove unused dependencies
   - Tree-shake unused exports
   - Monitor bundle size with `next/bundle-analyzer`

## Support and Contribution

For issues and contributions, please refer to the main project documentation.
