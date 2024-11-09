import socket
from unittest.mock import patch, MagicMock
from dice_py.connection.connect import Connect


def test_init():
    host = "localhost"
    port = 7379
    conn = Connect(host, port)

    assert conn.host == host
    assert conn.port == port
    assert isinstance(conn.sock, socket.socket)


@patch("socket.socket.connect")
def test_connect(mock_connect):
    host = "localhost"
    port = 7379
    conn = Connect(host, port)
    conn.connect()

    mock_connect.assert_called_once_with((host, port))


@patch("socket.socket.close")
def test_close(mock_close):
    host = "localhost"
    port = 7379
    conn = Connect(host, port)
    conn.close()

    mock_close.assert_called_once()


@patch("socket.socket.sendall")
@patch("socket.socket.recv", return_value=b"+PONG\r\n")
@patch("dice_py.connection.connect.to_resp", return_value="PING")
def test_ping(mock_to_resp, mock_recv, mock_sendall):
    host = "localhost"
    port = 7379
    conn = Connect(host, port)
    result = conn.ping()

    mock_to_resp.assert_called_once_with("PING")
    mock_sendall.assert_called_once_with(b"PING")
    mock_recv.assert_called_once()
    assert result == True
