#!/usr/bin/python

import socketserver

# You may want to change address and port below to suit your situation
myMailAddress = 'localhost'
myMailPort = 25

print('Running on ' + str(myMailPort) + ' for a while\n')


class SmtpSink(socketserver.StreamRequestHandler):
    """The instance variable we get are request, client_address, and server"""
    
    def handle(self):

        # send greeting
        self.wfile.write(b'220 SMTP sink here.\r\n')
        
        one_line = self.rfile.readline()
        while one_line != '':
            word_list = one_line.decode(encoding='utf-8').strip().split()
            if len(word_list) > 0:
                command = word_list[0].upper()
            else:
                command = 'unknown'

            # decide what to do based on the command
            if command == 'QUIT':
                self.wfile.write(b'221 Good-bye!\r\n')
                break
            elif command == 'RSET' or command == 'MAIL' or command == 'RCPT':
                self.wfile.write(b'250 OK\r\n')
            elif command == 'DATA':
                self.wfile.write(b'354 Send your data\r\n')
                self.do_read_data()
            elif command == 'HELO' or command == 'EHLO':
                self.do_helo()
            else:
                self.wfile.write(b'250 Unsupported Command\r\n')
            one_line = self.rfile.readline()

    def do_helo(self):
        client_addr = '%s:%i' % (self.client_address[0], self.client_address[1])
        response = '250 Hello %s, pleased to meet you\r\n' % client_addr
        self.wfile.write(bytearray(response, encoding='utf-8'))

    def do_read_data(self):
        line = self.rfile.readline().decode(encoding='utf-8')
        while line != '' and line is not None:
            if line[0] == '.' and len(line) >= 2:
                line = line.strip()
                if line == '.':
                    break
            line = self.rfile.readline().decode(encoding='utf-8')
        self.wfile.write(b'250 OK\r\n')

        
myServer = socketserver.ThreadingTCPServer((myMailAddress, myMailPort), SmtpSink)
myServer.allow_reuse_address = True

myServer.serve_forever()
