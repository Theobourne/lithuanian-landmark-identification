# Lithuanian Landmark Identification

Deep learning-based landmark recognition system for 10 famous Lithuanian landmarks. Uses MobileNetV3-Large with transfer learning, trained on the Google Landmarks Dataset v2.

## Features

- **10 Lithuanian Landmarks**: Freedom Avenue (Kaunas), Gate of Dawn, Gediminas Tower, Hill of Crosses, IX Fort, Parnidžio kopa, Rasos Cemetery, Trakai Island Castle, Užupis, Zarasas
- **High Accuracy**: 91%+ test accuracy with MobileNetV3-Large backbone
- **Streaming Dataset**: On-demand image downloading from Google Cloud Storage URLs
- **Efficient Deployment**: TFLite INT8 quantization for mobile devices
- **Full Stack**: Python training pipeline, .NET backend API, React Native mobile app
- **Experiment Tracking**: Weights & Biases integration for monitoring training

## Tech Stack

- **ML Framework**: TensorFlow 2.16.1, Keras 3
- **Model**: MobileNetV3-Large (pre-trained on ImageNet)
- **Dataset**: Google Landmarks Dataset v2 (Lithuania subset)
- **Backend**: .NET 9.0 minimal API
- **Mobile**: React Native with Expo
- **Tracking**: Weights & Biases

## Quick Start

### Prerequisites

- Python 3.11
- .NET 9.0 SDK
- Node.js 18+

### 1. Setup Python Environment

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
wandb login
```

### 2. Data Preparation

The dataset uses a streaming approach - images are downloaded on-demand from Google Cloud Storage URLs:

```bash
# Data files are already included:
# - data/metadata.json (image URLs for 10 landmarks)
# - data/train.txt, val.txt, test.txt (dataset splits)

# Images will be cached to data/image_cache/ on first use
```

**Dataset Statistics:**
- Total: 1,041 images
- Training: 722 images (69.4%)
- Validation: 152 images (14.6%)
- Test: 167 images (16.0%)

### 3. Train the Model

```bash
python src/model/train_keras_wandb.py
```

**Training Process:**
- **Phase 1** (25 epochs): Trains classification head with frozen MobileNetV3 backbone
- **Phase 2** (10 epochs): Fine-tunes entire model with low learning rate
- Models saved to `models/` directory
- Metrics logged to Weights & Biases

### 4. Export to TFLite

```bash
python scripts/export_tflite.py --keras-model models/phase2_ckpt_10_0.768.keras
```

Generates:
- `exports/landmark_mnv3_fp32.tflite` (FP32 model)
- `exports/landmark_mnv3_int8_drq.tflite` (INT8 quantized)
- `exports/labels.txt` (class names)

### 5. Run Backend API

```bash
cd backend/LandmarkApi
dotnet run
```

API runs at `http://localhost:5126`
- Swagger UI: `http://localhost:5126/swagger`
- Upload image via POST `/api/prediction`

### 6. Run Mobile App

```bash
cd mobile/LandmarkApp
npm install
npm start
```

## Project Structure

```
landmark-id/
├── data/                          # Dataset files
│   ├── metadata.json              # Image URLs from Google Cloud Storage
│   ├── train.txt, val.txt, test.txt  # Dataset splits
│   └── image_cache/               # Downloaded images cache
│       ├── train/, val/, test/
├── src/
│   ├── GLDV2_ds/                  # Dataset loading utilities
│   │   └── gldv2_dataset.py       # Streaming TF dataset loader
│   └── model/
│       └── train_keras_wandb.py   # Training script
├── scripts/
│   └── export_tflite.py           # TFLite export utility
├── models/                        # Trained model checkpoints
├── exports/                       # Exported TFLite models
├── backend/LandmarkApi/           # .NET API
│   ├── Controllers/
│   ├── Models/                    # TFLite models & labels
│   └── Services/
└── mobile/LandmarkApp/            # React Native app
    └── src/
```

## How It Works

### Dataset Pipeline

1. **Metadata Collection**: `data/metadata.json` contains image URLs from Google Landmarks Dataset v2
2. **Streaming Download**: Images are downloaded on-demand during training/inference
3. **Disk Caching**: Downloaded images cached in `data/image_cache/` to avoid re-downloading
4. **TensorFlow Dataset**: `gldv2_dataset.py` creates streaming TF datasets from URLs

