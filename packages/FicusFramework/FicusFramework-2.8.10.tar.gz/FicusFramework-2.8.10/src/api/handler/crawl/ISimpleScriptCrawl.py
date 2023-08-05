from abc import abstractmethod

from api.handler.script.ICacheAbleScript import ICacheAbleScript
from api.handler.script.IKillableScript import IKillableScript
from api.handler.ILogAbleHandler import ILogAbleHandler


class ISimpleScriptCrawl(IKillableScript, ILogAbleHandler, ICacheAbleScript):
    """
    Python脚本式的Crawl的基类
    """

    @abstractmethod
    def do_crawl(self, params: dict):
        """
        抓取的业务逻辑
        :return: 返回一个 OutputWrapper的 数组
        """
        pass
