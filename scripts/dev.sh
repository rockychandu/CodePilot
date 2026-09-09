#!/usr/bin/env bash
set -e

echo "=========================================================="
echo "   CodePilot Enterprise Development Platform              "
echo "=========================================================="

cleanup() {
    echo "Shutting down CodePilot services..."
    kill 0
}
trap cleanup EXIT INT TERM

echo "[1/2] Launching Backend REST API on http://127.0.0.1:5000..."
python -m backend.app &

sleep 2

echo "[2/2] Launching Frontend Development Server on http://127.0.0.1:5173..."
npm run dev
