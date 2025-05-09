/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/v1/chat",
        destination: "http://localhost:8000/api/v1/chat",
      },
    ];
  },
};

module.exports = nextConfig; 