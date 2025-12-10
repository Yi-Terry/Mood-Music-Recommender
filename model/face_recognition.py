import json
import os
import numpy as np
import logging
from deepface import DeepFace

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #suppresses tensorFlow logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def convert_numpy(obj):
    if isinstance(obj, np.generic):   
        return obj.item()
    elif isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy(v) for v in obj]
    else:
        return obj

def analyze_image(image_path, save_json=True, output_folder='test_data'):
    try:
        logging.info(f'starting analysis for image{image_path}')

        result = DeepFace.analyze(image_path, actions=['emotion'])
        logging.info("DeepFace analysis completed successfully.")

        clean_results = convert_numpy(result)
        if isinstance(clean_results, list):
            clean_results_index = clean_results[0]
        mood = clean_results_index.get('dominant_emotion', 'unknown')
        logging.info(f"Dominant emotion detected: {mood}")

        output_path = None
        if save_json:
            os.makedirs(output_folder, exist_ok=True)
            filename = os.path.basename(image_path)
            output_path = os.path.join(output_folder, f"{filename}_result.json")

            try:
                with open(output_path, "w") as f:
                    json.dump(clean_results, f, indent=4)
                logging.info(f'results saved to json:{output_path}')
            except Exception as e:
                logging.info(f'failed to save results to json: {e}')
                output_path = None
        return mood, clean_results, output_path
    except Exception as e:
        logging.error(f'error analyzing image {image_path}: {e}')
        return 'error',{}, None

def main():

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_image = os.path.join(BASE_DIR, "images", "headShot.jpg")
    
    if not os.path.exists(test_image):
        logging.error(f"Test image not found at: {test_image}")
        return

    mood, results, saved_path = analyze_image(test_image, save_json=True)
    
    logging.info(f"Test Complete! Dominant Mood: {mood}")
    logging.info(f"Full Results: {results}")
    if saved_path:
        logging.info(f"Results saved at: {saved_path}")

# Run main if script executed directly
if __name__ == "__main__":
    main()