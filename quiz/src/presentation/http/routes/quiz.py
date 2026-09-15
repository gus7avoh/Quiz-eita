from fastapi import APIRouter
from presentation.http.schemas.quiz import (
    QuizCreatedResponse,
    QuizRequest,
    QuizQuestionsResponse,
    QuizQuestionsRequest,
    QuizAnswerResponse,
    QuizAnswerRequest,
    QuizDeleteListRequest,
    QuizDeleteResponse
)
from presentation.http.services.quiz import create_quiz as create_quiz_service
from presentation.http.services.quiz import get_quiz    as get_quiz_service
from presentation.http.services.quiz import answer_quiz as answer_quiz_service
from presentation.http.services.quiz import delete_quiz as delete_quiz_service

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


@router.post("/answer", response_model=QuizAnswerResponse|None)
async def answer_quiz(data: QuizAnswerRequest) -> QuizAnswerResponse|None:
    return await answer_quiz_service(
        quiz_uuid=data.uuid,
        enunciado=data.enunciado,
        resposta=data.resposta_usuario
    )


@router.delete("/delete", response_model=QuizDeleteResponse|None)
async def delete_quiz(data: QuizDeleteListRequest) -> QuizDeleteResponse|None:
    return await delete_quiz_service(list_uuid=data.list_uuid)