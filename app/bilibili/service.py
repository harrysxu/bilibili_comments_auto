"""
Bilibili API 服务 - 处理与B站相关的所有业务逻辑
"""
import logging
from bilibili_api import creative_center, comment, Credential
from app.config import BILIBILI_SESSDATA, BILIBILI_BILI_JCT, BILIBILI_MID
from app.models import CommentInfo, UnrepliedCommentsResponse, ReplyResponse

logger = logging.getLogger(__name__)

def analyze_comments(result, mid):
    """
    分析评论数据，找出没有回复的评论
    """
    comments_list = result.get('list', [])
    
    # 存储所有评论信息
    all_comments = []
    replies = []  # 我的回复
    
    for comment in comments_list:
        comment_info = {
            'rpid': comment.get('rpid'),
            'mid': str(comment.get('mid')),
            'oid': comment.get('oid'),
            'root': comment.get('root'),
            'parent': comment.get('parent'),
            'content': comment.get('content', {}).get('message', ''),
            'title': comment.get('title', ''),  # 直接从评论对象获取标题
            'uname': comment.get('member', {}).get('uname', ''),
            "bvid": comment.get('bvid', '')
        }
        all_comments.append(comment_info)
        
        # 如果是我的评论，加入回复列表
        if str(comment.get('mid')) == mid:
            replies.append({
                'root': comment.get('root'),
                'parent': comment.get('parent')
            })
    
    # 找出没有回复的评论
    unreplied_comments = []
    for comment in all_comments:
        # 跳过我自己的评论
        if comment['mid'] == mid:
            continue
            
        # 检查是否已经回复过
        has_reply = False
        for reply in replies:
            # 如果回复的 root 是该评论的 rpid，或者 parent 是该评论的 rpid
            if reply['root'] == comment['rpid'] or reply['parent'] == comment['rpid']:
                has_reply = True
                break
        
        if not has_reply:
            unreplied_comments.append(comment)
    print(f"未回复的评论: {unreplied_comments}")
    return unreplied_comments


async def get_unreplied_comments() -> UnrepliedCommentsResponse:
    """获取未回复的评论"""
    try:
        """获取B站认证凭据"""
        credential=Credential(
            sessdata=BILIBILI_SESSDATA,
            bili_jct=BILIBILI_BILI_JCT
        )
        # 获取创作中心评论
        result = await creative_center.get_comments(credential=credential, order=creative_center.CommentManagerOrder.RECENTLY, ps=20)        

        # 检查返回数据是否有效
        if not isinstance(result, dict) or 'list' not in result:
            raise Exception(f"API返回数据格式不正确: {result}")
        
        # 分析评论数据 - 直接使用返回的数据
        unreplied_comments = analyze_comments(result, BILIBILI_MID)
        
        # 转换为 CommentInfo 对象
        comment_infos = [CommentInfo(**comment) for comment in unreplied_comments]
        
        return UnrepliedCommentsResponse(
            result=comment_infos,
            count=len(comment_infos)
        )
        
    except Exception as e:
        logger.error(f"获取未回复评论时发生错误: {str(e)}")
        raise e


async def reply_to_comment(oid: int, rpid: int, message: str, root: int) -> ReplyResponse:
    """回复评论"""
    try:
        credential = credential=Credential(
            sessdata=BILIBILI_SESSDATA,
            bili_jct=BILIBILI_BILI_JCT
        )
        
        # 发送回复
        reply_result = await comment.send_comment(
            text=message,
            oid=oid,
            type_=comment.CommentResourceType.VIDEO,
            root=root,
            parent=rpid,
            credential=credential
        )
        logger.info(f"成功回复评论 {rpid}: {message}, {reply_result}")
        return ReplyResponse(
            success=True,
            message="回复成功",
            rpid=reply_result.get('data', {}).get('rpid')
        )
            
    except Exception as e:
        error_msg = f"回复评论时发生错误: {str(e)}"
        logger.error(error_msg)
        return ReplyResponse(
            success=False,
            message=error_msg
        ) 