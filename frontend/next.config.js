/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    BACKEND_API_URL: process.env.BACKEND_API_URL || 'http://localhost:8000/api/v1/chat',
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.API_URL || 'http://localhost:8000/api/:path*',
      },
    ];
  },
};

module.exports = nextConfig; 