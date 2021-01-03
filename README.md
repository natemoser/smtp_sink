# smtp_sink
A simple Python socketserver.StreamRequestHandler that implements a very basic threaded SMTP server (no TLS/SSL or 
authentication) that simply reads the email message submitted and discards the data. You might find this useful for 
performance testing an SMTP client, or gauging network capacity. You should be able to run with Python 3.x and just

```python ./smtp_sink.py```

The smtp_client.jmx file is a [Jmeter](https://jmeter.apache.org/) workload that can be used to exercise the sink 
script.

