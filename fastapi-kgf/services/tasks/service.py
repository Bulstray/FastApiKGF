from sqlalchemy.ext.asyncio import AsyncSession

from storage.db import crud_tasks

from aiopath import AsyncPath


class TasksService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_task_by_id(self, task_id: int):
        result = await crud_tasks.get_task_by_id(
            session=self.session,
            task_id=task_id,
        )

        return result

    async def delete_files_for_db(self, task_id: int):
        task = await self.get_task_by_id(task_id=task_id)

        for file_in_chat in task.chat_messages:
            if file_in_chat.file:
                file = AsyncPath(file_in_chat.file.folder_path)
                await file.unlink()
