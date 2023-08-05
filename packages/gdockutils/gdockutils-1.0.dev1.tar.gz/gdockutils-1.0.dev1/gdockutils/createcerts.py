import time
import os

from .utils import run


def createcerts(names, ips, outputdir):
    ips = ips or []
    cn = names[0]
    spec = ["DNS:%s" % n for n in names]
    spec += ["IP:%s" % i for i in ips]
    san = ",".join(spec)
    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
    ca_name = "%s-ca-%s" % (cn, timestamp)
    cert_name = "%s-%s" % (cn, timestamp)

    # generate CA private key
    run(["openssl", "genrsa", "-out", ca_name + ".key", "2048"], cwd=outputdir)
    # self signed CA certificate
    run(
        [
            "openssl",
            "req",
            "-x509",
            "-new",
            "-nodes",
            "-subj",
            "/commonName=%s" % ca_name,
            "-key",
            ca_name + ".key",
            "-sha256",
            "-days",
            "999999",
            "-out",
            ca_name + ".crt",
        ],
        cwd=outputdir,
    )
    # generate private key
    run(["openssl", "genrsa", "-out", cert_name + ".key", "2048"], cwd=outputdir)
    # certificate request
    with open("/etc/ssl/openssl.cnf", "r") as f:
        orig_conf = f.read()
    with open(os.path.join(outputdir, "openssl.cnf"), "w") as f:
        f.write(orig_conf)
        f.write("\n[SAN]\nsubjectAltName=%s\n" % san)
    run(
        [
            "openssl",
            "req",
            "-new",
            "-sha256",
            "-subj",
            "/commonName=%s" % cn,
            "-key",
            cert_name + ".key",
            "-reqexts",
            "SAN",
            "-out",
            cert_name + ".csr",
            "-config",
            "openssl.cnf",
        ],
        cwd=outputdir,
    )
    # sign the certificate with CA
    run(
        [
            "openssl",
            "x509",
            "-req",
            "-in",
            cert_name + ".csr",
            "-CA",
            ca_name + ".crt",
            "-CAkey",
            ca_name + ".key",
            "-out",
            cert_name + ".crt",
            "-days",
            "999999",
            "-sha256",
            "-extensions",
            "SAN",
            "-CAcreateserial",
            "-CAserial",
            ca_name + ".srl",
            "-extfile",
            "openssl.cnf",
        ],
        cwd=outputdir,
    )

    for f in (ca_name + ".srl", ca_name + ".key", "openssl.cnf", cert_name + ".csr"):
        os.remove(os.path.join(outputdir, f))

    stat = os.stat(".")
    for f in (cert_name + ".crt", cert_name + ".key", ca_name + ".crt"):
        os.chown(os.path.join(outputdir, f), stat.st_uid, stat.st_gid)
