import urllib.parse
from abc import ABC, abstractmethod
from typing import Optional, Type

from popupdict.config import *
from ..result import QueryResult


# Base class for query client
class AbstractQueryClient(ABC):
    # 客户端 ID，需唯一，用于区分客户端（配置文件、缓存等）
    id = 'abstract'
    # 配置类
    config_class = QueryClientConfiguration  # type: Type[QueryClientConfiguration]

    def __init__(self, config: QueryClientConfiguration):
        config.validate()
        self.config = config

    @abstractmethod
    def query(self, text: str) -> Optional[QueryResult]:
        pass

    # Escape URL path segment
    @staticmethod
    def escape_url_path(s: str):
        return urllib.parse.quote(s, safe='')
