import hashlib
from pathlib import PosixPath

from aiogram.types import FSInputFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models import File


class FileService:
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def _hash_file(path: str) -> str:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h.hexdigest()

    async def get_file_by_path(self, path: str) -> File:
        file = (await self.session.execute(select(File).where(File.path == path))).scalar_one_or_none()
        return file

    async def create(self, path: str, file_id: str = None) -> File:
        file = File(
            path=path,
            file_id=file_id,
            hash=self._hash_file(path)
        )
        self.session.add(file)
        await self.session.flush()
        return file

    async def get_file_by_path_or_create(self, path: str, file_id: str = None) -> File:
        file = await self.get_file_by_path(path)
        if file is None:
            file = await self.create(path, file_id)
        if file.hash != self._hash_file(path):
            file = await self.update_file_id(file, None)
        return file

    async def update_file_id(self, file: File, new_file_id: str | None) -> File:
        file.file_id = new_file_id
        return file

    async def get_media(self, path: PosixPath, output_type: type = FSInputFile) -> tuple[type | str, File]:
        file = await self.get_file_by_path_or_create(str(path))
        if file.file_id is None:
            media = output_type(path, 'cool_muflon')
        else:
            media = file.file_id

        return media, file
