/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  compiler: {
    reactCompiler: true,
  },
};

module.exports = nextConfig;
