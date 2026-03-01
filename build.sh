#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "🎥 Installing FFmpeg static build..."
# Render free tier blocks apt-get, so we download the static binary directly.
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
tar -xf ffmpeg-release-amd64-static.tar.xz

# The extracted folder has a dynamic name like 'ffmpeg-7.0.1-amd64-static', so we find the executable and move it.
find . -name "ffmpeg" -type f -executable -exec mv {} ./ \;
find . -name "ffprobe" -type f -executable -exec mv {} ./ \;

# Clean up downloaded archives
rm -rf ffmpeg-release-amd64-static*

echo "✅ Build completed successfully!"
