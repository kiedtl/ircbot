import dataclasses
import socket
import ssl
import urllib.parse

import utils

MAX_REDIRECT = 16
MAX_TITLE_WIDTH = 60
DEF_PORT = 1965

RESPONSES = {
    10: lambda m: f"(Input: {m})",
    11: lambda m: f"(Sensitive input: {m})",
    30: lambda m: f"(Redirect to {m})",
    31: lambda m: f"(Permanent redirect to {m})",
    40: lambda m: f"(Temporary failure: {m})",
    41: lambda _: f"(Server unavailable)",
    42: lambda _: f"(CGI error)",
    43: lambda _: f"(Proxy error)",
    44: lambda _: f"(Rate limited)",
    50: lambda m: f"(Permanent failure: {m})",
    51: lambda _: f"(Area 51: Not found)",
    52: lambda _: f"(Resource gone)",
    53: lambda _: f"(Proxy request refused)",
    59: lambda _: f"(Malformed request)",
    60: lambda m: f"(Need client certificate)",
    61: lambda _: f"(Unauthorised client certificate)",
    62: lambda _: f"(Invalid client certificate)",
}

sslctx = ssl.create_default_context()
gemtext = utils.enum(
    TEXT=0, HEADER1=1, HEADER2=2, HEADER3=3, LINK=4, QUOTE=5, LIST=6, PREFORMAT=7
)


@dataclasses.dataclass
class GeminiDoc:
    doctype: int  # status code "family". e.g. 3, 2, 1
    status: int  # exact status code. e.g. 31, 20, 11
    meta: str  # text that comes after the status code.
    body: list  # the document body. comment unneeded.


# Enable TOFU, which Gemini needs. Stupid, right?
sslctx.check_hostname = False
sslctx.verify_mode = ssl.CERT_NONE

# monkey-patch Gemini support in urllib.parse
# stolen from the av98 source code
urllib.parse.uses_relative.append("gemini")
urllib.parse.uses_netloc.append("gemini")


def query(url):
    if not "://" in url:
        url = "gemini://" + url
    parsed = urllib.parse.urlparse(url)

    if parsed.scheme != "gemini":
        raise Exception("Unsupported URL scheme")

    host = parsed.hostname
    port = parsed.port or DEF_PORT
    r_buffer = ""

    with socket.create_connection((host, port)) as sock:
        with sslctx.wrap_socket(sock, server_hostname=host) as ssock:
            ssock.write((url + "\r\n").encode("utf-8"))

            while True:
                data = ssock.read()
                if len(data) == 0:
                    break
                else:
                    r_buffer += data.decode("utf-8")

    return r_buffer


def parse(rawdata):
    first = (rawdata.split("\n", 1)[0]).strip("\r")
    data = rawdata.split("\n", 1)[1]
    status = int(first.split(" ", 1)[0])
    dtype = int(str(status)[-2])
    meta = (first.split(" ", 1)[1]).strip("\r")
    parsed = []

    preformat = False

    for line in data.split("\n"):
        if line.startswith("```"):
            preformat = not preformat
            continue

        # Special case
        if preformat:
            parsed.append([gemtext.PREFORMAT, line])
            continue

        if line.startswith("#"):
            parsed.append([gemtext.HEADER1, line[1:].strip()])
        elif line.startswith("##"):
            parsed.append([gemtext.HEADER2, line[2:].strip()])
        elif line.startswith("###"):
            parsed.append([gemtext.HEADER3, line[3:].strip()])
        elif line.startswith("=>"):
            # FIXME: won't split on tabs
            # FIXME: trim spaces from description
            parsed.append([gemtext.LINK, line[2:].strip().split(" ", 1)])
        elif line.startswith(">"):
            parsed.append([gemtext.QUOTE, line[1:].strip()])
        elif line.startswith("*"):
            parsed.append([gemtext.LIST, line[1:].strip()])
        else:
            parsed.append([gemtext.TEXT, line])

    return GeminiDoc(dtype, status, meta, parsed)


def title(doc: GeminiDoc, follow_redirect=True, redirects=[]):
    # when searching for the title in text, grab the
    # first element which is a header. if no title is found,
    # try again, but search for header2's. and so on and
    # so on.
    attempts = [gemtext.HEADER1, gemtext.HEADER2, gemtext.HEADER3, gemtext.TEXT]

    if doc.doctype == 2:
        for attempt in attempts:
            for line in doc.body:
                if line[0] != attempt:
                    continue

                text = line[1].strip()
                if len(text) == 0:
                    continue

                if len(text) > MAX_TITLE_WIDTH:
                    text = text[: MAX_TITLE_WIDTH - 3]
                    text = text.strip() + "..."

                return text

        return "(Couldn't find title)"
    elif doc.doctype == 3 and follow_redirect:
        if len(redirects) >= MAX_REDIRECT:
            return "(Too many redirects)"

        redirects.append(doc.meta)
        return title(
            parse(query(doc.meta)), follow_redirect=follow_redirect, redirects=redirects
        )
    else:
        if doc.status in strings:
            return (strings[doc.status])(doc.meta)
        else:
            return "(Unknown reply: {doc.status}: {doc.meta})"
