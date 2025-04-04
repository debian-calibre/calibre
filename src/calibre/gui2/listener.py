#!/usr/bin/env python
# License: GPL v3 Copyright: 2020, Kovid Goyal <kovid at kovidgoyal.net>

import errno
import os
import socket
import sys
from contextlib import closing
from functools import partial
from itertools import count

from qt.core import QAbstractSocket, QLocalServer, pyqtSignal

from calibre.utils.ipc import gui_socket_address, socket_address


def unix_socket(timeout=10):
    ans = socket.socket(socket.AF_UNIX)
    ans.settimeout(timeout)
    return ans


class Listener(QLocalServer):

    message_received = pyqtSignal(object)

    def __init__(self, address=None, parent=None):
        QLocalServer.__init__(self, parent)
        self.address = address or gui_socket_address()
        self.uses_filesystem = self.address[0] not in '\0\\'
        self.setSocketOptions(QLocalServer.SocketOption.UserAccessOption)
        self.newConnection.connect(self.on_new_connection)
        self.connection_id = count()
        self.pending_messages = {}

    def start_listening(self):
        if self.address.startswith('\0'):
            s = unix_socket()
            s.bind(self.address)
            s.listen(16)
            if not self.listen(s.detach()):
                raise OSError(f'Could not start Listener for IPC at address @{self.address[1:]} with error: {self.errorString()}')
        else:
            if not self.listen(self.address):
                if self.serverError() == QAbstractSocket.SocketError.AddressInUseError and self.uses_filesystem:
                    self.removeServer(self.address)
                    if self.listen(self.address):
                        return
                code = self.serverError()
                if code == QAbstractSocket.SocketError.AddressInUseError:
                    raise OSError(errno.EADDRINUSE, os.strerror(errno.EADDRINUSE), self.address)
                raise OSError(f'Could not start Listener for IPC at address {self.address} with error: {self.errorString()}')

    def on_new_connection(self):
        while True:
            s = self.nextPendingConnection()
            if s is None:
                break
            cid = next(self.connection_id)
            self.pending_messages[cid] = b''
            s.readyRead.connect(partial(self.on_ready_read, cid, s))
            s.disconnected.connect(partial(self.on_disconnect, cid, s))

    def on_ready_read(self, connection_id, q_local_socket):
        num = q_local_socket.bytesAvailable()
        if num > 0:
            self.pending_messages[connection_id] += bytes(q_local_socket.readAll())

    def on_disconnect(self, connection_id, q_local_socket):
        self.on_ready_read(connection_id, q_local_socket)
        q_local_socket.close()
        q_local_socket.readyRead.disconnect()
        q_local_socket.disconnected.disconnect()
        q_local_socket.deleteLater()
        self.message_received.emit(self.pending_messages.pop(connection_id, b''))


def send_message_in_process(msg, address=None, timeout=5):
    address = address or gui_socket_address()
    if isinstance(msg, str):
        msg = msg.encode('utf-8')
    if address.startswith('\\'):
        with open(address, 'r+b') as f:
            f.write(msg)
    else:
        ps = unix_socket(timeout)
        ps.connect(address)
        ps.sendall(msg)
        ps.shutdown(socket.SHUT_RDWR)
        ps.close()


def send_message_in_worker(address, timeout):
    msg = sys.stdin.buffer.read()
    send_message_in_process(msg, address, timeout)


def send_message_via_worker(msg, address=None, timeout=5, wait_till_sent=True):
    # On Windows sending a message in a process that also is listening on the
    # same named pipe in a different thread deadlocks, so we do the actual sending in
    # a simple worker process
    from calibre.utils.ipc.simple_worker import start_pipe_worker
    if isinstance(msg, str):
        msg = msg.encode('utf-8')
    p = start_pipe_worker(f'from calibre.gui2.listener import *; send_message_in_worker({address!r}, {timeout!r})')
    with closing(p.stdin):
        p.stdin.write(msg)
    if wait_till_sent:
        return p.wait(timeout=timeout + 2) == 0


def listener_for_test(address):
    from qt.core import QCoreApplication, QTimer
    app = QCoreApplication([])
    s = Listener(address=address, parent=app)
    s.start_listening()
    def got_message(msg):
        if msg == b'quit':
            app.quit()
            return
        sys.stdout.buffer.write(msg)
        sys.stdout.buffer.write(os.linesep.encode())
        sys.stdout.buffer.flush()
    s.message_received.connect(got_message)
    QTimer.singleShot(0, lambda: print('started', flush=True))
    app.exec()


def find_tests():
    import unittest
    class TestIPC(unittest.TestCase):

        def test_listener_ipc(self):
            from calibre.utils.ipc.simple_worker import start_pipe_worker
            address = socket_address('test')
            server = start_pipe_worker(f'from calibre.gui2.listener import *; listener_for_test({address!r})')
            try:
                self.assertEqual(server.stdout.readline().rstrip(), b'started')
                for msg in 'one', 'two', 'three':
                    send_message_in_process(msg, address=address)
                    self.assertEqual(server.stdout.readline().rstrip(), msg.encode())
                self.assertTrue(send_message_via_worker('hello, world!', address=address))
                self.assertEqual(server.stdout.readline().rstrip(), b'hello, world!')
                msg = '123456789' * 8192 * 10
                send_message_in_process(msg, address=address)
                self.assertEqual(server.stdout.readline().rstrip(), msg.encode())
                send_message_in_process('quit', address=address)
                server.wait(2)
            finally:
                server.kill()
                server.wait()

    return unittest.defaultTestLoader.loadTestsFromTestCase(TestIPC)


def test():
    from qt.core import QApplication, QLabel, QTimer
    app = QApplication([])
    l = QLabel()
    l.setText('Waiting for message...')
    m = '123456789' * 8192 * 10

    def show_message(msg):
        q = msg.decode()
        if q != m:
            print(f'Received incorrect message of length: {len(q)} expecting length: {len(m)}', file=sys.stderr)
        else:
            print('Received msg correctly', file=sys.stderr)
        l.setText(q)
        QTimer.singleShot(1000, app.quit)

    def send():
        send_message_via_worker(m, wait_till_sent=False)

    QTimer.singleShot(1000, send)
    s = Listener(parent=l)
    s.start_listening()
    print('Listening at:', s.serverName(), s.isListening())
    s.message_received.connect(show_message)

    l.show()
    app.exec()


if __name__ == '__main__':
    test()
