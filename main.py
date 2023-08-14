import time
import picamera
import requests

# Configure the camera
camera = picamera.PiCamera()
camera.resolution = (640, 480)  # Adjust resolution as needed

try:
    while True:
        # Record video
        output_file = f'video_{time.time()}.h264'
        camera.start_recording(output_file)
        camera.wait_recording(5)  # Record for 5 seconds
        camera.stop_recording()

        # Upload the recorded video
        url = 'https://video.gratheon.com/graphql'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer YOUR_ACCESS_TOKEN'
        }
        query = '''
        mutation UploadVideo($file: Upload!, $boxId: ID!) {
            uploadGateVideo(file: $file, boxId: $boxId)
        }
        '''
        variables = {
            'file': (output_file, open(output_file, 'rb')),
            'boxId': '123'  # Replace with the actual box ID
        }
        data = {
            'query': query,
            'variables': variables
        }

        # Make GraphQL request
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            print("Video uploaded successfully")
            os.remove(output_file) 
        else:
            print("Error uploading video:", response.status_code)

except KeyboardInterrupt:
    print("Recording and uploading stopped by user")

finally:
    camera.close()