### Training Pipeline

1. **Phase 1 - Head Training**:
   - Freeze MobileNetV3-Large backbone
   - Train only classification head
   - 25 epochs with AdamW optimizer (lr=1e-3)
   - Data augmentation: flip, zoom, brightness, contrast

2. **Phase 2 - Fine-tuning**:
   - Unfreeze last 20 non-BatchNorm layers
   - Fine-tune entire model
   - 10 epochs with Adam optimizer (lr=3e-5)
   - Label smoothing (0.05) for better generalization

### Model Export

1. **Remove Augmentation**: Build inference-only graph without augmentation layers
2. **SavedModel**: Export to TensorFlow SavedModel format
3. **TFLite Conversion**: Convert to TFLite (FP32)
4. **INT8 Quantization**: Post-training quantization using representative dataset
5. **Generate Labels**: Auto-generate `labels.txt` from metadata

### Inference

1. **Backend API** (.NET):
   - Receives image upload
   - Calls Python subprocess with TFLite model
   - Returns top-3 predictions with confidence scores

2. **Mobile App** (React Native):
   - Capture photo or select from gallery
   - Send to backend API
   - Display results with landmark names and confidence

## API Endpoints

### POST `/api/prediction`

Upload an image for landmark prediction.

**Request:**
- Content-Type: `multipart/form-data`
- Body: Image file (max 10MB)

**Response:**
```json
{
  "predictions": [
    {
      "label": "Trakai_Island_Castle",
      "confidence": 0.9234
    },
    {
      "label": "Gediminas_Tower",
      "confidence": 0.0456
    },
    {
      "label": "Gate_of_Dawn",
      "confidence": 0.0123
    }
  ]
}
```

## Training Results

- **Architecture**: MobileNetV3-Large
- **Classes**: 10 Lithuanian landmarks
- **Test Accuracy**: 91.03%
- **Model Size**: ~15MB (INT8 quantized)
- **Training Time**: ~35 epochs total (25 + 10)

## Development

### Adding More Landmarks

1. Update `data/metadata.json` with new landmark URLs
2. Update `data/train.txt`, `val.txt`, `test.txt` with new samples
3. Retrain model: `python src/model/train_keras_wandb.py`
4. Export new model: `python scripts/export_tflite.py`
5. Update backend model files

### Adjusting Model Architecture

Edit `src/model/train_keras_wandb.py`:
- Change `CONFIG["arch"]` to use different MobileNetV3 variant
- Adjust `CONFIG["epochs"]` and `CONFIG["fine_tune_epochs"]`
- Modify data augmentation pipeline in `create_augmentation()`

### Testing Backend API

```bash
# Test with curl
curl -X POST http://localhost:5126/api/prediction \
  -F "file=@test_image.jpg"

# Or use Swagger UI
# Navigate to http://localhost:5126/swagger
```

## Troubleshooting

### Images Not Downloading
- Check internet connection
- Verify Google Cloud Storage URLs in `metadata.json` are accessible
- Images are cached in `data/image_cache/` after first download

### Model Training Errors
- Ensure TensorFlow 2.16.1 is installed: `pip install tensorflow==2.16.1`
- Check protobuf version: `pip install "protobuf<5,>=3.20.3"`
- Verify W&B login: `wandb login`

### Backend API Errors
- Ensure .NET 9.0 SDK is installed
- Check Python is accessible from system PATH
- Verify TFLite model exists in `backend/LandmarkApi/Models/`

### Mobile App Issues
- Clear Expo cache: `npm start -- --clear`
- Update API URL in `mobile/LandmarkApp/src/constants/config.ts`
- Check backend is running on correct port (5126)

## License

This project uses images from the Google Landmarks Dataset v2, which are available under various Creative Commons licenses. Please refer to the dataset documentation for specific license information.

## Acknowledgments

- Google Landmarks Dataset v2 for providing high-quality landmark images
- MobileNetV3 architecture from Google Research
- Weights & Biases for experiment tracking

---

**Project Status**: ✅ Production Ready

For questions or issues, please open a GitHub issue.
