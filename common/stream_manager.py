# -*- coding: utf-8 -*-
"""
Created by susy at 2021/5/11
"""
from common.resources import timer_r
from common import constant
import common
import time
from common.redis_producer import RedisProducer
logger = common.get_default_logger()


class Manager(object):

    def __init__(self, qname):
        self.is_master = True
        self.qname = qname
        self.ps = timer_r.pubsub(ignore_subscribe_messages=False)
        self.ps_thread = None

        self.worker_task_qname = "worker_tasks"
        self.task_producer = RedisProducer(self.worker_task_qname, max_len=200000)

    def get_queue(self):
        return self.task_producer

    def check_next_group_tasks(self):
        # logger.debug("check_next_group_tasks in..")

        def filter_fn(item_id, last_item_id):
            logger.debug("filter item id:{}, last item id:{}".format(item_id, last_item_id))
            return False

        def need_wait(item_id, start_at, item):
            now_timestamp = common.to_num(time.time() * 1000)
            timer_r.set("check_next_group_tasks", start_at, px=start_at - now_timestamp + 1)

        def do_item(item_id, item_obj_dict):
            logger.debug("will push task:{}".format(item_obj_dict))
            return True

        def progress(seg_cnt, seg_total, offset, total):
            logger.debug('progress, seg c:{},seg t:{},seg r:{};offset:{},t:{}, t r:{}'.format(
                seg_cnt, seg_total, float(seg_cnt)/seg_total, offset, total, float(offset + seg_total)/total
            ))

        def complete(size, offset, total):
            logger.debug('complete, size:{},offset:{},t:{}, t r:{}'.format(
                size, offset, total, float(offset + size) / total
            ))
            timer_r.set("start_sync_worker", common.get_now_ts(), px=5)

        self.task_producer.check_pool_item(filter_fn, need_wait, do_item, progress, complete)

    def expired_call_back(self, data):
        if data:
            try:
                cmd = common.to_str(data.get("data"))
                if self.is_master:
                    if cmd.startswith("check_next_group_tasks"):
                        self.check_next_group_tasks()

                if "heartbeat" == cmd:
                    if self.is_master:
                        timer_r.set("heartbeat", common.get_now_ts(), ex=constant.HEARTBEAT_DELAY)

                        self.check_next_group_tasks()

            except Exception:
                logger.error("expired_call_back failed!", exc_info=True)

    def setup_expired_listener(self):
        timer_r.set("heartbeat", common.get_now_ts(), ex=constant.HEARTBEAT_DELAY)
        # pxv, dt_str = self.next_5minute_delay_timestamp()
        # pxv, dt_str = self.next_day_delay_timestamp()
        # timer_r.set("scan_store", pxv, px=pxv)
        self.ps.psubscribe(**{"__keyevent@{}__:expired".format(timer_r._db_index): self.expired_call_back})

    def start(self):
        # self.check_manager_state(0)
        self.setup_expired_listener()
        self.ps_thread = self.ps.run_in_thread(sleep_time=1)
        self.ps_thread.run()
        # self.build_consumers_group()
        self.task_producer.start()
        logger.debug("manager start ok!")

    def shutdown(self):
        # if self.consumers:
        #     for c in self.consumers:
        #         c.shutdown()
        logger.debug("manager will shutdown...")
        expired_key = "__keyevent@{}__:expired".format(timer_r._db_index)
        if self.ps_thread:
            self.ps_thread.stop()
            self.ps.unsubscribe(expired_key)
        logger.debug("manager shutdown ok!")

