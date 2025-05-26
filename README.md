# PikeDex

A Pokémon classification system using machine learning.

## Setup Instructions

### Prerequisites
- Python 3.10 or higher
- Node.js 16 or higher
- Git LFS (Large File Storage)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/satvikgarimella/PikeDex.git
cd PikeDex
```

2. Install Git LFS:
```bash
# macOS
brew install git-lfs

# Ubuntu/Debian
sudo apt install git-lfs

# Windows
# Download from https://git-lfs.github.com/
```

3. Set up Python environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

4. Set up frontend:
```bash
cd frontend
npm install
```

### Download Required Files

The following files are not included in the repository due to size limitations. Download them from our Google Drive:

[Download Required Files](https://drive.google.com/drive/folders/1tjhaL-DLFeWEUHdcQwkCIAvSkPGqks5F?usp=sharing)

After downloading:
1. Extract the `pokedex_dataset_ready` directory to the root of the project
2. Place `pokedex_model.h5` in the root directory of the project

### Running the Application

1. Start the backend:
```bash
cd backend
python backend.py
```

2. Start the frontend:
```bash
cd frontend
npm run dev
```

The application will be available at http://localhost:3000

## Project Structure

- `backend/`: Python backend server
- `frontend/`: Next.js frontend application
- `pokedex_dataset_ready/`: Dataset for training (download from Google Drive)
- `pokedex_model.h5`: Trained model file (download from Google Drive)

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 