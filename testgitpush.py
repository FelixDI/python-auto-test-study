#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-09 16:40
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : testgitpush.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : git push, change dev env

# 踩坑折腾够呛，哈哈，给我传上去！！！

import sys; print(sys.executable); print(sys.version)

# 约定式提交（Conventional Commits）快速入门
#
# 格式就是：<type>: <简短描述>
#
# 前缀	含义	什么时候用
# feat:	新功能	新增一个脚本、一个模块
# fix:	修 Bug	修复了某个错误
# docs:	文档	只改了 README 或注释
# refactor:	重构	改代码结构，但功能不变
# test:	测试	新增或修改测试用例
# chore:	杂项	改配置、装依赖、环境切换

# 初学者经常写测试脚本、练手项目，建议新建项目时
# 默认不勾选 Create Git repository
# 只有在确定需要版本控制或推送到 GitHub 时，才手动：
# 创建 .gitignore
# 执行 VCS → Enable Version Control Integration → Git
# 按正常流程add commit首次提交、
# GitHub 上新建一个完全空白的仓库（不勾选 README、不勾选.gitignore、不勾选 License）
# 关联远程仓库 SSH 地址,push推送
# 这样既避免了不必要的 Git 初始化，又不会因为忘记 .gitignore 而踩坑。