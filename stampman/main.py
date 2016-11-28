import logging

from flask import request
from flask_api import FlaskAPI
from stampman.services import pool

app = FlaskAPI(__name__)

_pooled_service = pool.PooledService()


@app.route("/", methods=['GET', 'POST'])
def list_pool_domains():
    pools = _pooled_service.pools
    if request.method == 'GET':
        return [pool_representation(servicepool) for servicepool in pools]
    elif request.method == 'POST':
        api_key = request.data.get("admin_api_key")
        for admin in _pooled_service.admins:
            if api_key == admin.api_key:
                return [pool_representation(servicepool, is_admin=True)
                        for servicepool in pools]
        return [pool_representation(servicepool) for servicepool in pools]
    else:
        logging.error("Unsupported request made on list_pool_domain by".format(
            request.remote_addr))


@app.route("/<domain>/", methods=['GET', 'POST'])
def detail_pool_domain(domain):
    return domain


@app.route("/<domain>/send/", methods=['GET', 'POST'])
def send_pooled_email(domain):
    return domain


def pool_representation(service_pool, is_admin: bool = False):
    result = {"domain": service_pool.domain,
              "url": request.host_url + service_pool.domain}
    if is_admin:
        result["services"] = list(map(lambda x: {
            "name": x.name,
            "api_key": x.api_key,
            "priority": x.priority
        }, service_pool.services))
    else:
        result["services"] = list(map(lambda x: {
            "name": x.name,
            "priority": x.priority
        }, service_pool.services))
    result["url_send_email"] = "{}{}/send".format(request.host_url,
                                                  service_pool.domain)
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
