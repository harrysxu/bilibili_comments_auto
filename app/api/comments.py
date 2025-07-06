"""
评论相关API路由
"""
from fastapi import APIRouter, HTTPException
from app.models import ReplyCommentRequest, UnrepliedCommentsResponse, ReplyResponse
from app.bilibili.service import get_unreplied_comments, reply_to_comment

router = APIRouter()


@router.post("/unreplied", response_model=UnrepliedCommentsResponse)
async def get_unreplied_comments_endpoint():
    """
    获取未回复的评论
    """
    try:
        return await get_unreplied_comments()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reply", response_model=ReplyResponse)
async def reply_comment_endpoint(request: ReplyCommentRequest):
    """
    回复评论
    """
    try:
        print(f"收到回复请求 - OID: {request.oid}, RPID: {request.rpid}, ROOT: {request.root}, 消息: {request.message}")
        return await reply_to_comment(request.oid, request.rpid, request.message, request.root)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 