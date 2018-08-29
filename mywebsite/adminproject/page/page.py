from math import ceil


class Page:
    # current_page_number当前分页的数
    current_page_number = ""
    # start_page分类limit查询start
    start_page = ""
    # end_page分类limit查询end
    end_page = ""
    # page_total分类所有记录数
    page_total = ""
    # page_size每页的页数
    page_size = ""
    # page_total_number总页数
    page_total_number = ""

    def __init__(self, model_object_list, page_size, show_template_page_number, current_page_number):
        """

        :param model_object_list:查询列表对象
        :param page_size: 每页的页数
        :param show_template_page_number:前端展示多少个页数
        :param current_page_number: 当前页数
        """
        self.page_size = int(page_size)
        self.object_list = model_object_list
        print(self.object_list,"#######")
        self.current_page_number = current_page_number
        self.show_template_page_number = show_template_page_number

    # get_count 获取所有记录的总条数
    def get_count(self):

        self.page_total = self.object_list.count()
        return self.page_total

    # select_limit_number 限制每页的条数的列表记录
    def select_limit_number(self):

        start_page, end_page = self.count_start_end_size()

        # Acticle.objects.all().filter(c_id=self.c_id)[start_page, end_page]
        Acticle_limit_list = self.object_list[start_page:end_page]
        print(Acticle_limit_list)
        return Acticle_limit_list

    # count_start_end_size
    def count_start_end_size(self):
        """

        :return: start_page 当前页数 end_page 结束页数
        """
        self.current_page_number = self.current_page_number

        self.start_page = (self.current_page_number-1)*self.page_size

        self.end_page = self.current_page_number*self.page_size

        return self.start_page, self.end_page

    # page_range 显示模板分页范围数
    def page_range(self, current_page_index=1):

        if self.num_pages() > self.show_template_page_number:

                return range(current_page_index, self.show_template_page_number+current_page_index)
        else:

                return range(1, self.num_pages()+1)

    # next_page 跳转下一页
    def next_page(self):
        if self.has_next():
            return self.current_page_number+1
        else:
            return 1

    # last_page 跳转上一页
    def last_page(self):
        if self.has_previous():
            return self.current_page_number-1
        else:
            return self.num_pages()

    # has_next 判断是否有下一页
    def has_next(self):
        return self.current_page_number < self.num_pages()

    # has_previoius 判断是否有上一页
    def has_previous(self):
        return self.current_page_number > 1

    # num_pages总页数
    def num_pages(self):
        hits = max(1, self.page_total)
        return int(ceil(hits / self.page_size))
