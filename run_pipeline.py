
import subprocess
import logging
import sys
import time

# Configure logging to hook directly into our unified pipeline log
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)

def run_script(script_path):
    """
    Executes a Python script as a subprocess, monitors its stream,
    and catches failures immediately.
    """
    logging.info(f"🚀 [Orchestrator] Starting execution step: {script_path}")
    start_time = time.time()
    
    # Run the script via command line using the current Python environment
    result = subprocess.run([sys.executable, script_path])
    
    elapsed_time = time.time() - start_time
    
    if result.returncode == 0:
        logging.info(f"💪 [Orchestrator] Step completed successfully: {script_path} (Took {elapsed_time:.2f}s)\n")
        return True
    else:
        logging.error(f"💥 [Orchestrator] Critical Failure in step: {script_path} (Exit code: {result.returncode})")
        return False

def main():
    logging.info("🏁 ==================== STARTING MASTER PIPELINE RUN ====================")
    pipeline_start = time.time()
    
    # Define the exact execution sequence of our Medallion architecture
    pipeline_steps = [
        "scripts/extract_bronze.py",
        "scripts/process_silver.py",
        "scripts/aggregate_gold.py"
    ]
    
    for step in pipeline_steps:
        success = run_script(step)
        if not success:
            logging.critical("🛑 [Orchestrator] Pipeline execution halted due to upstream failure.")
            sys.exit(1)
            
    total_time = time.time() - pipeline_start
    logging.info(f"🏆 ==================== PIPELINE EXECUTION COMPLETE IN {total_time:.2f}s ====================")

if __name__ == "__main__":
    main()