import asyncio
import aiohttp

from .constants import REQUEST_UPLOAD_URL, AUTH_HEADERS


async def upload_files_to_yadisk(files):
    if not files:
        return []

    async with aiohttp.ClientSession(headers=AUTH_HEADERS) as session:
        tasks = [
            asyncio.ensure_future(upload_file_and_get_url(session, file))
            for file in files
        ]
        results = await asyncio.gather(*tasks)
    return results


async def upload_file_and_get_url(session, file):
    filename = file.filename
    file_path = f'/{filename}'

    async with session.get(
        REQUEST_UPLOAD_URL,
        params={'path': file_path, 'overwrite': 'true'}
    ) as response:
        data = await response.json()
        upload_url = data.get('href')

    content = file.read()
    async with session.put(upload_url, data=content) as response:
        await response.release()

    download_api_url = REQUEST_UPLOAD_URL.replace('/upload', '/download')

    async with session.get(
        download_api_url,
        params={'path': file_path}
    ) as response:
        data = await response.json()
        final_link = data.get('href')

    return {'filename': filename, 'url': final_link}
