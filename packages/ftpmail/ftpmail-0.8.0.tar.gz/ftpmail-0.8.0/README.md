# ftpmail

This program accepts FTP uploads (e.g. from a document scanner) and forwards them as emails via SMTP.

It'll terminate the FTP connection as fast as possible, this means directly after the upload has finished.
The email process will happen in a separate thread to not block the uploader.

It can do optional optical character recognition (OCR) for scanned PDFs and embed the read text into the PDF file
using the great [pdfsandwich](http://www.tobias-elze.de/pdfsandwich/) by Tobias Elze.


## Usage

```
usage: ftpmail.py [-h] --from FROM_ADDR --to TO_ADDR --smtp-host SMTP_HOST
                  [--smtp-port SMTP_PORT] --smtp-user SMTP_USER --smtp-pass
                  SMTP_PASS --ftp-addr FTP_ADDR --ftp-port FTP_PORT
                  --ftp-pasv-min FTP_PASV_MIN --ftp-pasv-max FTP_PASV_MAX
                  [--ocr] [--ocr-lang OCR_LANG]

Send FTP uploads via SMTP.

optional arguments:
  -h, --help            show this help message and exit
  --from FROM_ADDR      Sender email address
  --to TO_ADDR          Recipient email address
  --smtp-host SMTP_HOST
                        SMTP hostname
  --smtp-port SMTP_PORT
                        SMTP port
  --smtp-user SMTP_USER
                        SMTP username
  --smtp-pass SMTP_PASS
                        SMTP password
  --ftp-addr FTP_ADDR   FTP server address which will be returned for PASV
                        requests.
  --ftp-port FTP_PORT   FTP port to bind to.
  --ftp-pasv-min FTP_PASV_MIN
                        FTP PASV minimal port.
  --ftp-pasv-max FTP_PASV_MAX
                        FTP PASV maximal port.
  --ocr                 enable OCR (embeds a hidden text layer in PDF files)
  --ocr-lang OCR_LANG   OCR: language of the text; option to tesseract
                        (defaut: eng), e.g: eng, deu, deu-frak, fra, rus, swe,
                        spa, ita, ... Multiple languages may be specified,
                        separated by plus characters.
```
