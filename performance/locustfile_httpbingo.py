#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-26 22:13
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : locustfile_httpbingo.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : Locust性能测试代码练习


from locust import HttpUser, task, between, events
import random
import json
import time

class HttpbinPerformanceUser(HttpUser):
    # 模拟用户思考时间：普通操作间隔0.5~2秒，贴合真实用户行为
    wait_time = between(0.5, 2)
    host = "http://httpbingo.org"

    def on_start(self):
        """每个虚拟用户启动时执行1次，初始化全局配置（模拟登录态、通用请求头）"""
        self.common_headers = {
            "Content-Type": "application/json",
            "User-Agent": "Locust-Performance-Test/1.0"
        }
        # 模拟鉴权Token，对应真实项目的登录态
        self.auth_token = "Bearer test-perf-token-2026"

    # ===================== 核心压测场景（按用户行为占比分配权重） =====================
    @task(5)
    def basic_get_with_param(self):
        """权重5：高频基础查询，模拟用户最常做的浏览操作"""
        # 动态参数化：随机生成查询参数，避免缓存命中，模拟真实用户不同请求
        params = {
            "user_id": random.randint(1000, 9999),
            "page": random.randint(1, 20),
            "page_size": random.choice([10, 20, 50])
        }

        # catch_response=True：开启手动断言，自主标记请求成功/失败
        with self.client.get(
            "/get",
            params=params,
            headers=self.common_headers,
            name="基础GET查询",  # name聚合同类请求，避免参数不同导致统计分散
            catch_response=True
        ) as resp:
            # 断言1：状态码校验
            if resp.status_code != 200:
                resp.failure(f"状态码异常：{resp.status_code}")
                return

            # 断言2：业务数据校验，验证返回结果与请求参数一致
            # print(f"Response JSON: {resp.json()}")
            try:
                resp_data = resp.json()
                if resp_data["args"]["user_id"][0] == str(params["user_id"]):
                    resp.success()
                else:
                    resp.failure("返回数据与请求参数不匹配")
            except json.JSONDecodeError:
                resp.failure("响应非合法JSON格式")

    @task(3)
    def post_data_submit(self):
        """权重3：数据提交场景，模拟用户下单、填写表单等写操作"""
        # 动态生成请求体，参数化提交数据
        post_body = {
            "username": f"test_user_{random.randint(100, 999)}",
            "email": f"user{random.randint(100, 999)}@test.com",
            "age": random.randint(18, 60)
        }

        with self.client.post(
            "/post",
            json=post_body,
            headers={**self.common_headers, "Authorization": self.auth_token},
            name="POST数据提交",
            catch_response=True
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"提交失败，状态码：{resp.status_code}")
                return

            try:
                resp_json = resp.json()
                # 校验提交的数据被服务端正确接收
                if resp_json["json"]["username"] == post_body["username"]:
                    resp.success()
                else:
                    resp.failure("提交数据回显不一致")
            except Exception as e:
                resp.failure(f"响应解析失败：{str(e)}")

    @task(1)
    def slow_interface_scenario(self):
        """权重1：慢接口场景，模拟高耗时请求，验证系统超时处理能力"""
        delay = random.choice([0.5, 1, 2])  # 随机模拟不同耗时的接口
        with self.client.get(
            f"/delay/{delay}",
            headers=self.common_headers,
            name=f"慢接口_延迟{delay}s",
            catch_response=True,
            timeout=5  # 单请求超时阈值5秒，超过自动标记失败
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"慢接口异常，状态码：{resp.status_code}")

    @task(1)
    def error_status_injection(self):
        """权重1：异常状态码注入，模拟服务端错误场景，统计系统容错率"""
        expect_code = random.choice([400, 401, 403, 404, 500, 503])
        # 预期内的错误码标记为成功，避免误统计为压测失败
        with self.client.get(
            f"/status/{expect_code}",
            headers=self.common_headers,
            name=f"异常状态码_{expect_code}",
            catch_response=True
        ) as resp:
            if resp.status_code == expect_code:
                resp.success()
            else:
                resp.failure(f"状态码不符，预期{expect_code}，实际{resp.status_code}")

    # ===================== 事务统计：全链路业务流程 =====================
    @task(2)
    def complete_business_flow(self):
        """完整业务事务：查询→提交，统计整条链路的总耗时"""
        transaction_name = "查询-提交完整事务"
        start_time = time.time()

        # 步骤1：查询数据
        with self.client.get(
                "/get?from=flow_step1",
                name="事务_步骤1_查询",
                catch_response=True
        ) as step1:
            if step1.status_code != 200:
                self._report_transaction(transaction_name, start_time, "步骤1查询失败")
                step1.failure("事务步骤1失败")
                return

        # 步步骤2：提交数据
        with self.client.post(
                "/post",
                json={"flow": "step2", "data": "test"},
                name="事务_步骤2_提交",
                catch_response=True
        ) as step2:  # # 上报整条事务的总耗时
            if step2.status_code == 200:
                self._report_transaction(transaction_name, start_time, None)
                step2.success()
            else:
                self._report_transaction(transaction_name, start_time, "步骤2提交失败")
                step2.failure("事务步骤2失败")

    def _report_transaction(self, name, start, exception):
        """手动上报事务统计，在Locust控制台独立展示事务指标"""
        total_ms = (time.time() - start) * 1000
        events.request.fire(
            request_type="TRANSACTION",
            name=name,
            response_time=total_ms,
            response_length=0,
            exception=exception
        )
