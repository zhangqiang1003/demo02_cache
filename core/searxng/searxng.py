# from urllib.parse import urlencode
#
# import aiohttp
#
# from core.constant import SEARXNG_INSTANCE
#
#
# async def async_search_searxng(query: str, engines=None, page=1) -> dict:
#     """异步方式调用SearxNG"""
#     if engines is None:
#         engines = ["google"]
#     params = {
#         "q": query,
#         "format": "json",
#         "engines": ",".join(engines),
#         "pageno": page
#     }
#
#     async with aiohttp.ClientSession() as session:
#         try:
#             async with session.get(
#                     f"{SEARXNG_INSTANCE}/search?{urlencode(params)}",
#                     headers={"User-Agent": "Mozilla/5.0"},
#                     timeout=aiohttp.ClientTimeout(total=60)
#             ) as response:
#                 response.raise_for_status()
#                 return await response.json()
#         except Exception as e:
#             print(f"异步搜索失败: {str(e)}")
#             return {"error": str(e)}


import asyncio
import json
import sys

import aiohttp
from urllib.parse import urlencode

from core.constant import SEARXNG_INSTANCE


async def safe_search(params: dict) -> dict:
    """修复后的安全搜索方法"""
    connector = aiohttp.TCPConnector(limit=10)  # 添加连接限制

    params["optimizationMode"] = "speed"
    params["focusMode"] = "webSearch"

    try:
        async with aiohttp.ClientSession(
                connector=connector,
                timeout=aiohttp.ClientTimeout(total=60),
                headers={"User-Agent": "Mozilla/5.0"}
        ) as session:

            async with session.post(
                    f"{SEARXNG_INSTANCE}/api/search",
                    json=params,
                    ssl=False  # 如果本地测试可禁用SSL验证
            ) as response:
                response.raise_for_status()
                return await response.json()

        # return {"msg": "this is a good search"}

    except aiohttp.ClientError as e:
        print(f"网络请求异常: {str(e)}")
    except asyncio.TimeoutError:
        print("请求超时")
    except Exception as e:
        print(f"未处理异常: {str(e)}")
    finally:
        await connector.close()  # 显式关闭连接器

    return {"error": "搜索失败"}


# 调用示例
async def main():
    # if engines is None:
    engines = ["google scholar"]
    params = {
        "query": "AI最新进展"
    }
    result = await safe_search(params)
    print(result)


if __name__ == "__main__":
    # 修复事件循环策略
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())