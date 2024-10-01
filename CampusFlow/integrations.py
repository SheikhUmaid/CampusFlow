import os
from google.cloud import vision


os.environ["GOOGLE_CLOUD_PROJECT"] = "your-project-id"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "CampusFlow/credentials/campus-flow-31415-a053d7c1460a.json"


def safe_search_detection(image_path):
    # Initialize the Vision API client
    client = vision.ImageAnnotatorClient()

    # Load the image from the local file system
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    # Perform SafeSearch detection
    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    # Print the results
    
    print('SafeSearch results:')
    print(f'Adult: {safe.adult}')
    print(f'Spoof: {safe.spoof}')
    print(f'Medical: {safe.medical}')
    print(f'Violence: {safe.violence}')
    print(f'Racy: {safe.racy}')

    if response.error.message:
        raise Exception(f'{response.error.message}')
    return safe
if __name__ == '__main__':
    image_path = 'noblur2.jpeg'  # Replace with your image path
    safe_search_detection(image_path)