import logging
import os

from flask import request
from flask_api import FlaskAPI, status
from raven.contrib.flask import Sentry
from stampman.services import pool
from stampman.helpers import mail_

app = FlaskAPI(__name__)
sentry = Sentry(app, dsn=os.environ.get('SENTRY_API_DSN'))

_pooled_service = pool.PooledService()


@app.route("/", methods=['GET', 'POST'])
def list_pool_domains():
    """
    GET: List all pools associated with the service.

    POST: View further informaton when posted an "admin_api_key"
    """
    pools = _pooled_service.pools
    if request.method == 'GET':
        try:
            return [pool_representation(servicepool) for servicepool in pools]
        except Exception as e:
            logging.error(
                    "GET Request to '/' cannot be completed for {}: {}".format(
                            request.remote_addr, str(e)))
            return ({"error": "GET request to '/' failed"},
                    status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        try:
            api_key = request.data.get("admin_api_key")
            for admin in _pooled_service.admins:
                if api_key == admin.api_key:
                    return [pool_representation(servicepool, is_admin=True)
                            for servicepool in pools]
            return [pool_representation(servicepool) for servicepool in pools]
        except Exception as e:
            logging.error(
                    "POST to '/' cannot be completed for {}: {}".format(
                            request.remote_addr, str(e)))
            return ({"error": "POST request failed; Please check POST "
                              "data"}, status.HTTP_401_UNAUTHORIZED)
    else:
        logging.error("Unsupported request made on list_pool_domain by".format(
                request.remote_addr))
        return ({"error": "This endpoint only supports GET and POST requests"},
                status.HTTP_400_BAD_REQUEST)


@app.route("/<domain>/", methods=['GET', 'POST'])
def detail_pool_domain(domain):
    """
    GET: Detail a single pool associated with a mail domain

    POST: View further informaton when posted an "admin_api_key"
    """
    pools = _pooled_service.pools
    if domain not in _pooled_service.domains:
        logging.error("{} requested unknown domain {}".format(
                request.remote_addr, domain))
        return ({"error": "Unknown Domain '{}'".format(domain)},
                status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        try:
            return [pool_representation(servicepool, is_admin=False,
                                        list_urls=True) for servicepool in
                    pools]
        except Exception as e:
            logging.error(
                    "GET to '/{}' cannot be completed for {}: {}".format(
                            domain, request.remote_addr, str(e)))
            return ({"error": "GET request to '/{}' failed".format(domain)},
                    status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        try:
            api_key = request.data.get("admin_api_key")
            for admin in _pooled_service.admins:
                if api_key == admin.api_key:
                    return [pool_representation(servicepool, is_admin=True,
                                                list_urls=True) for servicepool
                            in
                            pools]
            return [
                pool_representation(servicepool, is_admin=False,
                                    list_urls=True)
                for servicepool in pools]
        except Exception as e:
            logging.error(
                    "POST to '/{}' cannot be completed for {}: {}".format(
                            domain, request.remote_addr, str(e)))
            return ({"error": "POST request failed; Please check POST data"},
                    status.HTTP_401_UNAUTHORIZED)
    else:
        logging.error("Unsupported request made on list_pool_domain by".format(
                request.remote_addr))
        return ({"error": "This endpoint only supports GET and POST requests"},
                status.HTTP_400_BAD_REQUEST)


@app.route("/<domain>/send/", methods=['GET', 'POST'])
def send_pooled_email(domain):
    """
    Send an email via the Stampman PooledEmailService on the domain associate
    with the pool.

    Parameters:

        - "pool_api_key" (required): API Key associated with a specific pool
        - "from_email" (required): E-mail address of the sender
        - "from_name" (required): Name of the sender
        - "recipients" (required): Recipients of the E-mail (Either a list
        of strings or a single string in case fo a single recipient)
        - "cc" (optional): CC Recipients of the E-mail (Either a list
        of strings or a single string in case fo a single recipient)
        - "bcc" (optional): BCC Recipients of the E-mail (Either a list
        of strings or a single string in case fo a single recipient)
        - "subject" (optional): Subject of the E-mail
        - "content" (optional): Body of the E-mail
        - "reply_to" (optional): Reply address for the E-mail

    Data must be JSON encoded.
    """
    if request.method == 'GET':
        return {"error": "Unexpected request; Expected POST."}
    if domain not in _pooled_service.domains:
        logging.error("{} requested unknown domain {}".format(
                request.remote_addr, domain))
        return {"error": "Unknown Domain '{}'".format(domain)}
    if request.method == 'POST' and request.data.get(
            "pool_api_key") in _pooled_service.service_map.keys():
        logging.info(
                "Attempting to send email from {}".format(request.remote_addr))
        try:
            sender_email = request.data['from_email']
            recipients = request.data['recipients']
            sender_name = request.data.get('from_name')
            sender_name = sender_name if sender_name else ""
            subject = request.data.get('subject')
            subject = subject if subject else ""
            content = request.data.get('content')
            content = content if content else ""
            cc = request.data.get('cc')
            cc = cc if cc else []
            bcc = request.data.get('bcc')
            bcc = bcc if bcc else []
            reply_to = request.data.get('reply_to')
            reply_to = reply_to if reply_to else sender_email
        except TypeError:
            return {"error": "Invalid Parameter Type"}
        except KeyError:
            return {"error": "Missing either from_email or recipients"}

        if not isinstance(recipients, list):
            recipients = [recipients]
        if not isinstance(cc, list):
            cc = [cc]
        if not isinstance(bcc, list):
            bcc = [bcc]

        response = _pooled_service.send_email(mail_.Email(sender=(
            sender_name, sender_email), recipients=recipients,
                subject=subject, content=content, cc=cc, bcc=bcc,
                reply_to=reply_to), request.data.get('pool_api_key'))
        if response["status"] == "failure":
            logging.error("Unable to send E-mail")
            return {"error": "Service temporarily unavailable"}
        else:
            logging.info(
                    "Email dispatched using {}".format(
                            response["service_used"]))
            return response
    else:
        logging.error("{} requested unauthorized access to domain {}".format(
                request.remote_addr, domain))
        return {"error": "Unauthorized Access: Please check your API key"}


def pool_representation(service_pool, is_admin: bool = False,
                        list_urls: bool = False):
    """
    Helper function for generating API docs.
    """
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

    if list_urls:
        result["url_send_email"] = "{}{}/send".format(request.host_url,
                                                      service_pool.domain)

    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
