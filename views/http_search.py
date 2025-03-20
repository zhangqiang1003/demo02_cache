
from quart import Blueprint, request
from core import logger

from core.http.base_response import ok
from core.redis.decorators import cache_request
from core.searxng.searxng import safe_search

search_bp = Blueprint("search", __name__)


@search_bp.route("/api/search", methods=["POST"])
@cache_request(ttl=300)  # 使用装饰器
async def search():
    """
    query: 对话请求参数
    """
    body: dict = await request.get_json()

    results = await safe_search(body)

    if results.get("error"):
        logger.info(f"async_search_searxng error : {results}")
        return ok("")

    return ok(results)
