# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

from src.tools.video_builder import VideoBuilder
import traceback
import click
import logging
from src.crawl import CrawlFactory
from src.logs import config_logging
from src.pub.bilib import BiliB
from src.config import configs
from src.pub.stream_live import StreamLive

logger = logging.getLogger(__name__)


@click.group()
def entrance():
    pass


@entrance.command()
@click.option('--website', type=click.Choice(["weibo", "huaban", "gaoxiaogif"], case_sensitive=False),
              default="weibo", help="which website to crawl")
@click.option("--output", default="./output", help="the path of media output ")
@click.option("--count", default=30, help="number of video crawl")
def download(**kwargs):
    configs.update(kwargs)
    factory = CrawlFactory(configs).crawl()
    if not factory.crawl():
        logger.error("crawl [{}] failure".format(factory.name))
        return False
    return True


@entrance.command()
@click.option("--target", type=click.Choice(["bili", "weibo"], case_sensitive=False), default="bili",
              help="which website to upload")
@click.option("--output", default="./output", help="the path of media output ")
@click.option("--copy", type=click.BOOL, default=False, help="copy from other website or not")
@click.option("--classify", default="生活", help="classify of video")
@click.option("--sub-classify", default="搞笑", help="subset classify of video")
def upload(**kwargs) -> bool:
    configs.update(kwargs)
    bili = BiliB(configs)
    bili.pub()
    return True


@entrance.command()
@click.option("--source", default=None, help="the images directory")
@click.option("--bgm", default=None, help="the video background music")
@click.option("--framerate", default=0.5, help="the framerate of video to generate")
@click.option("--output", default="output.mp4", help="video name for generate")
def vpkg(**kwargs):
    configs.update(kwargs)
    video_builder = VideoBuilder(configs)
    try:
        result = video_builder.built()
        logger.info("video build status: {}".format(result))
    except Exception as e:
        logger.error("video builder failure, err: {}".format("".join(traceback.extract_stack())))
    finally:
        logger.info("video build completed")


@entrance.command()
@click.option("--url",
              default="rtmp://live-push.bilivideo.com/live-bvc/?streamname=live_505797972_44307093&key" +
                      "=69f49942956030afd257668fee1f5497&schedule=rtmp",
              help="upstream address")
@click.option("--source", default=None, help="local video file")
@click.option("--db", default="live.db", help="database of live")
@click.option("--daemon", default=True, type=click.BOOL, help="run forever or not")
def live(**kwargs):
    stream_live = StreamLive(kwargs)
    stream_live.live()


def launch():
    config_logging()
    click.CommandCollection(sources=[entrance])()


if __name__ == '__main__':
    launch()
