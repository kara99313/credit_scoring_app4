#!/usr/bin/env python3
"""
Credit Scoring System - Main Entry Point

This module provides the main entry point for the credit scoring system.
It includes options to run data processing, model training, API service, or Streamlit app.

Author: Credit Scoring Team
Created: 2024
"""

import os
import sys
import logging
import click
import yaml
from pathlib import Path
from typing import Optional

# Add src to Python path
sys.path.append(str(Path(__file__).parent / "src"))

from src.utils import setup_logging
from pipelines.data_pipeline import DataPipeline
from pipelines.training_pipeline import TrainingPipeline
from pipelines.inference_pipeline import InferencePipeline


def load_config(config_path: str = "config/config.yaml") -> dict:
    """Load configuration from YAML file."""
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {config_path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        logging.error(f"Error parsing configuration file: {e}")
        sys.exit(1)


@click.group()
@click.option('--config', default='config/config.yaml', help='Path to configuration file')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.pass_context
def cli(ctx, config: str, verbose: bool):
    """Credit Scoring System - ML Pipeline and API."""
    
    # Ensure the context object exists
    ctx.ensure_object(dict)
    
    # Load configuration
    ctx.obj['config'] = load_config(config)
    
    # Setup logging
    log_level = logging.DEBUG if verbose else logging.INFO
    setup_logging(log_level)
    
    # Create necessary directories
    os.makedirs("logs", exist_ok=True)
    os.makedirs("models", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    
    logging.info("Credit Scoring System initialized")


@cli.command()
@click.option('--force', is_flag=True, help='Force reprocessing even if processed data exists')
@click.pass_context
def process_data(ctx, force: bool):
    """Process raw data and prepare it for training."""
    config = ctx.obj['config']
    
    logging.info("Starting data processing pipeline")
    
    try:
        pipeline = DataPipeline(config)
        pipeline.run(force_reprocess=force)
        logging.info("Data processing completed successfully")
    except Exception as e:
        logging.error(f"Data processing failed: {e}")
        sys.exit(1)


@cli.command()
@click.option('--experiment-name', default=None, help='MLflow experiment name')
@click.option('--auto-tune', is_flag=True, help='Enable hyperparameter tuning')
@click.pass_context
def train_model(ctx, experiment_name: Optional[str], auto_tune: bool):
    """Train the credit scoring model."""
    config = ctx.obj['config']
    
    logging.info("Starting model training pipeline")
    
    try:
        pipeline = TrainingPipeline(config)
        pipeline.run(
            experiment_name=experiment_name,
            hyperparameter_tuning=auto_tune
        )
        logging.info("Model training completed successfully")
    except Exception as e:
        logging.error(f"Model training failed: {e}")
        sys.exit(1)


@cli.command()
@click.option('--model-path', default=None, help='Path to trained model')
@click.option('--input-data', required=True, help='Path to input data for prediction')
@click.option('--output-path', default='predictions.csv', help='Path to save predictions')
@click.pass_context
def predict(ctx, model_path: Optional[str], input_data: str, output_path: str):
    """Make predictions using trained model."""
    config = ctx.obj['config']
    
    logging.info("Starting inference pipeline")
    
    try:
        pipeline = InferencePipeline(config)
        pipeline.run(
            model_path=model_path,
            input_data_path=input_data,
            output_path=output_path
        )
        logging.info(f"Predictions saved to {output_path}")
    except Exception as e:
        logging.error(f"Prediction failed: {e}")
        sys.exit(1)


@cli.command()
@click.option('--host', default='0.0.0.0', help='API host')
@click.option('--port', default=8000, help='API port')
@click.option('--reload', is_flag=True, help='Enable auto-reload for development')
@click.pass_context
def run_api(ctx, host: str, port: int, reload: bool):
    """Run the FastAPI service."""
    import uvicorn
    
    logging.info(f"Starting API service on {host}:{port}")
    
    try:
        uvicorn.run(
            "api_service.app:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except Exception as e:
        logging.error(f"API service failed: {e}")
        sys.exit(1)


@cli.command()
@click.option('--port', default=8501, help='Streamlit app port')
@click.pass_context
def run_app(ctx, port: int):
    """Run the Streamlit application."""
    import subprocess
    
    logging.info(f"Starting Streamlit application on port {port}")
    
    try:
        cmd = [
            "streamlit", "run", "streamlit_app/app.py",
            "--server.port", str(port),
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ]
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Streamlit application failed: {e}")
        sys.exit(1)
    except FileNotFoundError:
        logging.error("Streamlit not found. Please install it with: pip install streamlit")
        sys.exit(1)


@cli.command()
@click.pass_context
def run_mlflow(ctx):
    """Start MLflow tracking server."""
    import subprocess
    
    config = ctx.obj['config']
    tracking_uri = config.get('mlops', {}).get('experiment_tracking', {}).get('tracking_uri', 'http://localhost:5000')
    
    logging.info(f"Starting MLflow tracking server at {tracking_uri}")
    
    try:
        # Create mlruns directory if it doesn't exist
        os.makedirs("mlruns", exist_ok=True)
        
        cmd = [
            "mlflow", "ui",
            "--host", "0.0.0.0",
            "--port", "5000"
        ]
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"MLflow server failed: {e}")
        sys.exit(1)
    except FileNotFoundError:
        logging.error("MLflow not found. Please install it with: pip install mlflow")
        sys.exit(1)


@cli.command()
@click.pass_context
def full_pipeline(ctx):
    """Run the complete ML pipeline: data processing + training."""
    config = ctx.obj['config']
    
    logging.info("Starting full ML pipeline")
    
    try:
        # Data processing
        logging.info("Step 1/2: Processing data")
        data_pipeline = DataPipeline(config)
        data_pipeline.run()
        
        # Model training
        logging.info("Step 2/2: Training model")
        training_pipeline = TrainingPipeline(config)
        training_pipeline.run(hyperparameter_tuning=True)
        
        logging.info("Full pipeline completed successfully")
    except Exception as e:
        logging.error(f"Full pipeline failed: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def status(ctx):
    """Show system status and information."""
    config = ctx.obj['config']
    
    print("\n" + "="*50)
    print("CREDIT SCORING SYSTEM STATUS")
    print("="*50)
    
    # Project info
    project_info = config.get('project', {})
    print(f"Project: {project_info.get('name', 'Unknown')}")
    print(f"Version: {project_info.get('version', 'Unknown')}")
    print(f"Description: {project_info.get('description', 'Unknown')}")
    
    # Check data
    print("\nDATA STATUS:")
    raw_data_path = config.get('data', {}).get('raw_data_path', 'data/raw/')
    processed_data_path = config.get('data', {}).get('processed_data_path', 'data/processed/')
    
    print(f"  Raw data: {'✓' if os.path.exists(raw_data_path) else '✗'} ({raw_data_path})")
    print(f"  Processed data: {'✓' if os.path.exists(processed_data_path) else '✗'} ({processed_data_path})")
    
    # Check models
    print("\nMODEL STATUS:")
    models_path = "models/"
    if os.path.exists(models_path):
        model_files = [f for f in os.listdir(models_path) if f.endswith(('.pkl', '.joblib'))]
        if model_files:
            print(f"  Available models: {len(model_files)}")
            for model in model_files[:3]:  # Show first 3
                print(f"    - {model}")
            if len(model_files) > 3:
                print(f"    ... and {len(model_files) - 3} more")
        else:
            print("  No trained models found")
    else:
        print("  Models directory not found")
    
    # Check services
    print("\nSERVICE CONFIGURATION:")
    api_config = config.get('api', {})
    streamlit_config = config.get('streamlit', {})
    
    print(f"  API: {api_config.get('host', 'localhost')}:{api_config.get('port', 8000)}")
    print(f"  Streamlit: {streamlit_config.get('server_address', 'localhost')}:{streamlit_config.get('port', 8501)}")
    
    print("\nUSAGE:")
    print("  python main.py process-data    # Process raw data")
    print("  python main.py train-model     # Train model")
    print("  python main.py run-api         # Start API service")
    print("  python main.py run-app         # Start Streamlit app")
    print("  python main.py full-pipeline   # Run complete pipeline")
    print()


if __name__ == "__main__":
    cli() 