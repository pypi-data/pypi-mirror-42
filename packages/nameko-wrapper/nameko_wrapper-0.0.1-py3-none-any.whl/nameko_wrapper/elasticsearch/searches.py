"""
Search Object Wrapper
"""
from .utils.formatters import SearchResultFormatter


class SearchBase(object):
    """Search Base Class"""

    def search(self):
        """原始搜索方法，返回原始搜索结果"""
        pass

    @property
    def result(self):
        raise NotImplementedError('Not implement `result` property method.')


class ESSearch(SearchBase):
    """ElasticSearch Search"""

    def __init__(self, search, schema=None, *args, page=None, many=False, raise_exception=True, **kwargs):
        """

        Args:
            search: ElasticSearch Search object instance
            schema: 用于格式化输出结果（marshmallow schema class)
            page: pagination info dict
                format:
                    {
                        'offset': int,
                        'size': int
                    }
            many: 控制返回结果是否为多个
            raise_exception: 当`many=False`，结果查询为空时是否触发异常
        """
        self._search = search
        self.schema = schema
        self.page = page
        self.many = many
        self._args = args
        self._kwargs = kwargs
        self.raise_exception = raise_exception

    def search(self):
        """执行搜索并返回原始搜索结果"""
        if self.page and 'offset' in self.page and 'size' in self.page:
            search = self._search[self.page['offset']:(self.page['offset'] + self.page['size'])]
            return {'result': search.execute(), 'total': search.count()}
        else:
            search = self._search
            return {'result': search.execute()}

    @property
    def result(self):
        """返回最终搜索结果列表"""

        # 根据不同的返回要求，控制搜索结果为空的时候是否引发异常
        # raise_exception = False if self.many else True

        return SearchResultFormatter(
            self.search(), schema=self.schema, many=self.many, raise_exception=self.raise_exception,
            *self._args, **self._kwargs
        ).data
