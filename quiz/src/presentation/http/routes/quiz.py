from fastapi import APIRouter
from presentation.http.schemas.quiz import (
    QuizCreatedResponse,
    QuizRequest,
)
from presentation.http.services.quiz import create_quiz as create_quiz_service

router = APIRouter(
    prefix="/quiz",
    tags=["quiz"],
)

@router.post("/create", response_model=QuizCreatedResponse)
async def create_quiz(data: QuizRequest) -> QuizCreatedResponse:
    quiz_uuid = await create_quiz_service(
        tema=data.tema,
        quantidade=data.quantidade,
        dificuldade=data.dificuldade,
    )
    return QuizCreatedResponse(uuid=quiz_uuid)
