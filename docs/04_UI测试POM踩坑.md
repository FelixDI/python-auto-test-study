```
Page Object ≠ Playwright Page 误区:页面跳转 = 必须创建新的页面对象，实际上Page Object 是业务对象；
Playwright Page（通常由 pytest-playwright 的 page Fixture 提供）才是真正的浏览器页面实例。
POM负责页面抽象：BasePage封装通用能力，各Page Object封装页面操作与断言；Fixture负责测试数据、公共资源和页面对象创建；
业务链路方法，一定会前往下一个页面的，返回下一页面对象（如 cart_page = products_page.go_to_cart()）实现状态传递与可维护性；
Component Object独立成文件并通过页面对象__init__组合注入，避免BasePage演变为God Class；
组件涉及页面跳转时采用局部延迟导入（Lazy Import）返回目标页面对象，避免循环导入。
四个页面测试文件 只需判断组件正确集成，测试五种用户在当前页面的功能验证。 
组件测试单独一个测试文件 ，功能只需要测一次即可，避免每个页面重复测试组件功能。
```