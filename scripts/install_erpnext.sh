#!/usr/bin/env bash
set -euo pipefail

FRAPPE_BRANCH="version-14"
NODE_VERSION="18"
SITE_NAME="meu_site.local"
BENCH_DIR="$HOME/frappe-bench"

echo "=========================================="
echo " ERPNext Development Environment Setup"
echo "=========================================="

echo "[1/7] Updating packages..."
sudo apt update
sudo apt upgrade -y

echo "[2/7] Installing system dependencies..."
sudo apt install -y \
  python3-dev \
  python3.10-dev \
  build-essential \
  libssl-dev \
  libffi-dev \
  python3-pip \
  python3-setuptools \
  libmysqlclient-dev \
  wkhtmltopdf \
  git \
  curl \
  redis-server \
  xvfb \
  libfontconfig \
  mariadb-server \
  supervisor \
  python3-venv

echo "[3/7] Installing NVM and Node.js..."
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
export NVM_DIR="$HOME/.nvm"
# shellcheck source=/dev/null
source "$NVM_DIR/nvm.sh"
nvm install "$NODE_VERSION"
nvm use "$NODE_VERSION"
nvm alias default "$NODE_VERSION"
npm install -g yarn

echo "[4/7] Configuring MariaDB..."
sudo systemctl enable mariadb
sudo systemctl start mariadb
sudo tee /etc/mysql/mariadb.conf.d/50-server.cnf >/dev/null <<'EOF'
[mysql]
default-character-set = utf8mb4

[mysqld]
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
EOF
sudo systemctl restart mariadb

echo "[5/7] Installing Bench CLI..."
python3 -m pip install --user frappe-bench
export PATH="$HOME/.local/bin:$PATH"

if [[ -d "$BENCH_DIR" ]]; then
  echo "Directory already exists: $BENCH_DIR"
  echo "Rename or remove it before running this script again."
  exit 1
fi

echo "[6/7] Creating Bench and site..."
cd "$HOME"
bench init frappe-bench --frappe-branch "$FRAPPE_BRANCH"
cd "$BENCH_DIR"

read -rsp "MariaDB root password: " MARIADB_ROOT_PASSWORD
echo
read -rsp "ERPNext Administrator password: " ADMIN_PASSWORD
echo

bench new-site "$SITE_NAME" \
  --mariadb-root-password "$MARIADB_ROOT_PASSWORD" \
  --admin-password "$ADMIN_PASSWORD"

unset MARIADB_ROOT_PASSWORD ADMIN_PASSWORD

echo "[7/7] Installing ERPNext..."
bench get-app erpnext --branch "$FRAPPE_BRANCH"
bench --site "$SITE_NAME" install-app erpnext

echo
echo "Installation completed."
echo "Start the development server with:"
echo "  cd $BENCH_DIR"
echo "  bench start"
echo
echo "Development URL: http://localhost:8000"
