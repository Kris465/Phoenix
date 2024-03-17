import os
import asyncio
import aiohttp
from dotenv import load_dotenv, find_dotenv, set_key
from loguru import logger


class Translator:
    def __init__(self) -> None:
        self.key = self.get_data("IAM_TOKEN")
        self.token_link = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
        self.tr_link = 'https://translate.api.cloud.yandex.net/translate/v2/translate'  # noqa E501

    async def get_key(self):
        load_dotenv(find_dotenv())
        OAuth_token = os.environ.get('AOuth_token')

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = '{"yandexPassportOauthToken":"OAuth_token"}'.replace(
                                                            'OAuth_token',
                                                            OAuth_token)

        async with aiohttp.ClientSession() as session:
            async with session.post(self.token_link,
                                    headers=headers,
                                    data=data) as response:
                json_response = await response.json()
                TOKEN = json_response['iamToken']
                set_key(".env", "IAM_TOKEN", TOKEN)
                self.key = TOKEN
                os.environ['IAM_TOKEN'] = TOKEN

    def get_data(self, name: str):
        load_dotenv(find_dotenv())
        return os.environ.get(name)

    async def translate(self, text, source_language):
        IAM_TOKEN = self.key
        result = await self.request_form(text, source_language, IAM_TOKEN)
        if result is None:
            logger.warning("New IAM_TOKEN is set or connection is lost")
            await self.get_key()
            IAM_TOKEN = self.key
            await asyncio.sleep(10)
            result = await self.request_form(text, source_language, IAM_TOKEN)
        return str(result)

    async def request_form(self, text, source_language, IAM_TOKEN):
        folder_id = self.get_data('folder_id')
        target_language = 'ru'
        texts = text

        body = {
            "sourceLanguageCode": source_language,
            "targetLanguageCode": target_language,
            "texts": texts,
            "folderId": folder_id,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {0}".format(IAM_TOKEN)
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.tr_link,
                                    json=body,
                                    headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    lst = data['translations']
                    translation = lst[0]
                    return translation['text']
                else:
                    return None
