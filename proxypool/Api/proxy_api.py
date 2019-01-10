#coding:utf-8

"""
----------------------------------------
    description:
    author:sss
    date:
----------------------------------------
    change:
    
----------------------------------------
"""
__author__ = 'my'



from flask import Flask, request, Response
from flask import render_template, jsonify
from proxypool.Util.loggerhandler import LogHandler
from re import fullmatch


from proxypool.Util.getconfig import config
from proxypool.Manager.crawler_manage import CrawlerManager


# 自定义返回类
class MyResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, (list, dict)):
            response = jsonify(response)
        return super(Response, cls).force_type(response, environ)


app = Flask(__name__)
# 指定Response的格式化类
app.response_class = MyResponse
# 引用应用核心管理类
CRAWLER_DATA = CrawlerManager()


api_list = {
    'get': u'get an usable proxy',
    'delete?proxy=<ip>:<port>': u'delete an unable proxy',
    'status': u'proxy statistics'
}


@app.route('/')
def index():
    return render_template('index.html', tips=api_list)


@app.route('/get/')
def get():
    proxy = CRAWLER_DATA.get_proxy(0)
    #return Response(json.dumps(proxy), mimetype='application/json') if proxy else 'no proxy!'
    return proxy if proxy else 'no proxy!'


@app.route('/delete/', methods=['GET'])
def delete():
    proxy = request.args.get('proxy')
    if fullmatch('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', proxy):
        res = CRAWLER_DATA.delete(proxy)
        return res
    else:
        return '代理格式错误!'


@app.route('/status/')
def get_status():
    raw_nums, useful_nums = CrawlerManager().get_status()
    return 'raw proxy has {}, useful proxy has {}.'.format(raw_nums, useful_nums)


def run():
    logger = LogHandler('API')
    logger.info('API server init...')
    app.run(host=config.host_ip, port=config.host_port)


if __name__ == '__main__':
    run()
