/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',  // Static export for Cloudflare Pages
  images: {
    unoptimized: true  // Required for static export
  },
  // Environment variables exposed to browser
  env: {
    GRAPH_GATEWAY_URL: process.env.GRAPH_GATEWAY_URL || 'https://graph-gateway.your-domain.com'
  }
}

module.exports = nextConfig
