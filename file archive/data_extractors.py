from google import genai
from io import BytesIO
import json

class extractor:
    client = genai.Client()

    def analyse_shares(self, image):
        byte_io = BytesIO()
        image.save(byte_io, format='JPEG')
        image_bytes = byte_io.getvalue()

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[genai.types.Part.from_bytes(
                data=image_bytes,
                mime_type='image/png',
            ), "Output the data in this table in JSON format. Ignore rows that are cut off."
            "You can assume the columns are labelled as: "
            "Action, Amount, Leverage, Open, Current, Profit Loss and SL"]
        )

        return json.loads(response.text[7:-3])