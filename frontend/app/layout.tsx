import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Image Quality Optimizer',
  description: 'Compare and optimize image quality with advanced algorithms',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
