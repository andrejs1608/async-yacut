import asyncio
import aiohttp
from .constants import (
    REQUEST_UPLOAD_URL, UPLOAD_PATH, AUTH_HEADERS,
    API_RESOURCES_URL, PUBLISH_URL
)


async def upload_files_to_yadisk(files):
    if files:
        async with aiohttp.ClientSession() as session:
            tasks = [
                asyncio.ensure_future(upload_file_and_get_url(session, file))
                for file in files
            ]
            results = await asyncio.gather(*tasks)
            await asyncio.sleep(0.25)
        return results
    return []


async def upload_file_and_get_url(session, file):
    file_path = UPLOAD_PATH.format(file.filename)

    async with session.get(
        REQUEST_UPLOAD_URL,
        headers=AUTH_HEADERS,
        params={'path': file_path, 'overwrite': 'true'}
    ) as response:
        data = await response.json()
        if 'href' not in data:
            error_msg = data.get('message', 'Unknown Error')
            raise Exception(
                f"Ошибка получения ссылки для загрузки: {error_msg}"
            )
        upload_url = data['href']

    content = file.read()
    async with session.put(upload_url, data=content) as response:
        if response.status not in (201, 202):
            raise Exception(f"Ошибка при загрузке файла: {response.status}")

    async with session.put(
        PUBLISH_URL,
        headers=AUTH_HEADERS,
        params={'path': file_path}
    ) as response:
        if response.status not in (200, 201):
            data = await response.json()
            print(f"Ошибка публикации: {data.get('message')}")

    async with session.get(
        API_RESOURCES_URL,
        headers=AUTH_HEADERS,
        params={'path': file_path}
    ) as response:
        data = await response.json()
        public_url = data.get('public_url')

        if not public_url:
            raise Exception("Не удалось получить публичную ссылку на файл")

    return {'filename': file.filename, 'url': public_url}
