from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status

from core.models import Program
from core.schemas import ProgramCreate, ProgramRead
from crud.program_exceptions import (
    ProgramFileNameAlreadyExistsError,
    ProgramNameAlreadyExistsError,
    ProgramNameDoesNotExistError,
)
from dependencies.providers import get_program_service
from services.programs.service import ProgramService

router = APIRouter(tags=["Programs"])


@router.get(
    "",
    response_model=list[ProgramRead],
    status_code=status.HTTP_200_OK,
)
def get_programs(
    program_service: Annotated[
        ProgramService,
        Depends(get_program_service),
    ],
) -> list[Program]:
    """Endpoint for getting a list of programs"""
    return program_service.get_all_programs()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
def add_program(
    program_service: Annotated[
        ProgramService,
        Depends(get_program_service),
    ],
    file: UploadFile,
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    author: Annotated[str, Form()],
) -> dict[str, str]:
    """Endpoint for creating programs"""
    program_data = ProgramCreate(
        name=name,
        description=description,
        author=author,
    )

    try:
        program = program_service.create_program(
            program_data,
            file,
        )
    except ProgramNameAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except ProgramFileNameAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e

    return {"message": f"Program {program.name} created successfully"}


@router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_program(
    program_service: Annotated[
        ProgramService,
        Depends(get_program_service),
    ],
    program_name: str,
) -> None:
    """Endpoint for deleting a program"""
    try:
        program_service.delete_program(program_name)
    except ProgramNameDoesNotExistError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
