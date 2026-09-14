from fastapi import APIRouter
from presentation.http.schemas.quiz import (
    QuizCreatedResponse,
    QuizRequest,
    QuizQuestionsResponse,
    QuizQuestionsRequest
)
from presentation.http.services.quiz import create_quiz as create_quiz_service
from presentation.http.services.quiz import get_quiz as get_quiz_service

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



@router.post("/question", response_model=QuizQuestionsResponse|None)
async def get_quiz(data: QuizQuestionsRequest) -> QuizQuestionsResponse|None:
    return await get_quiz_service(quiz_uuid=data.uuid)