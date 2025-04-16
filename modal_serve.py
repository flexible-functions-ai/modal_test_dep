import modal
import pandas as pd

# Create app definition
app = modal.App("sticker-sales-api")

# Define image with SPECIFIC VERSIONS to ensure compatibility
image = (modal.Image.debian_slim()
         .pip_install("pydantic==1.10.8")         # Pin to a specific compatible version
         .pip_install("fastapi==0.95.2")          # Pin to a version that works with this pydantic
         .pip_install("uvicorn==0.22.0")          # For FastAPI server
         .pip_install([                           # Other dependencies
             "bentoml",
             "xgboost",
             "scikit-learn",
             "pandas",
             "numpy",
         ]))

# Create a separate image for fastai to avoid conflicts
fastai_image = (modal.Image.debian_slim()
                .pip_install(["fastai", "torch"])
                .pip_install("pydantic==1.10.8")  # Same pydantic version
                .pip_install("fastapi==0.95.2"))  # Same fastapi version

# Create volume to store model
model_volume = modal.Volume.from_name("sticker-model-volume", create_if_missing=True)

# Simple health endpoint that doesn't need FastAI
@app.function(image=image)
@modal.fastapi_endpoint(method="GET")
def health():
    return {"status": "healthy", "service": "sticker-sales-api"}

# Prediction function - using the fastai image
@app.function(image=fastai_image, volumes={"/models": model_volume})
def predict(input_data: dict):
    from fastai.tabular.all import add_datepart
    import bentoml
    
    # Process input data
    df = pd.DataFrame([input_data])
    df = add_datepart(df, 'date', drop=False)
    
    # Load model and predict
    try:
        model = bentoml.xgboost.load_model("sticker_sales_v1:latest")
        prediction = model.predict(df)
        return {"success": True, "prediction": prediction.tolist()}
    except Exception as e:
        return {"success": False, "error": str(e)}

# API endpoint that uses the prediction function
@app.function(image=image)
@modal.fastapi_endpoint(method="POST")
def predict_api(input_data: dict):
    result = predict.call(input_data)
    return result