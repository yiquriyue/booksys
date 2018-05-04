# 路由表

|  图书列表   |   {{url_for('book_list')}}   |
| :-----: | :--------------------------: |
|   登陆    |     {{url_for('login')}}     |
|   注册    |   {{url_for('register')}}    |
|   主页    |   {{url_for('homepage')}}    |
|  购物车列表  |     {{url_for('cart')}}      |
|  收藏夹列表  |    {{url_for('collect')}}    |
|  图书入库   |   {{url_for('book_add')}}    |
|  图书详情   |  {{url_for('book_detail')}}  |
| 图书添加收藏夹 | {{url_for('book_collect')}}  |
| 图书添加购物车 |   {{url_for('book_cart')}}   |
|   退出    |    {{url_for('logout')}}     |
|  活动列表   | {{url_for('activity_list')}} |
|   订单    |                              |
|         |                              |
|         |                              |
|         |                              |
|         |                              |
|         |                              |
|         |                              |
|         |                              |

# 订单状态



- obligation 待付款（提交订单的默认状态）

- success 成功（在管理端确认后）

- failed 失败 （订单失效）


提交订单返回信息：

[{'book_num': 1, 'book_id': 2}, {'book_num': 1, 'book_id': 8}]



# 任务清单

- [ ] 用户所有功能整合
- [ ] 订单状态修改
- [x] 用户界面订单列表：所有订单展示，订单明细展示
- [ ] 销量最高商品排序
- [ ] 收藏最多商品排序
- [ ] 最新上架商品
- [ ] 活动列表，参与人员列表
- [ ] 图书评价
- [ ] 积分制度添加
- [x] 用户主页：用户信息展示，用户信息修改