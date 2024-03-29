import requests


class OutpaintAPI:
    def __init__(self, image_data):
        self.url = 'https://niiab.navan.ai/sdxl/outpainting-langchain'
        self.image_data = image_data

    def outpend_image(self):
        files = {'file': self.image_data}
        response = requests.post(self.url, files=files)

        # Check the response
        if response.status_code == 200:
            print('Image sent successfully!')

            # Instead of saving, return the binary image data
            return response.content
        else:
            print('Error sending image:', response.status_code)
            return None
