# Импорт встроенной библиотеки для работы веб-сервера
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
BASE_DIR = Path.cwd()

# Для начала определим настройки запуска
hostName = "localhost" # Адрес для доступа по сети
serverPort = 8080 # Порт для доступа по сети
PATH_HTML = 'contacts.html'





class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            html_file = BASE_DIR / 'contacts.html'
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self._write_file(html_file)
            return

        if self.path.startswith('/css/'):
            css_file = BASE_DIR.joinpath(*self.path.split('/'))
            if css_file.exists():
                self.send_response(200)
                self.send_header('Content-type', 'text/css')
                self.end_headers()
                self._write_file(css_file)
                return

        self.send_error(404, "File Not Found")

    def _write_file(self, file_path: str):
        with open(file_path, 'rb') as f:
            self.wfile.write(f.read())
if __name__ == "__main__":
    # Инициализация веб-сервера, который будет по заданным параметрах в сети
    # принимать запросы и отправлять их на обработку специальному классу, который был описан выше
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Cтарт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")