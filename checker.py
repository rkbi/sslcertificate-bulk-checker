from urllib.request import ssl, socket
import datetime, csv, time


def get_data(hostname):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, "443")) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            certificate = ssock.getpeercert()

            expiry_date = get_expiry_date(certificate)
            issuer = get_issuer_name(certificate)
            alt_name_count = len(certificate["subjectAltName"])

            return [hostname, expiry_date, issuer, alt_name_count]


def get_expiry_date(cert):
    return datetime.datetime.strptime(
        cert["notAfter"], "%b %d %H:%M:%S %Y %Z"
    ).strftime("%d-%b-%Y %H:%M")


def get_issuer_name(cert):
    issuer = dict(x[0] for x in cert["issuer"])
    return issuer["organizationName"].replace(",", "")


with open("output.csv", "w", encoding="UTF8") as outputfile:
    writer = csv.writer(outputfile)

    # write the header
    header = ["Domain", "Expiry_Date", "Issuer_Company", "Additional_Domain_Count"]
    writer.writerow(header)

    # read data file, gather data and write to output file
    with open("data.csv", newline="") as datafile:
        r = csv.reader(datafile)
        for line in r:
            hostname = line[0]
            writer.writerow(get_data(hostname))
