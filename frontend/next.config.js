/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false,
  output: 'standalone',
  webpack: (config) => {
    config.resolve.alias['@'] = __dirname;
    return config;
  }
};
module.exports = nextConfig;
