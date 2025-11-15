# Creating New GitHub Repository - Clean Version

## Steps to Create a New Repo Without PostgreSQL

### 1. Prepare the Repository

```bash
cd c:\KaunasTechnicalUniversity\Classes\Computational_Intelligence_and_Decision_Making\CIDMProject\landmark-id
```

### 2. Replace README

```bash
# Replace old README with new one
del README.md
ren README_NEW.md README.md
```

### 3. Remove PostgreSQL-Related Files

```bash
# Remove database migration files
rmdir /s /q backend\LandmarkApi\Migrations

# Remove database context and related files  
del backend\LandmarkApi\Data\LandmarkDbContext.cs
del backend\LandmarkApi\DATABASE_SETUP.md
```

### 4. Clean Build Artifacts

```bash
# Backend
rmdir /s /q backend\LandmarkApi\bin
rmdir /s /q backend\LandmarkApi\obj

# Python cache
rmdir /s /q __pycache__
del /s *.pyc

# W&B runs (keep settings)
# Optional: keep recent runs for reference
```

### 5. Initialize Git (if not already)

```bash
git init
git add .
git commit -m "Initial commit: Lithuanian Landmark Identification (no PostgreSQL)"
```

### 6. Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `lithuanian-landmark-identification`
3. Description: "Deep learning-based landmark identification for Lithuanian landmarks using MobileNetV3-Large and TensorFlow Lite"
4. Keep it **Public** or **Private** (your choice)
5. **DO NOT** initialize with README (we already have one)
6. Click "Create repository"

### 7. Push to GitHub

```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/lithuanian-landmark-identification.git

# Push
git branch -M main
git push -u origin main
```

## What's Included in the New Repo

✅ **Included:**
- Training scripts (`src/model/`)
- Data preparation scripts (`src/GLDV2_ds/`)
- TFLite export script (`scripts/export_tflite.py`)
- Backend API (`.NET 9.0` - **no PostgreSQL**)
- Mobile app (React Native/Expo)
- Configuration files
- Documentation (new README)

✅ **Model Files** (if trained):
- `models/landmark_mnv3.keras` (final trained model)
- `exports/landmark_mnv3_fp32.tflite`
- `exports/landmark_mnv3_int8_drq.tflite`
- `assets/labels.txt`

❌ **Excluded** (via .gitignore):
- Python virtual environment (`.venv/`)
- Downloaded images (`data/image_cache/`)
- W&B run logs (`wandb/`)
- Build artifacts (`bin/`, `obj/`, `node_modules/`)
- Model checkpoints (keep only final exports)
- Database files (removed entirely)

## Repository Description

```
Deep learning-based landmark identification for Lithuanian landmarks. 
Features MobileNetV3-Large model with 91% test accuracy, 
.NET REST API, and React Native mobile app. 
No database required - lightweight deployment.
```

## Topics/Tags

Add these tags to your GitHub repo:
- `deep-learning`
- `tensorflow`
- `tensorflow-lite`
- `mobilenet`
- `image-classification`
- `landmark-recognition`
- `dotnet`
- `react-native`
- `computer-vision`
- `lithuania`

## After Pushing

### Update the README with your repo URL

In `README.md`, add:

```markdown
## 📦 Repository

GitHub: https://github.com/YOUR_USERNAME/lithuanian-landmark-identification
```

### Create Releases

Tag your trained model versions:

```bash
git tag -a v1.0 -m "Initial release: 91% accuracy, 10 landmarks"
git push origin v1.0
```

### Add Assets to Release

1. Go to Releases on GitHub
2. Create new release from `v1.0` tag
3. Upload:
   - `landmark_mnv3_fp32.tflite`
   - `landmark_mnv3_int8_drq.tflite`
   - `labels.txt`

## Clone Instructions for Others

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/lithuanian-landmark-identification.git
cd lithuanian-landmark-identification

# Setup Python environment
python3.11 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install tensorflow==2.16.1 pillow tqdm wandb requests "protobuf<5,>=3.20.3"

# Prepare data
python src/GLDV2_ds/fetch_metadata.py --top-n 10 --images-per-class balanced
python src/GLDV2_ds/create_split.py

# Train
export PYTHONPATH=.
python src/model/train_keras_wandb.py
```

## Notes

- **No database setup required** - API runs standalone
- **Images stream on-demand** - no need to download dataset manually
- **Model files optional** - can retrain from scratch or download from releases
- **Mobile app ready** - just update API URL in config
