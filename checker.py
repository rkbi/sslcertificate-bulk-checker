from urllib.request import ssl
import datetime
import csv
import tldextract
import OpenSSL


def get_data(unsanitized):
    print(unsanitized)

    sanitized = sanitize(unsanitized)
    hostname = tldextract.extract(sanitized).fqdn

    try:
        pem = ssl.get_server_certificate((hostname, "443"), timeout=3)
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, pem)

        issuer = x509.get_issuer().organizationName
        expiry_date = get_expiry_date(x509.get_notAfter())

        return [hostname, issuer, expiry_date, ""]

    except Exception as ex:
        ex_name = type(ex).__name__

        remark_list = {
            "gaierror": "Invalid or Expired domain",
            "TimeoutError": "Connection Timeout",
            "ConnectionRefusedError": "No certificate",
            "SSLError": "Invalid Certificate",
            "SSLEOFError": "Invalid Certificate",
        }

        remark = remark_list.get(ex_name, "")

        print(
            f"{hostname}: An exception of type {ex_name} occurred. Arguments:{ex.args}"
        )

        return [unsanitized, "", "", remark]


def get_expiry_date(notafter):
    """Converts date form YYYYMMDDhhmmssZ format to DD-Mon-Year HH:mm:SS suitable for excel"""

    try:
        exp_date = datetime.datetime.strptime(
            notafter[:-1].decode("utf-8"), "%Y%m%d%H%M%S"
        ).strftime("%d-%b-%Y %H:%M:%S")
        return exp_date
    except:
        print(notafter)


def get_alt_name_count(cert):
    try:
        alt_name_count = len(certificate["subjectAltName"])
        return alt_name_count
    except:
        print(cert)


def sanitize(u):
    return (
        u.lower()
        .replace("//:", "://")
        .replace("///", "//")
        .replace("http//", "http://")
        .replace("https//", "https://")
        .replace("www.", "")
        .replace(".con", ".com")
        .replace('"', "")
        .replace("'", "")
        .replace(",", "")
        .replace(" ", "")
    )


def main():
    with open("output.csv", "w", encoding="UTF8") as outputfile:
        writer = csv.writer(outputfile, quoting=csv.QUOTE_ALL)

        # write the header
        header = ["Domain", "Certificate Issuer", "Expiry Date", "Remarks"]
        writer.writerow(header)

        # read data file, gather data and write to output file
        with open("data.csv", newline="") as datafile:
            r = csv.reader(datafile)
            for line in r:
                writer.writerow(get_data(line[0]))


if __name__ == "__main__":
    main()
