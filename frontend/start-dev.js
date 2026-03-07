#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

const frontendDir = __dirname;

console.log('[v0] Starting Next.js development server...');
console.log('[v0] Frontend directory:', frontendDir);

const npm = spawn('npm', ['run', 'dev'], {
  cwd: frontendDir,
  stdio: 'inherit',
  shell: true
});

npm.on('error', (error) => {
  console.error('[v0] Failed to start dev server:', error);
  process.exit(1);
});

npm.on('exit', (code) => {
  process.exit(code);
});
